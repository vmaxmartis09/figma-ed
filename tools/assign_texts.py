#!/usr/bin/env python3
"""Second pass over texts.json: layers not verified by exact OCR match get an OCR line by reading-order alignment
between matched anchors (only when #layers == #free lines in the gap). Marks text_source: ocr_exact | ocr_sequence | layer_name.
Usage: assign_texts.py <_story>"""
import json, re, sys, glob, difflib
import os
D = os.path.abspath(sys.argv[1])
norm = lambda t: re.sub(r'[^0-9a-zA-ZÀ-ỿ؀-ۿ一-鿿]+', '', t).lower()
ocr = json.load(open(D + '/ocr_all.json')); sc = json.load(open(D + '/screens/screens.json'))
T = A = 0
for s in sc:
    f = glob.glob(f"{D}/screens/{s['folder']}/screen@*.png")
    tj = f"{D}/screens/{s['folder']}/texts.json"
    if not f or f[0] not in ocr: continue
    data = json.load(open(tj)); lines = [l for l in ocr[f[0]] if l['conf'] >= 0.5 and l['text'].strip()]
    lines.sort(key=lambda l: (round(l['y'] / 10), l['x']))
    nl = [norm(l['text']) for l in lines]; claimed = {}
    texts = data['texts']
    for i, t in enumerate(texts):
        n = norm(t['text']); t['text_source'] = 'layer_name'
        if not t['verified_by_ocr'] or not n: continue
        best, br = None, 0
        for j, x in enumerate(nl):
            if j in claimed.values(): continue
            r = 1.0 if n == x else (0.9 if n in x else difflib.SequenceMatcher(None, n, x).ratio())
            if r > br: best, br = j, r
        if best is not None and br >= .85: claimed[i] = best; t['text_source'] = 'ocr_exact'
    anchors = sorted(claimed.items()); bounds = [(-1, -1)] + anchors + [(len(texts), len(lines))]
    for (a_i, a_j), (b_i, b_j) in zip(bounds, bounds[1:]):
        layers = [i for i in range(a_i + 1, b_i) if texts[i]['text_source'] == 'layer_name']
        free = [j for j in range(a_j + 1, b_j)]
        if layers and len(layers) == len(free):
            for i, j in zip(layers, free):
                texts[i]['layer_name'] = texts[i]['text']; texts[i]['text'] = lines[j]['text']; texts[i]['text_source'] = 'ocr_sequence'
    for t in texts:
        T += 1; A += t['text_source'] != 'layer_name'
    json.dump(data, open(tj, 'w'), ensure_ascii=False, indent=1)
print(D.split('figma-ediva/')[-1], 'texts', T, 'resolved', A)
