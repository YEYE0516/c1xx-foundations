# Day 4 · 颜色

产出 `foundations/color.json`、`themes/site/theme.json`、`build/contrast.py`、`docs/04-contrast.md`。

## 结构：一条色阶 + 一份合同 + 两套角色

```
neutral.0 … 950      13 阶暖灰，两个主题共用（primitive）
accent.*             合同：base / strong / soft / on / signal，底座只声明，主题必须填
semantic.light.*     角色：bg / fg / border / action / focus / shadow
semantic.dark.*      同一组 key，值不同 → Figma 里是一个 collection 的两个 mode
```

底座里唯一的具体色值是暖灰色阶。盘点证明两个产品的灰在同一条色相上（`#f3f1ec→#121310`、`#f7f4ef→#1f1f1f`），所以共用；13 阶里的 100 / 200 / 300 / 600 / 950 直接取自网站现在的 Paper / Soft / Rule / Muted / Ink，900 取自 Syncline 的 ink。网站 74 个近中性灰全部吸附到这 13 阶。

## 角色（semantic）

| 组 | 角色 | light | dark | 用在 |
| --- | --- | --- | --- | --- |
| bg | canvas / surface / raised / sunken / inverse | 100 / 50 / 0 / 150 / 950 | 950 / 900 / 800 / 900 / 100 | 页面 / 卡片 / 弹层 / 凹陷 / 反色块 |
| fg | primary / secondary / muted / on-inverse / on-accent | 950 / 600 / 500 / 50 / accent.on | 50 / 400 / 500 / 950 / accent.on | 正文 / 次级 / 装饰性 metadata / 反色块文字 / 按钮文字 |
| border | subtle / strong | 300 / 950 | 800 / 300 | 分隔线 / 输入框和描边控件 |
| action | primary / primary-hover / primary-fg / selected-bg / signal | ← accent 合同 | ← accent 合同 | 主按钮 / hover / 按钮文字 / 选中态 / 激活与进度 |
| focus | ring | accent.signal | accent.signal | 焦点环，2px + 2px offset |
| shadow | hue / weak / base / strong | 主题色相 @ .06 / .10 / .18 | 黑 @ .30 / .45 / .60 | 被 shape.elevation 引用 |

## 网站主题填了什么

- 字体：Manrope（body）、Newsreader（display）、DM Mono（mono）。
- accent：**网站的主操作是 Ink，不是色相**——黑色胶囊按钮配米白文字，这是它现在的样子。所以 `accent.base = neutral.950`，dark mode 翻转成 `neutral.50`。`signal = #ed5138` 给激活导航和进度条。
- 项目 accent（Syncline 青、Blooming 粉、Clario 橙）和 acid / violet / orange 高亮放在 `scene.*`，属于主题层，底座不知道它们存在。
- aurora 四个氛围色和 16s 漂移时长放在 `aurora.*`，同样不进合同。

## 对比度：三处要你知道的决定

跑 `build/contrast.py` 得到 `docs/04-contrast.md`，light 12 对、dark 12 对。正文和按钮全部 AAA。三处没过的是有意的：

1. **焦点环改成 Ink。** DESIGN.md 定的焦点色 `#ff633c` 在 Paper 上只有 2.62:1，低于非文字元素 3:1 的底线，键盘用户可能看不到焦点在哪。改成 `neutral.950`（16.5:1）。橙色保留为 `scene.highlight.orange`，用途不变，只是不再承担焦点。

2. **`fg.muted`（neutral.500）在 light 下是 3.11:1，正文 AA 不过。** 保留它，但规则是：只能用于**非必要信息**（装饰性序号、禁用态、占位符），任何读者需要读的文字最低用 `fg.secondary`（5.43:1）。这条写进 token 的描述里了。

3. **`signal` 作为小字 3.19:1。** 它的角色是激活导航和进度条（非文字，3:1 ✓），不是正文色。同理三个项目 accent 在 Paper 上是 1.78 / 3.28 / 3.40，**不能直接当文字用**——这正是 DESIGN.md 原来写的"accent 只用于箭头、焦点瞬间、小字、指针光"，现在有了数字支撑。Syncline 主题下周填 accent 时，`accent.strong` 要给一个压暗到 ≥ 4.5 的值（`#1f7a77` 大概够），文字用 strong，色块用 base。

`border.subtle` 1.48:1 是分隔线，不需要达标；输入框描边用 `border.strong`。

## 合同：下周 Syncline 主题要填的

```
theme.font.body / display / mono
theme.accent.light.{base, strong, soft, on, signal}
theme.accent.dark.{…}
theme.shadow.hue            → Syncline 用 #152a55 海军蓝
（可选）bg.canvas 覆盖      → neutral.50
```

六个 energy form 各一组 accent 五件套，就是六个 mode。
