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

## 文件契约：每篇 paper 一个文件夹，**三件套**(v1.3：slides 按需,无 Connect)

读一篇 paper 默认在它的目录下产出**三件套**：

| 文件 | 角色 | 用户怎么用 |
|---|---|---|
| `note.md` | **事无巨细的 PDF → markdown 完整转写**（faithful，中文为主） | **主要学习材料**——他打开 VSCode 预览读 note，不读 PDF |
| `qa.md` | **默认只有 Q1 = 符号 / 公式 / 缩写对照表**，其他空 | 读 note 时 split-view 挂一边查符号；后续追问 Q2+ 才追加 |
| `paper-card.md` | **学完之后查漏补缺的对照卡**（canonical 1 屏，5 节） | 读完 note 凭记忆复述，翻这张卡找漏点 |
| `slides.pptx` | 12 页幻灯片 | **默认不产**；用户明确要求 "要 slides / 出幻灯片" 时才生成 |

**v1.1 的 `guide.md` 在 v1.2 已废**——它的"主讲稿"角色拆给了 note(完整内容) + paper-card(opinionated 提炼)。
**v1.3 在 v1.2 基础上**：移除 paper-card §5 Connect 段；slides 从默认产物挪到按需产物。

### 三件分得这么开的原因

| 问题 | 答案在哪 |
|---|---|
| paper 第 X 节第 Y 段说了什么？ | **note.md**（完整转写，跟随 paper 章节结构） |
| 公式里 $\alpha$ 是什么意思？ | **qa.md** Q1 符号表 |
| 读完该掌握的 K 件事？ | **paper-card.md** §2 |
| 这篇最该被批判的点？ | **paper-card.md** §4 |
| 这篇跟我之前读的 X paper 怎么 connect？ | **不主动写**(v1.3 移除)；用户问才答,进 qa.md 作 Q&A |

详细 schema：见 `skills/read-paper/references/note_schema.md` / `qa_schema.md` / `paper-card_schema.md`。

### qa.md 默认就 Q1，后续 Q2+ 才追加（v1.2 重订）

之前 v1.1 把 qa.md 当滚动 Q&A 日志，**第一条 entry 默认是符号速查表**。
v1.2 收窄：**默认就只有这一条**，其他都不写。用户后续在 chat 里追问时,answer 才作为 Q2+ 追加。

格式：

```markdown
---

## Q<n> — <用户问题的简短标题>
<!-- YYYY-MM-DD -->

<回答正文：公式用 $...$ / $$...$$，可以有推导、图示、要点 -->
```

- 用 `---` 分隔每次问答。
- **追加语义**——写之前不读不删旧内容，除非用户明说"重写这段 / 清空"。
- **agent 不 proactive 加 Q2+**，只在用户追问时加。

---

## 子技能

### `skills/read-paper/` — 读论文方法论（v1.3，自建，用户会迭代）
**三档模式**：Skim（旁支三行裁决，**不写文件**）/ Core（核心领域「先赌后验」深读，对话进 qa，押错落 paper-card）/ Teach（默认；agent 出 note + qa Q1 + paper-card，用户读 note 不读原文，自检靠 paper-card）。**承重数学进 note.md（在原文章节里）；符号查询表进 qa.md（Q1）；opinionated 评价进 paper-card.md（5 节，无 Connect）**。**Slides 默认不产**，用户明示要才跑。内含 `references/{note_schema,qa_schema,paper-card_schema,slide_schema,critique-rubric,output_layout}.md` 和 `templates/`。**每个 session 开头用户会给至少一篇论文链接，先定档。**

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
