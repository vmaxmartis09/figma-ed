#!/usr/bin/env python3
"""styles_all.css (Figma 'Copy as CSS (all layers)') + layers_names.json -> styles.css, texts.json, colors.json, layers.json, meta.json, screen.dart"""
import json, re, sys, os

def blocks(css):
    out = []
    for m in re.finditer(r"/\*\s*(.+?)\s*\*/\s*\n(.*?)(?=\n/\*\s*[^/*A][^*]*\*/\s*\n|\Z)", css, re.S):
        pass
    # Figma separates layers by a header comment line "/* Name */" followed by a blank line.
    parts = re.split(r"(?m)^/\*\s*(.+?)\s*\*/\s*$", css)
    # parts: [pre, name1, body1, name2, body2 ...]
    i = 1
    while i < len(parts) - 1:
        name, body = parts[i].strip(), parts[i + 1]
        if name in ("Auto layout", "Inside auto layout"):
            # sub-section comment; merge into previous body
            if out: out[-1]["body"] += f"\n/* {name} */\n" + body
            i += 2; continue
        out.append({"name": name, "body": body}); i += 2
    return out

def props(body):
    d = {}
    for m in re.finditer(r"([a-z-]+)\s*:\s*([^;]+);", body):
        d[m.group(1)] = m.group(2).strip()
    return d

def main(d):
    css_path = os.path.join(d, "styles_all.css")
    if not os.path.exists(css_path) or os.path.getsize(css_path) == 0:
        print("no css", d); return
    css = open(css_path).read()
    bl = blocks(css)
    names = json.load(open(os.path.join(d, "layers_names.json"))) if os.path.exists(os.path.join(d, "layers_names.json")) else []
    texts, colors = [], {}
    cls_used, outcss = {}, []
    for b in bl:
        p = props(b["body"]); b["props"] = p
        base = re.sub(r"[^A-Za-z0-9]+", "-", b["name"]).strip("-").lower() or "layer"
        cls_used[base] = cls_used.get(base, 0) + 1
        cls = base if cls_used[base] == 1 else f"{base}-{cls_used[base]}"
        outcss.append(f"/* {b['name']} */\n.{cls} {{\n" + "\n".join(f"  {k}: {v};" for k, v in p.items()) + "\n}")
        for k in ("background", "color", "border", "box-shadow"):
            for h in re.findall(r"#[0-9A-Fa-f]{3,8}", p.get(k, "")):
                colors[h.upper()] = colors.get(h.upper(), 0) + 1
        if "font-family" in p or "font-size" in p or "font" in p:
            t = {"name": b["name"], "text": b["name"]}
            for k in ("font-family", "font-size", "font-weight", "line-height", "letter-spacing", "text-align", "color"):
                if k in p: t[k] = p[k]
            texts.append(t)
    open(os.path.join(d, "styles.css"), "w").write("\n\n".join(outcss) + "\n")
    json.dump(texts, open(os.path.join(d, "texts.json"), "w"), indent=1, ensure_ascii=False)
    json.dump([{"hex": h, "uses": u} for h, u in sorted(colors.items(), key=lambda x: -x[1])], open(os.path.join(d, "colors.json"), "w"), indent=1)
    # layers.json = names tree merged with css props by order of appearance (best effort)
    root, stack = None, []
    for i, n in enumerate(names):
        node = {"name": n["name"], "depth": n["depth"], "children": []}
        same = [b for b in bl if b["name"] == n["name"]]
        cnt = sum(1 for x in names if x["name"] == n["name"])
        node["css"] = same[0]["props"] if len(same) == 1 and cnt == 1 else None
        while stack and stack[-1]["depth"] >= n["depth"]: stack.pop()
        (stack[-1]["children"] if stack else (root.__setitem__ if False else [])).append(node) if stack else None
        if not stack and root is None: root = node
        stack.append(node)
    def clean(n):
        n = dict(n); n.pop("depth", None); ch = [clean(c) for c in n.pop("children")]
        if ch: n["children"] = ch
        if n.get("css") is None: n.pop("css", None)
        return n
    json.dump(clean(root) if root else {}, open(os.path.join(d, "layers.json"), "w"), indent=1, ensure_ascii=False)
    matched = sum(1 for n in names if sum(1 for b in bl if b["name"] == n["name"]) == 1 and sum(1 for x in names if x["name"] == n["name"]) == 1)
    top = bl[0]["props"] if bl else {}
    json.dump({"screen": os.path.basename(d.rstrip('/')), "width": top.get("width"), "height": top.get("height"),
               "cssBlocks": len(bl), "layerNames": len(names), "namesMatchedToCss": matched,
               "assets": sorted(os.listdir(os.path.join(d, "assets"))) if os.path.isdir(os.path.join(d, "assets")) else []},
              open(os.path.join(d, "meta.json"), "w"), indent=1)
    print("ok", d, len(bl), "css blocks;", matched, "/", len(names), "names matched")

if __name__ == "__main__":
    for d in sys.argv[1:]: main(d)
