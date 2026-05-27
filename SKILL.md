---
name: research-paper-reading
description: Top-level entry for academic paper reading. Auto-triggers when user mentions reading / summarizing / understanding a paper, provides an arxiv URL or ID, or asks about a paper's method / math / results. Routes to sub-skill skills/read-paper/ for the main pipeline (LaTeX ingest → Chinese note + 12-slide .pptx). Math-bearing answers always go to <CWD>/<paper>/qa.md (rendered via VSCode markdown preview because sidebars don't render LaTeX). Three reading modes: Skim / Core (predict-then-verify) / Teach (default).
---

# Research / 读 Paper 技能集

这是一个**技能集**（不是单个技能）。顶层负责路由和约定输出方式，具体能力挂在 `skills/` 下的子技能里。

当前阶段：**框架已搭好，子技能尚未建立。**

---

## 唯一不可妥协的约定：数学输出走文件

Claude 侧边栏（CLI / VSCode 插件）**不渲染 LaTeX**。所以：

- 任何**包含数学公式**的回答，**不要只停在聊天里**，要写进用户在 VSCode 里打开的 markdown 文件。
- 行内公式用 `$...$`，独立公式用 `$$...$$`。
- 纯文字、不带公式的简短回答可以直接在聊天里说，不必动文件。

## 文件契约：每篇 paper 一个文件夹，三件套

读一篇 paper 默认在它的目录下产出三个文件（旁支只 Skim 的可省 guide.md）：

| 文件 | 性质 | 用途 |
|---|---|---|
| `guide.md` | **稳定主讲稿**，一次写完后基本不动 | Teach mode 下的核心产物——我提取重点 + 教学，用户读这个不读原文 |
| `qa.md` | **滚动追加的 Q&A 日志** | 用户问题 / 我的展开回答，公式都在这（`$...$` / `$$...$$`） |
| `paper-card.md` | **耐久卡片**，跨 session 累积 | 脊椎、批判要点、Connect。模板见 `skills/read-paper/templates/paper-card.md` |

### qa.md 的写入方式（默认：追加）

`qa.md` 是一个**滚动累积**的工作文件，不是每次覆盖。每次回答**追加**一个新段落块：

```markdown
---

## <用户的问题 / 主题>   <!-- 简短标题 -->
<!-- YYYY-MM-DD -->

<回答正文：公式用 $...$ / $$...$$，可以有推导、图示、要点 -->
```

- 用 `---` 分隔每次问答，方便在预览里滚动。
- 既是"问答记录"，也是"教学页"——该展开讲透就展开，公式该写就写。
- **写之前不读不删旧内容**（追加语义），除非用户明确说"重写这段 / 清空"。

### qa.md 的第一条 entry 默认是「符号速查表」

实际跑下来，**进任何内容前先把这篇 paper 用到的所有数学符号一次性表格化**是个非常稳的开头。包括：单步核心量（$o, a, l, o'$ 之类）、空间集合（$O, A, L$）、概率符号（$p, \mathcal{D}, \sim, \mathbb{E}$）、loss 项、各种 metric 里的符号、常用缩写。**先建术语共识，再讲内容**。

---

## 子技能

### `skills/read-paper/` — 读论文方法论（v1，自建，用户会迭代）
**三档模式**：Skim（旁支三行裁决）/ Core（核心领域「先赌后验」深读）/ Teach（讲解模式——Claude 出主讲稿，用户不读原文，问题进 qa.md）。承重数学进 qa.md，每篇核心论文产出一张 paper card。内含 `references/critique-rubric.md`（批判 rubric）和 `templates/paper-card.md`。**每个 session 开头用户会给至少一篇论文链接，先定档。**

### `skills/ml-paper-writing/` — 写论文（整包搬自 Orchestra，原样）
覆盖全英文论文写作全流程 + 各会议 LaTeX 模板。对本用户最关键的是 `references/writing-guide.md`（专治口语化：Gopen & Swan / Perez / Lipton / Steinhardt 的规范化改写）。
⚠️ **坑**：这个 skill 默认想"从头代写整篇论文"。本用户的需求是**改自己写的稿、纠正口语化**——用它时要主动掰向 writing-guide 的改写规则，别让它从零 ghostwrite。

### 未来可能再加（尚未建，别假设存在）
- 相关工作 / 文献脉络梳理
- 概念教学页生成（独立于某篇论文的主题讲解）
- **`read-industry-paper/`**：读公司/工业 paper 时需要的元区分——**paper 描述的设计 ≠ codebase 实际实现**。需要显式把 "paper claims X" / "codebase shows Y" / "README says Z" 分开标 source。数字优先信 codebase，设计 intent 优先信 paper。**列出"paper 有但 code 没"的 gap 清单给用户带去问 CTO**。**关键约束**：
  - **发现 paper vs code 差异时，先假设是版本差（v0/v0.1）而不是矛盾**。industry repo 经常多版本并存，公开 codebase 不一定对应 paper 那一版。"先核版本号，再谈对不对得上"——把"确认版本对齐"作为 Tier 0 问题，没这个其他问题都不用问。
  - **当用户是 paper 所在公司的员工/实习生**：措辞从"借鉴 / 偷 idea / steal"换成"内部 build on / 复用 / extend 自己的工作"。语义上跟读外部 paper 完全不同——他不是 outsider 在评判，是 insider 在熟悉自己公司的 vision。

---

## 目录结构

```
research skills/
├── SKILL.md          # 本文件：总入口 + 输出约定
├── skills/           # 子技能（现为空）
├── templates/        # 模板，如 qa.template.md
└── references/       # 共享参考资料（读 paper 方法论、LaTeX 速查等）
```
