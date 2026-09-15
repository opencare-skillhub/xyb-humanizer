# 冻结 Benchmark 数据集

第一轮目标为 20 篇：

| 前缀 | 类型 | 数量 |
| --- | --- | ---: |
| ZH-MED | 中文医学科普 | 5 |
| ZH-COM | 中文患者／社区 | 5 |
| ZH-GEN | 中文一般文章 | 5 |
| EN | 英文医学或一般文章 | 5 |

每篇目录：

```text
ZH-MED-001/
├── A.txt
├── B.txt
├── C.txt
└── D.txt
```

- A 保留原文；
- B 记录普通 Humanizer 输出；
- C 使用冻结的 xiaoyibao-humanizer v0.3；
- D 只接受真实人工编辑；没有则留空并在 manifest 标记。

先把原文放入、补全 `manifest.json`，人工确认后把 `frozen` 改为 `true`。冻结后不得替换文章、根据结果挑选文章或修改 v0.3。
