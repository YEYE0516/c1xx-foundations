# C1XX Foundations

One brand-agnostic token base, two products on top of it.

```
foundations/      scales + rules — no brand colour, no font name
     │
     ├── themes/site/        c1xxstudio.com            ← live, v0.1.0
     └── themes/syncline/    Syncline, 6 energy-form modes   (week 2)
```

`foundations/` defines *what exists* (a 24px row, a 4px unit, twelve type tiers, ten spacing steps, three elevations, four durations, colour **roles**). A theme defines *what it looks like* (families, the accent set, the shadow hue). `build/build.py` resolves one onto the other and writes `dist/<theme>/tokens.css`, which the product consumes.

## Why

Before this base existed, the portfolio site's single stylesheet held 111 distinct hex colours (74 of them near-identical warm greys), 63 spacing values, 63 font sizes and 28 line-heights; the Syncline prototype shipped a Tailwind palette that none of its 2 500 lines ever referenced. The full count is in [docs/inventory.md](docs/inventory.md). After the site moved onto tokens: 12 type tiers, 0 bare spacing values, 3 elevations, 4 durations; selectors untouched.

## Layers

| Layer | Lives in | Example | Rule |
| --- | --- | --- | --- |
| primitive | `foundations/` | `space.4 = 16px`, `neutral.600 = #62625d` | The only concrete values in the base: scales. |
| semantic | `foundations/` | `color.semantic.light.fg.secondary → {neutral.600}` | Roles components reference. Same key set in light and dark. |
| contract | `foundations/` → filled by a theme | `accent.base = {theme.accent.base}` | Declared in the base, never valued there. |
| theme | `themes/<name>/theme.json` | `theme.accent.light.base = {neutral.950}` | Families, accent set, shadow hue, optional canvas override, product-only extras (`scene.*`, `aurora.*`). |

A theme may override a semantic value. It may never edit `foundations/`.

## Files

| File | Holds | Day |
| --- | --- | --- |
| `foundations/typography.json` | font roles, weights, tracking, 24px row, text / heading / display tiers (display per breakpoint) | [02](docs/02-typography-grid.md) |
| `foundations/layout.json` | breakpoints 600 / 900 / 1280 / 1680, gutters, 12-col grid, measure, field heights, `rhythm.*` (whole rows) | [02](docs/02-typography-grid.md) |
| `foundations/spacing.json` | `space.0–12` (numeric = ×4px), control sizes, the snap table from old values | [03](docs/03-spacing-shape-motion.md) |
| `foundations/shape.json` | radius 4 / 8 / 16 / 24 / 32 / full, hairline, `elevation.1–3` (geometry only) | [03](docs/03-spacing-shape-motion.md) |
| `foundations/motion.json` | durations 120 / 200 / 320 / 600, easings, stagger, reduced-motion, GSAP seconds | [03](docs/03-spacing-shape-motion.md) |
| `foundations/color.json` | 13-step warm neutral, accent contract, semantic roles ×2 modes | [04](docs/04-color.md) · [contrast](docs/04-contrast.md) |
| `foundations/icons.json` + `icons/` | the UI icon system: 94 Lucide glyphs normalised to the grid (24 box, 20 live area, stroke 2, currentColor), 7 categories, 3 sizes, colour by role | [07](docs/07-icons.md) |
| `themes/site/theme.json` | Manrope / Newsreader / DM Mono, Ink as action, signal, scene accents, aurora | |
| `themes/syncline/theme.json` + `pictograms.json` | Inter / New York, Cloud accent, six energy forms, dance pictograms as shape tables with form colour slots | [05](docs/05-syncline-theme.md) · [07](docs/07-icons.md) |
| `build/build.py` | JSON → `dist/<theme>/tokens.css` + `tokens.flat.json` | |
| `build/icons.py` | vendor + build the icon set → `dist/icons/` (sprite, json, css, manifest) | |
| `build/pictograms.py` | `pictograms.json` → `dist/syncline/pictograms/` (svg, sprite, js) | |
| `build/inventory.py` | counts every hardcoded design value in a stylesheet / TSX (the before and after) | |
| `build/contrast.py` | WCAG report for a theme | |
| `build/migrate-site.py` | the one-shot rewrite of the site's `styles.css` onto tokens | |

## Naming

```
--<group>-<name>[-<facet>]
--space-4            --radius-full        --duration-base      --easing-enter
--fg-secondary       --bg-canvas          --border-subtle      --action-primary
--body-size / --body-lh                   --display-2-size / --display-2-lh
```

- Scales use **numbers that say the value**: `space.4` is 16px, `space.12` is 48px. No xs/sm/md that run out.
- Roles use **purpose, not appearance**: `fg.secondary`, never `grey-600`, in a component.
- Display tiers count down from the largest (`display-1`); text tiers are named (`meta`, `sm`, `body`, `lead`).
- Anything ≥ 48px vertical is `rhythm.*` (whole 24px rows), not `space.*`.

## Adding a token

1. Decide the layer. A new value on a scale → primitive. A new purpose → semantic role that references an existing primitive. A product-only thing → the theme, not the base.
2. Add it to the right `foundations/*.json` (or `themes/<name>/theme.json`) with a `$type`, a `$value` and one line of `$description` saying when to use it.
3. Keep the grid: vertical values are multiples of 4; block-level spacing multiples of 24; line-heights multiples of 4.
4. `python3 -I build/build.py site` and check `dist/site/tokens.css`. For colours also run `build/contrast.py themes/site/theme.json`.
5. Bump the version in the tag; note the change in the commit.

## Using the output

```css
@import './tokens.css';           /* light is :root; dark is [data-theme="dark"] */
.card { padding: var(--space-6); border-radius: var(--radius-3); box-shadow: var(--elevation-1); }
h1    { font-size: var(--display-2-size); line-height: var(--display-2-lh); }
```

Display tiers respond on their own (the breakpoints live inside `tokens.css`), so a component never writes its own `@media` for type size.

## Format

Tokens follow the [W3C Design Tokens (DTCG)](https://www.designtokens.org/) format. Type scale and layout were generated with [baseline-to-layers](https://github.com/YEYE0516/baseline-to-layers) (Müller-Brockmann's baseline-grid method).

## Figma

[C1XX Foundations](https://www.figma.com/design/ZThJK81NT635ehYKdTd3Si) — collections Primitives · Semantic (Light / Dark) · Product (site / syncline) · Energy (6 forms) · Syncline · forms · Site · scene, 28 text styles, 3 effect styles, 12 Syncline components incl. Icon (94) / Icon button / Pictogram, every variable carrying its CSS name as code syntax. Built from the JSON through the Figma MCP, not by hand; the JSON stays the source of truth.

## Status

See [docs/plan.md](docs/plan.md).

## Licence

MIT. Icon glyphs in `foundations/icons/` are from [Lucide](https://lucide.dev) (ISC) — see `foundations/icons/LICENSE`.
