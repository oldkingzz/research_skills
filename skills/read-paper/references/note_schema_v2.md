# note.html v2 schema —— 单文件契约(read-paper v1.6,2026-09-04)

> **一篇 paper 只有这一个用户可读文件。** 旧三件套(note.html / qa.md / paper-card.md)与 v1.5 的 lesson.html、临时的 drill.html 全部并入。
> 模板:`templates/note_v2.html`。本文件只讲**结构与编辑规则**;各部分的**内容标准**仍由旧 schema 负责(见 §6 映射表)。

## 0. 为什么改(一段,别删)

2026-08-31 到 09-04 在 TAMP 线上的实测:faithful 转写的 note.html 对跨领域论文是符号墙,能读的是讲义;qa.md 作为独立文件几乎没人往里写(A1、B1 只剩自动生成的符号表),真正问过的问题都是 chat 里问、agent 追加,但追加到独立文件后**问题和它对应的段落分开了**;paper-card 是 agent 写的,用户读完没有"自己写一遍"的位置,导致"读完了但不知道怎么收尾"。三个问题一个解:一个文件、讲义为主体、Q 插在段落旁、卡片留一栏给用户自己写。

## 1. 结构(自上而下,固定顺序)

```
<h1> + meta chips
① 一屏卡 <section class="card">        两栏:左 = agent 参考版,右 = 用户自己写(textarea,localStorage)
② Q 索引 <section class="qindex">      JS 自动从页内 .qa 块生成,agent 不维护
③ 标签栏 <div class="tabs">            讲义 | 原文对照 | 夯实 | 符号表
   ├ <section class="tab" data-tab="lesson">    讲义(课为单位;每课末尾一个 Q-INSERT 标记)
   ├ <section class="tab" data-tab="source">    原文对照(镜像 paper 章节;每节末尾一个 Q-INSERT 标记)
   ├ <section class="tab" data-tab="drill">     夯实(提取卡 / 判断题 / 必答题 / 雾定位器)
   └ <section class="tab" data-tab="symbols">   符号表(A–E 五组)
```

左侧 sticky 目录按 tab 分组,JS 只显示当前 tab 的那组。任何 `#锚点` 链接会自动切到目标所在 tab 再滚动。

## 2. 一屏卡:四行两栏

| 行 | 左栏(agent 写) | 右栏(用户写) |
|---|---|---|
| 脊椎 | 1–3 句,删掉就死的那一个想法 | 同题,自己的话 |
| 四格地图 | 本条研究线的四格(TAMP 线:谓词/算子/规划器/噪声;换线换四格) | 四格各一行 |
| 边界 | 2–4 条:它假设了什么、恰好没测什么、claim 超出证据的地方 | 同题 |
| 一句话裁决 | 值不值得深挖 / 用得上吗 | 同题 |

- **收尾的定义**:右栏四格全部非空 = 这篇收尾。页面底部状态行自动显示 `n/4`。
- **agent 不代填右栏**。用户在 chat 里口述,agent 也只能把它写进右栏对应位置(标注"用户 YYYY-MM-DD"),不得润色成自己的版本。
- 左栏不放"必须掌握的 K 件事"——那段整个搬进夯实 tab 的提取卡答案面,避免两处重复。

## 3. Q 块:编号、位置、格式

- **编号**:全局递增,按**提问顺序**,与位置无关。Q7 可以出现在 Q3 前面的节里。新 Q 号 = 页内现有最大 Q 号 + 1。符号表不占 Q 号。
- **位置**(2026-09-08 用户改定):**问题在哪里冒出来,Q 块就插在哪里**——紧跟引发问题的那段话 / 那个公式 / 那个框的正后面,不放节末。只有问题不针对页面上某个具体位置时(比如"这篇和 X 怎么 connect"),才退回到所属节末尾的 `<!-- Q-INSERT: <id> -->` 标记之前。
- **格式**(照抄):
  ```html
  <div class="qa" id="q3"><div class="qh"><span>Q3 · 〈简短标题〉</span><span class="qd">2026-09-04</span></div>
  <div class="qb">〈完整回答〉</div></div>
  ```
- **标题里不许放 LaTeX**(2026-09-18 新增):`<span>Q<n> · 标题</span>` 里只能是纯文本。Q 索引是用 `textContent` 取标题的,KaTeX 渲染后会同时留下 HTML 和 MathML 两份文本,索引里会出现 `ρt\rho^{t}ρt` 这种重复乱码。要提符号就用普通字符写(「第 t 步」「状态分布」),公式留在正文里。
- **插进 `<li>` / `<td>` 等容器里时**(2026-09-18):Q 块放在该容器内部、闭合标签之前,别放在 `<ol>` 的两个 `<li>` 之间(非法 HTML)。索引脚本已支持跨层向上找 `<h2>`(`h2=h2.previousElementSibling||(el=el.parentElement)&&el.previousElementSibling`),旧模板那版只找同级,会导致索引里缺节名。
- **用页面已有的样式类**:强调框用 `.dvbox` / `.exbox` / `.warnbox` / `.box`,表格用 `.tblwrap` 包。别自创类名,自创的没有 CSS,渲染成裸块。
- **完整度**:≥ chat 回复,含全部例子、推导、表格、类比(沿用 v1.4 硬规矩:chat 会滚走,note 才是留档;要压缩压缩 chat)。
- **写后核对**(硬规矩):重读整个文件,确认 ① 新 Q 号唯一 ② 标记仍在 ③ HTML 结构未被破坏(`<div class="qa"` 计数 = Q 索引应显示的条数)。有 Chrome headless 就截一张图看索引条数对不对。**更省事的核对法**:`chrome --headless=new --dump-dom` 把跑完 JS 的 DOM 抓出来,再检查 `<ol id="qlist">` 的条目数与文字是否干净、新 Q 块内 `class="katex` 节点数 > 0 且残留裸 `$` 数为 0、全页 `katex-error` 数为 0。
- **不许**:在标记以外的位置插 Q;改旧 Q 的正文(用户明确要求才改);把 Q 写成对 paper 的总结。

## 4. 夯实 tab:常设,分档

| | 主场论文 | 跨领域论文 |
|---|---|---|
| 提取卡(Ⅰ) | 5–8 条 = 原 paper-card 的 K 件事 + 承重数学,每条一问一答 | 8–10 条 |
| 判断题(Ⅱ) | 可省 | 8–12 题,每题写清为什么错、雾在哪一课 |
| 必答题(Ⅲ) | 1 题:paper 的承重问题 | 1–2 题:阅读路线里挂着的必答题 |
| 雾定位器(Ⅳ) | 有(按讲义课号或原文节号统计) | 有 |
| 合计 | ≤ 10 项 | 20–35 项 |

- 每个 `.item` 带 `data-lesson="<讲义课的 id>"`,雾定位器按它统计;主场论文讲义只有第 0 课时,`data-lesson` 指向原文节 id 也可以。
- 答案面 `.ans` 末尾放 `<div class="where">讲义 第 X 课 · 原文 Sec Y</div>`。
- 提取卡的答案面就是用户读完后的**参考**;这是 paper-card §2 的新家。

## 5. 讲义 tab 与原文 tab 的分工(按档位)

| | 跨领域 | 主场 |
|---|---|---|
| 讲义 tab | 完整 lesson(按 lesson_schema.md:理解曲线排课、一个 running example、先例子后定义、推导代具体数字、每课"回到原文"),**主读** | 第 0 课(用用户已会的语言说清这篇解决什么)+ 每节一段要点导读即可 |
| 原文 tab | faithful 转写(note_schema.md),查细节用 | faithful 转写,**主读** |

两个 tab 之间用 `<a href="#s3">` 互链;JS 会切 tab。讲义里出现的记号必须与符号表 tab 一致。

## 6. 旧 schema 的去向(内容标准仍以它们为准)

| 旧文件 / 旧概念 | 现在在 note.html 的哪里 | 规则仍看 |
|---|---|---|
| note.html v1.4(faithful 转写) | 原文对照 tab | `note_schema.md` |
| lesson.html(v1.5) | 讲义 tab | `lesson_schema.md` |
| paper-card §1 脊椎、§4 批判、§5 裁决 | 一屏卡左栏(脊椎 / 边界 / 裁决) | `paper-card_schema.md` |
| paper-card §2 K 件事、§3 承重数学 | 夯实 tab 提取卡答案面 | `paper-card_schema.md` |
| qa.md Q1 符号表 | 符号表 tab | `qa_schema.md` Q1 部分 |
| qa.md Q2+ | Q 块(插在节末)+ 自动 Q 索引 | 本文件 §3 |
| drill.html(临时,2026-09-02) | 夯实 tab | 本文件 §4 |

**不再生成**:`qa.md`、`paper-card.md`、`lesson.html`、`drill.html`。**已有的旧论文不迁移**;从下一篇起用 v2。

## 7. 载体与验证

- 单文件、内联 CSS、KaTeX jsdelivr CDN(auto-render `$`/`$$`)。**KaTeX 不支持 `\textsc`**,用 `\mathrm`;SVG `<text>` 里不写 `$…$`。
- `main{min-width:0}` 必须保留(否则手机端整页横向溢出);宽表用 `.tblwrap`,SVG 用 `.svgwrap`。
- localStorage key = `note:<slug>`;所有读写 try/catch。
- 写完必须用 Chrome headless(或任何可用浏览器)截桌面(1280 宽)和窄屏(**500 宽**;Chrome headless 窗口最小宽 500,`--window-size=390` 只是把 500 宽布局裁掉右边,会误判成横向溢出——要验真溢出,注入脚本比较 `document.documentElement.scrollWidth` 与 `innerWidth`)各一张并检查:标签切换、一屏卡两栏、Q 索引条数、公式渲染、SVG 文字不重叠、无整页横向滚动。没有浏览器工具就明说,不许声称验过。

- (2026-09-14)窄屏横向滚动的一个隐蔽来源:KaTeX 的隐藏 `.katex-mathml` 节点。模板已加 CSS 把它移到视口左外侧;老 note 出现 500 px 下 `scrollWidth > innerWidth` 时先查这个。

## 8. 写完 self-check(在 chat 里简短 report)

- [ ] 一屏卡左栏四行齐;右栏四个 textarea 空着(agent 没代填)
- [ ] 讲义 tab:跨领域 = 完整课程且每课末尾有 `Q-INSERT` 标记;主场 = 第 0 课 + 要点导读
- [ ] 原文 tab:section / equation / table / figure 全覆盖,每节末尾有 `Q-INSERT` 标记
- [ ] 夯实 tab:档位对(主场 ≤10 / 跨领域 20–35),每项有 `data-lesson`,答案面有 `where`
- [ ] 符号表 tab:A–E 五组,讲义与原文里的记号都能查到
- [ ] Q 索引显示"还没有提问"(新 paper)
- [ ] 桌面 + 手机截图各一张已看过

## 9. v1.7(2026-09-12):脉络与三镜(用户裁定:connect 解禁;允许联网拉引用;新三行全自动、不留右栏)

**为什么加**:用户 09-12 原话——"我拥有锤子,但并不是有钉子才有的锤子……我读论文不能仅仅为了学习知识,我还要知道他背后的脉络,知道他为什么做这个,他为什么能够用称得上 best paper 级别,解决了行业中什么特别严重的弊病,又用什么领域的人的思考方式解决的。"提案与依据见 `proposals/2026-09-12-lineage-three-lens.html`。

### 9.1 一屏卡从四行变七行

| 行 | 谁写 | 内容 |
|---|---|---|
| 脊椎 | agent 左 / 用户右 | 不变 |
| **脉络** | **agent 全自动,无右栏** | 五格:来处(接哪条线、上游 3–5 篇、作者谱系)/ 当时的极限 / 弊病(行业或学术,一句)/ 动作与代价(新在哪、为什么这时候能成、付出什么)/ 去处(下游、谁在乎、对本线意味着什么)。**每格标出处**:`[原句 Sec X]` / `[引用数据]` / `[agent 判断]` 三选一,不许混。 |
| **三镜** | **agent 全自动,无右栏** | Robotics(什么系统任务环境,成没成,快准稳的数字,换场景成不成)/ AI(本质难点是什么,现有方法为何在此失败,这篇把难点定位到哪一步、变成了什么可测的量)/ ML(方法为什么成立,机制有无被证明或消融隔离,与替代方法差在哪条假设)。每镜结尾标 **硬 / 软 / 空**。最后两句:主要成立于哪一镜;哪一镜空。 |
| 四格地图 | agent 左 / 用户右 | 不变 |
| 边界 | agent 左 / 用户右 | 不变 |
| 一句话裁决 | agent 左 / 用户右 | 不变 |
| **钉子候选** | **agent 全自动,无右栏** | 空的那一镜里的一个具体问题 + 只有具备什么的人能填 + 怎么验证。必须带"候选,未验证"字样。 |

- 收尾定义不变:原四行右栏填满 = 收尾;新三行不计。
- 新三行在模板里用 `<div class="row solo">`(两列:标签 + 内容),不放 textarea。

### 9.2 讲义必有「第 -1 课 · 脉络课」,放第 0 课之前

固定顺序:时代背景 → 当时怎么做、卡在哪 → 这篇的动作 → 代价 → 去处 → 为什么评审会给它高分(steelman,对着 CoRL / ICRA 的 significance / novelty / claims-established / impact 四条)。配一张谱系小图(内联 SVG:上游 → 本篇 → 下游)。篇幅 ≤ 讲义总量 20%。铁律:描述"当时的极限"时用当时的语言,不许用本篇发明的术语。

### 9.3 夯实加三题

提取卡加两道脉络题(`data-lesson="lm1"`):"这篇之前的做法是什么、坏在哪""这篇付出的代价是什么、为什么这时候能成";判断题加一道三镜题:"这篇主要在哪一镜下成立"。

### 9.4 connect 规则(替代 v1.3)

- v1.3 的"agent 不主动做跨 paper connect"**作废**。新规则:**连,每条连线标出处**(原句 / 引用数据 / agent 判断)。
- 仍然**不连到用户在职公司的论文**。
- 连线只写在脉络行、第 -1 课、第 6 课(对照课)三处,不散落到原文对照 tab。

### 9.5 Step 3.5:拉引用(允许联网)

`uv run <SKILL_DIR>/scripts/lineage.py <arxiv-id> --out <paper-dir>/lineage.json`:用 Semantic Scholar Graph API 取本篇的 references 与 citations(各按 citationCount 排前 15),写 `lineage.json`(title / year / venue / citationCount / 是否有 arXiv id)。agent 再拿论文自己的 related work 段核对,只把两边都支持的写进"来处 / 去处"。API 不可用时在 report 里明说,脉络行的来处只用论文原句。`lineage.json` 是中间产物,不是用户读物。

## 10. v1.7.1(2026-09-12):一屏卡改为图片

用户裁定:一屏卡要是**一张图**,第一眼不滚动看完。规则全部在 `references/card_image_schema.md`,这里只记结构变化:

- `<section class="card">` 的顺序变为:`<h2>` → `<div class="svgwrap cardimg">`(内联 `card.svg`)→ `<details class="cardfull">`(七行全文,全部 `row solo`,默认收起)→ `<div class="mineblock">`(用户四个 textarea:脊椎 / 四格 / 边界 / 裁决,`data-store` 不变)→ `#cardstatus`。
- 图由 `scripts/card_svg.py` 从 `<paper-dir>/card.json` 生成,落 `<paper-dir>/card.svg` 再内联。每格有字数上限,超了删字,脚本不缩字号。
- 收尾规则不变:用户四格填满 = 收尾。图和折叠区都是 agent 的参考版。
- 视觉验证:Chrome 不可用时 `qlmanage -t -s 1600 -o <dir> card.svg` 出 PNG 看图本身;整页仍需浏览器截图,做不到就明说。

---

## 11. v1.8(2026-09-18):讲义课的写法与交互组件

讲义 tab 每一课的骨架、交互组件的判据与技术规矩、证据强度分级板、以及三道验证流程,**独立成文件** `lesson_interactive_schema.md`,本节只做索引。

要点摘录(细节以那份为准):
- 一课八段,**零符号的物理直觉必须排在定义/定理之前**。
- 推导每一步都要写「为什么这么走」,不是只写「做了什么」。
- 交互组件只在四种场景做:参数扫描 / 两个量的赛跑 / 反直觉的极端情形 / 公式 vs 实测。静态 SVG 能说清的不做交互。
- JS:每课一个 `<script>`、一个外层 IIFE、id 加课号前缀、**不要用单字母变量遮蔽外层辅助函数**(遮蔽会抛异常并连带打断同一 IIFE 里后面所有组件)、SVG 文本不放 LaTeX、不测量布局。
- **写进页面的每个数值先用 `node -e` 独立算一遍**;「界 vs 真实值」这类对比必须确保两边是定理里的那两个对象。
- 收口课出一块证据强度分级板:定理 / 隔离实验 / 相关观察 / 未验证,每行带出处,分级标为 agent 判断。
- 验证用 headless Chrome 探针把结果写进 `document.title` 再 `--dump-dom` 抓,**截图不能替代**。

---

## 12. v1.9.2(2026-09-18):取消四格

用户裁定：**「以后不要有 4 格这个东西，我觉得填写没意义」**。

- **一屏卡从七行变六行**：脊椎 · 脉络 · 三镜 · 边界 · 裁决 · 钉子候选。**不再有四格。**
- **用户作答框从四个变三个**：脊椎 / 边界 / 裁决。**三格填满 = 这篇收尾。**
- `card.json` 不再写 `grid` 与 `grid_names`；`scripts/card_svg.py` 已改成**可选**，老卡片带着这两个字段仍照旧渲染。
- **旧笔记里的四格保留不动，不迁移。**
- **例外，而且这一条最容易漏：正在读的那篇不算旧笔记。** 只要一篇还没 DONE、用户还要往右栏填字，就必须当场把它的四格拿掉，否则下次打开笔记，摆在用户面前的仍是一个他已经判定「填写没意义」的框。2026-09-18 收 Belkhale 时只改了 Belkhale，隔壁标着 READING 的 2410.18647 被当成旧笔记放过了，开工第一件事就得回头补。**判据是状态不是日期：`READING` 一律跟改，`DONE` / `SHELVED` 一律不动。**
- 跟改的完整清单（七处，少一处就会留下痕迹）：`card.json` 的 `grid`/`grid_names` → 重跑 `card_svg.py` → 把新 SVG 换进 note 的 `.cardimg` → 目录那行 → 折叠区「七行全文」改「六行」并删掉四格那一行 → 作答框（表头「四格填满」改「三格填满」、删 `card-grid` 那个 textarea、复制提示）→ JS 两处（`cardStatus` 的 keys 数组、复制按钮的 names 映射）。**`card.png` 也要重出，它是位图，不会跟着 SVG 变。**
- 「这一条线的四格」这个概念本身也废除——线级的对照如果需要，写进讲义或主线文件，不占卡片一行。

**为什么**：四格是「这条线上每篇都要回答的四个问题」，但它同时要求用户复述论文事实（价值怎么定义、用什么量），而那些左栏已经写了，用户再填一遍只是抄写。保留的三格才是**只有用户能写**的东西：他自己的一句话、他看到的边界、他的裁决。
