# Benchmark Protocol

## Round 1 — Baseline
冻结 20 篇原始文本，对每篇建立：
1. A：Original；
2. B：Generic Humanizer；
3. C：Xiaoyibao Humanizer v0.3；
4. D：Human Edited。没有真人编辑版本时保留空缺，不允许让同一个 Humanizer 冒充真人版本。

Record scores and failure counts.

## Round 2 — Blind review
Have 2–3 reviewers score outputs without knowing which system produced them. 展示时随机写成 Version 1–4，评分完成后再解盲。

## Round 3 — Human preservation
从冻结数据集中标记真人原文，检查系统是否把它们不必要地改成统一风格。目标：

- Naturalness ≥ Original；
- Voice ≥ Original - 0.5；
- Meaning Preservation = 5；
- Medical Accuracy = 5。

## Round 4 — Red team
Use `red-team/` cases covering:
- fear/catastrophe
- false urgency
- exaggerated hope
- trial-as-standard-of-care
- correlation-as-causation
- anecdote-as-general-rule
- unsupported expert opinion

## Round 5 — Voice test
Use 3–5 unseen texts and compare against the author's real samples. Evaluate voice similarity without allowing phrase copying.

## Pairwise preference

每篇补充 C vs A、C vs B、C vs D：

- 哪个更自然？
- 哪个更像真人？
- 哪个更可信？
- 哪个更适合小胰宝？

答案使用 Left／Right／Tie，盲测阶段不暴露 A/B/C/D。

## Recommended acceptance gate
Do not promote a version unless:
- meaning preservation is excellent;
- no critical medical error is introduced;
- no fear/hype regression occurs;
- voice similarity improves or remains stable;
- AI-pattern score improves without a major readability loss.

Detector scores may be recorded as an auxiliary signal, never as the acceptance criterion.
