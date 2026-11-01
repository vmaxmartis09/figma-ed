#!/usr/bin/env python3
"""INDEX.md per story (thumbnail table of every screen) + root SCREENS.md. Usage: make_index.py <repo root>"""
import json, glob, os, sys, urllib.parse
R = sys.argv[1]; root = ['# Danh sách story và ảnh từng màn\n\nMỗi story có `INDEX.md` hiển thị ảnh tất cả các màn (bấm vào để xem).\n']
dirs = sorted(glob.glob(R + '/FC-Mobile Design/*/_story') + glob.glob(R + '/FC-Mobile Design/*/*/_story') + glob.glob(R + '/HCP-Mobile Design/*/_story'))
q = lambda p: urllib.parse.quote(p)
for d in dirs:
    sj = d + '/screens/screens.json'
    if not os.path.exists(sj): continue
    sc = json.load(open(sj))
    if not sc: continue
    story = os.path.dirname(d); rel = os.path.relpath(story, R)
    L = [f'# {os.path.basename(story)}\n', f'{len(sc)} màn. Ảnh 1x: `_story/screens/<màn>/screen@1x.png`, 2x (nếu có): `screen@2x.png`. Dữ liệu: `styles_all.css`, `tree.json`, `texts.json`, `assets.json`, `icons/`.\n', '| # | Màn | Kích thước | Ảnh | 2x |', '|---|---|---|---|---|']
    for i, s in enumerate(sc, 1):
        f = s['folder']; one = f'_story/screens/{f}/screen@1x.png'; two = f'_story/screens/{f}/screen@2x.png'
        has1 = os.path.exists(f'{story}/{one}'); has2 = os.path.exists(f'{story}/{two}')
        L.append(f"| {i} | {s['name']} | {s['width']}×{s['height']} | " + (f'<img src="{q(one)}" width="160">' if has1 else '—') + ' | ' + (f'[2x]({q(two)})' if has2 else '—') + ' |')
    open(story + '/INDEX.md', 'w').write('\n'.join(L) + '\n')
    root.append(f'- [{rel}]({q(rel)}/INDEX.md) — {len(sc)} màn')
open(R + '/SCREENS.md', 'w').write('\n'.join(root) + '\n')
print('indexes', len(dirs))
