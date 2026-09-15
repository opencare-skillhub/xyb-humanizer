# 小胰宝 Humanizer v0.3

一个面向中文医学科普、患者教育、社区内容、专家观点整理以及中英文内容的 Humanizer Skill。

## 设计目标

它不是“AI 检测器规避器”。核心目标是：

> **自然度 + 作者感 + 医学可信度 + 对读者的尊重。**

尤其强调：**不能靠恐吓、羞耻、灾难化语言或虚假紧迫感来提高读者注意力。**

## v0.3 新增

- `references/ai-tells-en.md`：英文 AI 痕迹诊断
- `references/fear-free-communication.md`：无恐吓医学沟通规范
- `references/medical-writing.md`：医学事实、证据层级和患者行动信息保护
- `references/voice-sam.md`：Sam / 小胰宝项目默认 Voice Profile
- `references/voice-profile.md`：自定义作者声音的方法
- `workflows/audit.md`：只审不改的 Audit 模式
- `evals/`：Benchmark、A/B/C/D 对比和 Red Team 回归测试框架
- 中英文医学内容的证据等级与语义保护

## Voice：支持自定义作者风格

Humanizer 不应该把所有文章改成同一种“人味”。因此支持 Voice Profile。

### 最简单的用法

在 `references/` 下创建：

```text
voice-yourname.md
```

然后在提示中说：

```text
使用 voice-yourname 风格，standard 去 AI 味。
```

### 更推荐的做法

准备 5–10 篇你真正喜欢、并且确实代表自己写作习惯的文章。不要只提供一篇。

让 Agent 分析：
- 句子长短
- 段落节奏
- 常用词
- 不喜欢的词
- 专业程度
- 判断是否直接
- 如何表达不确定性
- 如何写结论
- 是否使用第一人称
- 口语程度
- 幽默程度

然后生成一个 Voice Profile。

**不要让模型复制原文句子。** Voice Profile 应该描述稳定的写作规律，而不是保存可直接拼接的句库。

### 项目级 Voice

如果这个 Skill 用在项目中，可以放一个：

```text
VOICE.md
```

或者：

```text
references/voice-project.md
```

当前任务明确指定的声音优先级最高。

## 建议的目录

```text
humanize/
├── SKILL.md
├── README.md
├── references/
│   ├── ai-tells-zh.md
│   ├── ai-tells-en.md
│   ├── medical-writing.md
│   ├── fear-free-communication.md
│   ├── voice-profile.md
│   └── voice-sam.md
├── workflows/
│   ├── article.md
│   ├── community.md
│   ├── medical.md
│   └── audit.md
└── evals/
    ├── README.md
    ├── benchmark.md
    ├── dataset/
    └── red-team/
```

## 使用模式

- `light`：只修明显 AI 味，尽量不动结构。
- `standard`：默认；重构模板化表达、节奏和连接方式。
- `deep`：两轮编辑，再做医学和 Voice 审稿。
- `audit`：只诊断，不重写。

## Custom Voice

xiaoyibao-humanizer 不要求所有用户都使用 Sam Voice。可以创建自己的 Voice Profile：

1. 收集 5–10 篇本人真实写作；
2. 放入本地 Voice Corpus；
3. 分析稳定的语气、句式、节奏、词汇和判断方式；
4. 创建 `references/voice-yourname.md`；
5. 由作者人工校正；
6. 在改写时明确指定该 Voice；
7. 使用盲测重新运行 Benchmark。

Voice Profile 描述“作者如何表达”，不是提供固定文章模板。

示例：

```text
/humanize --voice sam
/humanize --voice my-voice
/humanize --voice community
```

如果指定的 Voice 文件不存在，Skill 会提示创建，不会默默套用 Sam 风格。

## 推荐测试方法

不要只看 AI detector。第一轮建立并冻结 20 篇 Benchmark：

- 中文医学科普 5 篇；
- 中文患者／社区文章 5 篇；
- 中文一般文章 5 篇；
- 英文文章 5 篇。

每篇做：

```text
A 原文
B 普通 Humanizer
C Xiaoyibao Humanizer
D 真人编辑
```

盲测自然度、作者感、医学准确性、证据校准、恐吓倾向、意义保留等指标。

特别加入真人文章做 Human Preservation Test，防止 Humanizer 把真正的人类文字也改成统一模板。

## 核心原则

1. 事实不可动。
2. 证据等级不可升级。
3. 不伪造个人经历、专家观点或引用。
4. 不用恐吓提高注意力。
5. 不制造虚假希望。
6. 不为了 AI detector 而牺牲自然度和准确性。
7. 尊重读者，把复杂问题讲清楚，而不是替读者制造情绪。
