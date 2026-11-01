"""Figma vector network blob -> SVG path data; tree node -> SVG fragment."""
import struct
def parse_net(b):
    b = bytes(b); nv, ns, nr = struct.unpack('<3I', b[:12]); o = 12
    V = [struct.unpack('<Iff', b[o + i * 12:o + i * 12 + 12]) for i in range(nv)]; o += nv * 12
    S = [struct.unpack('<IIffIff', b[o + i * 28:o + i * 28 + 28]) for i in range(ns)]; o += ns * 28
    R = []
    for _ in range(nr):
        fl, nl = struct.unpack('<2I', b[o:o + 8]); o += 8; loops = []
        for _ in range(nl):
            c = struct.unpack('<I', b[o:o + 4])[0]; o += 4; loops.append(list(struct.unpack(f'<{c}I', b[o:o + 4 * c]))); o += 4 * c
        R.append((fl, loops))
    return V, S, R
f = lambda x: ('%.3f' % x).rstrip('0').rstrip('.')
def seg_cmd(V, s, rev, sx, sy):
    _, a, tsx, tsy, b, tex, tey = s; va, vb = V[a], V[b]
    p0 = (va[1] * sx, va[2] * sy); p1 = (vb[1] * sx, vb[2] * sy)
    c1 = ((va[1] + tsx) * sx, (va[2] + tsy) * sy); c2 = ((vb[1] + tex) * sx, (vb[2] + tey) * sy)
    if rev: p0, p1, c1, c2 = p1, p0, c2, c1
    if tsx == tsy == tex == tey == 0: return p0, f'L{f(p1[0])} {f(p1[1])}', p1
    return p0, f'C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p1[0])} {f(p1[1])}', p1
def paths(net, sx, sy):
    V, S, R = net; fill = []; stroke = []
    for fl, loops in R:
        for lp in loops:
            rest = list(lp); first = rest.pop(0); order = [(first, False)]; endv = S[first][4]
            while rest:
                nxt = next((i for i in rest if S[i][1] == endv or S[i][4] == endv), None)
                if nxt is None: nxt = rest[0]
                rest.remove(nxt); rev = S[nxt][4] == endv and S[nxt][1] != endv
                order.append((nxt, rev)); endv = S[nxt][1] if rev else S[nxt][4]
            d = ''
            for k, (i, rev) in enumerate(order):
                p0, cmd, p1 = seg_cmd(V, S[i], rev, sx, sy)
                if k == 0: d += f'M{f(p0[0])} {f(p0[1])}'
                d += cmd
            fill.append(d + 'Z')
    used = {i for _, lps in R for lp in lps for i in lp}
    for i, s in enumerate(S):
        p0, cmd, p1 = seg_cmd(V, s, False, sx, sy); stroke.append(f'M{f(p0[0])} {f(p0[1])}{cmd}')
    return ' '.join(fill), ' '.join(stroke)
def paint_attr(ps, key):
    for p in ps or []:
        if p.get('type') == 'SOLID':
            c = p['color']; a = f' {key}-opacity="{f(p["opacity"])}"' if p.get('opacity', 1) != 1 else ''
            if len(c) == 9: a += f' {key}-opacity="{int(c[7:9], 16) / 255:.3f}"'; c = c[:7]
            return f'{key}="{c}"{a}'
    return f'{key}="none"'
def node_svg(n, blobs):
    """n: reduced tree node (needs 'vec' for vector nodes)."""
    if n.get('visible') is False: return ''
    tr = f'transform="translate({f(n["x"])} {f(n["y"])})"'
    if n.get('transform'):
        m00, m01, m10, m11 = n['transform']; tr = f'transform="matrix({f(m00)} {f(m10)} {f(m01)} {f(m11)} {f(n["x"])} {f(n["y"])})"'
    op = f' opacity="{f(n["opacity"])}"' if n.get('opacity') not in (None, 1) else ''
    fills, strokes = n.get('fills'), n.get('strokes'); sw = n.get('strokeWeight') or 0
    sattr = (' ' + paint_attr(strokes, 'stroke') + f' stroke-width="{f(sw)}"' + (f' stroke-linecap="{n["strokeCap"].lower()}"' if n.get('strokeCap') and n['strokeCap'] != 'NONE' else '') + (f' stroke-linejoin="{n["strokeJoin"].lower()}"' if n.get('strokeJoin') else '')) if strokes and sw else ''
    t = n['type']; body = ''
    if n.get('vec') is not None:
        v = n['vec']; sx = n['w'] / v['nw'] if v['nw'] else 1; sy = n['h'] / v['nh'] if v['nh'] else 1
        fd, sd = paths(parse_net(blobs[v['blob']]['bytes']), sx, sy)
        if fd and fills: body = f'<path d="{fd}" {paint_attr(fills, "fill")} fill-rule="evenodd"{sattr}/>'
        if sd and (not fd or not fills) and strokes and sw: body = f'<path d="{sd}" fill="none"{sattr}/>'
        elif sd and fd and fills and sattr: body += ''
    elif t == 'ELLIPSE': body = f'<ellipse cx="{f(n["w"]/2)}" cy="{f(n["h"]/2)}" rx="{f(n["w"]/2)}" ry="{f(n["h"]/2)}" {paint_attr(fills, "fill")}{sattr}/>'
    elif t in ('ROUNDED_RECTANGLE', 'RECTANGLE'): body = f'<rect width="{f(n["w"])}" height="{f(n["h"])}" rx="{f(n.get("cornerRadius", 0))}" {paint_attr(fills, "fill")}{sattr}/>'
    elif t == 'LINE': body = f'<line x2="{f(n["w"])}" {paint_attr(strokes, "stroke")} stroke-width="{f(sw or 1)}"/>'
    inner = ''.join(node_svg(c, blobs) for c in n.get('children', []))
    if not body and not inner: return ''
    return f'<g {tr}{op}>{body}{inner}</g>'
