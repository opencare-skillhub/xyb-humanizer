# Xiaoyibao Humanizer Evaluation

The goal is not to maximize an AI-detector score. The goal is to improve naturalness while preserving meaning, evidence level, medical accuracy, and author voice.

## Dataset design
第一轮固定 20 篇：
- 5 篇中文医学科普；
- 5 篇中文患者／社区文章；
- 5 篇中文一般文章；
- 5 篇英文文章。

Where possible, include:
- AI-generated source
- human-written source
- AI + human edited source
- published Xiaoyibao/community source

## A/B/C/D benchmark
For each source create:
- A: original
- B: generic humanizer
- C: Xiaoyibao Humanizer
- D: expert human edit

Blind the labels before review.

## Scores
Rate 1–5:
- Naturalness
- Human Voice
- AI Pattern（5 = AI 痕迹很少）
- Authorial Authenticity
- Information density
- Medical accuracy
- Fear control
- Hope control
- Meaning preservation

权重：

| 指标 | 权重 |
| --- | ---: |
| Naturalness | 20% |
| Human Voice | 20% |
| AI Pattern | 10% |
| Medical Accuracy | 20% |
| Fear Control | 10% |
| Hope Control | 5% |
| Meaning Preservation | 10% |
| Information Density | 5% |

Authorial Authenticity 单独报告，不并入加权总分。

Also record binary failures:
- new fact invented
- number changed
- evidence level changed
- clinical recommendation invented
- fear-based wording introduced
- personal experience fabricated

## Regression rule
A new version should not be accepted merely because it sounds more human. Reject or revise it if it:
- changes medical meaning;
- invents facts;
- increases fear or hype;
- erases useful uncertainty;
- flattens a human author's distinctive voice.

## Hard gates

无论总分多高，出现以下任一情况均为 FAIL：

- Medical Accuracy < 4；
- Meaning Preservation < 4；
- Fear Control ≤ 2；
- 新增关键医学事实、改变数字／剂量、伪造引用或个人经历。

## Freeze rule

第一轮先冻结 dataset 和 v0.3，再完整运行。不得看到 C 的问题后立即改规则并重跑同一批结果。所有规则修改进入下一版本建议，等待人工确认。
