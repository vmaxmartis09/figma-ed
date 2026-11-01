#!/usr/bin/env python3
"""Crop each screen out of the exported story image using screens.json. Usage: crop_story.py <_story dir>"""
import json, sys, os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
d = sys.argv[1]
img = Image.open(os.path.join(d, 'story.png')).convert('RGBA')
sc = json.load(open(os.path.join(d, 'screens/screens.json')))
for s in sc:
    k = img.width / s['rootW']
    x, y = s['x'] * k, s['y'] * k
    w, h = float(s['width'][:-2]) * k, float(s['height'][:-2]) * k
    img.crop((round(x), round(y), round(x + w), round(y + h))).save(os.path.join(d, 'screens', s['folder'], 'screen@%gx.png' % (round(k * 2) / 2)))
print(len(sc), 'cropped scale', img.width / sc[0]['rootW'] if sc else '')
