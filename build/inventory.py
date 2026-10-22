"""Design-value inventory: scan CSS / TSX / Tailwind config and emit a markdown report.

usage: python3 -I inventory.py OUT.md LABEL=path [LABEL=path ...]
"""
import re, sys, json
from collections import Counter, defaultdict

out_path = sys.argv[1]
sources = []
for arg in sys.argv[2:]:
    label, path = arg.split("=", 1)
    sources.append((label, path))

# ---------- helpers ----------
HEX = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b")
FUNC_COLOR = re.compile(r"\b(?:rgba?|hsla?|oklch|color-mix)\((?:[^()]|\([^()]*\))*\)")
DECL = lambda prop: re.compile(r"(?<![-\w])" + prop + r"\s*:\s*([^;{}]+?)\s*(?:;|\}|$)", re.M)
FONT_FAMILY = DECL(r"font-family")
FONT_SIZE = DECL(r"font-size")
LINE_HEIGHT = DECL(r"line-height")
LETTER = DECL(r"letter-spacing")
RADIUS = DECL(r"border-radius")
SHADOW = DECL(r"box-shadow")
TRANSITION = DECL(r"transition(?:-duration)?")
ANIM = DECL(r"animation(?:-duration)?")
SPACING_PROPS = r"(?:padding|margin|gap|row-gap|column-gap)(?:-(?:top|right|bottom|left|inline|block|inline-start|inline-end))?"
SPACING = DECL(SPACING_PROPS)
WIDTH = DECL(r"(?:max-width|width|min-width|max-height|height|min-height)")
DUR = re.compile(r"(\d*\.?\d+)(ms|s)\b")
EASE = re.compile(r"(cubic-bezier\([^)]*\)|ease-in-out|ease-in|ease-out|ease|linear|steps\([^)]*\))")
LEN = re.compile(r"-?\d*\.?\d+(?:px|rem|em|vw|vh|%|ch)")
FONT_WEIGHT = DECL(r"font-weight")

# Tailwind class tokens in TSX
TW_CLASS = re.compile(r'className=\{?["\'`]([^"\'`]+)["\'`]')
TW_SPACING = re.compile(r"^(?:-?)(?:p|px|py|pt|pr|pb|pl|m|mx|my|mt|mr|mb|ml|gap|gap-x|gap-y|space-x|space-y)-(\d+(?:\.\d+)?|px|\[[^\]]+\])$")
TW_TEXT = re.compile(r"^text-(xs|sm|base|lg|xl|[2-9]xl|\[[\d.]+(?:rem|px|em)\])$")
TW_LEADING = re.compile(r"^leading-(\w+|\[[^\]]+\])$")
TW_TRACKING = re.compile(r"^tracking-(\w+|\[[^\]]+\])$")
TW_ROUNDED = re.compile(r"^rounded(?:-[trbl]{1,2})?(?:-(\w+|\[[^\]]+\]))?$")
TW_SHADOW = re.compile(r"^shadow(?:-(\w+|\[[^\]]+\]))?$")
TW_COLOR = re.compile(r"^(?:bg|text|border|ring|from|to|via|fill|stroke|shadow|outline)-(\[#[0-9a-fA-F]{3,8}\]|\[rgba?\([^\]]+\)\]|[a-z]+-(?:[a-z]+|\d{2,3})(?:/\d+)?)$")
TW_DURATION = re.compile(r"^duration-(\d+|\[[^\]]+\])$")
TW_EASE = re.compile(r"^ease-(\w+|\[[^\]]+\])$")
TW_FONT = re.compile(r"^font-(display|ui|sans|serif|mono|thin|light|normal|medium|semibold|bold|extrabold|black)$")
TW_SIZE = {"xs": "12/16", "sm": "14/20", "base": "16/24", "lg": "18/28", "xl": "20/28", "2xl": "24/32", "3xl": "30/36", "4xl": "36/40", "5xl": "48/48", "6xl": "60/60", "7xl": "72/72"}
TW_RAD = {"none": "0", "sm": "2px", "": "4px", "md": "6px", "lg": "8px", "xl": "12px", "2xl": "16px", "3xl": "24px", "4xl": "28px*", "5xl": "36px*", "full": "9999px"}

# ---------- collectors ----------
cats = {k: defaultdict(Counter) for k in [
    "color", "font_family", "font_size", "line_height", "letter_spacing", "font_weight",
    "spacing", "radius", "shadow", "duration", "easing", "width",
    "tw_spacing", "tw_text", "tw_leading", "tw_tracking", "tw_rounded", "tw_shadow", "tw_color", "tw_duration", "tw_ease", "tw_font",
]}
css_var_defs = defaultdict(dict)   # label -> {var: value}
css_var_uses = defaultdict(Counter)
inline_hex_in_tsx = defaultdict(Counter)
file_lines = {}

def add(cat, label, value):
    cats[cat][value.strip()][label] += 1

def norm_color(c):
    c = c.strip()
    if c.startswith("#"):
        c = c.lower()
        if len(c) == 4:
            c = "#" + "".join(ch * 2 for ch in c[1:])
        elif len(c) == 5:
            c = "#" + "".join(ch * 2 for ch in c[1:])
        return c
    return re.sub(r"\s+", "", c)

for label, path in sources:
    txt = open(path, encoding="utf-8", errors="replace").read()
    file_lines[label] = txt.count("\n") + 1
    is_css = path.endswith(".css")
    is_tsx = path.endswith((".tsx", ".ts", ".jsx", ".js"))
    is_tw_config = path.endswith("tailwind.config.js")

    # colours anywhere
    for m in HEX.finditer(txt):
        add("color", label, norm_color(m.group(0)))
    for m in FUNC_COLOR.finditer(txt):
        add("color", label, norm_color(m.group(0)))

    if is_css or is_tw_config:
        for m in re.finditer(r"(?<![\w-])(--[\w-]+)\s*:\s*([^;{}]+);", txt):
            css_var_defs[label][m.group(1)] = m.group(2).strip()
        for m in re.finditer(r"var\((--[\w-]+)", txt):
            css_var_uses[label][m.group(1)] += 1
        for rx, cat in [(FONT_FAMILY, "font_family"), (FONT_SIZE, "font_size"), (LINE_HEIGHT, "line_height"),
                        (LETTER, "letter_spacing"), (RADIUS, "radius"), (SHADOW, "shadow"), (FONT_WEIGHT, "font_weight")]:
            for m in rx.finditer(txt):
                add(cat, label, m.group(1))
        for m in SPACING.finditer(txt):
            v = m.group(1)
            if v.startswith("var(") or v in ("0", "auto", "inherit"):
                continue
            for tok in v.split():
                if LEN.fullmatch(tok) or tok == "0":
                    add("spacing", label, tok)
        for m in WIDTH.finditer(txt):
            v = m.group(1)
            if LEN.fullmatch(v) or v.startswith("clamp") or v.startswith("min(") or v.startswith("max("):
                add("width", label, v)
        for rx in (TRANSITION, ANIM):
            for m in rx.finditer(txt):
                v = m.group(1)
                for d in DUR.finditer(v):
                    num, unit = d.groups()
                    ms = float(num) * (1000 if unit == "s" else 1)
                    add("duration", label, f"{ms:g}ms")
                for e in EASE.finditer(v):
                    add("easing", label, e.group(1))
        if is_tw_config:
            for m in re.finditer(r'"?([\w-]+)"?:\s*"((?:cubic-bezier|0 )[^"]+)"', txt):
                k, v = m.groups()
                if v.startswith("cubic"):
                    add("easing", label, v)
                else:
                    add("shadow", label, v)
            for m in re.finditer(r'"(\dxl)":\s*"(\d+px)"', txt):
                add("radius", label, m.group(2))

    if is_tsx:
        # inline style objects
        for m in re.finditer(r"style=\{\{([^}]*)\}\}", txt):
            body = m.group(1)
            for h in HEX.finditer(body):
                inline_hex_in_tsx[label][norm_color(h.group(0))] += 1
            for kv in re.finditer(r"(\w+)\s*:\s*['\"]([^'\"]+)['\"]", body):
                k, v = kv.groups()
                if k in ("fontSize",): add("font_size", label, v)
                elif k in ("lineHeight",): add("line_height", label, v)
                elif k in ("borderRadius",): add("radius", label, v)
                elif k.startswith(("padding", "margin", "gap")): add("spacing", label, v)
        # Tailwind classes
        for m in TW_CLASS.finditer(txt):
            for tok in m.group(1).split():
                tok = tok.split(":")[-1]   # drop variants (sm:, hover:, data-[..]:)
                if TW_SPACING.match(tok): add("tw_spacing", label, tok)
                elif TW_TEXT.match(tok): add("tw_text", label, tok)
                elif TW_LEADING.match(tok): add("tw_leading", label, tok)
                elif TW_TRACKING.match(tok): add("tw_tracking", label, tok)
                elif TW_ROUNDED.match(tok): add("tw_rounded", label, tok)
                elif TW_SHADOW.match(tok): add("tw_shadow", label, tok)
                elif TW_COLOR.match(tok): add("tw_color", label, tok)
                elif TW_DURATION.match(tok): add("tw_duration", label, tok)
                elif TW_EASE.match(tok): add("tw_ease", label, tok)
                elif TW_FONT.match(tok): add("tw_font", label, tok)

# ---------- report ----------
labels = [l for l, _ in sources]

def table(cat, title, note="", limit=None, sort_key=None):
    rows = cats[cat]
    if not rows:
        return ""
    items = list(rows.items())
    if sort_key:
        items.sort(key=sort_key)
    else:
        items.sort(key=lambda kv: -sum(kv[1].values()))
    if limit:
        items = items[:limit]
    lines = [f"### {title}", ""]
    if note:
        lines += [note, ""]
    lines.append("| 值 | 总次数 | " + " | ".join(labels) + " |")
    lines.append("| --- | --- | " + " | ".join("---" for _ in labels) + " |")
    for v, c in items:
        lines.append(f"| `{v}` | {sum(c.values())} | " + " | ".join(str(c.get(l, "")) for l in labels) + " |")
    lines.append("")
    lines.append(f"去重后 **{len(rows)}** 个不同值。")
    lines.append("")
    return "\n".join(lines)

def px_key(v):
    m = re.match(r"-?(\d*\.?\d+)(px|rem|em)", v)
    if not m: return (1, v)
    n = float(m.group(1)); u = m.group(2)
    return (0, n * 16 if u in ("rem", "em") else n)

def tw_key(v):
    m = re.search(r"-(\d+(?:\.\d+)?)$", v)
    return (0, float(m.group(1))) if m else (1, v)

parts = ["# 盘点 · inventory", "",
         "扫描日期 2026-10-22。脚本从下列文件里抽出所有硬编码的设计值，去重、计数、标出处。这是底座建立之前的 **before**。", "",
         "| 标签 | 文件 | 行数 |", "| --- | --- | --- |"]
for l, p in sources:
    parts.append(f"| {l} | `{p.split('/home/claude/')[-1]}` | {file_lines[l]} |")
parts.append("")

summary = {
    "颜色（hex / rgba / hsl，含 Tailwind 任意值）": len(cats["color"]),
    "font-family 声明": len(cats["font_family"]),
    "font-size": len(cats["font_size"]) + len(cats["tw_text"]),
    "line-height": len(cats["line_height"]) + len(cats["tw_leading"]),
    "间距值（padding/margin/gap）": len(cats["spacing"]),
    "Tailwind 间距 class": len(cats["tw_spacing"]),
    "border-radius": len(cats["radius"]) + len(cats["tw_rounded"]),
    "box-shadow": len(cats["shadow"]) + len(cats["tw_shadow"]),
    "动效时长": len(cats["duration"]) + len(cats["tw_duration"]),
    "easing": len(cats["easing"]) + len(cats["tw_ease"]),
}
parts += ["## 一眼看完的数字", "", "| 类别 | 不同值的个数 |", "| --- | --- |"]
for k, v in summary.items():
    parts.append(f"| {k} | {v} |")
parts.append("")

parts += ["## CSS 变量", ""]
for l in labels:
    if css_var_defs[l]:
        parts += [f"**{l}** 定义了 {len(css_var_defs[l])} 个变量：", ""]
        parts.append("| 变量 | 值 | 被引用次数 |")
        parts.append("| --- | --- | --- |")
        for k, v in css_var_defs[l].items():
            parts.append(f"| `{k}` | `{v}` | {css_var_uses[l].get(k, 0)} |")
        parts.append("")
    else:
        parts += [f"**{l}**：没有 CSS 变量。", ""]

parts += ["## 颜色", ""]
parts.append(table("color", "所有颜色值", "按出现次数排序。rgba 里的基色和 hex 是否同一个色，需要人工判断。"))
if any(inline_hex_in_tsx.values()):
    parts += ["### TSX 内联 style 里的颜色", ""]
    for l, c in inline_hex_in_tsx.items():
        if c:
            parts.append(f"- {l}: " + ", ".join(f"`{k}` ×{n}" for k, n in c.most_common()))
    parts.append("")
parts.append(table("tw_color", "Tailwind 颜色 class", "`bg-[#…]` 这种任意值是绕过 config 的硬编码。"))

parts += ["## 字体", ""]
parts.append(table("font_family", "font-family 声明"))
parts.append(table("tw_font", "Tailwind font-* class"))
parts.append(table("font_weight", "font-weight"))

parts += ["## 字号与行距", ""]
parts.append(table("font_size", "font-size（CSS）", sort_key=lambda kv: px_key(kv[0])))
parts.append(table("tw_text", "Tailwind text-* 字号 class", "标准档对应 字号/行距：" + "、".join(f"{k}={v}" for k, v in TW_SIZE.items()), sort_key=lambda kv: kv[0]))
parts.append(table("line_height", "line-height（CSS）", sort_key=lambda kv: px_key(kv[0])))
parts.append(table("tw_leading", "Tailwind leading-* class"))
parts.append(table("letter_spacing", "letter-spacing"))
parts.append(table("tw_tracking", "Tailwind tracking-* class"))

parts += ["## 间距", ""]
parts.append(table("spacing", "padding / margin / gap 的值（CSS）", "按数值排序；`var(--…)`、0、auto 和定位用的 inset/top/left 已排除。", sort_key=lambda kv: px_key(kv[0])))
parts.append(table("tw_spacing", "Tailwind 间距 class", "Tailwind 默认 1 单位 = 4px，所以 p-4 = 16px。`[…]` 是任意值。", sort_key=lambda kv: tw_key(kv[0])))
parts.append(table("width", "width / max-width / height 的固定值", limit=40))

parts += ["## 圆角、阴影", ""]
parts.append(table("radius", "border-radius（CSS + tailwind.config）", sort_key=lambda kv: px_key(kv[0])))
parts.append(table("tw_rounded", "Tailwind rounded-* class", "默认档：" + "、".join(f"{k or 'rounded'}={v}" for k, v in TW_RAD.items()) + "（* 为 config 里自定义）"))
parts.append(table("shadow", "box-shadow"))
parts.append(table("tw_shadow", "Tailwind shadow-* class"))

parts += ["## 动效", ""]
parts.append(table("duration", "transition / animation 时长（CSS）", sort_key=lambda kv: float(kv[0][:-2])))
parts.append(table("tw_duration", "Tailwind duration-* class"))
parts.append(table("easing", "easing（CSS + tailwind.config）"))
parts.append(table("tw_ease", "Tailwind ease-* class"))

open(out_path, "w", encoding="utf-8").write("\n".join(p for p in parts if p is not None))
print("wrote", out_path)
print(json.dumps(summary, ensure_ascii=False, indent=1))
