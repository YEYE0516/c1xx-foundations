# 对比度报告 · themes/site/theme.json

WCAG 2.x。正文 AA ≥ 4.5，大字（≥ 24px 或 ≥ 19px 粗体）AA ≥ 3，非文字 UI ≥ 3。AAA ≥ 7。

## light

| 前景 | 背景 | 比值 | 正文 AA | 大字 AA | AAA | 用途 |
| --- | --- | --- | --- | --- | --- | --- |
| fg.primary `#121310` | bg.canvas `#f3f1ec` | **16.52** | ✓ | ✓ | ✓ | 正文 |
| fg.primary `#121310` | bg.surface `#f7f5f0` | **17.11** | ✓ | ✓ | ✓ | 卡片正文 |
| fg.primary `#121310` | bg.raised `#fbfaf7` | **17.86** | ✓ | ✓ | ✓ | 弹层正文 |
| fg.secondary `#62625d` | bg.canvas `#f3f1ec` | **5.43** | ✓ | ✓ | ✗ | 次级文字 |
| fg.secondary `#62625d` | bg.surface `#f7f5f0` | **5.63** | ✓ | ✓ | ✗ | 卡片次级文字 |
| fg.muted `#8a8982` | bg.canvas `#f3f1ec` | **3.11** | ✗ | ✓ | ✗ | metadata ≥ 12px |
| fg.on-inverse `#f7f5f0` | bg.inverse `#121310` | **17.11** | ✓ | ✓ | ✓ | 反色块文字 |
| action.primary-fg `#f7f5f0` | action.primary `#121310` | **17.11** | ✓ | ✓ | ✓ | 主按钮文字 |
| fg.primary `#121310` | action.selected-bg `#ebe8e1` | **15.24** | ✓ | ✓ | ✓ | 选中态文字 |
| border.subtle `#cbc8bf` | bg.canvas `#f3f1ec` | **1.48** | ✗ | ✗ | ✗ | 分隔线（非文字，3:1 即可） |
| action.signal `#ed5138` | bg.canvas `#f3f1ec` | **3.19** | ✗ | ✓ | ✗ | signal 作为小字 |
| focus.ring `#121310` | bg.canvas `#f3f1ec` | **16.52** | ✓ | ✓ | ✓ | 焦点环（非文字，3:1） |

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
| action.primary-fg `#121310` | action.primary `#f7f5f0` | **17.11** | ✓ | ✓ | ✓ | 主按钮文字 |
| fg.primary `#f7f5f0` | action.selected-bg `#343532` | **11.33** | ✓ | ✓ | ✓ | 选中态文字 |
| border.subtle `#343532` | bg.canvas `#121310` | **1.51** | ✗ | ✗ | ✗ | 分隔线（非文字，3:1 即可） |
| action.signal `#ed5138` | bg.canvas `#121310` | **5.18** | ✓ | ✓ | ✗ | signal 作为小字 |
| focus.ring `#ed5138` | bg.canvas `#121310` | **5.18** | ✓ | ✓ | ✗ | 焦点环（非文字，3:1） |

