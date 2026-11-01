#!/usr/bin/env python3
"""Per screen assets.json from tree.json: icon-like nodes (small INSTANCE/VECTOR/BOOLEAN_OPERATION/ELLIPSE-groups) and image fills,
with absolute position, size, colour and best-matching Library SVG by name. Usage: build_assets.py <repo root>"""
import json, glob, os, re, sys
R = sys.argv[1]
lib = {}
for f in glob.glob(R + '/Library/*/*.svg'):
    lib.setdefault(re.sub(r'[^a-z0-9]+', '', os.path.basename(f)[:-4].lower()), os.path.relpath(f, R))
def color(n):
    for p in n.get('fills', []) + n.get('strokes', []):
        if p.get('type') == 'SOLID': return p['color']
def has_text(n): return n['type'] == 'TEXT' or any(has_text(c) for c in n.get('children', []))
def vec_only(n): return n['type'] in ('VECTOR', 'BOOLEAN_OPERATION', 'LINE', 'ELLIPSE', 'ROUNDED_RECTANGLE', 'STAR') or (n.get('children') and all(vec_only(c) for c in n['children']))
tot = 0
for tj in glob.glob(R + '/*/*/_story/screens/*/tree.json') + glob.glob(R + '/*/*/*/_story/screens/*/tree.json'):
    if tj.startswith(R + '/Archive') or '/Proposal/' in tj or '/Cover/' in tj: continue
    tree = json.load(open(tj)); out = []
    def walk(n, ox, oy, top, hid=False):
        x, y = ox + n['x'], oy + n['y']; hid = hid or n.get('visible') is False
        if not top and not hid:
            img = [p for p in n.get('fills', []) if p.get('type') == 'IMAGE']
            small = n['w'] <= 80 and n['h'] <= 80
            if img and n['w'] > 8: out.append({'kind': 'image', 'name': n['name'], 'x': x, 'y': y, 'w': n['w'], 'h': n['h'], 'radius': n.get('cornerRadius')})
            elif small and n['w'] > 3 and not has_text(n) and (n['type'] == 'INSTANCE' or vec_only(n)) and n['type'] not in ('ROUNDED_RECTANGLE', 'ELLIPSE') and not n.get('stackMode'):
                c = color(n) or next((color(k) for k in n.get('children', []) if color(k)), None)
                key = re.sub(r'[^a-z0-9]+', '', n['name'].lower())
                out.append({'kind': 'icon', 'name': n['name'], 'x': x, 'y': y, 'w': n['w'], 'h': n['h'], 'color': c, 'library_svg': lib.get(key)})
                return
        for c in n.get('children', []): walk(c, x if not top else 0, y if not top else 0, False, hid)
    walk(tree, 0, 0, True)
    json.dump(out, open(os.path.dirname(tj) + '/assets.json', 'w'), ensure_ascii=False, indent=1); tot += len(out)
print('assets entries', tot)
