#!/usr/bin/env python3
"""Per screen: texts.json = every text layer from the screen CSS (name, font, size, weight, line-height, color)
cross-checked against OCR of the screen image. Usage: build_texts.py <_story dir>"""
import json, re, sys, os, glob, subprocess, difflib
D = sys.argv[1]
OCR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ocr')
sc = json.load(open(D + '/screens/screens.json'))
imgs = {}
for s in sc:
    f = glob.glob(f"{D}/screens/{s['folder']}/screen@*.png")
    if f: imgs[s['folder']] = f[0]
cache = D + '/ocr_all.json'
ocr = json.load(open(cache)) if os.path.exists(cache) else {}
todo = [p for p in imgs.values() if p not in ocr]
for i in range(0, len(todo), 10):
    ocr.update(json.loads(subprocess.run([OCR] + todo[i:i + 10], capture_output=True, text=True).stdout or '{}'))
json.dump(ocr, open(cache, 'w'), ensure_ascii=False)
norm = lambda t: re.sub(r'[^0-9a-zA-ZÀ-ỿ؀-ۿ一-鿿]+', '', t).lower()
def prop(c, k):
    m = re.search(r'(?m)^\s*' + k + r':\s*([^;]+);', c); return m.group(1).strip() if m else None
tot = ver = 0
for s in sc:
    css = open(f"{D}/screens/{s['folder']}/styles_all.css").read()
    blocks = ['']; L = css.split('\n')
    for k, ln_ in enumerate(L):
        m = re.match(r'^/\* (.+?) \*/\s*$', ln_)
        nxt = L[k + 1] if k + 1 < len(L) else ''
        if m and m.group(1) not in ('Inside auto layout', 'Auto layout') and not m.group(1).startswith('identical') and not nxt.startswith('font-family') and not nxt.startswith('font-style'):
            blocks += [m.group(1), '']
        else:
            blocks[-1] += ln_ + '\n'
    lines = [l['text'] for l in ocr.get(imgs.get(s['folder']), [])]
    ln = [norm(l) for l in lines]; joined = ''.join(ln)
    out, seen = [], set()
    for i in range(1, len(blocks), 2):
        name, c = blocks[i], blocks[i + 1]
        if not prop(c, 'font-family'): continue
        n = norm(name)
        ok = bool(n) and (n in joined or any(difflib.SequenceMatcher(None, n, x).ratio() >= .85 for x in ln))
        best = max(lines, key=lambda l: difflib.SequenceMatcher(None, n, norm(l)).ratio(), default=None) if not ok else None
        key = (name, prop(c, 'font-size'), prop(c, 'color'))
        if key in seen: continue
        seen.add(key)
        out.append({'text': name, 'verified_by_ocr': ok, **({'ocr_candidate': best} if best else {}),
                    'style': (re.search(r'(?m)^/\* ([^*]+?) \*/\n\s*font-family', c) or [None, None])[1], 'font_family': (prop(c, 'font-family') or '').strip("'\""), 'font_size': prop(c, 'font-size'), 'font_weight': prop(c, 'font-weight'),
                    'line_height': prop(c, 'line-height'), 'letter_spacing': prop(c, 'letter-spacing'), 'color': prop(c, 'color'),
                    'text_align': prop(c, 'text-align')})
    tot += len(out); ver += sum(o['verified_by_ocr'] for o in out)
    json.dump({'screen': s['name'], 'texts': out, 'ocr_lines': lines}, open(f"{D}/screens/{s['folder']}/texts.json", 'w'), ensure_ascii=False, indent=1)
print(D.split('figma-ediva/')[-1], 'texts', tot, 'verified', ver)
