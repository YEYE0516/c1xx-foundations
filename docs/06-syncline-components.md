# Week 2 · Day 2–3 · Syncline components（Figma）

文件：[C1XX Foundations](https://www.figma.com/design/ZThJK81NT635ehYKdTd3Si) → 页 `04 · Components · Syncline`。组件只绑 Semantic 角色 + `space` / `radius` / `size` / `border` 变量，没有一个裸值；页面 frame 设 Product = syncline、Energy = cloud、Semantic = Light，换 mode 组件跟着变。

## 共同规则（Button 定稿后套到所有组件）

| 规则 | 值 |
| --- | --- |
| 高度 | 不写死，由 padding + 行高推出：md = 14/24 + 8+8 = 40，lg = 16/24 + 12+12 = 48 |
| 按钮内边距 | 竖 space/2–3，横 space/5–6（rem 系统：横松竖紧） |
| 圆角 | 按钮、chip 用 radius/full；输入框 radius/2；卡片 radius/4（= 卡片 padding space/6，圆角 ≈ padding） |
| 描边 | 1px（border/hairline），焦点 2px（border/emphasis）；描边不计入布局 |
| Hover | 填充升一档：Primary → action/primary-hover（accent strong），Secondary / Ghost → action/selected-bg（accent soft） |
| Pressed | Hover 的填充 + 88% 不透明度（你定的方案） |
| Disabled | action/disabled-bg（neutral/150）+ action/disabled-fg（neutral/500），不用 accent 半透明 |
| 次级描边 | fg/accent（energy form 的 strong，≥ 4.5:1）——你把 border/strong 判为太重后改的 |
| 输入框描边 | 新角色 border/control = neutral/500（3.2:1，过非文字 3:1） |
| 字体 | Inter Semi Bold（按钮）/ Medium（chip、eyebrow）/ Regular（正文、输入） |

## 组件

| 组件 | 矩阵 | 属性 |
| --- | --- | --- |
| Button | Style（Primary / Secondary / Ghost）× State（Default / Hover / Pressed / Disabled）× Size（md / lg）= 24 | Label（文字）、Show icon（布尔，AR 按钮用） |
| Input | State（Default / Focus / Filled / Disabled）× Size（md / lg）= 8 | Value（文字）。Filled 靠 fg/primary 区分占位的 fg/muted |
| Chip | Selected（Off / On）× State（Default / Hover / Disabled）= 6 | Label。On = accent soft 填充 + accent strong 描边 + accent 圆点 |
| Card | Style（Flat / Raised / Selected）= 3 | Eyebrow / Title / Body（文字）、Show media（布尔）。Raised 用 elevation/2，在 Syncline 下是海军蓝阴影；media 槽高度 = rhythm/4 |

Button 下方一排：同一个 Primary/lg 实例放进七个容器，只有容器的 Energy mode 不同——演示用。

## 新增的 Semantic 角色

- `action/disabled-bg`、`action/disabled-fg`
- `border/control`
- （Day 1 加的）`fg/accent`

这三个要回填到 `foundations/color.json`，保持 JSON 是真源。

## 踩过的坑（写下来免得再犯）

1. `resize()` 会把 auto-layout 的 hug 重置成固定——Card 被裁成 50px 高、Input 高度不对、specimen 两张卡裁空，三次都是它。规则：resize 之后必须重新设 `primaryAxisSizingMode = 'AUTO'`。
2. `strokesIncludedInLayout` 默认把描边算进高度，40 变 42。所有控件设为 false。
3. TEXT 属性在 variant 之间共享默认值，不能靠文字内容区分状态；状态差异用颜色表达。
