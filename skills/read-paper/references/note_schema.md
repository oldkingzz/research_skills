# Note Schema —— 一篇 paper 一份 note.md 的硬约定

> 这是 agent 写 `note.md` 时**必须遵循的 schema**。每段都是 required,空着就别写这个 note。
> 主笔记**用中文**(母语 thinking 更深);**Key Takeaways 段强制中英双语**(英文为投稿/讨论复用)。
>
> 来源:抄 [DeepPaperNote](https://github.com/917Dhj/DeepPaperNote) 的 schema + 用户偏好 + Karpathy 三遍法。

## 文件位置

`<paper-dir>/note.md`,跟 `main.tex` / `figs/` / `slides.pptx` 同级。

## 顶层 schema

```markdown
---
arxiv_id: "1706.03762"
slug: "1706.03762-attention-is-all-you-need"
title: "<原文标题,strip latex 后>"
authors: "<逗号分隔>"
year: 2017
venue: ""               # NeurIPS / ICML / ICLR / Nature / arxiv preprint 等
url: "https://arxiv.org/abs/1706.03762"
read_date: "YYYY-MM-DD"
mode: "Teach"           # Skim | Core | Teach
tags: [tag1, tag2, ...]   # 你自己的 domain tag,如 [transformers, attention] 或 [biology, single-cell] 等
---

# <一句话标题:这篇到底干了什么>

> 标题应该是**你用自己的话**重述这篇 paper 的核心 contribution,不是原标题翻译。
> 不超过 20 个字。

## 0. TL;DR(一屏看完)

3-5 个 bullet:
- 核心 claim 一句话
- 它**新**的是什么(component 层面拆,不是整体)
- 它**借的**是什么
- 它的精度 / 延迟 / 数据效率定位
- 一句话裁决:值不值得我深挖

## 1. 研究问题 (Research Question)

paper 要解决的**抽象问题**是什么,不是它的具体技术 framing。
2-4 句。**这跟下面 Task Definition 是分开的两个 field**,不能混。

## 2. 任务定义 (Task Definition)

paper 在哪个**具体任务上验证**?(LIBERO / GemBench / real-robot / 自建 benchmark)
- benchmark 名 + 任务数
- input / output 形态(observation 模态 + action space 维度)
- 评测指标

## 3. 关键 idea (Spine —— 删掉就死的那一个想法)

**用你自己的话**写,1-3 句。不许直接抄 abstract。
**复述不出 = 没读懂,回到 main.tex 重读**。

## 4. 方法 (Method)

按"机制"组织,不按 paper section:

### 4.1 整体架构
ASCII / mermaid / 文字描述都行,但要让人 30 秒看懂数据流。

### 4.2 承重组件(逐个拆)
对每个承重组件:
- **它干什么** (1 句)
- **它新还是旧** (新 = paper 提的;旧 = 借的,标来源)
- **去掉会坏什么**(强迫自己想 ablation 角度)

### 4.3 承重数学
列承重公式(`$...$` / `$$...$$`),**详细推导不在这写**,在 qa.md。
- 损失函数 / 目标分布 / 关键操作
- 关键超参 + 默认值(从 paper Table 抄)

## 5. 实验 (Experiments)

### 5.1 关键数字(必须是表格)

| Method | benchmark 1 | benchmark 2 | ... |
|---|---|---|---|
| baseline A | ... | ... | ... |
| **this paper** | ... | ... | ... |

每个数字标 paper 里的位置(Table X / Fig Y)。

### 5.2 重要 ablation
列 paper 真做了的 ablation,跳过那些 paper 只 promise 不做的(标 ⚠️ "promised but not in paper")。

### 5.3 不在 paper 里但你想看的对比
你**期待 paper 有但没有**的 ablation —— 这些是审稿人会问的,也是你 paper #1 候选的潜在空位。

## 6. Limitations(诚实拆,paper 自己讲的 + 你看到的)

### Paper 自承
列 paper limitations 章节 / discussion 自己承认的。

### 你看到的(paper 没承认)
- 假设
- 不可推广的场景
- claim 跟 evidence 对不上的地方(🔴 / 🟠 / 🟡 三级)

## 7. 在版图里的位置 (Connect)

只在 mode = Core / Teach 才填(Skim 跳过):

- 这篇相对**你已知的什么**,是 **补充 / 矛盾 / 推进** 了什么?
- 它改变了你对 **什么** 的判断?
- 下一步它打开了什么问题?

## 8. Key Takeaways(强制中英双语)

3-5 条,**每条中文一行 + 英文一行**:

- **CN**: <用一句话总结这篇 paper 的关键 takeaway>
- **EN**: <one-line English version, usable in related-work / discussion>

—— 中英分行写,不要并行翻译;英文要 polish 到可以直接 paste 进 paper writing。

## 9. 我押错的 1%(可选,仅 Core/Teach)

> 如果用了「先赌后验」: 列 你**押错的关键点**。这些是真正值钱的。
> Teach mode: 列读完后**反直觉的发现**。

- ⚠️ 我原以为 ___,其实 ___。
- ⚠️ ...

## 10. Open Questions / 给 CTO 的问题(可选)

读完后**想问别人**的问题清单。
```

---

## 写作规则(硬约束)

1. **Grounding**:每个 claim 都能在 main.tex 找到出处,不能编。引数字带 "(Table X / Fig Y)"。
2. **Spine 段必须独立写**:不许从 abstract / intro 抄。是你自己的话。
3. **Key Takeaways 强制中英双语**,英文质量要 publishable(可直接进 paper / Slack 讨论)。
4. **数学不在这里展开**,展开放 `qa.md`(VSCode 预览渲染)。
5. **批判 ≥ 总结**:第 5.3 + 第 6 + 第 8 占的篇幅应该跟 1-4 节相当,不能只总结不批判。
6. **诚实标 mode**:Skim 可以省 1, 7, 9, 10;Core / Teach 必须全填。
