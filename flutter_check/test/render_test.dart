import 'dart:io';
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
