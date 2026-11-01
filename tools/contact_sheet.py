#!/usr/bin/env python3
"""contact_sheet.py <_story> : thumbnail grid of all cropped screens (numbered) -> contact.png"""
import sys, glob, os, json
from PIL import Image, ImageDraw
O = sys.argv[1]; sc = json.load(open(O + '/screens/screens.json'))
items = []
for s in sc:
    f = glob.glob(O + '/screens/' + s['folder'] + '/screen@*.png')
    if f: items.append((s['folder'][:2], f[0]))
T = 150; cols = 12; rows = (len(items) + cols - 1) // cols
sheet = Image.new('RGB', (cols * (T + 6), rows * (T * 2 + 22)), 'white'); d = ImageDraw.Draw(sheet)
for i, (n, f) in enumerate(items):
    im = Image.open(f).convert('RGB'); im.thumbnail((T, T * 2))
    x, y = (i % cols) * (T + 6), (i // cols) * (T * 2 + 22)
    sheet.paste(im, (x, y + 14)); d.text((x + 2, y), n, fill='red')
sheet.save(O + '/contact.png'); print(len(items), sheet.size)
