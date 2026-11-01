#!/usr/bin/env python3
"""Crop screen@2x.png from story_copy.png (Figma 'Copy as PNG' of the whole story at 2x). Usage: crop_2x.py <_story>"""
import sys, json, os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
D = sys.argv[1]; src = D + '/story_copy.png'
sc = json.load(open(D + '/screens/screens.json')); im = Image.open(src).convert('RGBA'); k = im.width / sc[0]['rootW']
k = round(k * 2) / 2
if k < 1.5: print(D.split('figma-ediva/')[-1], 'copy is 1x only, skipped'); sys.exit(0)
n = 0
for s in sc:
    w, h = float(s['width'][:-2]), float(s['height'][:-2])
    box = (round(s['x'] * k), round(s['y'] * k), round((s['x'] + w) * k), round((s['y'] + h) * k))
    im.crop(box).save(f"{D}/screens/{s['folder']}/screen@{k:g}x.png"); n += 1
print(D.split('figma-ediva/')[-1], 'scale', round(k, 3), 'cropped', n)
