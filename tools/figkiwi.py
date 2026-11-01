#!/usr/bin/env python3
"""Decode a Figma clipboard (fig-kiwi) buffer: schema (deflate) + message (zstd or deflate) -> python dict.
Usage as module: load_clip_html(path) -> message dict."""
import re, base64, zlib, struct, html, subprocess, tempfile, os, sys
NATIVE = ['bool', 'byte', 'int', 'uint', 'float', 'string', 'int64', 'uint64']
class R:
    def __init__(s, b): s.b = b; s.i = 0
    def byte(s): v = s.b[s.i]; s.i += 1; return v
    def varuint(s):
        v = sh = 0
        while True:
            c = s.byte(); v |= (c & 127) << sh; sh += 7
            if not c & 128: return v
    def varint(s):
        v = s.varuint(); return (~(v >> 1)) if v & 1 else (v >> 1)
    def string(s):
        j = s.b.index(0, s.i); v = s.b[s.i:j].decode('utf8', 'replace'); s.i = j + 1; return v
    def varfloat(s):
        f = s.b[s.i]
        if f == 0: s.i += 1; return 0.0
        bits = s.b[s.i] | s.b[s.i + 1] << 8 | s.b[s.i + 2] << 16 | s.b[s.i + 3] << 24; s.i += 4
        bits = ((bits << 23) | (bits >> 9)) & 0xFFFFFFFF
        return struct.unpack('<f', struct.pack('<I', bits))[0]
def parse_schema(b):
    r = R(b); defs = []
    for _ in range(r.varuint()):
        name = r.string(); kind = r.byte(); fields = []
        for _ in range(r.varuint()):
            fn = r.string(); t = r.varint(); arr = r.byte(); val = r.varuint(); fields.append((fn, t, arr, val))
        defs.append((name, kind, fields))
    return defs
def decode(defs, r, t):
    if t < 0:
        n = NATIVE[~t]
        if n == 'bool': return bool(r.byte())
        if n == 'byte': return r.byte()
        if n == 'int': return r.varint()
        if n == 'uint': return r.varuint()
        if n == 'float': return r.varfloat()
        if n == 'string': return r.string()
        if n in ('int64', 'uint64'): return r.varint() if n == 'int64' else r.varuint()
    name, kind, fields = defs[t]
    if kind == 0:
        v = r.varuint()
        for fn, _, _, val in fields:
            if val == v: return fn
        return v
    if kind == 1:
        return {fn: (decode_arr(defs, r, ft) if arr else decode(defs, r, ft)) for fn, ft, arr, _ in fields}
    out = {}
    while True:
        fid = r.varuint()
        if fid == 0: return out
        f = next(x for x in fields if x[3] == fid)
        out[f[0]] = decode_arr(defs, r, f[1]) if f[2] else decode(defs, r, f[1])
def decode_arr(defs, r, t):
    return [decode(defs, r, t) for _ in range(r.varuint())]
def load_clip_html(path):
    h = html.unescape(open(path).read()); i = h.index('(figma)')
    seg = re.match(r'[A-Za-z0-9+/=_-]+', h[i + 7:]).group(0); seg += '=' * (-len(seg) % 4)
    b = base64.b64decode(seg); off = 12; ch = []
    while off + 4 <= len(b):
        n = struct.unpack('<I', b[off:off + 4])[0]; off += 4; ch.append(b[off:off + n]); off += n
    defs = parse_schema(zlib.decompress(ch[0], -15))
    if ch[1][:4] == b'\x28\xb5\x2f\xfd':
        with tempfile.TemporaryDirectory() as d:
            open(d + '/c', 'wb').write(ch[1]); subprocess.run(['zstd', '-d', '-q', '-f', d + '/c', '-o', d + '/o'], check=True); data = open(d + '/o', 'rb').read()
    else: data = zlib.decompress(ch[1], -15)
    root = next(i for i, d in enumerate(defs) if d[0] == 'Message')
    r = R(data); fields = defs[root][2]; out = {}
    try:
        while True:
            fid = r.varuint()
            if fid == 0: break
            f = next(x for x in fields if x[3] == fid)
            out[f[0]] = decode_arr(defs, r, f[1]) if f[2] else decode(defs, r, f[1])
    except (StopIteration, IndexError, ValueError):
        pass  # trailing fields after nodeChanges are not needed
    return out
if __name__ == '__main__':
    import json
    m = load_clip_html(sys.argv[1]); print(list(m.keys()), len(m.get('nodeChanges', [])))
