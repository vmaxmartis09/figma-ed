#!/usr/bin/env python3
"""Split a story-level "CSS (all layers)" dump into one folder per phone screen.
Usage: split_story.py <story_all.css> <out_dir>
A screen starts at a position:relative block about 375px wide and at least 600px tall."""
import json, re, sys, os

def get(c, k):
    m = re.search(r'(?m)^' + k + r': ([^;]+);', c)
    return m.group(1) if m else ''

def px(v):
    return float(v[:-2]) if v.endswith('px') else 0

def main(src, out):
    t = open(src).read()
    p = re.split(r'(?m)^(/\* .+? \*/)\s*$', t)
    b = [(p[i][3:-3], p[i] + p[i + 1]) for i in range(1, len(p), 2)]
    # absolute origin of each relative block (parent = nearest earlier relative block that can contain it)
    absx = {}; parent = {}
    def num(c, k):
        v = get(c, k); return float(v[:-2]) if v.endswith('px') else 0.0
    rel = [i for i, (_, c) in enumerate(b) if get(c, 'position') == 'relative']
    for n, i in enumerate(rel):
        c = b[i][1]; w, h = num(c, 'width'), num(c, 'height'); l, t_ = num(c, 'left'), num(c, 'top')
        if n == 0: absx[i] = (0.0, 0.0); continue
        par = None
        for j in reversed(rel[:n]):
            cj = b[j][1]
            if num(cj, 'width') >= l + w - 1 and num(cj, 'height') >= t_ + h - 1 and not (num(cj, 'width') == w and num(cj, 'height') == h):
                par = j; break
        px0, py0 = absx.get(par, (0.0, 0.0)) if par is not None else (0.0, 0.0)
        absx[i] = (px0 + l, py0 + t_); parent[i] = par
    root_w, root_h = num(b[0][1], 'width'), num(b[0][1], 'height')
    rel = [i for i, (_, c) in enumerate(b) if get(c, 'position') == 'relative']
    root_i = rel[0] if rel else 0
    def top_section(i):
        while parent.get(i) is not None and parent[i] != root_i: i = parent[i]
        return i if parent.get(i) == root_i else None
    secs, secidx = [], {}
    for i in rel[1:]:
        if parent.get(i) == root_i:
            c = b[i][1]; secidx[i] = len(secs)
            secs.append({'name': b[i][0], 'x': absx[i][0], 'y': absx[i][1], 'w': num(c, 'width'), 'h': num(c, 'height')})
    os.makedirs(out, exist_ok=True)
    json.dump(secs, open(os.path.join(os.path.dirname(out.rstrip('/')), 'sections.json'), 'w'), indent=1, ensure_ascii=False)
    idx, seen = [], {}
    for n, i in enumerate(rel):
        c = b[i][1]
        if not (340 <= px(get(c, 'width')) <= 440 and px(get(c, 'height')) >= 600):
            continue
        name = b[i][0]
        k = i
        while name == 'Auto layout' and k > 0:
            k -= 1
            name = b[k][0]
        end = rel[n + 1] if n + 1 < len(rel) else len(b)
        start = k if b[k][0] == name and k >= i - 1 else i
        seen[name] = seen.get(name, 0) + 1
        base = re.sub(r'[/:\\]+', '-', name).strip() + (f'_{seen[name]}' if seen[name] > 1 else '')
        d = os.path.join(out, f'{len(idx) + 1:02d}_{base}')
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'styles_all.css'), 'w').write('\n'.join(x[1] for x in b[start:end]))
        idx.append({'name': name, 'folder': os.path.basename(d), 'width': get(c, 'width'),
                    'height': get(c, 'height'), 'blocks': end - start, 'x': absx[i][0], 'y': absx[i][1], 'rootW': root_w, 'rootH': root_h, 'section': secidx.get(top_section(i))})
    os.makedirs(out, exist_ok=True)
    json.dump(idx, open(os.path.join(out, 'screens.json'), 'w'), indent=1, ensure_ascii=False)
    print(len(b), 'blocks', len(idx), 'screens')
    return idx

if __name__ == '__main__':
    for s in main(sys.argv[1], sys.argv[2]):
        print(s['folder'], s['width'], s['height'], s['blocks'])
