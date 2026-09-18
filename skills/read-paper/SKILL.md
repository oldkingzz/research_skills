---
name: read-paper
description: Use whenever the user wants to read / summarize / understand / critique an academic paper. Auto-triggers on arxiv URLs (arxiv.org/abs/, arxiv.org/pdf/), arxiv IDs (e.g. 1706.03762), DOIs, paper titles, or natural-language asks like "读这篇 / 看一下 / summarize / explain this paper / 解释一下这篇". v1.6 (2026-09-04): each paper produces ONE user-readable file, <paper-dir>/note.html (template templates/note_v2.html, contract references/note_schema_v2.md), with five parts: (a) 一屏卡 one-screen card, two columns — left = agent reference (spine / four-grid / boundaries / verdict), right = the user's own version in localStorage textareas; right column filled = paper closed; (b) auto-generated Q index; (c) tab 讲义 = beginner-first lecture (full lesson for out-of-field papers, lesson-0 + section digests for home-field papers); (d) tab 原文对照 = exhaustive faithful Chinese transcription following the paper's own section order, every equation/table/figure/footnote retained; (e) tab 夯实 = standing retrieval drill (≤10 items home-field, 20–35 out-of-field: recall cards carrying the old paper-card must-know list, true/false misconception items, must-answer questions, per-lesson fog locator); (f) tab 符号表 = symbol/abbreviation table. User questions asked in chat are inserted as numbered Q blocks (global ask-order numbering) at the end of the relevant lesson/section before its <!-- Q-INSERT --> marker; the Q index rebuilds itself. v1.7 (2026-09-12): the one-screen card gains three agent-only rows — 脉络 lineage (origin / limits of prior practice / the disease it fixes / move and cost / where it leads, each item tagged with its source), 三镜 three-lens verdict (Robotics: does it work on a concrete system; AI: where the hard part is and what measurable quantity the paper turned it into; ML: why the method holds — each marked hard/soft/empty, plus which lens the paper mainly stands on and which is empty), and 钉子候选 nail candidate (a concrete question in the empty lens, who can fill it, how to verify; always marked candidate). The lecture tab opens with a mandatory 第 -1 课 lineage lesson with an inline lineage SVG. Cross-paper connections are now made by the agent but every link is tagged [原句]/[引用数据]/[agent 判断]; never link to the user's employer's papers. Step 3.5 fetches references/citations from the Semantic Scholar API into lineage.json (network allowed). qa.md / paper-card.md / lesson.html / drill.html are no longer generated (legacy schemas still govern the corresponding parts). Slides (.pptx) only on explicit request. LaTeX source ONLY (no PDF parsing). Three reading modes: Skim (3-line verdict, no files) / Core (predict-then-verify dialogue, answers land as Q blocks) / Teach (default). Cross-platform: same SKILL.md works in Claude Code / Codex CLI / Cursor.
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
| **核心深读（Core）** | 用户想真"读懂"+ 自己批判 | 跑下面的「先赌后验」全流程，绝不一上来给完整讲解 | `note.html`(v1.6 单文件);先赌后验的问答落 Q 块,押错点落一屏卡「边界」 |
| **讲解模式（Teach）** | 用户**不想自己读原文**，要 Claude 出主讲稿、做提取，自己只问问题 | 通读全文 → 出 `note.html`(讲义 tab 主读;跨领域为完整 lesson)→ 用户在 chat 问问题,agent 插为 Q 块 | `note.html`(v1.6 单文件) |

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

### 3. 数学（→ 写进 note.html 的 Q 块 / 讲义）
先分类，别全推：
- **承重公式**（定义了方法本身、改了它结论就变）→ 深入，写进 note.html(讲义推导框或 Q 块)。
- **装饰公式**（标准 loss、众所周知的定义、纯记号）→ 一句话带过。

对每个承重公式，跑先赌后验：
- 揭晓推导前，让用户押："这一项是干嘛的？把它去掉/改了会坏什么？"
- 然后把讲解 + 推导作为 Q 块插进 note.html 引发问题的位置正后面(格式见 `references/note_schema_v2.md` §3),用 `$...$` / `$$...$$`(KaTeX)。
- 押错的那一项，在该 Q 块里用一行标出"⚠️ 我原以为…，其实…"，并同步落到一屏卡左栏「边界」——这是他的 1%。

### 4. 证据诚实度（Evidence）——批判性评估
这步用 `references/critique-rubric.md`（从 rigor-reviewer 抠出来的 6 维 rubric 的精简版，已改成直接套原始论文）。重点不是给分，是找"claim 和证据对不对得上":
- 它**实际测了**什么 vs. 它**声称**了什么？范围有没有超？
- baseline 公不公平？有没有该做没做的消融？
- 那个"可能反过来"的关键实验，结果站得住吗？
先让用户押"你觉得这篇最可能被审稿人攻击的点是哪？"，再用 rubric 对一遍。

### 5. 边界（Boundaries）
假设、失效场景、它"恰好没测"的东西。一句话押 + 揭晓。

<!-- v1.3：原 step 6「接线 / Connect」已移除。跨 paper connect 是用户的认知工作,agent 不主动做。
     用户在 chat 里主动问 "这跟 X paper 怎么 connect" 时,答案作为 Q 块插进 note.html,不进一屏卡。 -->

---

## 产物与文件契约(v1.6:单文件 note.html;三件套并入)

**每篇 paper 只产一个用户可读文件:`<paper-dir>/note.html`。** 模板 `templates/note_v2.html`,结构与编辑规则见 `references/note_schema_v2.md`。旧三件套(note / qa / paper-card)、v1.5 的 lesson.html、2026-09-02 临时的 drill.html **不再作为独立文件生成**;它们的内容标准分别并入 note.html 的五个部分:

| note.html 的部分 | 来自旧的哪件 | 内容标准仍看 |
|---|---|---|
| **一屏卡**(两栏:左 agent 参考版 / 右 用户自己写) | paper-card §1 脊椎、§4 批判(→边界)、§5 裁决,+ 本线四格地图 | `paper-card_schema.md` |
| **Q 索引**(JS 自动生成) | qa.md 的目录功能 | `note_schema_v2.md` §3 |
| **讲义 tab** | lesson.html | `lesson_schema.md` |
| **原文对照 tab** | note.html v1.4 faithful 转写 | `note_schema.md` |
| **夯实 tab**(常设,分档) | drill.html + paper-card §2 K 件事、§3 承重数学(答案面) | `note_schema_v2.md` §4 |
| **符号表 tab** | qa.md Q1 | `qa_schema.md` Q1 部分 |
| **Q 块**(插在各节末尾) | qa.md Q2+ | `note_schema_v2.md` §3 |
| `slides.pptx` | — | 默认不产;用户明示要 slides 才跑 Step 8 |

### 档位决定讲义与夯实的厚度

| | 跨领域 paper | 主场 paper |
|---|---|---|
| 讲义 tab | 完整 lesson(理解曲线排课、一个 running example、先例子后定义、推导代数字),**主读** | 第 0 课 + 各节要点导读;原文 tab **主读** |
| 夯实 tab | 20–35 项(提取卡 + 判断题 + 必答题 + 雾定位) | ≤10 项(提取卡 + 1 道必答题 + 雾定位) |

主场 / 跨领域由用户画像(memory)与当场判断决定,不确定问一句。

### 三条硬规则(v1.6 新增)

1. **收尾 = 一屏卡右栏四行由用户自己填满。** agent 不代填;用户口述时原样写入并标注日期,不润色。
2. **Q 块的编号、位置、完整度**:全局按提问顺序递增;**插在引发问题的那段 / 公式 / 框的正后面**(问题在哪冒出来就放哪;不针对具体位置的才放节末 `<!-- Q-INSERT: id -->` 标记前);详细度 ≥ chat;写后重读整文件核对 Q 号唯一、标记仍在、结构未破。
3. **写完必须截图验证**(桌面 1280 + 手机 390):标签切换、一屏卡两栏、Q 索引、公式(KaTeX 不支持 `\textsc`,用 `\mathrm`)、SVG 文字不重叠、无整页横向滚动。没有浏览器工具就明说。

### v1.7(2026-09-12):脉络与三镜(用户裁定三条:connect 解禁 / 允许联网拉引用 / 新三行全自动无右栏)

- 一屏卡七行:脊椎 · **脉络** · **三镜** · 四格 · 边界 · 裁决 · **钉子候选**。加粗三行 agent 全自动填、不留右栏;收尾仍按原四行。规则见 `references/note_schema_v2.md` §9。
- **v1.9(2026-09-18)研究主线文件与三盏灯分类法**:用户要求「maintain 一个文件,这个文件是我们的 research 主线……每次我要求你调用 subagent 搜的时候,你都需要记录进去,这将是我们的钉子所在」,并要求分类准则<b>必须包含「一次性点亮了三盏灯中的哪几盏」</b>。一个工作区只有一个主线文件(当前:`research-mainline.html`),固定六节:钉子当前表述与<b>版本历史</b>／分类准则／证据台账／检索日志／还空着什么／下一步。三盏灯 R 机器人(有人正为它付真实代价且有具体系统证据)、A 人工智能(把说不清的难点变成能算的量)、M 机器学习(给出机制:证明或能隔离因果的消融),<b>「一次性点亮」单独一栏</b>——删掉其中一盏对应的部分,另外两盏会不会跟着灭。**派检索代理时必须明确要求它找反面证据**——本轮就是靠这条发现钉子已被 2019 年的工作做过。**主线文件分两部分**：前半是给用户的结论，**硬约束一屏**，只放钉子一句话 / 三盏灯各靠什么亮 / 现在做哪三件事 / 必须记住的约束 / 版本表，不放出处链接与引用数；后半是给 agent 的台账，**不追求可读性，追求覆盖全**，用一条分隔线隔开并注明「你不用读」。**三盏灯的校准结果（实测，别凭印象说）**：RSS 2021–2025 十七位获奖者里真机 15/17、机制 3/17、「把模糊说法变成能算的量」≈0/17，**三盏灯买到的是能在跨系委员会前站住的选题，不是奖**；且 ML 暗的论文大多修不好、机器人暗的大多是能修而没修，**所以最便宜的三灯选题是把一个被整条线引用却从没上过硬件的现成定理搬到真机上**。另有一条提案阶段就能用的测试：**你提出的量若写不成你主张机制的推论，你有的就是两个贡献而不是一个**。详见 `references/research_mainline_schema.md`（§2 两部分结构、§8 校准结果、§9 agent 自己的 drift 清单）。
- **v1.8(2026-09-18)讲义课要能被拖动**:用户读第 4 课时说「云里雾里,核心问题在于我不理解这个实在干什么」,要求「大量例子 + 用上 HTML 的丰富特性 + 交互」,重写后评价「非常非常好」并要求其余各课全部照此重构。**一课的固定骨架八段**:本课要回答的问题 → 零符号的物理直觉 → 交互组件 → 易混概念辨析表 → 定义/定理 → **每步都写「为什么这么走」的推导** → 带真实数字走一遍 → 证据边界。**②必须在⑤之前**——用户卡住的根因几乎总是「先看到符号,没看到东西」。收口课加一块**证据强度分级板**(定理/隔离实验/相关观察/未验证,可筛选,每行带出处)。交互组件的判据、CSS 类白名单、JS 硬规矩(id 加课号前缀、单一 IIFE、不遮蔽外层辅助函数、SVG 文本不放 LaTeX、不测量布局)、**数值先在 node 里独立验过再写进页面**、以及用 headless Chrome 探针而非截图来验运行时,全部见 `references/lesson_interactive_schema.md`。
- **v1.7.1(2026-09-12)一屏卡是一张图**:七行压缩进 `card.json` → `uv run <SKILL_DIR>/scripts/card_svg.py card.json --out <paper-dir>/card.svg` → Chrome 出 `card.png`(2x)→ svg 内联进 note 顶部、点图开 png;七行全文进折叠区,用户四个作答框在图下。画布 860 宽、正文 14px,在 note 栏内 1:1 显示。画法与每格字数上限见 `references/card_image_schema.md`,超字数删字不缩字号。
- 讲义必有「第 -1 课·脉络课」(谱系 SVG + steelman 评审理由),放第 0 课之前。
- 夯实加两道脉络题、一道三镜题。
- **connect 规则改**:v1.3 的"不主动 connect"作废;现在主动连,但每条连线标 `[原句 Sec X]` / `[引用数据]` / `[agent 判断]`;仍不连用户在职公司的论文。
- Step 3.5:`uv run scripts/lineage.py <arxiv-id> --out <paper-dir>/lineage.json` 拉 Semantic Scholar 的 references / citations;失败就明说,来处只用原句。
- 动因:用户 09-12——"有锤子没钉子;读论文不能只为知识,要知道脉络、目的、修了什么弊病、为什么 best paper 级、用哪个社区的思路解的"。提案:`proposals/2026-09-12-lineage-three-lens.html`。

### 不迁移旧论文

已生成三件套的论文保持原样,从下一篇起用 v2。需要给旧论文补讲义 / 夯实时,顺手按 v2 重做整份 note.html,并把旧文件留在原处不删(用户决定何时清)。

### 历史(浓缩;完整理由在 git log)

- v1.2 把 note / qa / paper-card 拆开:note = faithful 转写,qa = 符号查询,paper-card = 自检对照。
- v1.3 去掉 paper-card §5 Connect(跨 paper 关联是用户的认知工作);slides 改按需。
- v1.4(2026-08-31)note 载体 .md → .html。
- v1.5(2026-09-01)跨领域加 lesson.html:faithful 转写隐含"读者在领域内",对新领域是符号墙。
- v1.6(2026-09-04)合并为单文件:实测 qa.md 无人写(问题与段落分离),paper-card 是 agent 写的、用户没有"自己写一遍"的位置导致"读完不知怎么收尾",lesson 与 note 双文件切换成本高。三个问题一个解:一个文件、讲义为主体、Q 插段落旁、卡片留一栏给用户。

放哪:默认跟着用户当前在读的论文目录走(`<CWD>/<slug>/`);用户没指定就问一次。

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

**Step 3.5 — Lineage(v1.7,允许联网)**

执行:`uv run <SKILL_DIR>/scripts/lineage.py <arxiv-id> --out <CWD>/<slug>/lineage.json`。取 Semantic Scholar 的 references 与 citations(各前 15,按被引排序)。再读 main.tex 的 related work 段,把两边都支持的上游 / 下游写进一屏卡「脉络」行与第 -1 课;每条标出处。API 失败:report 里写明,脉络只用原句。

**Step 3.6 — 录用与奖项核查(2026-09-14 用户要求:"你需要看看他是不是被 accept 了,是不是 best paper")**

执行:`uv run <SKILL_DIR>/scripts/venue.py <arxiv-id> --out <paper-dir>/venue.json`。它读 arXiv 备注栏(作者常写 "accepted to X")、journal_ref、Semantic Scholar 的 venue。API 限流(429)很常见,这时直接抓网页:arXiv abs 页、作者主页 / 实验室书目页、IEEE Xplore / OpenReview、会议 awards 页。奖项**只能靠搜**:按 `search_queries` 里的三条搜,再搜 `<会议或期刊> best paper award <年>`。
写进三处:`metadata.json` 的 `venue`(录用刊物 + 年 + DOI)和 `award`(`{"name","source"}`,没有就 `null`);一屏卡图元信息行「发表:… · 奖项:…」;report 里一句。
规则:**没有可点开的来源就不写奖项**;一手来源(IEEE RAS / 会议官网 / 作者主页)写"已确认",只有新闻稿或二手页面写"据 X 报道,待官方页确认";都没有写"未查到"。预印本状态写"arXiv 预印本,未查到录用"。

**Step 4 — Write note.html(v1.6 单文件:一屏卡 + Q 索引 + 四个 tab;v1.7 加脉络 / 三镜 / 钉子候选行与第 -1 课;v1.7.1 一屏卡为 card.svg 图,见 `references/card_image_schema.md`)**

从 `<SKILL_DIR>/templates/note_v2.html` 起手,按 `<SKILL_DIR>/references/note_schema_v2.md` 填五个部分。各部分的内容硬约束:
- **原文对照 tab**:按 `note_schema.md` —— 跟随 paper 章节顺序;每一个公式 / 表格 / figure / footnote / algorithm / 实验细节都转写;中文为主、术语首次中英对照;**不加 agent 评价、不加例子**;每节末尾留 `<!-- Q-INSERT: s<n> -->`。
- **讲义 tab**:跨领域按 `lesson_schema.md` 写完整课程;主场只写第 0 课 + 各节要点导读。每课末尾留 `<!-- Q-INSERT: l<n> -->`。
- **一屏卡左栏**:按 `paper-card_schema.md` 的脊椎 / 批判 / 裁决标准写,加本线四格;**右栏四个 textarea 留空**。
- **(v1.7)脉络 / 三镜 / 钉子候选三行**:agent 全自动填,`row solo` 不带 textarea;脉络五格每格标出处;三镜每镜标硬 / 软 / 空并给"主要成立于哪一镜、哪一镜空";钉子候选必带"候选,未验证"。
- **(v1.7)讲义第 -1 课脉络课**必有,含谱系 SVG 与 steelman 评审理由;夯实加两道脉络题(`data-lesson="lm1"`)、一道三镜题。
- **夯实 tab**:按 `note_schema_v2.md` §4 分档;提取卡答案面 = 原 paper-card 的 K 件事 + 承重数学。
- **符号表 tab**:按 `qa_schema.md` Q1 的 A–E 分组,覆盖讲义与原文里全部记号。
- 长度不设上限,不要担心 token;图引用 `figs/<filename>`。

**Step 5 — 视觉验证(必做)**

Chrome headless(或任何可用浏览器)截桌面 1280 宽与手机 390 宽各一张,检查:四个 tab 能切、一屏卡两栏、Q 索引显示"还没有提问"、KaTeX 全部渲染(`\textsc` 会渲染成源码,改 `\mathrm`)、SVG 文字不重叠、无整页横向滚动。修完再截。没有浏览器工具就在 report 里明说。

**Step 6 —(v1.6 并入 Step 4;保留编号以免其他文档引用失效)**

**Step 7 — Mark DONE + report(默认不产 slides)**

执行:`uv run <SKILL_DIR>/scripts/update_queue.py <CWD>/queue.md mark <slug> DONE`

在 chat 给用户**简短** report(不要在 chat 里复述内容,内容已经在文件里):
- ✓ `<slug>` 已读完
- note.html:原文 tab <字数> 字 / 讲义 <n> 课(档位:主场|跨领域)/ 夯实 <n> 项 / 符号表 <n> 条 / Q 索引空
- self-check 清单结果(按 note_schema_v2.md §8):
  - 原文 tab: section / equation / table / figure 全覆盖 ✓
  - 每节 / 每课末尾有 Q-INSERT 标记 ✓
  - 一屏卡左栏四行齐、右栏空;脉络 / 三镜 / 钉子候选三行齐且每条脉络带出处 ✓
  - lineage.json 已生成(或 API 失败已注明)✓
  - 桌面 + 手机截图已看 ✓
- 推荐下一篇:queue.md 里下一个 TODO 的 slug

**Step 8(按需)— Slides**

**默认不跑**。**只有用户明确说 "要 slides / 做幻灯片 / 出个 deck / 我要讲这个"** 才跑:

1. 按 `<SKILL_DIR>/references/slide_schema.md` 写 `<CWD>/<slug>/outline.json`,默认 11 个 content slide(加 title = 12)
2. `ls <CWD>/<slug>/figs/` 看有什么图可以引用,至少 3 个 slide 配 figure
3. 执行:`uv run <SKILL_DIR>/scripts/render_slides.py <CWD>/<slug>/`
4. 输出 `<CWD>/<slug>/slides.pptx`(纯 .pptx,**永远不产 PDF**)

### 模式映射(v1.3 重订)

| Mode | 跑 Step 几 | 产物 |
|---|---|---|
| **Skim** | 1, 2, 7 + 跳过 3-6 | 只在 chat 给三行裁决,**不写文件**;queue.md 标 SHELVED 或 DONE |
| **Core** | 1-7 + 跑「先赌后验」对话流程(在 chat) | note.html;先赌后验过程中的问答作为 Q 块插入,押错的 1% 落一屏卡「边界」 |
| **Teach** | **1-7 全跑** | note.html(一屏卡 + 讲义 + 原文 + 夯实 + 符号表) |
| (任何模式 + 用户要 slides) | 加跑 Step 8 | + slides.pptx |

注:
- Skim 跳过文件产物是因为旁支领域不值得花 token;直接给三行裁决在 chat 就够
- Core 模式里,先赌后验**对话过程中**的 Q&A 作为 Q 块插进 note.html;押错点同时落一屏卡左栏「边界」
- Teach 模式是 default,新 paper 没说档位时默认走 Teach
- **slides 都不在默认产物里**(v1.3),用户主动要才跑 Step 8
- v1.6 起 qa.md / paper-card.md / lesson.html / drill.html 都不再生成

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
4. 押错处必须显式标出来并落进一屏卡「边界」（Core），那是这套方法论的全部价值。
5. 数学一律进 note.html（讲义推导框或 Q 块），不在聊天里堆公式。**符号表 tab 默认必填**。
6. **鼓励跨领域类比提问**。当用户问 "这跟 X 一样吗?"（X 来自他熟悉的另一个领域），认真对照、把共享根 + 关键差异都列清楚——这种"跨领域看 pattern"的直觉很值钱，主动 prompt 用户用上自己的旧知识。答案作为 Q 块插进 note.html。
8. **一屏卡右栏是用户的**。不代填、不润色;用户说"我读完了"但右栏是空的,提醒他填,不替他关掉这篇。
9. **(v1.7)脉络里的每一条连线都要有出处标签**;没有出处的连线不写。三镜的"硬 / 软 / 空"是判决,不是描述——每镜必须落一个字。
10. **(2026-09-12)主场之外的词,默认用户没见过。** 用户主场 = 模仿学习那一套(BC、diffusion policy、DAgger、teacher-student、VLA、遥操、在线 / 离线蒸馏),这些**不解释**,解释了反而啰嗦(用户原话:"BC diffusion 这种不需要解释")。主场之外的一切——规划器(RRT / PRM / 贪心)、接触动力学、控制理论、神经符号、动作捕捉、具体硬件(Allegro 手)、人名 / 机构名、本 skill 自己的行话(三镜、钉子候选)——在**每一个产物**里(一屏卡图、卡的七行、讲义、夯实、chat 回复)第一次出现就给一句白话解释,篇幅不设上限。拿不准算不算主场就解释。一屏卡图末尾的「名词」带必有,卡上出现的主场外词都在里面。
11. **(2026-09-14)不再对照 Path-OPD。** 用户说"以后不需要你对照 path opd,我现在基本理解他的意思了"。一屏卡「去处」、裁决、钉子候选、讲义末课里不再写"对你 / 对 Path-OPD 意味着什么";70 线四格的名字(监督从哪来 / teacher 给什么 / student 怎么学 / 部署差距)照用,但格子里只写这篇论文自己的做法。用户主动问"这跟我的项目怎么连"时再答,答成 Q 块。
19. **(2026-09-18)「三格填满 = 收尾」不是硬条件，用户可以直接宣布 DONE。** 原话：「这一篇标注为 done，<b>虽然那 3 格我没写</b>」。契约里那句「三格填满这篇才算收尾」是给<b>用户自己</b>用的完成信号，<b>不是 agent 卡住流程的门闩</b>。用户说 DONE 就 DONE，queue 里如实记「三格未填，用户裁定可以不填」，**不要追问、不要提醒他去填**。
    - 判据：**这个信号是为了让他确认自己真的读懂了，而不是为了让 agent 收集数据**。他自己判断读懂了，就不需要这个信号。

20. **(2026-09-18)新增状态 `CONCLUSION GET`，在 READING 和 DONE 之间。** 用户原话：「最后两篇 paper 标注 conclusion get，并不是 done。**因为推导我没看懂，但结论我知道了**。」
    - **它不是 DONE 的弱化版，是一个独立档位**：结论已拿到并能用于讨论，推导欠着。queue 里标 `[~]`。
    - **和分档挂钩**：对 **T3 / T4**（价值在数字里）的论文，拿到结论基本等于读完；对 **T1 / T1− / T2·ML**（价值在推导里）的论文，`CONCLUSION GET` 意味着**这篇还欠着一笔**，将来要用它的机制时得回来补。**在 queue 里写明欠的是哪一部分。**
    - **不要催他回去补推导。** 他自己知道欠着；催是把「读懂」变成任务，而这个状态存在的意义正是承认「先往前走」是合法的。

12. **一屏卡右栏 agent 读不到。** 右栏存在浏览器 localStorage 里,不是文件。用户说"我填了,你看看"时,让他点卡片下方的「复制我的版本」按钮把四格贴进 chat,再评;不要假装看过。
13. **录用与奖项是事实,不是印象。** 讲义里的 steelman("评审为什么给高分")是练习,必须和 Step 3.6 查到的实际录用 / 奖项分开写;卡上「发表」行只写查到的,写不出来源就写"未查到"。
14. **(2026-09-18)讲义课按 `references/lesson_interactive_schema.md` 写,不按论文的章节顺序写。** 论文的结构是给审稿人的,讲义必须按理解的顺序重排。推导写对只是及格线,**每一步「为什么这么走」才是讲义的价值**。所有非主场词(概率、统计、信息论、优化、控制的术语<b>全部</b>算)第一次出现就从零解释,篇幅不设上限。写完必跑三道验证:标签平衡、`node --check`、headless Chrome 探针(1280 与 500 两个宽度,合格线 err=none / empty=none / overflow=0 / katexErr=0)。**截图只能看长相,看不出抛异常,不能替代探针。**

15. **(2026-09-18)用户要求派子代理做文献检索时,必须同时更新主线文件。** 规范见 `references/research_mainline_schema.md`。顺序是:①先在本地 `main.tex` 上做能做的核查(全文词频、引用关系、措辞是否出现)——这一步常常就能定性,不必花代理;②再派代理,简报里给全命题原话、判决取值表、三盏灯判据、并<b>明确要求找反面证据和列出返回空的查询词</b>;③结果回来后<b>追加检索日志、追加台账、重算空位</b>;④钉子表述若因此改变,版本历史加一行并写明为什么改。<b>最有价值的一次记录往往是发现「钉子的一块已经被人做掉了」</b>——没有这个文件，这种发现会散在聊天记录里。

16. **(2026-09-18)取消四格。** 用户原话「以后不要有 4 格这个东西，我觉得填写没意义」。一屏卡六行(脊椎·脉络·三镜·边界·裁决·钉子候选)，用户作答框三个(脊椎/边界/裁决)，**三格填满 = 收尾**。`card.json` 不写 `grid`/`grid_names`，`card_svg.py` 已改可选、老卡片仍可渲染，**旧笔记不迁移**。理由：四格要求用户复述论文事实，而左栏已经写了，等于抄写；留下的三格才是只有用户能写的东西。

17. **(2026-09-18)ML 灯暗的论文，结论顶到最前面，不要陪它走完整课程。** 用户原话「对于 ML 这一个灯没有亮的情况，结论的展示要尽可能的提前，并加粗高亮……你需要强化对他结论的描述和可以 take away 的结论，我不想在这种论文上浪费太多的时间」。
    - **触发条件（2026-09-18 当天改正，原写「ML 空」是错的）**：**AI 与 ML <u>都</u>不达标**，即主线文件 §2.0 判 **T3 / T4**。单看「ML 空」会误伤——Geometric Entropy 与 Belkhale 都是 ML 空，但它们的量是<b>推导/定义</b>出来的，属 T2·AI，该给的是下面规则 18 的「AI 侧详写」，**不是**速读块。**分界线是那个量怎么来的**：推出来的 → T2 起步，详写；拟出来／实测出来的 → T3，速读块。
    - **产物**：`note.html` 顶部加一个 `.tldr` 速读块，**位置在一屏卡之前**，是打开页面第一眼看到的东西（放在卡后面等于要滚过整张卡片图，实测 2188 px，不算「提前」）。目录里单开一组「先读这个」置顶。
    - **速读块的固定五段**：①一句话裁决，说清它**测出了什么**和**解释不了什么**，加粗；②**能带走的**，编号列，**每条必须是数字或可执行的规则**，不是概括；③**不能带走的**，逐条写清外推到哪里就错（指数不是跨任务常数、阈值不普适、哪条预测作者自己没验、哪些比较不可比）；④**ML 灯为什么暗**，配作者自己承认缺口的原句；⑤**「读到这里就可以走了」**，并说明下面的课**什么情况下**才值得看。
    - **讲义照常写完，不许偷工**。速读块是**入口**不是**替代**——用户要的是「不浪费时间」，不是「少一份材料」；他哪天要复制这套实验设计时还得回来翻。
    - **(2026-09-18 当天补)顶部速读块还不够，<u>第 0 课本身必须就是结论</u>。** 用户原话：「**为什么结论不应该在第 0 课就出现？我还要去看她的 exp？**」旧模板的第 0 课写「为什么读这篇 / 什么模式 / 我会用哪些行话」——<b>一条结论都没有</b>，等于逼用户走完实验才拿到结果。
        - **T3 / T4 的第 0 课固定叫「这篇的结论，以及你怎么用」**，四段：①几条结论，每条一个框，<b>每条必须是数字或可执行规则</b>；②<b>把它变成你自己的预算/配方</b>——这一段该放交互组件，让用户拖出自己的数；③<b>什么时候这套数不能用</b>；④「这一课到此为止」加三个指路（数怎么来的 / 为什么不能外推 / 实验设计）。
        - 「为什么读这篇 / 行话 / 路线存稿原文」这些**元信息折叠到第 0 课末尾的 `<details>` 里**，不删，但不挡路。
        - **实验课排在结论之后，作为佐证，不作为通路。** 顺序不是论文的顺序，也不是推理的顺序，是<b>「先给答案，再给理由」</b>。
        - **ML 灯亮的论文不适用这条**——那种论文的结论离开推导就不成立，第 0 课仍写「为什么读」。
    - **反过来也成立**：ML 灯**亮**的论文不加速读块。那种论文的价值就在推导里，把结论抽出来放最前面反而鼓励跳读。
    - 理由（用户的原话值得记全）：「这只是一个迁移，得奖主要靠的是工作量和确实解决了很多问题。**但他无法解释任何东西不是吗？**」——工作量换来的是**可查表的数字**，那就让它以数字的形式被取走，几分钟的事。

18. **(2026-09-18)note 的详略跟着论文的侧重走，不是一视同仁。** 用户原话：「如果 AI 侧占比多，你就要详细的说明这个定量指标是什么，能指代什么，怎么来的，以及应该怎么用，这就是偏应用的。而如果是 ML 侧多，你在详细说明以上内容的同时，就要更偏向推导。」
    - **先判侧重**（判据见主线文件 `references/research_mainline_schema.md` §3 改定版）：**T1 / T1−** = 两侧都占；**T2·ML** = 只占 ML；**T2·AI** = 只占 AI；**T3 / T4** = 都不达标。
    - **AI 侧占（T2·AI）→ 讲义必须把那个量讲穿，四问缺一不可**：①**是什么**（定义、单位、取值范围）②**能指代什么**（它替代了原来哪句说不清的话，不能指代什么）③**怎么来的**（从哪个定义或机制导出，为什么是这个形式不是别的）④**应该怎么用**（拿到数据后具体怎么算、算出来怎么读、什么情况下会骗人）。**这一档偏应用，例子要多，推导可以点到为止。**
    - **ML 侧占（T2·ML / T1）→ 上面四问照写，另外<u>更偏推导</u>**：每一步都要有「为什么这么走」，关键步骤补一个自己算过的数值例子，玩具模型与一般情形的距离要说清。**这一档的价值在推导里，不许用结论概述替代。**
    - **都不达标（T3 / T4）→ 走规则 17 的速读块**，讲义照常写完但不必加厚。
    - 背后的排序（用户原话）：「**ML 侧是否能很好解释要好于单纯提出一个 AI 指标并 scale up**，或者说，**真相本身比他的应用要好**」「我本人更倾向于 science 风格，即发现道理，其次才是效果」。

7. 这是 **v1 草稿，用户会在上面改**。用的过程中如果发现某步骤别扭/多余，主动提出来让他调，不要默默将就。**而且：发现的改进应该 fold 回这份 SKILL.md，不要只留在 memory 里**——memory 是 workaround，SKILL.md 才是 durable home。
