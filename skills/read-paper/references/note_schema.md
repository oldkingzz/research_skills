# note.html schema —— **事无巨细的 PDF 完整转写**(v1.4 起 HTML 载体)

> **v1.6(2026-09-04)适用范围**:本文件的 faithful 约束现在管的是 `note.html` 的**「原文对照」tab**。文件位置、frontmatter、"不该出现在 note 里的东西"里关于 paper-card / qa.md 的引用按 `note_schema_v2.md` §6 映射。


> 这是三件套(note / qa / paper-card)里**最厚**的一件,**也是最重要的一件**。
> 它是用户**主要的学习材料**:他在浏览器里打开 note.html 读,不读 PDF 原文。

## 核心约定(跟之前完全不一样,务必看清)

> **note ≠ 总结 / 提取 / 重组 / 主讲稿**。
> **note = 完整 faithful 的 PDF → markdown 转写**。
>
> "Faithful" 在这里是**强约束**:paper 里有的内容,note 里都要有;paper 里没的话术,note 里不要有。
>
> **唯一被允许去掉的东西**:致谢、参考文献本身(citation 出现位置保留,但 bib 整页跳过)、版权声明、扉页里的格式化样板。
>
> **其他全留**:每一个公式、每一个表格、每一个证明步骤、每一个图的 caption 和说明文本、每一个 footnote、每一个 algorithm box、每一个 limitation 段。

## 为什么这样设计

| 之前(v1.1 旧 note) | 现在(v1.2) |
|---|---|
| 结构化 10 section 的 summary 卡 | 完整 PDF 内容的 markdown 转写 |
| 重组按"理解曲线",可能 reorder paper 的章节 | **跟随 paper 自己的 section 顺序**,不 reorder |
| 强调"重要的留下,次要的省略" | **事无巨细,不省 token** |
| 用户对照原 PDF 看 note | **用户不看 PDF,只看 note** |

之所以这么改 —— **用户的目的是把 PDF 完整内化,不是先消化后看摘要**。AI 帮忙的地方是**翻译 + 整理为 markdown + 公式用 LaTeX 渲染 + 中文化**,**不是替用户做"什么重要"的取舍**。取舍由用户读 note 时自己做。

## 文件位置

`<paper-dir>/note.html`(v1.4 起代替 note.md),跟 `main.tex` / `figs/` / `qa.md` / `paper-card.md` / `slides.pptx` 同级。载体约定(单文件 + 内联 CSS + KaTeX CDN + sticky 目录 + 语义色块 + 紧凑表格)见 SKILL.md「v1.4」节;本文件其余 faithful 约束全部继续适用,frontmatter 信息改放页首 meta 卡。

## 必填:YAML frontmatter

```yaml
---
arxiv_id: "1706.03762"
slug: "1706.03762-attention-is-all-you-need"
title: "<原文标题,strip latex 后,完整>"
authors: "<逗号分隔,所有作者全列,不许 et al.>"
year: 2017
venue: ""
url: "https://arxiv.org/abs/1706.03762"
read_date: "YYYY-MM-DD"
mode: "Teach"
tags: [tag1, tag2, ...]
---
```

## 正文结构 —— **跟着 paper 自己的章节走**

note 的章节**镜像 paper 的 section 划分**,不是固定模板。例如 paper 有 `1 Introduction / 2 Background / 3 Method / 4 Experiments / 5 Discussion / 6 Conclusion`,note 里就是这 6 节;paper 有 7 节就 7 节。

**例外:** 在 paper 的 Section 1 之前,先加一段 `0. 元信息`,包括:
- arxiv 完整 abstract(中文翻译 + 原文 quote)
- paper 自己的关键词(如果有)
- 这篇的 keywords / area (你判断)

之后**每一节都要按 paper 顺序覆盖**,**每一个 subsection 不能跳**。

## 每节内的转写原则

### 1. 文字
- 用中文转写 paper 的核心句子,**保留逻辑结构**(不能跳 sentence)
- 关键术语第一次出现时**中英对照**:`World Action Model (WAM,世界动作模型)`
- 引用其他工作时**保留 citation**:`Vaswani et al. 2017 [12] 证明了 ...`
- paper 的强调(italics、bold)在 markdown 里保留

### 2. 公式
- **每一个公式都转写**,用 LaTeX(行内 `$...$` / 独立 `$$...$$`)
- 公式编号沿用 paper(`(1)`、`(2)` 等)
- 公式紧跟着的解释段也要 transcribe
- **不要省略推导步骤**,paper 里逐步给的公式,note 里也逐步给

### 3. 图表
- **每个 figure 必须出现**:用 `<img src="figs/<filename>">` 引用(filename 跟 `ingest.py` 抽出来的对应)
- **每个 figure 的 caption 完整翻译**
- **figure 的 inline 引用文字也保留**:"As shown in Figure 3, ..." → "如 Figure 3 所示,..."
- **table 整张转写为 markdown table**,**不能省**

### 4. 算法 / pseudocode
- algorithm box 用 ``` ``` 代码块包,**完整转写步骤**,可加中文注释

### 5. footnote
- paper 的 footnote 在 note 里**就近放**,用 `> [^1]: ...` 或者直接在原段落用括号说明,**不要漏**

### 6. 实验细节
- 所有 hyperparameter 表格、所有 ablation 表格、所有数据集说明 **完整转写**
- "Implementation details" 段是常见的"看似不重要其实重要"的段,**绝对不要省**

## 不该出现在 note 里的东西

- **你的总结 / 你的评价 / 你的批判** —— 这些走 `paper-card.md`,**不在 note 里**
- **你给用户的"建议"或"提问"** —— note 是 paper 本身的转写,不是讲解材料
- **公式的"直观解释"或"举例"** —— 除非 paper 原文里有,否则不加(你额外的解释会污染 faithful 性)
- **"为什么这样设计"的推测** —— paper 自己讲就转写,paper 没讲就不要补
- **跨 paper 的 connect** —— **v1.3 不主动做**(无论 note 还是 paper-card);用户主动问就 qa.md 答

## 长度预期

一篇 30 页 ML paper → note.html 正文通常 **8,000-25,000 字符**(中文,不含 CSS/骨架)。
**不要担心长度**。用户已明确:**事无巨细 > token 成本**。

## 写完 self-check checklist

写完 note.html 后,agent 在 chat 里**简单 report 这 5 项**:
- [ ] paper 的所有 section + subsection 都覆盖了
- [ ] paper 的所有 equation 都转写了(数一下)
- [ ] paper 的所有 table 都转写了
- [ ] paper 的所有 figure 都用 `![](figs/...)` 引用了
- [ ] note 里**没有出现** "I think" / "我认为" / "我觉得" / "依我看" 这种 agent 主观评价
