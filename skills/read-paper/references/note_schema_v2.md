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
- **位置**:插在它所属那一节(课)末尾的 `<!-- Q-INSERT: <id> -->` 标记**之前**。属于哪节由问题内容决定;跨节的问题放在最相关的一节,或放讲义最后一课。
- **格式**(照抄):
  ```html
  <div class="qa" id="q3"><div class="qh"><span>Q3 · 〈简短标题〉</span><span class="qd">2026-09-04</span></div>
  <div class="qb">〈完整回答〉</div></div>
  ```
- **完整度**:≥ chat 回复,含全部例子、推导、表格、类比(沿用 v1.4 硬规矩:chat 会滚走,note 才是留档;要压缩压缩 chat)。
- **写后核对**(硬规矩):重读整个文件,确认 ① 新 Q 号唯一 ② 标记仍在 ③ HTML 结构未被破坏(`<div class="qa"` 计数 = Q 索引应显示的条数)。有 Chrome headless 就截一张图看索引条数对不对。
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
- 写完必须用 Chrome headless(或任何可用浏览器)截桌面(1280 宽)和手机(390 宽)各一张并检查:标签切换、一屏卡两栏、Q 索引条数、公式渲染、SVG 文字不重叠、无整页横向滚动。没有浏览器工具就明说,不许声称验过。

## 8. 写完 self-check(在 chat 里简短 report)

- [ ] 一屏卡左栏四行齐;右栏四个 textarea 空着(agent 没代填)
- [ ] 讲义 tab:跨领域 = 完整课程且每课末尾有 `Q-INSERT` 标记;主场 = 第 0 课 + 要点导读
- [ ] 原文 tab:section / equation / table / figure 全覆盖,每节末尾有 `Q-INSERT` 标记
- [ ] 夯实 tab:档位对(主场 ≤10 / 跨领域 20–35),每项有 `data-lesson`,答案面有 `where`
- [ ] 符号表 tab:A–E 五组,讲义与原文里的记号都能查到
- [ ] Q 索引显示"还没有提问"(新 paper)
- [ ] 桌面 + 手机截图各一张已看过
