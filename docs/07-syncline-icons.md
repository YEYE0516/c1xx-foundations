# Week 2 · Day 3½ · Syncline icons（整理）

Day 4 把原型换到 token 之前，先把图形资产理清楚——否则换完 token 原型里还是三套来历不同的图。盘点结果：原型里一共三类图形，处理方式各不相同。

| 类 | 数量 | 来源 | 处理 |
| --- | --- | --- | --- |
| UI icon | 7 | `lucide-react`（Check、ChevronLeft、Menu、RotateCcw、Save、UsersRound、X） | 保留 Lucide，定规则，进 Figma `Icon` 组件 |
| 舞种 pictogram | 8 × 2 态 | `icon-refinements.js` 里用 DOM 现画的 SVG | 抽成数据文件 + 构建脚本，颜色绑 energy form，进 Figma `Pictogram` 组件 |
| 插画 | 13 | App.tsx 里的 inline SVG（240×220 ×8、360×500、360×420、350×172、320×150） | 只登记为插画，不进 icon 体系；Day 4 只把它们的硬编码颜色换成 token |

## 1 · UI icon：Lucide，三条规则

Lucide 是 24 格、2px 描边、圆头圆角——和底座的 `border/emphasis = 2` 正好对上，所以不重画，只定规则：

1. **尺寸只有三档**：`size/icon-sm` 16（chip、行内）、`size/icon-md` 20（按钮、输入框，默认）、`size/icon-lg` 24（导航、空状态）。原型里 `h-4 w-4` ×8、`h-5 w-5` ×1 分别对应 sm / md。
2. **描边恒为 2**：ChevronLeft 的 `strokeWidth={2.4}` 去掉。想要更重用 lg 尺寸，不改线宽。
3. **颜色只走 fg 角色**：icon 跟它旁边的文字同色——按钮里是 `action/primary-fg`，正文里是 `fg/primary` / `fg/secondary`，禁用是 `action/disabled-fg`。代码里 `stroke="currentColor"` 已经是这个意思，别再给 icon 单独写颜色。

Figma：页 `05 · Icons · Syncline` 的 `Icon` 组件（`Name` = 7 个），描边绑 `fg/primary` + `border/emphasis`。**Button 的 `icon` 空槽换成了 `Icon` 的 INSTANCE_SWAP 属性**（`Show icon` 开关保留），icon 描边绑到和 Label 同一个颜色变量，所以 Secondary / Ghost / Disabled 自动跟着文字变色，AR 按钮选 `users-round` 即可。

## 2 · 舞种 pictogram：80 × 64 格，颜色 = energy form

原来的问题：8 个图在 JS 里用 `document.createElementNS` 现画，颜色写死 `#54B8AB / #B69ADE / #F28B6D`（idle）和 `#54B8AB / #E98BA7 / #F6C04D`（active），设计稿里根本没有。

现在：

- 真源：`themes/syncline/pictograms.json`——每个图是 path / circle / rect 的数据表，三个**颜色槽**而不是颜色值。
- 槽位对应 energy form 的 base：**Idle = cloud / jelly / fuzz，Active = cloud / bloom / star**。原来的 `#F28B6D` 不在任何 form 里，吸附到 fuzz `#e87555`。
- `build/pictograms.py` 生成 `dist/syncline/pictograms/`：16 个单文件 SVG、一个 sprite、一个 `pictograms.js`。颜色写成 `var(--form-cloud, #54b8ab)`，inline 时跟 token 走，当图片用时有回退值。
- `build.py` 新增 `--form-{cloud,peak,star,fuzz,bloom,jelly}`：六个 form 的 base 并排给出，给 pictogram、avatar 环、form 选择器这种"几个 form 同时出现"的场景用；"当前 form"仍用 `--accent-*`。
- 网格 80 × 64，描边 4（辅助虚线 2），用在风格选择器里按 40 × 32 渲染（宽 = `space/10`）。

Figma：新增 collection **`Syncline · forms`**（`form/cloud … form/jelly`，单 mode，固定值），Energy collection 的 `energy/base` 改为引用它——同一个颜色只定义一次。`Pictogram` 组件 `Name`（8）× `State`（Idle / Active）= 16 个 variant，每个形状的描边/填充绑 `form/*`。

## 3 · 插画：登记，不动

13 张 inline SVG 是场景插画，不是 icon：尺寸各异、有渐变、有角色。它们留在 App.tsx，Day 4 只把里面的硬编码颜色换成 `--form-*` / `--bg-*`，不进组件库。

## Day 4 要做的衔接

- `icon-refinements.js` 的 `createDanceIcon` 删掉，改为 import `dist/syncline/pictograms/pictograms.js`（或直接 inline sprite）。
- `ChevronLeft strokeWidth={2.4}` → 去掉；`h-4 w-4` / `h-5 w-5` → `size-icon-sm` / `size-icon-md`（Tailwind theme 指向 `--size-icon-*`）。
- `data-energy` 切换时 pictogram 不变（它用的是固定 `--form-*`），avatar 环变（它用 `--accent-*`）——这是刻意的：选舞种时六个 form 要同时可辨。

## 盘点数字（给案例用）

| | before | after |
| --- | --- | --- |
| icon 来源 | 3 套（Lucide、JS 现画、inline SVG） | 2 套 + 插画登记 |
| icon 尺寸 | 2 个裸 class + 1 个自定义线宽 | 3 档 token，线宽 1 个 |
| pictogram 颜色 | 6 个写死 hex，设计稿里没有 | 0 个 hex；5 个 form 颜色槽，Figma 与代码同源 |
