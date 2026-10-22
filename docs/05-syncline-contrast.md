# 对比度报告 · themes/syncline/theme.json

WCAG 2.x。正文 AA ≥ 4.5，大字（≥ 24px 或 ≥ 19px 粗体）AA ≥ 3，非文字 UI ≥ 3。AAA ≥ 7。

## light

| 前景 | 背景 | 比值 | 正文 AA | 大字 AA | AAA | 用途 |
| --- | --- | --- | --- | --- | --- | --- |
| fg.primary `#121310` | bg.canvas `#f7f5f0` | **17.11** | ✓ | ✓ | ✓ | 正文 |
| fg.primary `#121310` | bg.surface `#f7f5f0` | **17.11** | ✓ | ✓ | ✓ | 卡片正文 |
| fg.primary `#121310` | bg.raised `#fbfaf7` | **17.86** | ✓ | ✓ | ✓ | 弹层正文 |
| fg.secondary `#62625d` | bg.canvas `#f7f5f0` | **5.63** | ✓ | ✓ | ✗ | 次级文字 |
| fg.secondary `#62625d` | bg.surface `#f7f5f0` | **5.63** | ✓ | ✓ | ✗ | 卡片次级文字 |
| fg.muted `#8a8982` | bg.canvas `#f7f5f0` | **3.22** | ✗ | ✓ | ✗ | metadata ≥ 12px |
| fg.on-inverse `#f7f5f0` | bg.inverse `#121310` | **17.11** | ✓ | ✓ | ✓ | 反色块文字 |
| action.primary-fg `#121310` | action.primary `#54b8ab` | **7.83** | ✓ | ✓ | ✓ | 主按钮文字 |
| fg.primary `#121310` | action.selected-bg `#e0ece6` | **15.37** | ✓ | ✓ | ✓ | 选中态文字 |
| border.subtle `#cbc8bf` | bg.canvas `#f7f5f0` | **1.54** | ✗ | ✗ | ✗ | 分隔线（非文字，3:1 即可） |
| action.signal `#cc3b12` | bg.canvas `#f7f5f0` | **4.59** | ✓ | ✓ | ✗ | signal 作为小字 |
| focus.ring `#cc3b12` | bg.canvas `#f7f5f0` | **4.59** | ✓ | ✓ | ✗ | 焦点环（非文字，3:1） |

## dark

| 前景 | 背景 | 比值 | 正文 AA | 大字 AA | AAA | 用途 |
| --- | --- | --- | --- | --- | --- | --- |
| fg.primary `#f7f5f0` | bg.canvas `#121310` | **17.11** | ✓ | ✓ | ✓ | 正文 |
| fg.primary `#f7f5f0` | bg.surface `#1f1f1f` | **15.13** | ✓ | ✓ | ✓ | 卡片正文 |
| fg.primary `#f7f5f0` | bg.raised `#343532` | **11.33** | ✓ | ✓ | ✓ | 弹层正文 |
| fg.secondary `#aaa9a3` | bg.canvas `#121310` | **7.91** | ✓ | ✓ | ✓ | 次级文字 |
| fg.secondary `#aaa9a3` | bg.surface `#1f1f1f` | **7.00** | ✓ | ✓ | ✗ | 卡片次级文字 |
| fg.muted `#8a8982` | bg.canvas `#121310` | **5.31** | ✓ | ✓ | ✗ | metadata ≥ 12px |
| fg.on-inverse `#121310` | bg.inverse `#f3f1ec` | **16.52** | ✓ | ✓ | ✓ | 反色块文字 |
| action.primary-fg `#121310` | action.primary `#54b8ab` | **7.83** | ✓ | ✓ | ✓ | 主按钮文字 |
| fg.primary `#f7f5f0` | action.selected-bg `#1e312c` | **12.59** | ✓ | ✓ | ✓ | 选中态文字 |
| border.subtle `#343532` | bg.canvas `#121310` | **1.51** | ✗ | ✗ | ✗ | 分隔线（非文字，3:1 即可） |
| action.signal `#cc3b12` | bg.canvas `#121310` | **3.73** | ✗ | ✓ | ✗ | signal 作为小字 |
| focus.ring `#cc3b12` | bg.canvas `#121310` | **3.73** | ✗ | ✓ | ✗ | 焦点环（非文字，3:1） |

## energy forms

| form | mode | base on canvas (非文字 ≥3) | strong on canvas (文字 ≥4.5) | on over base (文字 ≥4.5) |
| --- | --- | --- | --- | --- |
| cloud | light | 2.18 ✗ | 4.69 ✓ | 7.83 ✓ |
| cloud | dark | 7.83 ✓ | 7.83 ✓ | 7.83 ✓ |
| peak | light | 4.96 ✓ | 4.96 ✓ | 4.96 ✓ |
| peak | dark | 3.45 ✓ | 4.58 ✓ | 4.96 ✓ |
| star | light | 1.53 ✗ | 4.59 ✓ | 11.16 ✓ |
| star | dark | 11.16 ✓ | 11.16 ✓ | 11.16 ✓ |
| fuzz | light | 2.71 ✗ | 4.59 ✓ | 6.31 ✓ |
| fuzz | dark | 6.31 ✓ | 6.31 ✓ | 6.31 ✓ |
| bloom | light | 2.21 ✗ | 4.52 ✓ | 7.74 ✓ |
| bloom | dark | 7.74 ✓ | 7.74 ✓ | 7.74 ✓ |
| jelly | light | 2.22 ✗ | 4.61 ✓ | 7.69 ✓ |
| jelly | dark | 7.69 ✓ | 7.69 ✓ | 7.69 ✓ |

