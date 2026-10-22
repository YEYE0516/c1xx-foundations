"""Rewrite c1xxstudio.com's styles.css onto C1XX Foundations tokens.

Values change, selectors and structure do not. Deliberate exceptions are left as literals and
listed at the end. usage: python3 -I build/migrate-site.py IN.css OUT.css
"""
import re, sys
from collections import Counter

src = open(sys.argv[1], encoding="utf-8").read()
report = Counter()
exceptions = []

# ---------- neutral ramp (same as foundations/color.json) ----------
NEUTRAL = {0: "fbfaf7", 50: "f7f5f0", 100: "f3f1ec", 150: "ebe8e1", 200: "d8d5cd", 300: "cbc8bf", 400: "aaa9a3",
           500: "8a8982", 600: "62625d", 700: "4c4d49", 800: "343532", 900: "1f1f1f", 950: "121310"}
def lum(h):
    r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
NL = {k: lum(v) for k, v in NEUTRAL.items()}
def nearest_neutral(h):
    L = lum(h)
    return min(NL, key=lambda k: abs(NL[k] - L))
def is_grey(h):
    r, g, b = [int(h[i:i+2], 16) for i in (0, 2, 4)]
    return max(r, g, b) - min(r, g, b) <= 10
def norm_hex(h):
    h = h.lstrip("#").lower()
    return "".join(c*2 for c in h) if len(h) == 3 else h

SCENE = {"df543c": "--scene-clario-accent", "59c8c2": "--scene-syncline-accent", "d9568f": "--scene-blooming-sydney-accent",
         "d7ff43": "--scene-highlight-acid", "7b62ff": "--scene-highlight-violet", "ff633c": "--scene-highlight-orange",
         "ed5138": "--action-signal"}

def grey_role(step, prop):
    if prop == "color":
        if step >= 800: return "--fg-primary"
        if step >= 600: return "--fg-secondary"
        if step == 500: return "--fg-muted"
        return f"--neutral-{step}"
    if prop in ("background", "background-color"):
        return {0: "--bg-raised", 50: "--bg-surface", 100: "--bg-canvas", 150: "--bg-sunken", 950: "--bg-inverse", 900: "--bg-inverse"}.get(step, f"--neutral-{step}")
    if prop.startswith("border") or prop == "outline":
        return {300: "--border-subtle", 950: "--border-strong"}.get(step, f"--neutral-{step}")
    return f"--neutral-{step}"

def replace_hex(value, prop):
    def sub(m):
        h = norm_hex(m.group(0))
        if h in SCENE:
            report["colour→scene/signal"] += 1; return f"var({SCENE[h]})"
        if h in ("000000", "ffffff"):
            return m.group(0)  # masks, sheen: literal black/white is structural
        if is_grey(h):
            step = nearest_neutral(h)
            report["grey→neutral"] += 1
            return f"var({grey_role(step, prop)})"
        exceptions.append(f"#{h} in {prop}")
        return m.group(0)
    return re.sub(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", sub, value)

def replace_rgba(value):
    def sub(m):
        r, g, b, a = m.groups()
        h = f"{int(r):02x}{int(g):02x}{int(b):02x}"
        if h in ("000000", "ffffff"): return m.group(0)
        if is_grey(h):
            step = nearest_neutral(h)
            pct = round(float(a) * 100)
            report["rgba→color-mix"] += 1
            return f"color-mix(in srgb, var(--neutral-{step}) {pct}%, transparent)"
        return m.group(0)
    return re.sub(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)", sub, value)

# ---------- spacing ----------
def snap_space(px):
    px = abs(px)
    for lo, hi, tok in [(1, 3, "--space-1"), (4, 7, "--space-2"), (8, 13, "--space-3"), (14, 18, "--space-4"), (19, 22, "--space-5"),
                        (23, 28, "--space-6"), (29, 36, "--space-8"), (37, 42, "--space-10"), (43, 50, "--space-12"),
                        (51, 65, "--rhythm-3"), (66, 100, "--rhythm-4"), (101, 165, "--rhythm-6"), (166, 10000, "--rhythm-8")]:
        if lo <= px <= hi: return tok
    return None

def replace_spacing(value):
    def px_sub(m):
        n = float(m.group(1))
        if n == 0: return m.group(0)
        tok = snap_space(n)
        if not tok: return m.group(0)
        report["spacing→token"] += 1
        return f"calc(-1 * var({tok}))" if n < 0 else f"var({tok})"
    return re.sub(r"(?<![\w.])(-?\d+(?:\.\d+)?)px", px_sub, value)

# ---------- radius / shadow / motion / tracking ----------
def replace_radius(value):
    v = value.strip()
    if v in ("999px", "9999px", "50%"):
        report["radius→full"] += 1; return "var(--radius-full)"
    m = re.fullmatch(r"(\d+)px", v)
    if m:
        n = int(m.group(1))
        if n >= 40:
            exceptions.append(f"border-radius {v} (device bezel, deliberate)"); return v
        tok = "--radius-1" if n <= 6 else "--radius-2" if n <= 11 else "--radius-3" if n <= 20 else "--radius-4" if n <= 28 else "--radius-5"
        report["radius→token"] += 1; return f"var({tok})"
    exceptions.append(f"border-radius {v}"); return v

def replace_shadow(value):
    v = value.strip()
    if "var(--" in v or v == "none":
        return v
    layers = [l.strip() for l in re.split(r",(?![^(]*\))", v)]
    non_inset = [l for l in layers if "inset" not in l]
    if not non_inset:
        report["shadow→inset-hairline"] += 1; return "var(--elevation-inset-hairline)"
    blurs = []
    for l in non_inset:
        m = re.match(r"-?\d+(?:px)?\s+-?\d+(?:px)?\s+(\d+)px", l)
        if m: blurs.append(int(m.group(1)))
    if not blurs: return v
    mx = max(blurs)
    tok = "--elevation-1" if mx <= 14 else "--elevation-2" if mx <= 46 else "--elevation-3"
    report["shadow→elevation"] += 1
    return f"var({tok})"

def snap_duration(ms):
    if ms >= 5000: return None
    if ms <= 260: return "--duration-fast"
    if ms <= 380: return "--duration-base"
    if ms <= 700: return "--duration-slow"
    return "--duration-scene"

def replace_motion(value):
    def dur(m):
        n, unit = m.groups(); ms = float(n) * (1000 if unit == "s" else 1)
        tok = snap_duration(ms)
        if not tok: return m.group(0)
        report["duration→token"] += 1; return f"var({tok})"
    v = re.sub(r"(?<![\w-])(\d*\.?\d+)(ms|s)\b", dur, value)
    v = v.replace("cubic-bezier(.22,1,.36,1)", "var(--easing-enter)").replace("cubic-bezier(0.22, 1, 0.36, 1)", "var(--easing-enter)")
    v = re.sub(r"\bease-in-out\b", "var(--easing-standard)", v)
    v = re.sub(r"(?<![\w-])ease(?![\w-])", "var(--easing-standard)", v)
    return v

def replace_tracking(value):
    m = re.fullmatch(r"(-?)((?:\d+)?\.?\d+)em", value.strip())
    if not m: return value
    neg, n = m.group(1) == "-", float(m.group(2))
    report["tracking→token"] += 1
    if neg: return "var(--tracking-display)" if n >= 0.03 else "var(--tracking-tight)"
    if n >= 0.15: return "var(--tracking-wide)"
    if n >= 0.07: return "var(--tracking-label)"
    return "var(--tracking-normal)"

# ---------- type ----------
def tier_for_px(n):
    if n <= 10.5: return "meta"
    if n <= 12.5: return "sm"
    if n <= 15: return "body"
    if n <= 17: return "body-lg"
    if n <= 19: return "lead"
    if n <= 23: return "h4"
    if n <= 28: return "h3"
    if n <= 36: return "h2"
    if n <= 72: return "display-4"
    if n <= 110: return "display-3"
    if n <= 152: return "display-2"
    return "display-1"

def tier_for_clamp(mx):
    if mx <= 20: return "lead" if mx >= 18 else "body-lg"
    if mx <= 26: return "h4"
    if mx <= 34: return "h3"
    if mx <= 48: return "h2"
    if mx <= 74: return "display-4"
    if mx <= 112: return "display-3"
    if mx <= 150: return "display-2"
    return "display-1"

def tier_vars(t):
    return (f"var(--{t}-size)", f"var(--{t}-lh)")

# ---------- rule-level pass ----------
SEL_TIER = {}
def process_decls(block, selector="", nested=False):
    """block = declarations of one rule (no braces). Returns rewritten declarations."""
    decls = [d for d in block.split(";") if d.strip()]
    out = []
    tier = None
    # first pass: find the type tier from font-size / font shorthand
    for d in decls:
        if ":" not in d: continue
        prop, val = d.split(":", 1); prop, val = prop.strip(), val.strip()
        if prop == "font-size":
            m = re.fullmatch(r"(\d+(?:\.\d+)?)px", val)
            if m: tier = tier_for_px(float(m.group(1)))
            m = re.match(r"clamp\(\s*[\d.]+px\s*,\s*[\d.]+vw\s*,\s*([\d.]+)px\s*\)", val)
            if m: tier = tier_for_clamp(float(m.group(1)))
    key = selector.strip()
    if nested and key in SEL_TIER and tier and tier.startswith(("display", "h2")):
        tier = SEL_TIER[key]  # tiers are already responsive: keep the base rule's tier
        report["nested override→same tier"] += 1
    elif tier and not nested:
        SEL_TIER[key] = tier
    for d in decls:
        if ":" not in d: out.append(d); continue
        prop, val = d.split(":", 1); prop, val = prop.strip(), val.strip()
        lead = d[: len(d) - len(d.lstrip())]
        if prop.startswith("--"):
            val = replace_rgba(replace_hex(val, "custom"))
            out.append(f"{lead}{prop}: {val}"); continue
        if prop in ("mask-image", "-webkit-mask-image", "transform", "content", "background-image", "filter", "animation-name"):
            out.append(d); continue
        if prop == "font-size" and tier:
            if re.fullmatch(r"(\d+(?:\.\d+)?)px", val) or val.startswith("clamp("):
                val = tier_vars(tier)[0]; report["font-size→tier"] += 1
        elif prop == "line-height" and tier:
            if re.fullmatch(r"\.?\d*\.?\d+", val) or val.endswith("px"):
                val = tier_vars(tier)[1]; report["line-height→tier"] += 1
        elif prop == "font":
            m = re.match(r"(\d{3})\s+(\d+(?:\.\d+)?)px(?:/([\d.]+))?\s+(.*)", val)
            if m:
                w, size, lh, fam = m.groups()
                t = tier_for_px(float(size)); s, l = tier_vars(t)
                fam = fam.replace("var(--mono)", "var(--font-mono)").replace("var(--sans)", "var(--font-body)").replace("var(--serif)", "var(--font-display)")
                val = f"{w} {s}/{l} {fam}"; report["font shorthand→tier"] += 1
        elif prop == "letter-spacing":
            val = replace_tracking(val)
        elif prop == "border-radius":
            val = replace_radius(val)
        elif prop == "box-shadow":
            val = replace_shadow(val)
        elif prop in ("transition", "animation", "transition-duration", "animation-duration"):
            val = replace_motion(val)
        elif prop in ("padding", "margin", "gap", "row-gap", "column-gap") or re.match(r"(padding|margin)-", prop):
            val = replace_spacing(val)
        elif prop == "min-height":
            val = {"34px": "var(--size-control-sm)", "38px": "var(--size-control-md)", "40px": "var(--size-control-md)",
                   "42px": "var(--size-touch-min)", "44px": "var(--size-touch-min)", "48px": "var(--size-control-lg)"}.get(val, val)
        elif prop == "font-family":
            val = val.replace("var(--mono)", "var(--font-mono)").replace("var(--sans)", "var(--font-body)").replace("var(--serif)", "var(--font-display)")
        # colours in any remaining property
        val = replace_hex(val, prop)
        val = replace_rgba(val)
        # old variable names
        if prop == "color":
            val = val.replace("var(--paper-raised)", "var(--fg-on-inverse)").replace("var(--paper)", "var(--fg-on-inverse)")
        val = (val.replace("var(--paper-raised)", "var(--bg-surface)").replace("var(--paper)", "var(--bg-canvas)")
                  .replace("var(--muted)", "var(--fg-secondary)").replace("var(--rule)", "var(--border-subtle)")
                  .replace("var(--soft)", "var(--neutral-200)").replace("var(--acid)", "var(--scene-highlight-acid)")
                  .replace("var(--violet)", "var(--scene-highlight-violet)").replace("var(--orange)", "var(--scene-highlight-orange)")
                  .replace("var(--signal)", "var(--action-signal)")
                  .replace("var(--mono)", "var(--font-mono)").replace("var(--sans)", "var(--font-body)").replace("var(--serif)", "var(--font-display)"))
        if "var(--ink)" in val:
            if prop == "color": val = val.replace("var(--ink)", "var(--fg-primary)")
            elif prop in ("background", "background-color"): val = val.replace("var(--ink)", "var(--action-primary)")
            elif prop.startswith("border") or prop == "outline": val = val.replace("var(--ink)", "var(--border-strong)")
            else: val = val.replace("var(--ink)", "var(--neutral-950)")
        if prop == "outline" and "var(--scene-highlight-orange)" in val:
            val = val.replace("var(--scene-highlight-orange)", "var(--focus-ring)"); report["focus→ring"] += 1
        out.append(f"{lead}{prop}: {val}")
    return ";".join(out) + (";" if block.rstrip().endswith(";") else "")

# walk braces: process innermost declaration blocks only
def walk(css, nested=False):
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0: out.append(css[i:]); break
        selector = css[i:j].strip().split("\n")[-1]
        out.append(css[i:j+1]); i = j + 1
        # find matching close, accounting for nesting
        depth, k = 1, i
        while k < n and depth:
            if css[k] == "{": depth += 1
            elif css[k] == "}": depth -= 1
            k += 1
        inner = css[i:k-1]
        if "{" in inner:
            out.append(walk(inner, nested=True))
        else:
            out.append(process_decls(inner, selector, nested))
        out.append("}"); i = k
    return "".join(out)

# ---------- :root block: drop old tokens, import generated ones ----------
src = re.sub(r"  --paper: #f3f1ec;\n.*?  --serif: 'Newsreader', serif;\n", "", src, flags=re.S)
src = src.replace("@import url('https://fonts.googleapis.com", "@import './tokens.css';\n@import url('https://fonts.googleapis.com", 1)

result = walk(src)
open(sys.argv[2], "w", encoding="utf-8").write(result)
print("replacements:"); [print(f"  {k}: {v}") for k, v in sorted(report.items(), key=lambda kv: -kv[1])]
print("deliberate literals kept:", len(exceptions))
for e in sorted(set(exceptions)): print("  ", e)
