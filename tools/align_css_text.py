#!/usr/bin/env python3
"""Align text layers of tree.json with the CSS text blocks of styles_all.css (same layer names, DFS order) and copy the CSS
font-size/weight/line-height/letter-spacing/colour into tree.json (CSS is Figma's resolved style, covers shared text styles
that the clipboard tree lacks). Originals kept in text.orig. Usage: align_css_text.py <_story>..."""
import json, re, sys, glob, os, difflib
WS = {'300': 'Light', '400': 'Regular', '500': 'Medium', '600': 'SemiBold', '700': 'Bold', '800': 'ExtraBold', '900': 'Black'}
def css_texts(path):
    L = open(path).read().split('\n'); blocks = []; cur = None
    for k, ln in enumerate(L):
        m = re.match(r'^/\* (.+?) \*/\s*$', ln); nxt = L[k + 1] if k + 1 < len(L) else ''
        if m and m.group(1) not in ('Inside auto layout', 'Auto layout') and not m.group(1).startswith('identical') and not nxt.startswith('font-family') and not nxt.startswith('font-style'):
            cur = {'name': m.group(1), 'body': ''}; blocks.append(cur)
        elif cur is not None: cur['body'] += ln + '\n'
    out = []
    for b in blocks:
        if 'font-family' in b['body']:
            g = lambda k: (re.search(r'(?m)^\s*' + k + r':\s*([^;]+);', b['body']) or [None, None])[1]
            out.append({'name': b['name'], 'size': g('font-size'), 'weight': g('font-weight'), 'lh': g('line-height'), 'ls': g('letter-spacing'), 'color': g('color'), 'family': (g('font-family') or '').strip("'\"")})
    return out
def num(v):
    m = re.search(r'-?\d+(\.\d+)?', v or ''); return float(m.group()) if m else None
tot = ch = 0
for D in sys.argv[1:]:
    for tj in glob.glob(D + '/screens/*/tree.json'):
        d = os.path.dirname(tj); cp = d + '/styles_all.css'
        if not os.path.exists(cp): continue
        tree = json.load(open(tj)); ct = css_texts(cp); nodes = []
        def walk(n, hid=False):
            hid = hid or n.get('visible') is False or n.get('opacity') == 0
            if n['type'] == 'TEXT' and n.get('text') and not hid: nodes.append(n)
            for c in n.get('children', []): walk(c, hid)
        walk(tree)
        sm = difflib.SequenceMatcher(None, [c['name'] for c in ct], [n['name'] for n in nodes], autojunk=False)
        for a, b, size in sm.get_matching_blocks():
            for i in range(size):
                c, n = ct[a + i], nodes[b + i]; t = n['text']; tot += 1
                orig = {k: t.get(k) for k in ('fontSize', 'font', 'lineHeight', 'letterSpacing')}
                fs = num(c['size']); new = {}
                if fs: new['fontSize'] = fs
                st = WS.get(c['weight']); 
                if st: new['font'] = dict(t.get('font') or {}, style=st, family=c['family'] or (t.get('font') or {}).get('family'))
                if c['lh'] and 'px' in c['lh']: new['lineHeight'] = {'value': num(c['lh']), 'units': 'PIXELS'}
                if c['ls'] and c['ls'] not in ('normal',): new['letterSpacing'] = {'value': num(c['ls']) * (100 if c['ls'].endswith('em') else 1), 'units': 'PERCENT' if c['ls'].endswith('em') else 'PIXELS'} if num(c['ls']) else {'value': 0, 'units': 'PIXELS'}
                if any(t.get(k) != v for k, v in new.items()): ch += 1; t.setdefault('orig', orig)
                t.update(new)
                if c['color'] and re.match(r'^#[0-9A-Fa-f]{6}', c['color']): n['fills'] = [{'type': 'SOLID', 'color': c['color'][:7].upper()}]
        json.dump(tree, open(tj, 'w'), ensure_ascii=False, indent=1)
print('aligned text layers', tot, 'with changed style', ch)
