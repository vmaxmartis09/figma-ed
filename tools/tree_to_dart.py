#!/usr/bin/env python3
"""tree.json -> Dart widget (Stack/Positioned, exact geometry, text styles). Usage: tree_to_dart.py <tree.json> <ClassName> > out.dart
Vector nodes are skipped (icons live in icons/*.svg)."""
import json, sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figsvg
BLOBS = []
def has_text(n): return n['type'] == 'TEXT' or any(has_text(c) for c in n.get('children', []))
def vec_only(n): return n['type'] in ('VECTOR', 'BOOLEAN_OPERATION', 'LINE', 'ELLIPSE', 'ROUNDED_RECTANGLE', 'STAR') or (n.get('children') and all(vec_only(c) for c in n['children']))
def icon_svg(n):
    if not (n['w'] <= 80 and n['h'] <= 80 and n['w'] > 3 and not has_text(n) and (n['type'] == 'INSTANCE' or vec_only(n)) and n['type'] not in ('ROUNDED_RECTANGLE', 'ELLIPSE') and not n.get('stackMode')): return None
    frag = figsvg.node_svg(dict(n, x=0, y=0), BLOBS)
    if not frag: return None
    W, H = n['w'], n['h']; sw = max([n.get('strokeWeight') or 0] + [c.get('strokeWeight') or 0 for c in n.get('children', [])]); p = max(sw, 1) / 2 if (W < .5 or H < .5) else 0
    tr = n.get('transform'); pts = [(0, 0), (W, 0), (0, H), (W, H)]
    if tr: pts = [(tr[0] * a + tr[2] * b, tr[1] * a + tr[3] * b) for a, b in pts]
    x0, x1 = min(q[0] for q in pts) - p, max(q[0] for q in pts) + p; y0, y1 = min(q[1] for q in pts) - p, max(q[1] for q in pts) + p
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{x1-x0:g}" height="{y1-y0:g}" viewBox="0 0 {x1-x0:g} {y1-y0:g}"><g transform="translate({-x0:g} {-y0:g})">{frag}</g></svg>', x0, y0, x1 - x0, y1 - y0
WEIGHT = {'thin': 100, 'extralight': 200, 'light': 300, 'regular': 400, 'normal': 400, 'medium': 500, 'semibold': 600, 'semi bold': 600, 'bold': 700, 'extrabold': 800, 'black': 900}
def col(c):
    c = c.lstrip('#'); a = 'FF'
    if len(c) == 8: c, a = c[:6], c[6:]
    return f'Color(0x{a}{c})'
def paint(fills):
    for p in fills or []:
        if p['type'] == 'SOLID':
            c = p['color']; op = p.get('opacity', 1)
            return f'Color(0x{c.lstrip("#")[6:8] if len(c.lstrip("#"))==8 else "FF"}{c.lstrip("#")[:6]})' if op == 1 else f'{col(c)}.withOpacity({op})'
    return None
def esc(t):
    t = json.dumps(t, ensure_ascii=False)[1:-1].replace("'", "\\'").replace('$', '\\$')
    return ''.join(c if ord(c) >= 32 and c not in '\u2028\u2029\x85' else '\\u%04x' % ord(c) for c in t)
out = []
IMG = {}
def emit(n, ind, top=False, ox=0, oy=0):
    if n.get('visible') is False: return None
    pad = '  ' * ind; t = n['type']
    x, y, w, h = n['x'], n['y'], n['w'], n['h']
    ax, ay = (0, 0) if top else (ox + x, oy + y)
    body = None
    ic = None if top else icon_svg(n)
    if ic:
        svg, dx, dy, iw, ih = ic
        return f"{pad}Positioned(left: {x + dx}, top: {y + dy}, width: {iw}, height: {ih}, child: SvgPicture.string(r'''{svg}''', width: {iw}, height: {ih}))"
    imgfile = None
    if not top and any(p.get('type') == 'IMAGE' for p in n.get('fills', [])): imgfile = IMG.get((round(ax, 2), round(ay, 2), round(w, 2), round(h, 2)))
    if imgfile:
        r = n.get('cornerRadius'); im = f"Image(image: FileImage(File('{imgfile}')), width: {w}, height: {h}, fit: BoxFit.fill)"
        body = f"ClipRRect(borderRadius: BorderRadius.circular({r or 0}), child: {im})"
    elif t == 'TEXT':
        tx = n['text']; f = tx.get('font') or {}; style = (f.get('style') or 'Regular').lower()
        wt = 400
        for k, v in WEIGHT.items():
            if k in style.replace(' italic', '').strip(): wt = v
        fs = tx['fontSize']; lh = tx.get('lineHeight') or {}; ls = tx.get('letterSpacing') or {}
        hh = f', height: {lh["value"] / fs:.4f}' if lh.get('units') == 'PIXELS' and fs else ''
        lsp = f', letterSpacing: {ls["value"] * fs / 100 if ls.get("units") == "PERCENT" else ls["value"]:.4f}' if ls.get('value') else ''
        color = paint(n.get('fills')) or 'Color(0xFF000000)'
        al = {'CENTER': 'TextAlign.center', 'RIGHT': 'TextAlign.right', 'JUSTIFIED': 'TextAlign.justify'}.get(tx.get('alignH'), 'TextAlign.left')
        ital = ', fontStyle: FontStyle.italic' if 'italic' in style else ''
        body = f"Text('{esc(tx['characters'] or '')}', textAlign: {al}, softWrap: true, overflow: TextOverflow.visible, style: TextStyle(fontFamily: 'Roboto', fontSize: {fs}, fontWeight: FontWeight.w{wt}{ital}{hh}{lsp}, color: {color}, decoration: TextDecoration.none, leadingDistribution: TextLeadingDistribution.even))"
    elif t in ('VECTOR', 'BOOLEAN_OPERATION', 'LINE', 'STAR') or n.get('vec') is not None:
        return None
    else:
        fill = paint(n.get('fills')); r = n.get('cornerRadius')
        rad = f'BorderRadius.circular({r})' if r else None
        if any(n.get(k) for k in ('rectangleTopLeftCornerRadius', 'rectangleTopRightCornerRadius', 'rectangleBottomLeftCornerRadius', 'rectangleBottomRightCornerRadius')):
            rad = 'BorderRadius.only(' + ', '.join(f'{nm}: Radius.circular({n.get(k) or 0})' for nm, k in (('topLeft', 'rectangleTopLeftCornerRadius'), ('topRight', 'rectangleTopRightCornerRadius'), ('bottomLeft', 'rectangleBottomLeftCornerRadius'), ('bottomRight', 'rectangleBottomRightCornerRadius'))) + ')'
        sk = paint(n.get('strokes')); sw = n.get('strokeWeight') or 0
        dec = []
        if t == 'ELLIPSE' and abs(w - h) < .01: dec.append('shape: BoxShape.circle')
        if fill: dec.append(f'color: {fill}')
        if sk and sw: dec.append(f'border: Border.all(color: {sk}, width: {sw})')
        if rad and t != 'ELLIPSE': dec.append(f'borderRadius: {rad}')
        sh = [e for e in n.get('effects', []) if e['type'] == 'DROP_SHADOW']
        if sh: dec.append('boxShadow: [' + ', '.join(f'BoxShadow(color: {col(e["color"])}, offset: Offset({e["x"]}, {e["y"]}), blurRadius: {e["radius"]}, spreadRadius: {e.get("spread", 0)})' for e in sh) + ']')
        kids = [emit(c, ind + 2, False, ax, ay) for c in n.get('children', [])]; kids = [k for k in kids if k]
        inner = f"Stack(clipBehavior: Clip.none, children: [\n{(',' + chr(10)).join(kids)},\n{pad}  ])" if kids else None
        box = f"DecoratedBox(decoration: BoxDecoration({', '.join(dec)}), child: SizedBox(width: {w}, height: {h}, child: {inner or 'null'}))" if (dec or inner) else None
        clip = (not n.get('frameMaskDisabled')) and t in ('FRAME', 'INSTANCE', 'SYMBOL') and kids
        if box and clip: box = f"ClipRRect(borderRadius: {rad or 'BorderRadius.zero'}, child: {box})"
        body = box
    if body is None: return None
    if n.get('opacity') not in (None, 1): body = f"Opacity(opacity: {n['opacity']}, child: {body})"
    if top: return body
    return f"{pad}Positioned(left: {x}, top: {y}, width: {w}, height: {h}, child: {body})"
tree = json.load(open(sys.argv[1])); cls = sys.argv[2]
bp = os.path.join(os.path.dirname(sys.argv[1]), '..', '..', 'blobs.json')
BLOBS = [{'bytes': b} for b in json.load(open(bp))] if os.path.exists(bp) else []
aj = os.path.join(os.path.dirname(sys.argv[1]), 'assets.json')
if os.path.exists(aj):
    for e in json.load(open(aj)):
        if e.get('kind') == 'image' and e.get('file'): IMG[(round(e['x'], 2), round(e['y'], 2), round(e['w'], 2), round(e['h'], 2))] = os.path.abspath(os.path.join(os.path.dirname(sys.argv[1]), e['file']))
root = emit(tree, 2, True) or 'const SizedBox()'
print(f"import 'dart:io';\nimport 'package:flutter/material.dart';\nimport 'package:flutter_svg/flutter_svg.dart';\n\nclass {cls} extends StatelessWidget {{\n  const {cls}({{super.key}});\n  @override\n  Widget build(BuildContext context) {{\n    return SizedBox(width: {tree['w']}, height: {tree['h']}, child: {root});\n  }}\n}}")
