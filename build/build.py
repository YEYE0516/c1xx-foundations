"""Compile foundations/*.json + themes/<theme>/theme.json → dist/<theme>/tokens.css (+ tokens.flat.json).

usage: python3 -I build/build.py site
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
theme_name = sys.argv[1] if len(sys.argv) > 1 else "site"

F = {}
for f in ["typography", "layout", "spacing", "shape", "motion", "color"]:
    F.update(json.load(open(ROOT / "foundations" / f"{f}.json")))
T = json.load(open(ROOT / "themes" / theme_name / "theme.json"))

# ---------- flatten ----------
def walk(node, path, out):
    if isinstance(node, dict):
        if "$value" in node:
            out[".".join(path)] = {"value": node["$value"], "type": node.get("$type")}
            return
        for k, v in node.items():
            if not k.startswith("$"):
                walk(v, path + [k], out)

flat = {}
walk(F, [], flat)
walk(T, [], flat)

def lookup(ref, mode):
    cands = []
    if ref.startswith("theme.accent."):
        cands.append(ref.replace("theme.accent.", f"theme.accent.{mode}."))
    if ref.startswith("color."):
        ref = ref[len("color."):]
    if ref.startswith(("shadow.", "border.")):
        cands.append(f"semantic.{mode}.{ref}")
    cands.append(ref)
    for c in cands:
        if c in flat:
            return flat[c]["value"]
    raise KeyError(ref)

def to_css_color(v):
    """rgb(from #hex r g b / a) → rgb(r g b / a)."""
    m = re.fullmatch(r"rgb\(from (#[0-9a-fA-F]{6}) r g b / ([\d.]+)\)", v.strip())
    if m:
        h, a = m.groups()
        r, g, b = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
        return f"rgb({r} {g} {b} / {a})"
    return v

def resolve(v, mode, depth=0):
    if isinstance(v, list) and v and isinstance(v[0], str) and not isinstance(v, dict):
        return v
    if isinstance(v, dict):
        return {k: resolve(x, mode, depth + 1) for k, x in v.items()}
    if isinstance(v, list):
        return [resolve(x, mode, depth + 1) for x in v]
    if isinstance(v, str):
        while "{" in v and depth < 12:
            m = re.search(r"\{([^}]+)\}", v)
            if not m:
                break
            val = resolve(lookup(m.group(1), mode), mode, depth + 1)
            if isinstance(val, list):
                val = ", ".join(f'"{x}"' if " " in x else x for x in val)
            v = v.replace(m.group(0), str(val))
            depth += 1
        return to_css_color(v)
    return v

def css_name(path):
    p = path
    for pre in ("semantic.light.", "semantic.dark.", "theme.", "font.", "text.", "heading."):
        if p.startswith(pre):
            p = p[len(pre):]
    return "--" + p.replace(".", "-")

def shadow_css(layers):
    parts = []
    for l in layers:
        col = l['color']
        m = re.fullmatch(r"\{color\.(shadow|border)\.([\w-]+)\}", col)
        col = f"var(--{m.group(1)}-{m.group(2)})" if m else col
        s = f"{l['offsetX']} {l['offsetY']} {l['blur']} {l['spread']} {col}"
        if l.get("inset"):
            s = "inset " + s
        parts.append(s)
    return ", ".join(parts)

def bezier(v):
    return f"cubic-bezier({', '.join(str(x) for x in v)})"

# ---------- emit ----------
root, dark, bp = [], [], {"wide": [], "tablet": [], "mobile": []}
flat_out = {}

def emit(target, name, value):
    target.append(f"  {name}: {value};")
    flat_out[name] = value

for path, tok in flat.items():
    typ, val = tok["type"], tok["value"]
    if path.startswith(("semantic.dark.", "theme.accent.dark.")):
        mode = "dark"
    else:
        mode = "light"
    if path.startswith("theme.accent."):
        continue  # surfaced through semantic.action.*
    if path.startswith(("snap.", "field.span-formula", "reduced.keep", "reduced.drop", "accent.", "energy.", "theme.canvas", "theme.signal")):
        continue
    if path.endswith("shadow.hue") or path.startswith("font.family."):
        continue
    if path.startswith("theme.font."):
        emit(root, "--font-" + path.split(".")[-1], ", ".join(f'"{x}"' if " " in x else x for x in val))
        continue
    if path.startswith(("theme.focus.",)):
        continue  # applied as an override below
    try:
        r = resolve(val, mode)
    except KeyError as e:
        print("unresolved", path, e, file=sys.stderr)
        continue
    target = dark if mode == "dark" else root
    name = css_name(path)
    if typ == "typography":
        # display.N.{desktop,tablet,mobile} → breakpoint vars; others fixed
        m = re.match(r"display\.(\d)\.(wide|desktop|tablet|mobile)", path)
        if m:
            n, b = m.groups()
            tgt = root if b == "desktop" else bp[b]
            tgt.append(f"  --display-{n}-size: {r['fontSize']};")
            tgt.append(f"  --display-{n}-lh: {r['lineHeight']};")
            flat_out[f"--display-{n}-size@{b}"] = r["fontSize"]
            flat_out[f"--display-{n}-lh@{b}"] = r["lineHeight"]
        else:
            emit(target, name + "-size", r["fontSize"])
            emit(target, name + "-lh", r["lineHeight"])
            if "letterSpacing" in r and not path.startswith("text.meta"):
                pass
        continue
    if typ == "shadow":
        emit(target, name, shadow_css(val))
        continue
    if typ == "cubicBezier":
        emit(target, name, bezier(r))
        continue
    if typ == "fontFamily":
        if isinstance(r, list):
            r = ", ".join(f'"{x}"' if " " in x else x for x in r)
        emit(target, name, r)
        continue
    if typ in ("number", "string"):
        if path.startswith("gsap.") or path.startswith("field.") or path.startswith("grid.columns"):
            emit(target, name, str(r))
        continue
    if typ == "dimension" and (path.startswith(("space.", "rhythm.", "radius.")) and not path.endswith("full")) and str(r).endswith("px"):
        pxv = float(str(r)[:-2]); r = "0" if pxv == 0 else f"{pxv/16:g}rem"
    emit(target, name, str(r))

# theme focus override (light only; dark keeps semantic)
if "theme.focus.ring" in flat:
    root.append(f"  --focus-ring: {resolve(flat['theme.focus.ring']['value'], 'light')};")
    flat_out["--focus-ring"] = resolve(flat['theme.focus.ring']['value'], 'light')

# theme canvas override (light only)
if "theme.canvas" in flat:
    cv = resolve(flat["theme.canvas"]["value"], "light")
    root.append(f"  --bg-canvas: {cv};"); flat_out["--bg-canvas"] = cv

# energy forms → data-attribute scopes that re-point the accent-derived roles
energy_blocks = []
forms = sorted({p.split(".")[1] for p in flat if p.startswith("energy.") and p.count(".") >= 3})
for form in forms:
    for mode, sel in (("light", f'[data-energy="{form}"]'), ("dark", f'[data-theme="dark"][data-energy="{form}"]')):
        g = lambda k: resolve(flat[f"energy.{form}.{mode}.{k}"]["value"], mode)
        lines = [f"  --accent-base: {g('base')};", f"  --accent-strong: {g('strong')};", f"  --accent-soft: {g('soft')};", f"  --accent-on: {g('on')};",
                 f"  --action-primary: {g('base')};", f"  --action-primary-hover: {g('strong')};", f"  --action-primary-fg: {g('on')};",
                 f"  --action-selected-bg: {g('soft')};", f"  --fg-on-accent: {g('on')};", f"  --fg-accent: {g('strong')};"]
        energy_blocks += [f"{sel} {{", *lines, "}", ""]
if forms:
    # default accent exposed under the same names (so components can use --accent-* without a data attribute)
    for mode, target in (("light", root), ("dark", dark)):
        g = lambda k: resolve(flat[f"theme.accent.{mode}.{k}"]["value"], mode)
        target += [f"  --accent-base: {g('base')};", f"  --accent-strong: {g('strong')};", f"  --accent-soft: {g('soft')};", f"  --accent-on: {g('on')};", f"  --fg-accent: {g('strong')};"]
    # fixed palette: every form's base colour side by side (pictograms, avatar rings, form pickers)
    for form in forms:
        emit(root, f"--form-{form}", resolve(flat[f"energy.{form}.light.base"]["value"], "light"))

# remove duplicates keeping last (override order: foundations then theme focus)
def dedupe(lines):
    seen, out = {}, []
    for l in lines:
        k = l.split(":")[0]
        seen[k] = l
    return list(seen.values())

root, dark = dedupe(root), dedupe(dark)
tablet_bp = flat["breakpoint.tablet"]["value"]
wide_bp = flat["breakpoint.wide"]["value"]
mobile_bp = flat["breakpoint.mobile"]["value"]

css = ["/* C1XX Foundations · generated by build/build.py — do not edit by hand */",
       f"/* theme: {theme_name} · light = :root, dark = [data-theme=\"dark\"] */", "",
       ":root {", *root, "}", "",
       f"@media (min-width: {wide_bp}) {{", "  :root {", *["  " + l for l in bp["wide"]], "  }", "}", "",
       f"@media (max-width: {tablet_bp}) {{", "  :root {", *["  " + l for l in bp["tablet"]], "  }", "}", "",
       f"@media (max-width: {mobile_bp}) {{", "  :root {", *["  " + l for l in bp["mobile"]], "  }", "}", "",
       '[data-theme="dark"] {', *dark, "}", "",
       *energy_blocks,
       "@media (prefers-reduced-motion: reduce) {",
       "  :root { --duration-fast: var(--reduced-duration); --duration-base: var(--reduced-duration); --duration-slow: var(--reduced-duration); --duration-scene: var(--reduced-duration); }",
       "}", ""]

out = ROOT / "dist" / theme_name
out.mkdir(parents=True, exist_ok=True)
(out / "tokens.css").write_text("\n".join(css), encoding="utf-8")
(out / "tokens.flat.json").write_text(json.dumps(flat_out, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"wrote {out/'tokens.css'} ({len(root)} light vars, {len(dark)} dark vars, {len(bp['tablet'])+len(bp['mobile'])} breakpoint vars)")
