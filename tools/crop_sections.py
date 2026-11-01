#!/usr/bin/env python3
"""Crop screens out of section images. Usage: crop_sections.py <_story dir>"""
import json, sys, os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
d = sys.argv[1]
secs = json.load(open(d + '/sections.json')); sc = json.load(open(d + '/screens/screens.json'))
import zipfile
for fn in sorted(os.listdir(d + '/sections')):
    fp = d + '/sections/' + fn
    if zipfile.is_zipfile(fp):
        z = zipfile.ZipFile(fp); png = [x for x in z.namelist() if x.lower().endswith('.png')]
        data = z.read(png[0]); z.close(); open(fp, 'wb').write(data)
cache = {}; n = miss = 0
for s in sc:
    i = s['section']
    f = f"{d}/sections/{i:02d}.png" if i is not None else None
    if not f or not os.path.exists(f): miss += 1; continue
    if f not in cache: cache[f] = Image.open(f).convert('RGBA')
    im = cache[f]; sec = secs[i]; k = max(1.0, round(im.width / sec['w'] * 2) / 2)
    x, y = (s['x'] - sec['x']) * k, (s['y'] - sec['y']) * k
    w, h = float(s['width'][:-2]) * k, float(s['height'][:-2]) * k
    im.crop((round(x), round(y), round(x + w), round(y + h))).save(f"{d}/screens/{s['folder']}/screen@{round(k * 2) / 2:g}x.png"); n += 1
print('cropped', n, 'missing', miss)
