#!/usr/bin/env python3
import json, os, glob, sys
from PIL import Image, ImageStat
Image.MAX_IMAGE_PIXELS = None
S = sys.argv[1]; R = '/Volumes/Data/figma-ediva'
rows = []
for l in open(S + '/stories.tsv'):
    page, pj, name, d = l.rstrip('\n').split('\t'); O = d + '/_story'
    r = {'page': page, 'story': d.replace(R + '/', ''), 'css': os.path.getsize(O + '/story_all.css') if os.path.exists(O + '/story_all.css') else 0,
         'png': os.path.exists(O + '/story.png') or bool(glob.glob(O + '/sections/*.png')), 'screens': 0, 'cropped': 0, 'blank': 0, 'badsize': 0, 'dup': 0, 'old_items': 0, 'old_done': 0}
    j = O + '/screens/screens.json'
    if os.path.exists(j):
        sc = json.load(open(j))
        try: secs = json.load(open(O + '/sections.json'))
        except Exception: secs = []
        sc = [x for x in sc if not (isinstance(x.get('section'), int) and x['section'] < len(secs) and 'out date' in secs[x['section']]['name'].lower())]
        sc = [x for x in sc if not x.get('image_missing')]
        r['screens'] = len(sc)
        for i, s in enumerate(sc):
            f = glob.glob(O + '/screens/' + s['folder'] + '/screen@*.png')
            if f:
                r['cropped'] += 1
                try:
                    im = Image.open(f[0]).convert('L'); w = float(s['width'][:-2]); h = float(s['height'][:-2]); k = float(f[0].split('@')[1].split('x')[0])
                    if abs(im.width - w * k) > 2 or abs(im.height - h * k) > 2: r['badsize'] += 1
                    if ImageStat.Stat(im).stddev[0] < 3: r['blank'] += 1
                except Exception: r['badsize'] += 1
            for t in sc[:i]:  # nested duplicate: same size box almost same position
                if abs(t['x'] - s['x']) < 4 and abs(t['y'] - s['y']) < 4: r['dup'] += 1; break
    for x in glob.glob(d + '/*/'):
        if os.path.basename(x.rstrip('/')) == '_story': continue
        if os.path.exists(x + '.done') or os.path.exists(x + 'styles_all.css'): r['old_items'] += 1
        r['old_done'] += os.path.exists(x + '.done') and not os.path.exists(x + 'SKIPPED_OUTDATED')
    rows.append(r)
json.dump(rows, open(R + '/verify.json', 'w'), indent=1, ensure_ascii=False)
for r in rows:
    ok = r['css'] > 0 and r['png'] and r['screens'] > 0 and r['cropped'] == r['screens'] and not r['blank'] and not r['badsize'] and not r['dup']
    st = 'XONG' if ok else ('DO' if r['css'] else 'CHUA')
    print(f"{st}\t{r['story']}\tcss={r['css']//1024}KB png={'y' if r['png'] else 'n'} màn={r['screens']} cắt={r['cropped']} trắng={r['blank']} sai_cỡ={r['badsize']} trùng={r['dup']}")
