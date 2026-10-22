# Week 2 · Day 1 · Syncline brand layer

产出 `themes/syncline/theme.json`、`build/derive-accent.py`、`dist/syncline/tokens.css`、`docs/05-syncline-contrast.md`。底座一行没改——`build.py site` 和 `build.py syncline` 用的是同一份 `foundations/`。

## 填了合同的哪些项

| 合同项 | 网站（主题 A） | Syncline（主题 B） |
| --- | --- | --- |
| font.body | Manrope | Inter |
| font.display | Newsreader（light italic，用于一句话） | New York → Georgia（bold，用于屏幕标题） |
| font.mono | DM Mono | 没有 mono 声音，alias 到 body |
| accent.base | Ink `#121310` | Cloud `#54b8ab`（默认 energy form） |
| accent.strong | neutral.800 | `#1f7a77`（原型已有，4.69:1） |
| accent.soft | neutral.150 | `#e0ece6`（14% tint） |
| accent.on | paper | ink |
| signal | `#ed5138` | `#cc3b12`（Fuzz 的 strong） |
| shadow.hue | ink | navy `#152a55` —— 原型 13 个 `shadow-[…]` 全是这个蓝 |
| bg.canvas 覆盖 | — | neutral.50（原型的 `#f7f4ef` 比网站 paper 浅一阶） |

同一个 `elevation.2` 在网站上是暖黑阴影，在 Syncline 上是海军蓝阴影，几何一样——这是 Day 3 "阴影只定几何"那个决定兑现的地方。

## 六个 energy form

每个 form 一套 base / strong / soft / on，light 和 dark 各一份，共 6 × 2 × 4 = 48 个值。**全部由 `build/derive-accent.py` 推导，不目测**：

- base：原型 `data.ts` 里的原色
- strong：把 base 往暗推（dark 模式往亮推）直到在 canvas 上 ≥ 4.5:1，可以当文字用
- soft：base 与 canvas 按 14%（dark 18%）混合，做选中态背景
- on：ink 和 paper 里跟 base 对比更高的那个

| form | base | light strong | 性格（来自原型） |
| --- | --- | --- | --- |
| cloud | `#54b8ab` | `#1f7a77` | Calm · Gentle · Flowing |
| peak | `#3f68b8` | `#3f68b8`（本身就过） | Focused · Grounded |
| star | `#f6c04d` | `#966600` | Radiant · Bold · Expressive |
| fuzz | `#e87555` | `#cc3b12` | Playful · Free · Spontaneous |
| bloom | `#e98ba7` | `#da1b54` | Warm · Open · Tender |
| jelly | `#b69ade` | `#8753d0` | Soft · Flexible · Bouncy |

Star 和 Bloom 的 strong 推得比较远（黄→深赭、粉→玫红），因为浅色要达到 4.5:1 只能压很深。在 Figma 里看着不顺眼可以手调，但对比度数字不能回到 4.5 以下。

## 在 CSS 里怎么切

`tokens.css` 为每个 form 生成一个作用域：

```html
<body data-energy="jelly">            <!-- 整页切到 Jelly -->
<section data-energy="star">           <!-- 或者只切一块 -->
```

作用域里重指 `--action-primary / -hover / -fg`、`--action-selected-bg`、`--fg-on-accent`、`--fg-accent` 和 `--accent-*` 六个。组件只引用这些角色，不知道当前是哪个 form。Dark 模式用 `[data-theme="dark"][data-energy="…"]` 叠加。

## 对比度发现

`docs/05-syncline-contrast.md`。正文、按钮文字、六个 strong 全部达标。**没过的是 light 模式下的 base 色块本身**：除了 Peak，五个 pastel 在米白 canvas 上都在 1.5–2.7:1，低于非文字元素 3:1 的边界要求。

规则：light 模式下 base 填充的控件必须靠 `on` 色文字（全部 ≥ 6.3:1）或 `border/strong` 描边来界定，不能只靠色块边缘。这正是原型现在的做法（pastel 按钮 + 黑字 + 阴影），现在有了数字。Dark 模式下六个 base 全部 ≥ 3.45:1，没有这个问题。

## 明天（Day 2）Figma 要先定的事

Pro 计划一个 collection 最多 4 个 mode，6 个 energy form 放不进一个 collection。两种拆法：

1. **两个 collection**：`Energy · A`（cloud / peak / star）+ `Energy · B`（fuzz / bloom / jelly）。组件绑 A 的变量，演示 B 时要重新绑——不好。
2. **一个 collection 放 4 个，另外两个作为"扩展"**：组件只绑一个 collection；演示 6 个切换时用 4 个 mode + 两个 form 用 variable 的 alias 手工换。
3. **Figma 里只做 4 个 mode**（cloud / peak / star / jelly，视觉差异最大的四个），6 个全部在 CSS 和 live 子页上切换。案例里诚实写"Figma Pro 限 4 mode，完整六个见 live 页"。

建议 3：Figma 是对照，不是真源；真源是 JSON，六个都在。
