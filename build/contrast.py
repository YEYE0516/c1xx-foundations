"""WCAG contrast report for foundations/color.json resolved against a theme.

usage: python3 -I build/contrast.py themes/site/theme.json > docs/04-contrast.md
"""
import json, re, sys

found = json.load(open("foundations/color.json"))
theme = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}

def get(path, root):
    cur = root
    for part in path.split("."):
        cur = cur[part]
    return cur["$value"]

def resolve(v, mode):
    seen = 0
    while isinstance(v, str) and "{" in v and seen < 10:
        seen += 1
        m = re.search(r"\{([^}]+)\}", v)
        ref = m.group(1)
        if ref.startswith("theme.accent."):
            try: val = get(ref.replace("theme.accent.", f"theme.accent.{mode}."), theme)
            except KeyError: val = get(ref, theme)
        elif ref.startswith("theme."):
            val = get(ref, theme)
        elif ref.startswith("energy."):
            val = get(ref, theme)
        elif ref.startswith("neutral.") or ref.startswith("accent."):
            val = get(ref, found)
        elif ref.startswith("shadow."):
            val = get(f"semantic.{mode}." + ref, found)
        else:
            val = get(ref, found)
        v = v.replace(m.group(0), val if isinstance(val, str) else val[0])
    return v

def lum(hexs):
    hexs = hexs.lstrip("#")
    r, g, b = [int(hexs[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

pairs = [
    ("fg.primary", "bg.canvas", "正文"), ("fg.primary", "bg.surface", "卡片正文"), ("fg.primary", "bg.raised", "弹层正文"),
    ("fg.secondary", "bg.canvas", "次级文字"), ("fg.secondary", "bg.surface", "卡片次级文字"),
    ("fg.muted", "bg.canvas", "metadata ≥ 12px"),
    ("fg.on-inverse", "bg.inverse", "反色块文字"),
    ("action.primary-fg", "action.primary", "主按钮文字"),
    ("fg.primary", "action.selected-bg", "选中态文字"),
    ("border.subtle", "bg.canvas", "分隔线（非文字，3:1 即可）"),
    ("action.signal", "bg.canvas", "signal 作为小字"),
    ("focus.ring", "bg.canvas", "焦点环（非文字，3:1）"),
]

print("# 对比度报告 · " + (sys.argv[1] if len(sys.argv) > 1 else "foundations only"))
print()
print("WCAG 2.x。正文 AA ≥ 4.5，大字（≥ 24px 或 ≥ 19px 粗体）AA ≥ 3，非文字 UI ≥ 3。AAA ≥ 7。")
print()
for mode in ("light", "dark"):
    print(f"## {mode}")
    print()
    print("| 前景 | 背景 | 比值 | 正文 AA | 大字 AA | AAA | 用途 |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for fg, bg, use in pairs:
        try:
            src = found["semantic"][mode]
            if fg == "focus.ring" and mode == "light" and "focus" in theme.get("theme", {}):
                a = resolve(theme["theme"]["focus"]["ring"]["$value"], mode)
            else:
                a = resolve(get(f"semantic.{mode}.{fg}", found), mode)
            if bg == "bg.canvas" and mode == "light" and "canvas" in theme.get("theme", {}):
                b = resolve(theme["theme"]["canvas"]["$value"], mode)
            else:
                b = resolve(get(f"semantic.{mode}.{bg}", found), mode)
        except KeyError as e:
            print(f"| {fg} | {bg} | — | | | | 未解析 {e} |"); continue
        if not (a.startswith("#") and b.startswith("#")):
            print(f"| {fg} | {bg} | — | | | | 非纯色 `{a}` / `{b}` |"); continue
        c = contrast(a, b)
        ok = lambda t: "✓" if c >= t else "✗"
        print(f"| {fg} `{a}` | {bg} `{b}` | **{c:.2f}** | {ok(4.5)} | {ok(3)} | {ok(7)} | {use} |")
    print()

# energy forms (if the theme has them)
if "energy" in theme:
    canvas = {"light": resolve(theme["theme"]["canvas"]["$value"], "light") if "canvas" in theme["theme"] else resolve(get("semantic.light.bg.canvas", found), "light"),
              "dark": resolve(get("semantic.dark.bg.canvas", found), "dark")}
    print("## energy forms")
    print()
    print("| form | mode | base on canvas (非文字 ≥3) | strong on canvas (文字 ≥4.5) | on over base (文字 ≥4.5) |")
    print("| --- | --- | --- | --- | --- |")
    for form, node in theme["energy"].items():
        if form.startswith("$"): continue
        for mode in ("light", "dark"):
            g = lambda k: resolve(node[mode][k]["$value"], mode)
            c1, c2, c3 = contrast(g("base"), canvas[mode]), contrast(g("strong"), canvas[mode]), contrast(g("on"), g("base"))
            ok = lambda c, t: "✓" if c >= t else "✗"
            print(f"| {form} | {mode} | {c1:.2f} {ok(c1,3)} | {c2:.2f} {ok(c2,4.5)} | {c3:.2f} {ok(c3,4.5)} |")
    print()
