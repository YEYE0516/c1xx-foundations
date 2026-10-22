# C1XX Foundations · 三周计划

截止 2026-11-12。周一到周五每天一个任务日，周末缓冲。每个任务日的完成标准都一样：当天的产出能被 Day 5 的构建脚本读进去，或者能直接放进案例页。

**三条红线**

1. 不碰网站改版和 GSAP，动效以后引用 motion token 就行
2. Figma 组件只给 Syncline 做；网站那边只建 variables 和 text styles 对照
3. 第 2 周时间不够就把组件砍到 6 个，但 modes 不砍

## 第 1 周 · 底座（10/21 – 10/29）

目标：`foundations/` 里的刻度和规则全部定稿，网站带着 token 上线，Figma 有对照。前四天写的是数据不是画图，别打开 Figma。

- [x] **10/21 周三 · Day 0** — 建仓库，立目录；本表存到 `docs/plan.md`
  产出：空仓库 · 标准：目录结构和 README 一致
- [x] **10/22 周四 · Day 1** — 盘点：脚本扫 Syncline 原型 CSS 和网站 CSS，抽出颜色、字号/行距、间距、圆角、阴影、动效时长，去重 + 计数 + 出处；做三个决定（留哪两套字体、近似色怎么合并、neutral 是否共用）
  产出：`docs/inventory.md` · 标准：每个值有次数和出处；三个决定写了理由；数字能直接当案例的 before
- [x] **10/23 周五 · Day 2** — 字阶与网格：用 baseline-to-layers 生成 4pt 基线字阶（行距互为整数倍，正文 16/24 上下各推 3–4 档）；三个断点的栏宽和页边距（每行 7–10 个单词反推）
  产出：`foundations/typography.json`、`layout.json` · 标准：每档 line-height 都是 4 的倍数；栏宽给出 `max-width` 的 ch 值
- [x] **10/26 周一 · Day 3** — 间距 / 圆角 / 层级 / 动效：间距刻度数字命名约 10 档；圆角 3 档 + full；阴影 2–3 档；duration 三档、easing 三条（enter / exit / emphasis）、reduced-motion 规则
  产出：`spacing.json`、`shape.json`、`motion.json` · 标准：间距全是 4 的倍数；motion 的值能被 GSAP 直接引用
- [x] **10/27 周二 · Day 4** — 颜色：primitive 色阶（neutral + accent 各 10 阶）；semantic 角色（bg / fg / border / action / focus）；light + dark 两个 mode；对比度脚本跑一遍。网站具体色值放 `themes/site/`
  产出：`color.json`、对比度报告 · 标准：所有前景/背景对达 WCAG AA；`foundations/` 里不出现任何品牌色值
- [x] **10/28 周三 · Day 5** — 组装上线：合并为 DTCG `tokens.json`；构建脚本生成 `tokens.css` + Tailwind theme；套到现网站只换值不改结构；README 写三层规则、命名规范、新增 token 五步；打 tag v0.1.0
  产出：网站带底座上线、README、v0.1.0 · 标准：网站 CSS 里 grep 不到裸 hex 和裸 px（1px 边框除外）；改一个 token 整站跟着变
- [x] **10/29 周四 · Figma 对照** — 用 Figma MCP 把 `tokens.json` 导成 Primitives、Semantic 两个 collection（含 light/dark modes）；建 text styles 对应字阶；不画组件
  产出：Figma 文件 v0.1 · 标准：collection 里每个 variable 名和 JSON 一致

周末 10/24–10/25 是缓冲。

## 第 2 周 · Syncline 主题（10/30 – 11/5）

目标：Syncline 作为第二个品牌主题挂在底座上，Figma 里一键切 energy form，原型跑在 token 上。

- [x] **10/30 周五 · Day 1** — brand layer：把 Syncline 的 teal / lavender / sand 和 Inter + New York 写进 `themes/syncline/`，只覆盖 semantic 层；六种 energy form 各一组 accent
  产出：`themes/syncline/*.json` · 标准：构建脚本能用同一套 foundations 生出网站和 Syncline 两份 `tokens.css`
- [ ] **11/2 周一 · Day 2** — Figma 组件 I：Button（primary / secondary / ghost / AR / icon × 状态）、Input、Chip、Card；每个 variant 绑 variables，auto layout 用 spacing variables
  产出：Figma 组件库前半 · 标准：任何组件选中后属性面板里没有裸数值
- [ ] **11/3 周二 · Day 3** — Figma 组件 II + modes：Slider、Page control、Bottom sheet、Toast、Avatar（6 个 variant）；Syncline brand collection，6 个 energy-form modes
  产出：Figma 组件库全部 + modes · 标准：切一次 mode 整页变色，avatar 跟着换
- [ ] **11/4 周三 · Day 4** — 原型换 token：Tailwind config 指向生成的 token；`hig-refinements.css` 里的硬编码全部换成 variables；三套字体收成两套
  产出：原型新版本上线 · 标准：原型 CSS 里 grep 不到裸 hex；盘点脚本再跑一次，数字写进案例
- [ ] **11/5 周四 · Day 5** — 校验 + 收尾：Figma 和代码逐个组件对状态；Code Connect 把 Button 挂到 React 组件（可跳过）；Figma 文件设为公开
  产出：校验清单、公开链接 · 标准：每个组件每个状态两边一致；before / after 两组数字齐

周末 10/31–11/1 是缓冲。组件做不完先砍 Toast 和 Bottom sheet，再砍 Card，modes 和 Avatar 不砍。

## 第 3 周 · 呈现（11/6 – 11/12）

目标：Work 下的案例页上线，面试官 30 秒内能看到 live 页、Figma 文件、代码三样东西。案例页本身也用底座 token 和基线网格排。

- [ ] **11/6 周五 · Day 1** — 案例页骨架 + `/foundations` 子页：Work 列表加第 4 个条目；按问题—决策—证据—数字四段搭结构；foundations 子页用 token 本身渲染字阶、间距、颜色、动效
  产出：案例页空壳、foundations 子页 · 标准：子页每个展示块的样式来自 token，改 JSON 页面跟着变
- [ ] **11/9 周一 · Day 2** — `/syncline` 子页：顶部 energy-form 切换器，下面组件全部跟着变
  产出：syncline 子页 · 标准：6 个状态都对，移动端不溢出
- [ ] **11/10 周二 · Day 3** — 案例写作：问题段放盘点表的 before 数字和代码截图；决策段讲为什么分底座和主题、刻度怎么定；结果段放 after 数字；录 10 秒 mode 切换视频
  产出：案例全文、视频 · 标准：至少 3 个量化数字；before / after 对比图一张
- [ ] **11/11 周三 · Day 4** — 外部链接 + 简历：Figma 公开链接、GitHub README 架构图、Syncline 案例第 05 节改成摘要 + 跳转；简历加一行中英版
  产出：链接齐、简历更新 · 标准：三个外链从案例页一跳可达；简历那行有数字
- [ ] **11/12 周四 · Day 5** — 自查 + 上线：手机、桌面各过一遍；找一个人 5 分钟内看完说出它是什么；修完发布
  产出：案例上线 · 标准：对方能复述出"一个底座两个主题"

周末 11/7–11/8 是缓冲。视频和 Code Connect 是最先可以放弃的两项。

## 最终交付清单

- [ ] GitHub 仓库：`tokens.json`（DTCG）、构建脚本、README 架构图，tag v1.0.0
- [ ] c1xxstudio.com 跑在底座 token 上，CSS 无裸 hex / px
- [ ] Syncline 原型跑在 token 上
- [ ] Figma 公开文件：三个 collection，6 个 modes，8–10 个组件
- [ ] Work 第 4 条目案例页：问题 → 决策 → 证据 → 数字
- [ ] `/foundations`、`/syncline` 两个 live 子页
- [ ] before / after 盘点数字
- [ ] 10 秒 mode 切换视频
- [ ] Syncline 案例第 05 节改为摘要 + 跳转
- [ ] 简历一行（中 / 英）
