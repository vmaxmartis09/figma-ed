#!/usr/bin/env python3
"""Crop every image-fill node (photos, avatars, thumbnails) of each screen out of screen@2x.png into <screen>/images/NN.png
and record 'file' in assets.json. Usage: crop_images.py <repo root>"""
import json, glob, os, sys
from PIL import Image
R = sys.argv[1]; n = 0
for aj in glob.glob(R + '/*/*/_story/screens/*/assets.json') + glob.glob(R + '/*/*/*/_story/screens/*/assets.json'):
    if aj.startswith(R + '/Archive') or '/Proposal/' in aj or '/Cover/' in aj: continue
    d = os.path.dirname(aj); p = d + '/screen@2x.png'; a = json.load(open(aj))
    if not os.path.exists(p) or not any(x['kind'] == 'image' for x in a): continue
    im = Image.open(p).convert('RGBA'); os.makedirs(d + '/images', exist_ok=True); k = 0
    for x in a:
        if x['kind'] != 'image': continue
        k += 1; box = tuple(round(v * 2) for v in (x['x'], x['y'], x['x'] + x['w'], x['y'] + x['h']))
        im.crop(box).save(f'{d}/images/{k:02d}.png'); x['file'] = f'images/{k:02d}.png'; n += 1
    json.dump(a, open(aj, 'w'), ensure_ascii=False, indent=1)
print('images cropped', n)
