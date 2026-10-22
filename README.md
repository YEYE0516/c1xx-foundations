# C1XX Foundations

One brand-agnostic token base, two products on top of it.

`foundations/` holds only scales and rules — type scale, spacing, radius, motion, colour roles. It never contains a brand colour or a font name. Each product adds a thin theme that fills those roles in:

```
foundations/   scales + rules            (brand-agnostic)
     │
     ├── themes/site/        c1xxstudio.com
     └── themes/syncline/    Syncline — dance app prototype, 6 energy-form modes
```

Build output goes to `dist/<theme>/tokens.css` and a Tailwind theme, which each product consumes.

## Layers

| Layer | What lives here | Example |
| --- | --- | --- |
| primitive | raw values on a scale | `space.4 = 16px`, `neutral.100` |
| semantic | roles that components reference | `color.bg.canvas`, `color.action.primary` |
| component | per-component bindings | `button.primary.bg = {color.action.primary}` |

Themes override semantic values only. Foundations are never edited to make a theme work.

## Status

Work in progress — see [docs/plan.md](docs/plan.md).

| | |
| --- | --- |
| Week 1 | Foundations, applied to c1xxstudio.com |
| Week 2 | Syncline theme, Figma component library |
| Week 3 | Case study, live docs pages |

## Format

Tokens follow the [W3C Design Tokens (DTCG)](https://www.designtokens.org/) format so they load into Figma Variables, Tokens Studio and Style Dictionary without conversion.

Type scale and layout values are generated with [baseline-to-layers](https://github.com/YEYE0516/baseline-to-layers).

## Licence

MIT
