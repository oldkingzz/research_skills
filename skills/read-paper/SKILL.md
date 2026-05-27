---
name: read-paper
description: Use whenever the user wants to read / summarize / understand / critique an academic paper. Auto-triggers on arxiv URLs (arxiv.org/abs/, arxiv.org/pdf/), arxiv IDs (e.g. 1706.03762), DOIs, paper titles, or natural-language asks like "读这篇 / 看一下 / summarize / explain this paper / 解释一下这篇". Pipeline (Teach mode = default): pulls arxiv LaTeX source via uv-runnable scripts/ingest.py, writes Chinese note.md with bilingual CN+EN Key Takeaways per references/note_schema.md, generates 12-slide .pptx via render_slides.py per references/slide_schema.md, updates a global queue.md. Outputs land in <CWD>/<arxiv-id-slug>/. Three modes available: Skim (3-line verdict, no artifacts), Core (predict-then-verify deep read + paper-card), Teach (default — Claude produces guide + slides, user reads + asks questions). LaTeX source ONLY (no PDF parsing), .pptx output ONLY (no PDF). Cross-platform: same SKILL.md works in Claude Code / Codex CLI / Cursor.
---

# read-paper —「先赌后验」式深读

## 这个 skill 想解决的真问题

用户能在 AI 帮助下 5 分钟"看懂"一篇论文，但那是 **gist 的错觉**：能复述结论，不能重建推理、不能批判、不能在自己领域里接着往下想。同时他觉得细节抓不住、而且 99% 细节不重要——**对**，但问题在于他没有筛子去找那决定性的 1%。

**本 skill 的唯一核心机制：先赌后验（predict-then-verify）。**

> 不要直接把答案喂给用户。在每个承重环节，先让用户押一个答案，再揭晓。
> **用户押错的地方 = 对他个人真正重要的那 1%。押对的，直接跳过。**

这一个机制同时干三件事：① 刺破"我懂了"的错觉；② 把"哪 1% 值得较真"自动个性化筛出来（= 他的认知和论文现实分歧的地方）；③ 把通读变成一连串小赌注，高效。

记住：你（Claude）默认**不是讲解员**，是**发牌的庄家 + 事后复盘的对手**。只有在"快速过"档（见下）才允许直接喂 gist。

---

## 三档模式：开读前先定档

| 档位 | 何时用 | 你怎么做 | 产物 |
|---|---|---|---|
| **快速过（Skim）** | 旁支领域、出于兴趣、或先判断"值不值得深读" | 允许直接给 gist。给三行裁决：①核心 claim 一句话 ②对用户可能有什么用 ③要不要深读 Y/N | 三行裁决，不进 card |
| **核心深读（Core）** | 用户想真"读懂"+ 自己批判 | 跑下面的「先赌后验」全流程，绝不一上来给完整讲解 | qa.md 累积 + 一张 paper card |
| **讲解模式（Teach）** | 用户**不想自己读原文**，要 Claude 出主讲稿、做提取，自己只问问题 | 通读全文 → 出 `guide.md`（稳定主讲稿，按"理解曲线"重排）→ 用户在 chat 问问题，追加到 `qa.md`（公式 LaTeX 走 VSCode 预览） | `guide.md` + `qa.md` + 一张 paper card |

每个 session 开头用户给论文链接时，**先问一句这篇走哪档**（或自己根据是不是他核心领域判断，并说出判断让他纠正）。

**Teach 和 Core 的根本区别**：Core 是「**反错觉**」（先押后揭，找用户自己的 1%），Teach 是「**省时间**」（用户信任 Claude 的提取，把精力留给问问题和验证）。**别把两者混了** —— Teach mode 下不要硬塞先赌后验，Core mode 下不要直接喂讲解。哪个模式由用户当场选 / 你判断后说出来让他确认。

---

## 核心深读流程（Core）

不是线性"逐节读"，是围绕承重点的几轮下注。

### 0. 取全文，自己先读
先把论文全文取来（链接 / arXiv / PDF）自己通读，定位承重结构。**不要让用户先读**——他押注前不该被原文剧透到细节，但你要心里有数。

### 1. 立框（Frame）——给用户押第一注
不讲内容，先抛三个问题让用户答（凭标题/摘要/他已有的领域知识）：
- 这篇要解决的问题是什么？
- 它声称的核心贡献，一句话？
- **要让这个贡献"重要"，什么必须为真？**（把它放进用户的领域坐标系）

用户答完，你再对照原文揭晓。**分歧处记进 card。**

### 2. 找脊椎（Spine）——最关键的一注
全篇只有一个承重想法：**删掉它论文就死。** 让用户先猜"这篇的脊椎是哪一句话/哪个机制"，再揭晓。
- 揭晓后让用户用**自己的话**把脊椎复述一遍，不许看原文 → 这是最硬的反错觉检查。复述不出 = 没真懂，回到这里。

### 3. 数学（→ 写进 qa.md）
先分类，别全推：
- **承重公式**（定义了方法本身、改了它结论就变）→ 深入，写进 qa.md。
- **装饰公式**（标准 loss、众所周知的定义、纯记号）→ 一句话带过。

对每个承重公式，跑先赌后验：
- 揭晓推导前，让用户押："这一项是干嘛的？把它去掉/改了会坏什么？"
- 然后把讲解 + 推导写进 `qa.md`，用 `$...$` / `$$...$$`（VSCode 预览渲染）。格式见 `templates/` 里 qa 段落约定。
- 押错的那一项，在 qa.md 里用一行标出"⚠️ 我原以为…，其实…"——这是他的 1%。

### 4. 证据诚实度（Evidence）——批判性评估
这步用 `references/critique-rubric.md`（从 rigor-reviewer 抠出来的 6 维 rubric 的精简版，已改成直接套原始论文）。重点不是给分，是找"claim 和证据对不对得上":
- 它**实际测了**什么 vs. 它**声称**了什么？范围有没有超？
- baseline 公不公平？有没有该做没做的消融？
- 那个"可能反过来"的关键实验，结果站得住吗？
先让用户押"你觉得这篇最可能被审稿人攻击的点是哪？"，再用 rubric 对一遍。

### 5. 边界（Boundaries）
假设、失效场景、它"恰好没测"的东西。一句话押 + 揭晓。

### 6. 接线（Connect）——只有核心领域做，且最重要
这步是"积累"的全部意义所在：
- 这篇相对你**已知的**那条线，是补充 / 矛盾 / 推进了哪一点？
- 它改变了你对这个领域的什么判断？
- 下一步它打开了什么问题？
写进 card 的 "Connect" 区。card 跨论文累积 = 你这个领域的活地图。

---

## 产物与文件契约

每篇 paper 默认产出三件套（旁支只 Skim 的可省 guide.md）：

- **`guide.md`**（仅 Teach mode 必产）：稳定主讲稿，**通读 paper 后一次性写完**，按"理解曲线"重排（不是逐节复述）。结构建议：TL;DR → 领域背景 → 数学定义 → 架构/方法 → 实验数据 → 批判性评价。**写完基本不动**，除非用户要求重写某段。
- **`qa.md`**：用户在 VSCode 开着的滚动文件，承重数学的讲解/推导追加进去（`$...$`/`$$...$$`）。追加语义，`---` 分隔，带日期。不读不删旧内容除非用户明说。**第一条 entry 默认是「符号速查表」**（一次性表格化 paper 用到的所有数学符号 + 缩写，先建术语共识再讲内容）。
- **`paper-card.md`**：每篇核心论文一张一屏的耐久笔记，模板见 `templates/paper-card.md`。脊椎、押错的 1%、批判要点、Connect 都落在这。card 是跨 session 积累的，别每次从零开始。
- 放哪：默认跟着用户当前在读的论文目录走；用户没指定就问一次。

---

## 执行 workflow：Teach mode 的自动化 pipeline（plug-and-play）

> 这一节是 v1.1 新增。给在 Cursor / Codex CLI / Claude Code 里运行的 agent 用的「跑」的部分。
> 跨平台:三个 platform 都读同一份 `SKILL.md` + `scripts/`,行为应一致。

### 触发

用户在 chat 自然说 "读这篇 https://arxiv.org/abs/..." / "看下 <arxiv-id>" / "summarize this paper: <url>" / "解释一下这篇" 都视为同一意图。**现代 LLM (Claude Opus 4.x / GPT-5.x / Gemini 2.x) 基于本 SKILL.md description 自动 match 用户意图,不需要 explicit skill 名**。Slash 风格(`/arxiv <id>`、`$read-paper`)也兼容,但不强求。

### 工作流(7 步,严格顺序)

**Step 1 — Ingest LaTeX source**

执行:`uv run <SKILL_DIR>/scripts/ingest.py <arxiv-id-or-url> --out-dir <CWD>`

约束:
- **只用 arxiv e-print(LaTeX source),不要碰 PDF**。脚本会自动从 `https://arxiv.org/e-print/<id>` 下载 tar.gz、解压、扁平化 `\input{}` / `\include{}`。
- 失败(无 source / 非 arxiv URL)直接报错给用户,**不要 fallback 到 PDF**。

输出:
- `<CWD>/<slug>/main.tex` (flattened)
- `<CWD>/<slug>/figs/` (png/jpg + pdf 已转 png)
- `<CWD>/<slug>/metadata.json`

**Step 2 — Update queue (mark READING)**

执行:`uv run <SKILL_DIR>/scripts/update_queue.py <CWD>/queue.md add <slug> "<title>" <arxiv_id>`
然后:`uv run <SKILL_DIR>/scripts/update_queue.py <CWD>/queue.md mark <slug> READING`

(如果 queue.md 不存在,update_queue.py 会自动 init。)

**Step 3 — Read main.tex (you, the agent)**

读 `<CWD>/<slug>/main.tex`。**严格 ground 在文本里**:每个 claim 都能从 .tex 找到出处,不能编。

**Step 4 — Write note.md**

按 `<SKILL_DIR>/references/note_schema.md` 的 schema 写,模板在 `<SKILL_DIR>/templates/note.template.md`。

硬约束:
- **中文主笔记 + Key Takeaways 强制中英双语**
- Spine 段必须你自己的话,不许 abstract 直抄
- Limitations 双拆(paper 自承 + 你看到的,带 🔴/🟠/🟡 严重度)
- 5.3 (你期待 paper 有但没的对比)必填

**Step 5 — Write outline.json**

按 `<SKILL_DIR>/references/slide_schema.md`,**默认 11 个 content slide(加 title = 12)**。

写之前:
- `ls <CWD>/<slug>/figs/` 看有什么图可以引用
- 至少 3 个 slide 配 figure

**Step 6 — Render slides.pptx**

执行:`uv run <SKILL_DIR>/scripts/render_slides.py <CWD>/<slug>/`

输出 `<CWD>/<slug>/slides.pptx`(纯 .pptx,**永远不产 PDF**)。

**Step 7 — Mark DONE + report**

执行:`uv run <SKILL_DIR>/scripts/update_queue.py <CWD>/queue.md mark <slug> DONE`

在 chat 给用户报:
- ✓ slug
- 笔记:`<paths>/note.md`
- 幻灯片:`<paths>/slides.pptx`(12 页,VSCode 里 cmd+click 打开)
- 一句话 highlight(从 note 的 takeaways 抽一句)
- 推荐下一篇:queue.md 里下一个 TODO

### 模式映射

| Mode | 跑 Step 几 |
|---|---|
| **Skim** | 1, 3(只读不写 note), 在 chat 给三行裁决 + Step 2/7 标 DONE |
| **Core** | 1, 2, 跑「先赌后验」流程 + 写 qa.md + paper-card.md, 不一定生成 slides |
| **Teach** | **1-7 全跑** |

### 决策点(开干前你要明确)

- 用户给的是 arxiv ID / URL 吗?不是的话(给了本地 PDF):**先报错让用户给 arxiv ID**,不接受 PDF 输入(per LaTeX-only policy)
- 用户当前 CWD 是不是合适的 paper 工作根?不确定就问一句
- 用户的 mode 选 Skim / Core / Teach?Teach 是 default,但如果是旁支领域考虑 Skim
- 这篇的目标语言(note 是中文,但用户偶尔可能要英文)— 默认中文,只在用户明示时换

### 错误处理

| 错误 | 处理 |
|---|---|
| arxiv 没 source | 报错 + 让用户去 arxiv 找 paper 是不是 withdrawn / 没 source / 是 paper review 等 |
| LaTeX 扁平化失败(循环 \input 等) | ingest 自动 fallback 到不扁平化(用 source/ 里的多个 .tex 文件) |
| 没 figs | outline 里就别配 figure,deck 全是文字也行 |
| pptx 渲染失败 | 检查 outline.json 格式;让用户看 stderr,**不要自动重试** |
| queue.md 冲突 | update_queue 自动检查重复,不会覆盖 |

### 跨平台兼容(Cursor / Codex / Claude Code)

- **同一份 SKILL.md** 在三个 platform 都生效
- **同一份 scripts/** 都用 `uv run` 跑(PEP 723 inline metadata 自带依赖,无需预装 venv)
- **同一份 references/** 是 schema 真源
- Codex CLI:用户 `$read-paper <url>` 或 `/skills` 选
- Claude Code:用户 `/skills read-paper <url>` 或 description 自动匹配
- Cursor:用户在 chat 说自然语言或 `@read-paper`

不同 platform 的差异**不应该需要 conditional code** —— 全部约定在这份 SKILL.md 里。

---

## 给 Claude 的硬规矩

1. **先确定档位**（Skim / Core / Teach），不要默认上 Core。问一句或者自己判断说出来让用户确认。
2. **Core 模式下「先赌后验」是默认**。忍住"我直接讲给你听"的冲动——那正是制造错觉的机器。**Teach 模式下反过来**：用户明确不想自己读，硬塞先赌后验是不尊重 user intent。
3. 用户押对的就快速跳过（Core），别浪费他时间复述他已经会的。
4. 押错处必须显式标出来并落进 card（Core），那是这套方法论的全部价值。
5. 数学一律进 qa.md，不在聊天里堆公式。**qa.md 第一条默认是符号速查表**。
6. **鼓励跨领域类比提问**。当用户问 "这跟 X 一样吗?"（X 来自他熟悉的另一个领域），认真对照、把共享根 + 关键差异都列清楚——这种"跨领域看 pattern"的直觉很值钱，主动 prompt 用户用上自己的旧知识。
7. 这是 **v1 草稿，用户会在上面改**。用的过程中如果发现某步骤别扭/多余，主动提出来让他调，不要默默将就。**而且：发现的改进应该 fold 回这份 SKILL.md，不要只留在 memory 里**——memory 是 workaround，SKILL.md 才是 durable home。
