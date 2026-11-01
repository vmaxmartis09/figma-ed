#!/usr/bin/env python3
"""Turn layers_raw.json (Figma Properties panel dump) into layers.json, texts.json,
colors.json, styles.css, meta.json and a Flutter screen skeleton. Usage: postprocess.py <screen_dir>"""
import json, re, sys, os

SECTIONS = {"Layout", "Content", "Typography", "Colors", "Borders", "Effects", "Auto layout",
            "Export", "Constraints", "Appearance", "Fill", "Stroke", "Layout grid", "Styles"}
LAYOUT_KEYS = {"Flow", "Width", "Height", "Top", "Left", "Gap", "Padding", "Radius", "Opacity",
               "Clip content", "Rotation"}
TYPO_KEYS = {"Name", "Font", "Weight", "Style", "Size", "Line height", "Paragraph spacing",
             "Letter spacing", "Horizontal alignment", "Vertical alignment", "Text decoration",
             "Text case", "Paragraph indent", "List style"}
HEX = re.compile(r"^#[0-9A-Fa-f]{6,8}$")


def num(v):
    m = re.search(r"-?\d+(\.\d+)?", v or "")
    return float(m.group()) if m else None


def parse(lines):
    out = {"layout": {}, "typography": {}, "content": None, "colors": [], "borders": [], "effects": []}
    section, i, pend = None, 0, None
    while i < len(lines):
        l = lines[i]
        if l in SECTIONS:
            section, pend = l, None
            i += 1
            continue
        if section == "Layout" and l in LAYOUT_KEYS and i + 1 < len(lines):
            out["layout"][l] = lines[i + 1]; i += 2; continue
        if section == "Typography" and l in TYPO_KEYS and i + 1 < len(lines):
            out["typography"][l] = lines[i + 1]; i += 2; continue
        if section == "Content":
            out["content"] = (out["content"] + "\n" if out["content"] else "") + l
        elif section in ("Colors", "Borders", "Effects"):
            if l in ("Color format", "Hex", "Border", "All sides"):
                pass
            elif HEX.match(l):
                item = {"hex": l.upper(), "token": pend}
                pend = None
                tgt = {"Colors": "colors", "Borders": "borders", "Effects": "effects"}[section]
                out[tgt].append(item)
            elif section == "Borders" and re.match(r"^\d+(\.\d+)?px$", l):
                out["borders"].append({"width": l})
            else:
                pend = l
        i += 1
    return out


def css_name(s):
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s or "layer"


def main(d):
    raw = json.load(open(os.path.join(d, "layers_raw.json")))
    screen = os.path.basename(d.rstrip("/"))
    nodes = []
    for r in raw:
        p = parse(r.get("lines") or [])
        nodes.append({"name": r["name"], "depth": r["depth"], "ok": bool(r.get("lines")), **p})
    # tree
    root, stack = None, []
    for n in nodes:
        n["children"] = []
        while stack and stack[-1]["depth"] >= n["depth"]:
            stack.pop()
        if stack:
            stack[-1]["children"].append(n)
        elif root is None:
            root = n
        stack.append(n)

    def clean(n):
        n = dict(n); ch = [clean(c) for c in n.pop("children")]
        n.pop("depth", None)
        for k in ("layout", "typography", "colors", "borders", "effects"):
            if not n[k]: n.pop(k)
        if n.get("content") is None: n.pop("content", None)
        if ch: n["children"] = ch
        return n
    json.dump(clean(root) if root else {}, open(os.path.join(d, "layers.json"), "w"), indent=1, ensure_ascii=False)

    texts = [{"name": n["name"], "text": n["content"], **n["typography"], "color": (n["colors"] or [{}])[0]}
             for n in nodes if n["typography"] and n["content"]]
    json.dump(texts, open(os.path.join(d, "texts.json"), "w"), indent=1, ensure_ascii=False)

    cols = {}
    for n in nodes:
        for c in n["colors"]:
            k = (c["hex"], c["token"])
            cols[k] = cols.get(k, 0) + 1
    json.dump([{"hex": h, "token": t, "uses": u} for (h, t), u in sorted(cols.items(), key=lambda x: -x[1])],
              open(os.path.join(d, "colors.json"), "w"), indent=1)

    # css (flat, class per layer, indexed to stay unique)
    css, used = [], {}
    for idx, n in enumerate(nodes):
        base = css_name(n["name"]); used[base] = used.get(base, 0) + 1
        cls = base if used[base] == 1 else f"{base}-{used[base]}"
        L, T = n["layout"], n["typography"]
        rules = []
        if num(L.get("Width")) is not None and "Fixed" in L.get("Width", "") or re.fullmatch(r"[\d.]+px", L.get("Width", "")):
            rules.append(f"width:{num(L['Width'])}px")
        if re.fullmatch(r"[\d.]+px", L.get("Height", "")) or "Fixed" in L.get("Height", ""):
            rules.append(f"height:{num(L['Height'])}px")
        if "Padding" in L: rules.append(f"padding:{L['Padding']}")
        if "Gap" in L: rules.append(f"gap:{L['Gap']}")
        if "Radius" in L: rules.append("border-radius:" + (re.search(r"\d+(\.\d+)?", L["Radius"]).group() + "px" if re.search(r"\d", L["Radius"]) else L["Radius"]))
        if L.get("Flow") in ("Horizontal", "Vertical"):
            rules.append("display:flex;flex-direction:" + ("row" if L["Flow"] == "Horizontal" else "column"))
        if T:
            rules.append(f"font-family:'{T.get('Font','Roboto')}';font-size:{num(T.get('Size'))}px;font-weight:{T.get('Weight')}"
                         f";line-height:{num(T.get('Line height'))}px;letter-spacing:{T.get('Letter spacing','0')}")
            if T.get("Horizontal alignment"): rules.append("text-align:" + T["Horizontal alignment"].lower())
            if n["colors"]: rules.append(f"color:{n['colors'][0]['hex']}")
        elif n["colors"]:
            rules.append(f"background:{n['colors'][0]['hex']}")
        tok = [c["token"] for c in n["colors"] if c["token"]] + ([T["Name"]] if T.get("Name") else [])
        css.append(f"/* {n['name']} (depth {n['depth']}){' tokens: ' + ', '.join(tok) if tok else ''} */\n.{cls} {{ {'; '.join(rules)} }}")
    open(os.path.join(d, "styles.css"), "w").write("\n".join(css) + "\n")

    r0 = nodes[0] if nodes else {"layout": {}}
    json.dump({"screen": screen, "width": r0["layout"].get("Width"), "height": r0["layout"].get("Height"),
               "layerCount": len(nodes), "layersWithoutProps": [n["name"] for n in nodes if not n["ok"]]},
              open(os.path.join(d, "meta.json"), "w"), indent=1)

    # Flutter skeleton
    def dart(n, ind):
        sp = "  " * ind; L, T = n["layout"], n["typography"]
        if T and n["content"]:
            nm = re.sub(r"[^A-Za-z0-9]", "", (T.get("Name") or "").title().replace("/", ""))
            txt = n["content"].replace("'", "\\'").replace("\n", "\\n")
            return f"{sp}Text('{txt}', style: TextStyle(fontFamily: '{T.get('Font','Roboto')}', fontSize: {num(T.get('Size'))}, fontWeight: FontWeight.w{T.get('Weight','400')}, height: {num(T.get('Line height'))}/{num(T.get('Size'))})), // {T.get('Name','')}"
        kids = [dart(c, ind + 1) for c in n["children"]]
        if not kids:
            w, h = num(L.get("Width")), num(L.get("Height"))
            return f"{sp}SizedBox(width: {w}, height: {h}), // {n['name']}"
        widget = "Row" if L.get("Flow") == "Horizontal" else "Column"
        gap = num(L.get("Gap"))
        body = ",\n".join(kids)
        return f"{sp}{widget}( // {n['name']}\n{sp}  spacing: {gap or 0},\n{sp}  children: [\n{body},\n{sp}  ],\n{sp})"
    # nodes already carry children in the cleaned copy; rebuild from original tree
    def to_dart_tree(n): return n
    cls = "".join(w.capitalize() for w in re.split(r"[^A-Za-z0-9]+", re.sub(r"^\d+_", "", screen))) or "Screen"
    body = dart(root, 3) if root else "SizedBox()"
    open(os.path.join(d, "screen.dart"), "w").write(
        "import 'package:flutter/material.dart';\n\n// Skeleton generated from Figma properties; adjust widgets manually.\n"
        f"class {cls}Screen extends StatelessWidget {{\n  const {cls}Screen({{super.key}});\n\n  @override\n  Widget build(BuildContext context) {{\n    return Scaffold(\n      body: SafeArea(\n        child: SingleChildScrollView(\n          child:\n{body},\n        ),\n      ),\n    );\n  }}\n}}\n")


if __name__ == "__main__":
    for d in sys.argv[1:]:
        if os.path.exists(os.path.join(d, "layers_raw.json")):
            main(d); print("ok", d)
