#!/usr/bin/env python3
"""Generate Dart widgets for every screen of a story + a golden-render test + pixel diff report.
Usage: story_to_flutter.py <_story dir> <project dir>"""
import sys, os, json, re, subprocess, glob
from PIL import Image, ImageChops, ImageStat
story, proj = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
sc = json.load(open(story + '/screens/screens.json')); T = os.path.dirname(os.path.abspath(__file__))
os.makedirs(proj + '/lib/gen', exist_ok=True); os.makedirs(proj + '/out', exist_ok=True)
for f in glob.glob(proj + '/lib/gen/*.dart') + glob.glob(proj + '/out/*.png'): os.remove(f)
reg, items = [], []
for i, s in enumerate(sc):
    tj = f"{story}/screens/{s['folder']}/tree.json"
    if not os.path.exists(tj): continue
    cls = f'S{i + 1:02d}'; code = subprocess.run([sys.executable, T + '/tree_to_dart.py', tj, cls], capture_output=True, text=True).stdout
    open(f'{proj}/lib/gen/{cls.lower()}.dart', 'w').write(code)
    tr = json.load(open(tj)); items.append((cls, s['folder'], tr['w'], tr['h']))
import re as _re
imgs = sorted({m for c, *_ in items for m in _re.findall(r"FileImage\(File\('([^']+)'", open(f'{proj}/lib/gen/{c.lower()}.dart').read())})
imgjoin = ', '.join(repr(x) for x in imgs)
imports = ''.join(f"import 'gen/{c.lower()}.dart';\n" for c, *_ in items)
entries = ',\n'.join(f"  ('{c}', {w}, {h}, () => const {c}())" for c, _, w, h in items)
open(proj + '/lib/registry.dart', 'w').write(f"import 'package:flutter/widgets.dart';\n{imports}\nfinal imagePaths = <String>[{imgjoin}];\nfinal screens = <(String, double, double, Widget Function())>[\n{entries}\n];\n")
open(proj + '/test/render_test.dart', 'w').write('''import 'dart:io';
import 'dart:typed_data';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import '../lib/registry.dart';

void main() {
  testWidgets('render all', (tester) async {
    final loader = FontLoader('Roboto');
    for (final f in ['Regular', 'Light', 'Medium', 'Bold', 'Black']) {
      loader.addFont(Future.value(ByteData.sublistView(File('fonts/Roboto-$f.ttf').readAsBytesSync())));
    }
    await loader.load();
    for (final s in screens) {
      final key = GlobalKey();
      tester.view.devicePixelRatio = 1.0;
      tester.view.physicalSize = Size(s.$2, s.$3);
      await tester.pumpWidget(Directionality(textDirection: TextDirection.ltr, child: Center(child: RepaintBoundary(key: key, child: s.$4()))));
      await tester.runAsync(() async { for (final p in imagePaths) { await precacheImage(FileImage(File(p)), tester.element(find.byKey(key))); } });
      await tester.pumpAndSettle();
      await tester.runAsync(() async {
        final boundary = key.currentContext!.findRenderObject() as RenderRepaintBoundary;
        final image = await boundary.toImage(pixelRatio: 2.0);
        final data = await image.toByteData(format: ui.ImageByteFormat.png);
        File('out/${s.$1}.png').writeAsBytesSync(data!.buffer.asUint8List());
      });
    }
  });
}
''')
r = subprocess.run(['flutter', 'test', 'test/render_test.dart'], cwd=proj, capture_output=True, text=True); print(r.stdout[-300:], r.stderr[-300:])
res = []
for c, folder, w, h in items:
    ref = f"{story}/screens/{folder}/screen@2x.png"; out = f'{proj}/out/{c}.png'
    if not (os.path.exists(ref) and os.path.exists(out)): res.append((c, folder, None, None)); continue
    a = Image.open(out).convert('RGB'); b = Image.open(ref).convert('RGB')
    if a.size != b.size: res.append((c, folder, 'size %s vs %s' % (a.size, b.size), None)); continue
    d = ImageChops.difference(a, b); res.append((c, folder, round(sum(ImageStat.Stat(d).mean) / 3, 2), round(ImageStat.Stat(d.convert('L').point(lambda v: 255 if v > 24 else 0)).mean[0] / 2.55, 2)))
json.dump(res, open(proj + '/out/report.json', 'w'), indent=1, ensure_ascii=False)
for r_ in res: print(r_)
