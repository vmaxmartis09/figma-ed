#!/usr/bin/env python3
"""clip.html (Figma clipboard of a whole story) -> per screen tree.json (nested layers with real text, geometry, fills,
auto layout) and real text in texts.json (text_source=figma_clipboard). Usage: clip_to_screens.py <_story dir>"""
import sys, os, json, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figkiwi
D = sys.argv[1]
m = figkiwi.load_clip_html(D + '/clip.html'); BLOBS = m.get('blobs', []); nc = [n for n in m['nodeChanges'] if 'guid' in n and 'type' in n and 'name' in n]
g = lambda n: (n['guid']['sessionID'], n['guid']['localID'])
by = {g(n): n for n in nc}; kids = {}
for n in nc:
    p = n.get('parentIndex')
    if p: kids.setdefault((p['guid']['sessionID'], p['guid']['localID']), []).append(n)
for k in kids: kids[k].sort(key=lambda n: n['parentIndex']['position'])
hexc = lambda c: '#%02X%02X%02X' % tuple(round(c[k] * 255) for k in 'rgb') + ('' if c.get('a', 1) >= .999 else '%02X' % round(c['a'] * 255))
def paint(p):
    if not p.get('visible', True): return None
    t = p['type']
    if t == 'SOLID': return {'type': t, 'color': hexc(p['color']), **({'opacity': p['opacity']} if p.get('opacity', 1) != 1 else {})}
    if t.startswith('GRADIENT'): return {'type': t, 'stops': [{'pos': s['position'], 'color': hexc(s['color'])} for s in p.get('stops', [])]}
    return {'type': t}
GK = lambda d: (d['sessionID'], d['localID'])
def okey(n): return GK(n['overrideKey']) if n.get('overrideKey') else g(n)
def paths(lst, field='guidPath'):
    out = {}
    for o in lst or []:
        gp = tuple(GK(x) for x in o.get(field, {}).get('guids', []))
        out.setdefault(gp, {}).update({k: v for k, v in o.items() if k != field})
    return out
def applyprops(n, props):
    for r in n.get('componentPropRefs') or []:
        v = (props or {}).get(GK(r['defID']))
        if v is None: continue
        fld = r.get('componentPropNodeField')
        if fld == 'VISIBLE' and 'boolValue' in v: n['visible'] = v['boolValue']
        elif fld == 'TEXT_DATA' and (v.get('textValue') is not None or v.get('textDataValue') is not None):
            tv = v.get('textValue') if v.get('textValue') is not None else v.get('textDataValue'); ch = tv.get('characters') if isinstance(tv, dict) else tv
            if ch is not None: n['textData'] = dict(n.get('textData') or {}, characters=ch)
        elif fld == 'OVERRIDDEN_SYMBOL_ID' and v.get('guidValue'): n['overriddenSymbolID'] = v['guidValue']
def reduce(n, ov=None, depth=0, props=None):
    n = dict(n)
    applyprops(n, props)
    if ov and ov.get(()): n.update({k: v for k, v in ov[()].items() if k not in ('guid',)})
    applyprops(n, props)
    t = n['transform']; o = {'name': n['name'], 'type': n['type'], 'x': round(t['m02'], 2), 'y': round(t['m12'], 2), 'w': n['size']['x'], 'h': n['size']['y']}
    if n.get('rotation') or abs(t['m01']) > 1e-6 or abs(t['m10']) > 1e-6: o['transform'] = [t['m00'], t['m01'], t['m10'], t['m11']]
    if not n.get('visible', True): o['visible'] = False
    if n.get('opacity', 1) != 1: o['opacity'] = n['opacity']
    for k in ('cornerRadius', 'rectangleTopLeftCornerRadius', 'rectangleTopRightCornerRadius', 'rectangleBottomLeftCornerRadius', 'rectangleBottomRightCornerRadius', 'strokeWeight', 'strokeAlign', 'stackMode', 'stackSpacing', 'stackPaddingLeft', 'stackPaddingRight', 'stackPaddingTop', 'stackPaddingBottom', 'stackPrimaryAlignItems', 'stackCounterAlignItems', 'stackPrimarySizing', 'stackCounterSizing', 'stackChildPrimaryGrow', 'stackPositioning', 'horizontalConstraint', 'verticalConstraint', 'frameMaskDisabled'):
        if n.get(k) not in (None, 0, 0.0): o[k] = n[k]
    if n.get('vectorData') and n['vectorData'].get('vectorNetworkBlob') is not None:
        vd = n['vectorData']; o['vec'] = {'blob': vd['vectorNetworkBlob'], 'nw': vd['normalizedSize']['x'], 'nh': vd['normalizedSize']['y']}
    for k in ('strokeCap', 'strokeJoin'):
        if n.get(k): o[k] = n[k]
    fp = [x for x in (paint(p) for p in n.get('fillPaints', [])) if x]
    if fp: o['fills'] = fp
    sp = [x for x in (paint(p) for p in n.get('strokePaints', [])) if x]
    if sp: o['strokes'] = sp
    ef = [{'type': e['type'], 'color': hexc(e['color']), 'x': e['offset']['x'], 'y': e['offset']['y'], 'radius': e['radius'], **({'spread': e['spread']} if e.get('spread') else {})} for e in n.get('effects', []) if e.get('visible', True) and 'color' in e]
    if ef: o['effects'] = ef
    if n['type'] == 'TEXT':
        td = n.get('textData', {}); o['text'] = {'characters': td.get('characters'), 'fontSize': n.get('fontSize'), 'font': n.get('fontName'), 'lineHeight': n.get('lineHeight'), 'letterSpacing': n.get('letterSpacing'), 'alignH': n.get('textAlignHorizontal'), 'alignV': n.get('textAlignVertical'), 'case': n.get('textCase'), 'decoration': n.get('textDecoration'), 'autoResize': n.get('textAutoResize')}
    if n['type'] == 'INSTANCE' and not kids.get(g(n)) and n.get('symbolData') and depth < 12:
        sym = by.get(GK(n['overriddenSymbolID'])) if n.get('overriddenSymbolID') else by.get(GK(n['symbolData']['symbolID']))
        mine = paths(n['symbolData'].get('symbolOverrides')); der = paths(n.get('derivedSymbolData'))
        merged = {}
        for src in (der, mine):
            for pth, f in src.items(): merged.setdefault(pth, {}).update(f)
        for pth, f in (ov or {}).items():
            if pth: merged.setdefault(pth, {}).update(f)
        ch = []
        ip = {}
        if sym is not None:
            for d in sym.get('componentPropDefs') or []:
                if d.get('initialValue') is not None: ip[GK(d['id'])] = d['initialValue']
        for a in n.get('componentPropAssignments') or []:
            val = a.get('value') or (a.get('varValue') or {}).get('value')
            if val is not None: ip[GK(a['defID'])] = val
        if sym is not None:
            for c in kids.get(g(sym), []):
                kc = okey(c); sub = {(q[1:] if q and q[0] == kc else q): f for q, f in merged.items() if q}
                ch.append(reduce(c, sub, depth + 1, ip))
    else:
        sub_all = ov or {}
        ch = []
        for c in kids.get(g(n), []):
            kc = okey(c); sub = {(q[1:] if q and q[0] == kc else q): f for q, f in sub_all.items() if q}
            ch.append(reduce(c, sub, depth, props))
    if ch: o['children'] = ch
    return o
def absxy(n, root):
    x = y = 0
    while n is not None and g(n) != root:
        t = n['transform']; x += t['m02']; y += t['m12']
        p = n.get('parentIndex'); n = by.get((p['guid']['sessionID'], p['guid']['localID'])) if p else None
    return x, y
# selected root = node whose parent is not in the copied set
def _par(n):
    q = n.get('parentIndex'); return by.get((q['guid']['sessionID'], q['guid']['localID'])) if q else None
_sc0 = json.load(open(D + '/screens/screens.json'))[0]
root = next(n for n in nc if 'size' in n and _par(n) is not None and _par(n)['type'] == 'CANVAS' and abs(n['size']['x'] - _sc0['rootW']) < 1.5 and abs(n['size']['y'] - _sc0['rootH']) < 1.5)
rid = g(root)
sc = json.load(open(D + '/screens/screens.json')); used = set()
_ocr = json.load(open(D + '/ocr_all.json')) if os.path.exists(D + '/ocr_all.json') else {}
_nm = lambda t: re.sub(r'[^0-9a-zA-ZÀ-ỿ؀-ۿ一-鿿]+', '', t or '').lower(); matched = tot_t = real_t = 0
cands = [n for n in nc if n['type'] in ('FRAME', 'SYMBOL', 'INSTANCE', 'COMPONENT')]
for s in sc:
    w, h = float(s['width'][:-2]), float(s['height'][:-2]); nm = re.sub(r'^\d+_', '', s['folder'])
    best, bd = None, 1e9
    for n in cands:
        if g(n) in used or abs(n['size']['x'] - w) > .6 or abs(n['size']['y'] - h) > .6: continue
        ax, ay = absxy(n, rid); d = abs(ax - s['x']) + abs(ay - s['y']) + (0 if n['name'] == s['name'] else 50)
        if d < bd: best, bd = n, d
    if best is None or bd > 60: continue
    used.add(g(best)); matched += 1; s['node_id'] = '%d:%d' % g(best); _ids = True
    tree = reduce(best); open(f"{D}/screens/{s['folder']}/tree.json", 'w').write(json.dumps(tree, ensure_ascii=False, indent=1))
    texts = []
    def walk(n, path, ox, oy, hid=False):
        x, y = ox + n['x'], oy + n['y']; hid = hid or n.get('visible') is False or n.get('opacity') == 0
        if n['type'] == 'TEXT' and n.get('text') and not hid:
            t = n['text']; fill = (n.get('fills') or [{}])[0]
            texts.append({'text': t['characters'], 'layer': n['name'], 'path': '/'.join(path), 'x': round(x, 2), 'y': round(y, 2), 'w': n['w'], 'h': n['h'],
                          'font_family': (t['font'] or {}).get('family'), 'font_style': (t['font'] or {}).get('style'), 'font_size': t['fontSize'],
                          'line_height': t['lineHeight'], 'letter_spacing': t['letterSpacing'], 'align': t['alignH'], 'color': fill.get('color'), 'opacity': n.get('opacity', 1)})
        for c in n.get('children', []): walk(c, path + [c['name']], x if n is not tree else 0, y if n is not tree else 0, hid)
    walk(tree, [tree['name']], 0, 0)
    _f = glob.glob(f"{D}/screens/{s['folder']}/screen@*.png"); _ab = os.path.abspath(_f[0]) if _f else None
    _j = ''.join(_nm(l['text']) for l in _ocr.get(_ab, []))
    for t in texts: t['ocr_confirmed'] = bool(_nm(t['text'])) and _nm(t['text']) in _j
    tj = f"{D}/screens/{s['folder']}/texts.json"
    if os.path.exists(tj):
        data = json.load(open(tj)); pool = {}
        for t in texts: pool.setdefault((t['layer'], t['font_size']), []).append(t['text'])
        for t in data['texts']:
            fs = float(re.sub(r'[^0-9.]', '', t.get('font_size') or '0') or 0); key = (t.get('layer_name') or t['text'], fs)
            if t.get('text_source') in ('ocr_exact',) and False: continue
            vals = pool.get(key)
            if vals:
                uniq = list(dict.fromkeys(vals)); t.setdefault('layer_name', t['text']); t['text'] = uniq[0] if len(uniq) == 1 else uniq; t['text_source'] = 'figma_clipboard'
        data['texts_real'] = texts
        json.dump(data, open(tj, 'w'), ensure_ascii=False, indent=1)
        tot_t += len(data['texts']); real_t += sum(t.get('text_source') == 'figma_clipboard' for t in data['texts'])
json.dump(sc, open(D + '/screens/screens.json', 'w'), indent=1, ensure_ascii=False)
json.dump(BLOBS and [list(b['bytes']) for b in BLOBS] or [], open(D + '/blobs.json', 'w'))
print(D.split('figma-ediva/')[-1], 'screens', len(sc), 'matched', matched, 'texts', tot_t, 'real', real_t)
