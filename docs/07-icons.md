# Week 2 · Day 3½ · Icon system

原型里的图形来历有三种（7 个 Lucide icon、8 个 JS 现画的舞种图、13 张 inline 插画），没有规则、没有尺寸档、颜色写死。这一步不是把它们"提取出来"，而是**建一套可复用的 icon 体系**，原型只是第一个消费者。

体系分三层：

| 层 | 归属 | 数量 | 用途 |
| --- | --- | --- | --- |
| **UI icon** | `foundations/`（底座，两个主题共用） | 94 | 导航、操作、状态——功能性，单色 |
| **Pictogram** | `themes/syncline/`（主题） | 8 × 2 态 | 舞种选择器——表意性，三色 |
| 插画 | 留在 App.tsx | 13 | 场景插画，只登记，Day 4 换颜色 token |

## 1 · UI icon（底座）

### 为什么用 Lucide 而不是自己画

Lucide 是 24 格、2px 描边、圆头圆角、ISC 许可——和底座的 `border/emphasis = 2`、`radius/1 = 4`（icon 内角 2）正好同一套语言。自己画 94 个 icon 要一周，而且质量不会更好。**系统的价值在规则、选集和绑定，不在手绘。**

### 规格（`foundations/icons.json → grid`）

| | 值 |
| --- | --- |
| 画布 | 24 × 24 |
| 活动区 | 20 × 20（四边各留 2，16px 时视觉重量才不塌） |
| 关键线 | 圆 20 · 方 18 · 横矩 20×16 · 竖矩 16×20（圆形图填满 20，方形图填满 18，看起来才一样大） |
| 描边 | 2 = `border/emphasis`，圆头圆角，内角半径 2 |
| 颜色 | `currentColor`，文件里不出现任何颜色值 |

### 三条规则

1. **尺寸只有三档**：`size/icon-sm` 16（行内、chip）、`size/icon-md` 20（默认：按钮、输入框、列表行）、`size/icon-lg` 24（导航栏、空状态、icon button lg）。
2. **描边恒为 2**。想要更重用大一档，不改线宽。原型里 ChevronLeft 的 `strokeWidth={2.4}` 去掉。
3. **icon 不带自己的颜色**。跟旁边文字同色（`currentColor`），或只取一个角色：`fg/primary`（默认）、`fg/secondary`、`fg/muted`、`fg/accent`、`fg/on-accent`、`action/signal`、`action/disabled-fg`。

另外：icon 单独不作为点击目标；要点击就用 **Icon button**（40 / 48），命中区 ≥ `size/touch-min` 44。

### 选集：7 类 94 个

| 类 | 数 | 内容 |
| --- | --- | --- |
| navigation | 20 | chevron ×4、arrow ×3、menu、x、ellipsis ×2、house、search、settings、sliders、list-filter、expand、shrink、layers、grid-2x2 |
| action | 18 | plus、minus、check、save、pencil、trash-2、share、download、upload、copy、rotate-ccw、refresh-cw、external-link、link、log-out、qr-code、scan、bookmark |
| status | 16 | info、circle-alert、triangle-alert、circle-check、circle-x、circle-help、bell、bell-off、eye、eye-off、lock、lock-open、wifi、wifi-off、loader-circle、globe |
| people | 9 | user-round、users-round、user-round-plus、heart、star、message-circle、hand、smile、thumbs-up |
| media | 15 | play、pause、square、skip-back、skip-forward、volume-2、volume-x、mic、mic-off、camera、video、image、music、headphones、audio-lines |
| time-place | 5 | clock、calendar、timer、map-pin、compass |
| energy | 11 | zap、sparkles、activity、flame、moon、sun、footprints、orbit、gauge、waves、wind |

选集原则：原型现在用到的 7 个全在；一个移动端社交/舞蹈 app 的完整流程（登录、设置、媒体控制、AR 扫码、通知、反馈）都能覆盖；energy 这一类是 Syncline 的词汇，但选的都是网站也能用的通用形。

命名：lucide 原名，kebab-case。方向写实（chevron-left），状态做后缀（bell-off、lock-open）。名字里不带尺寸和颜色。

### 加一个 icon 的流程

1. `foundations/icons.json` 对应类别里加名字
2. `python3 -I build/icons.py vendor <lucide-static/icons>` → 复制并归一化到 `foundations/icons/<name>.svg`
3. `build/icons.py build` → `dist/icons/`：`sprite.svg`、`icons.json`（name → body）、`icons.css`（`.icon` / `.icon--sm|lg` / 颜色角色 / `.icon-button`）、`manifest.md`
4. Figma 里 `Icon` 组件集加一个 variant（脚本化，和这次一样）

不手绘、不从别的库混进来。

### Figma

页 **`05 · Icons`**：

- `Icon` 组件集，`Name` = 94 个 variant，按 7 类分行排列，左侧类别标签。描边绑 `fg/primary` + `border/emphasis`，形状设 SCALE 约束——实例改尺寸时线条跟着缩。
- 规格块：24 格 + 20 活动区（虚线）+ 关键线（圆 20 / 方 18），8 倍放大的 bell 示例。
- 三档尺寸行（绑 `size/icon-*`），八个颜色角色行（DEFAULT … ON INVERSE，每个是实例上覆盖一个变量）。
- 六条规则直接写在页面上。

页 `04 · Components · Syncline`：

- **Button 的 `icon` 空槽换成 `Icon` 的 INSTANCE_SWAP 属性**（`Show icon` 开关保留），icon 描边绑到和 Label 同一个颜色变量——Secondary / Ghost / Disabled 自动跟文字变色。
- 新增 **`Icon button`**：Style（Primary / Secondary / Ghost）× State（4）× Size（md 40 / lg 48）= 24，配方和 Button 完全一致，md 配 icon-md 20、lg 配 icon-lg 24，`Icon` 实例替换。原型里的返回、关闭、菜单按钮都应该是它。

## 2 · Pictogram（Syncline 主题）

原来 8 个舞种图在 `icon-refinements.js` 里用 `document.createElementNS` 现画：颜色写死、每个图的网格、线宽、留白各不相同（有的贴边、有的只占一半，有虚线辅助线、有实心圆点、有 4 个矩形），放在一起没有一套形态。第一版只是把它们抽成数据；第二版按规范重画。

**规则 = UI icon 的规则 × 2**

| | UI icon | Pictogram |
| --- | --- | --- |
| 画布 | 24 | 48 |
| 活动区 | 20（留 2） | 40（留 4） |
| 描边 | 2 | 4（线宽 : 画布 都是 1 : 12） |
| 端点 | 圆 | 圆 |
| 颜色 | 1 个角色 | 3 个槽（form 色） |

额外的语法：**每个图恰好三笔**，一笔一个颜色槽，没有填充、没有虚线、没有透明度；三笔填满 40 活动区（横排 y = 12 / 24 / 36，或竖排 x = 12 / 24 / 36，间距 12 保证相邻笔画净空 ≥ 6）；每个舞种一个母题，32px 下仍可辨：

| 舞种 | 母题 |
| --- | --- |
| hiphop | 楼梯——三个踏步，一拍一级 |
| cultural | 正弦波——流动、有规律 |
| freestyle | 三条互不重复的自由曲线 |
| gentle | 浅弧——低幅 |
| bounce | 双拱——反复的竖向弹跳 |
| sway | 竖向 S——左右重心转移 |
| spin | 同一个环上的三段弧——绕中心旋转 |
| step | 左右交替的踏板 |

槽位 = energy form 的 base：**Idle = cloud / jelly / fuzz，Active = cloud / bloom / star**。

- 真源 `themes/syncline/pictograms.json`（规则也写在 `rules` 节点里）。
- `build/pictograms.py` → `dist/syncline/pictograms/`：16 个 SVG、sprite、`pictograms.js`。颜色写 `var(--form-cloud, #54b8ab)`。
- 原型里在 `rhythm/3`（72）的方形容器里按 56 渲染；行内 32。
- `build.py` 的 `--form-{cloud,peak,star,fuzz,bloom,jelly}` 给"几个 form 同时出现"的场景用；"当前 form"仍用 `--accent-*`。

Figma：collection **`Syncline · forms`**（`form/cloud … form/jelly`），Energy 的 `energy/base` 引用它。`Pictogram` 组件集 `Name`（8）× `State`（Idle / Active）= 16，每一笔绑 `form/*`，约束 SCALE。

## 3 · Avatar 图片已入库

六张 energy-form 头像以 192px PNG 放进 `Avatar` 组件的 `image` 层（椭圆 + 图片填充，`placeholder` 隐藏作回退）。代理网络不允许上传到 mcp.figma.com，改为把 PNG 压到 5 KB 以内直接经 Plugin API `createImage` 写入，SHA-1 和本地文件逐一核对。

## Day 4 要做的衔接

- `h-4 w-4` / `h-5 w-5` → `size-icon-sm` / `size-icon-md`；`strokeWidth={2.4}` 去掉；icon 颜色 class 删掉，靠 `currentColor`。
- 返回 / 关闭 / 菜单按钮改成 Icon button 的 class（`.icon-button`，`.icon-button--lg`）。
- `createDanceIcon` 删掉，改 import `dist/syncline/pictograms/pictograms.js`。
- 13 张插画里的硬编码颜色换成 `--form-*` / `--bg-*`。
- `data-energy` 切换时 pictogram 不变（固定 `--form-*`），avatar 环变（`--accent-*`）——刻意的：选舞种时六个 form 要同时可辨。

## 盘点数字（给案例用）

| | before | after |
| --- | --- | --- |
| icon 来源 | 3 套（Lucide 7 个、JS 现画 8 个、inline SVG 13 张），无规则 | 1 套 UI icon（94，7 类）+ 1 套 pictogram（主题层）+ 插画登记 |
| icon 尺寸 / 线宽 | 2 个裸 class + 1 个自定义线宽 | 3 档 token，线宽 1 个 |
| pictogram 颜色 | 6 个写死 hex，设计稿里没有 | 0 个 hex；5 个 form 颜色槽，Figma 与代码同一份数据 |
| Figma 组件 | 9 | 12（+ Icon 94 variants、Icon button 24、Pictogram 16） |
