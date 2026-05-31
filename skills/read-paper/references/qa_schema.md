# qa.md schema —— **默认只有 Q1 = 符号对照表,其他空**

> 三件套里**最瘦**的一件,**也是结构最稳的一件**。

## 核心约定

**qa.md 默认就一条 entry:Q1 = 这篇 paper 用到的所有符号 / 公式 / 缩写的对照表。**
**其他什么都不写。**

后续 Q2、Q3、... 是**用户主动追问时**才追加,不是 agent 一开始就生成的。

## 为什么这样设计

note.md 已经事无巨细 (完整转写 paper);paper-card.md 已经有 spine / takeaway / 批判 (查漏补缺);**qa.md 不再需要承担"滚动 Q&A 日志"的全部功能**。

但用户读 note.md 时,**对照符号定义**是高频操作 —— 公式里冒出来一个 $\mathbf{H}_B^{(l)}$,需要立即查它是什么。**符号表是用户在 VSCode 里 split-view 的第二个窗口**:左边 note,右边 qa。

所以 qa.md = **可被 split-view 长期挂在屏幕一边的符号查询表**,不是 chat log。

## 文件位置

`<paper-dir>/qa.md`,跟 note.md / paper-card.md 同级。

## 默认初始内容(agent 在 read 流程里生成)

```markdown
# QA — <paper title>

> [arXiv <id>](https://arxiv.org/abs/<id>) · <authors short> · <year>
>
> **使用方式**:在 VSCode 里打开,`Cmd+K V` 开 Markdown 预览(侧边窗渲染 LaTeX 公式)。
>
> 配合 [note.md](note.md) 用 —— note 讲故事,qa 查符号。
>
> 后续追问由用户在 chat 里发起,agent 把答案追加到本文件,用 `---` 分隔。

---

## Q1 — 符号 / 公式 / 缩写对照表
<!-- YYYY-MM-DD · 由 read-paper skill 自动生成 -->

### A. 单个时间步的核心量(最高频)

| 符号 | 含义 | paper 里出现位置 |
|---|---|---|
| ... | ... | Sec X / Eq Y |

### B. 集合 / 空间

| 符号 | 含义 |
|---|---|
| ... | ... |

### C. 概率 / 期望 / 损失符号

| 符号 | 含义 |
|---|---|
| ... | ... |

### D. 评估指标符号(如有)

| 符号 | 含义 |
|---|---|
| ... | ... |

### E. 缩写

| 缩写 | 全称 | 含义 |
|---|---|---|
| ... | ... | ... |

---

> 后续 Q&A 在这条线下面追加。
```

## Q1 写作硬约定

1. **覆盖完整**:paper 用到的所有 distinct 符号都进表(看 note.md 的公式部分,把出现过的都收)
2. **分组**:按上面 A-E 分类,**别全堆一起**
3. **含义中文为主**,但**核心词 + 关键定义 不要漏英文术语**(`p` = 概率 probability)
4. **出现位置 column 选填**:能定位到 paper 里第一次定义/使用的 Section / Equation 编号就填,不能就空
5. **缩写表(E 节)是必填**,即使 paper 看上去没有特定 jargon

## 后续追加(Q2+)

用户在 chat 里追问时,agent 把答案追加到 qa.md 末尾,格式:

```markdown
---

## Q<n> — <用户问题的简短标题>
<!-- YYYY-MM-DD -->

<回答正文,公式 `$...$` / `$$...$$`>
```

## 不该出现在 qa.md 里的东西

- **paper 内容的总结 / 复述** —— 那是 note.md 的事
- **批判 / 评价** —— 那是 paper-card 的事
- **跨 paper connect** —— **v1.3 不主动做**;用户在 chat 主动问时,答案才进 qa.md 作 Q&A entry
- **用户没问的"为你而设的提示"** —— 不要 proactive 加 Q2

## 写完 self-check

- [ ] note.md 里出现的所有公式符号,qa.md Q1 里都有定义
- [ ] 缩写表至少 5 条(每篇 paper 至少 5 个缩写,通常更多)
- [ ] Q1 之后没有任何额外 entry(除非用户已问过)
