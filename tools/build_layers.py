#!/usr/bin/env python3
"""styles_all.css of each screen -> layers.json (flat list in Figma DFS order; no depth)."""
import re, json, sys, glob, os
KEYS = ["width","height","left","top","background","color","border-radius","border","box-shadow","opacity",
        "display","flex-direction","align-items","justify-content","gap","padding","font-family","font-size",
        "font-weight","line-height","letter-spacing","text-align","position","flex-grow","align-self"]
def parse(css):
    blocks, cur, comments = [], None, []
    for line in css.splitlines():
        t = line.strip()
        m = re.fullmatch(r"/\*\s*(.*?)\s*\*/", t)
        if m:
            if cur and not cur["props"] and not comments: pass
            comments.append(m.group(1)); continue
        if not t: continue
        m = re.fullmatch(r"([a-z-]+):\s*(.*?);", t)
        if not m: continue
        if comments:
            name = [c for c in comments if not c.startswith(("Auto layout","Inside auto layout","identical","Note","Style"))]
            if name or cur is None:
                cur = {"name": name[0] if name else "?", "props": {}}; blocks.append(cur)
            comments = []
        cur["props"][m.group(1)] = m.group(2)
    return blocks
tot = 0
for p in sys.argv[1:]:
    for f in glob.glob(os.path.join(p, "_story/screens/*/styles_all.css")):
        b = parse(open(f).read())
        out = [{"i": i, "name": x["name"], **{k: v for k, v in x["props"].items() if k in KEYS}} for i, x in enumerate(b)]
        json.dump(out, open(os.path.join(os.path.dirname(f), "layers.json"), "w"), ensure_ascii=False, indent=1)
        tot += 1
print("layers.json written", tot)
