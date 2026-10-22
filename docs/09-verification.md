# Week 2 · Day 5 · 校验 + 收尾

方法：从 Figma 读出每个组件每个 variant 的绑定（填充 / 描边 / 文字变量、内边距、圆角、尺寸），对照原型里消费它的 JSX，逐项打勾；不一致的要么改代码、要么改 Figma，不留"约等于"。

## 逐个组件

| 组件 | 代码里的消费者 | Day 5 前的差异 | 处理 | 结果 |
| --- | --- | --- | --- | --- |
| **Button** 24 | `PrimaryButton` / `SecondaryButton` / `GhostButton` + Live 页手写的一个 | 高度 56 / 48（`min-h-14/12`），Figma 是 lg 48 / md 40；Secondary 是淡紫描边 + 白 72%，Figma 是 `bg/surface` + `fg/accent` 描边；没有 hover / pressed；Ghost 高 44 / 32 | 代码改：md = `min-h-control-md px-5 py-2 text-sm`，lg = `min-h-control-lg px-6 py-3 text-base`；Secondary 按 Figma；三种都加 hover（升一档填充）、pressed（88%，`opacity-pressed`）、disabled；手写的那个换成同一套 class | ✓ |
| **Icon button** 24 → 32 | `FloatingBackButton` / `FloatingMenuButton` / 关闭按钮 | 代码是玻璃态（白 78% + 描边 + 阴影）浮在照片上，Figma 没有这种样式 | Figma 加 **Style=Glass**（`bg/raised` 80% + `border/subtle` + `elevation/2`，hover 实心，pressed 88%）；代码三个按钮统一为 `bg-raised/80 border-line-subtle text-ink shadow-2` | ✓ |
| **Card** 3 | `MoodCard` / `DanceStyleCard` / `StateCard`（Flat ↔ Selected）、`IntensitySelector`（Raised）、`AvatarCard` | 内边距 16（圆角 24，违反"圆角 ≈ 内边距"）；选中态是 `accent` 描边 + 白底 + 阴影，Figma 是 `selected-bg` + `fg/accent` 描边；未选中是白 55% 玻璃，Figma 是 `bg/surface` + `border/subtle`；标题 Figma 用 Inter h4，代码用衬线 | 代码改 `p-6`、选中 `border-accent-ink bg-accent-soft`、Flat `bg-surface border-line-subtle`；Figma 标题改 `heading/h3`（display 字体）——衬线卡片标题是产品声音，系统跟着产品 | ✓ |
| **Page control** 6 → 7 | `<PageControl>` | 原来是 CSS `::before/::after` 画的，和组件无关；Figma 6 点，原型 7 屏 | 代码写成真组件（Day 4 收尾时）；Figma 补第 7 点和 Active=7 | ✓ |
| **Avatar** 12 | `AvatarImage` | 原型展示整张插画，不裁圆 | 圆形裁切留给列表 / 摘要场景；六张图已入库；描述里写明 | ✓（用法不同，不是不一致） |
| **Icon** 94 | `lucide-react` + `h-icon-md w-icon-md` | — | 7 个用到的全在集合里；线宽 2、`currentColor` | ✓ |
| **Pictogram** 16 | `<DanceGlyph>` | — | 同一份 JSON 生成 | ✓ |
| **Chip** 6 | 无 | 原型没有 chip 场景 | 描述里写明候选用法（GOOD FOR / traits 标签） | — |
| **Input** 8 | 无 | 流程里没有文本输入 | — | — |
| **Slider** 2 | 无 | 强度是三选一卡片 | — | — |
| **Toast** 3 | 无 | 保存反馈在按钮上 | — | — |
| **Bottom sheet** 1 | 无 | `SavedMomentsMenu` 刻意做成全屏结果页 | — | — |

12 个组件：7 个有消费者，全部一致；5 个原型暂未用到，Figma 描述里写了原因 / 候选场景。

## Code Connect

Figma 的 Code Connect 需要 Organization / Enterprise 计划（API 直接拒绝：*Code connections can only be made in libraries that are in Organization or Enterprise plans*）。替代：每个组件的 description 末尾加了 `Code:` 一行，指向源码里的消费者和关键 class。够用了——面试官点开组件就能看到代码在哪。

## before / after 齐了

| | before | after |
| --- | --- | --- |
| 网站 hex | 111 | 28（场景色，刻意保留） |
| 网站 spacing 裸值 | 63 | 0 |
| 网站 font-size | 63 | 12 tier |
| 网站 duration | 16 | 4 |
| 原型 hex | 17 种 / 189 次 | 0 |
| 原型 `shadow-[…]` | 18 | 0 |
| 原型字体层 | 3 | 2 |
| 原型构建后补丁 | 3 个文件 21.8 KB | 0 |
| Figma | — | 6 collection · 24 mode 组合 · 12 组件 237 variant · 94 icon |

## Figma 公开

API 改不了分享权限——你在 Figma 里 **Share → Anyone with the link → can view**，把链接贴进 README 和案例页。

## Week 2 收尾清单

- [x] 原型跑在 token 上
- [x] 组件逐个核对
- [x] before / after 两组数字
- [ ] Figma 设公开（你来）
- [ ] Week 3 Day 1：案例页骨架 + `/foundations`
