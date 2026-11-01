#!/usr/bin/env python3
"""Draw the detected screen boxes on the story image: overview.png. Usage: overview.py <_story dir>"""
import json, sys, os
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
d = sys.argv[1]
img = Image.open(os.path.join(d, 'story.png')).convert('RGB')
sc = json.load(open(os.path.join(d, 'screens/screens.json')))
k = img.width / sc[0]['rootW'] if sc else 1
dr = ImageDraw.Draw(img)
for i, s in enumerate(sc, 1):
    x, y = s['x'] * k, s['y'] * k; w, h = float(s['width'][:-2]) * k, float(s['height'][:-2]) * k
    dr.rectangle([x, y, x + w, y + h], outline=(255, 0, 0), width=max(3, int(img.width / 600)))
    dr.text((x + 6, y + 6), str(i), fill=(255, 0, 0))
f = 1600 / img.width
if f < 1: img = img.resize((1600, int(img.height * f)))
img.save(os.path.join(d, 'overview.png'))
print(d, len(sc), img.size)
