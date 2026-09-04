# paper-card.md schema —— **学完之后查漏补缺的对照卡**

> **v1.6(2026-09-04)适用范围**:不再生成独立 paper-card.md。§1 脊椎、§4 批判(改叫"边界")、§5 裁决 → `note.html` **一屏卡左栏**;§2 K 件事、§3 承重数学 → **夯实 tab 提取卡的答案面**。"1 屏内"约束仍适用于一屏卡。右栏由用户自己写,agent 不碰。


> 三件套里**最薄**的一件,但**密度最高、最值钱**。

## 核心约定

`paper-card.md` 不是 paper 内容的摘要,**是用户读完 `note.html` 之后,合上 PDF + 合上 note,凭记忆复述时,用来对照自己漏了什么的"答案卡"**。

**类比**:期末考试的时候,你做完模拟题再对照标准答案找漏点 —— paper-card 就是那张标准答案。

## 设计原则

- **canonical**:写的是"读完这篇 paper 应该掌握的最核心 X 条",不是 paper 内容的 mirror
- **opinionated**:可以有 agent 的判断(spine 是什么 / 哪里最该被批判 / 一句话裁决要不要深挖)
- **可对照**:用户读完 note 后,翻到 paper-card,**一项一项问自己"这条我想到了吗 / 这条的细节我能复述吗"**,没想到 / 复述不清 = 漏了,回 note 补
- **跨 paper 不主动 connect**(v1.3):paper-card 只对单篇 paper 负责,**跨 paper 关联是用户自己的认知工作**,agent 不替他做。用户主动问 "这跟 X paper 怎么 connect" 时,答案进 qa.md 作 Q&A,不回头改 paper-card

## 文件位置

`<paper-dir>/paper-card.md`,跟 `note.html` / `qa.md` 同级。

## 必填结构 —— **5 个章节,固定顺序**(v1.3:去掉 Connect)

```markdown
# <一句话标题:这篇到底干了什么>

> [arXiv <id>](https://arxiv.org/abs/<id>) · <authors short> · <year-MM> · 读于 <YYYY-MM-DD>

## 1. 脊椎(删掉就死的那一个想法)

<用 agent 自己的话,1-3 句。这是 paper 的 single most important claim。
读 paper 的人合上书复述不出脊椎 = 没读懂。>

## 2. 必须掌握的 K 件事(canonical 知识点)

<列 5-8 条,每条 1-2 句。这是"这篇 paper 你必须能跟人讲清楚的核心点"。
覆盖:核心方法、关键数学、主要实验数字、关键 limitations。
用户读完 note 后翻到这里,逐条自问"我能复述吗"。>

- ✏️ **<点 1 一句话>**: 一两句具体描述
- ✏️ **<点 2 ...>**: ...
- ...

## 3. 关键数学(承重公式表)

<只列**承重**公式 —— 删了它论文死的那几个。
每条:公式 + "它是干嘛的" + "去掉/改了会坏什么"。
**详细推导不在这,在 note.html 对应章节**。>

- $\mathcal{L} = ...$ —— 作用:___;改/删后果:___
- ...

## 4. 批判要点(claim ↔ 证据对不对得上)

<🔴 严重 / 🟠 中等 / 🟡 轻度,按强度排。
找 paper 的"声称 vs 实际证据"的不匹配,以及隐藏假设。
用户对照这里 + paper 的 limitations,可以判断这篇有多硬。>

- 🔴 它实际测了 ___,却声称 ___
- 🟠 隐藏假设:___
- 🟡 ablation 缺了 ___

## 5. 一句话裁决

<两个维度:值不值得我接着深挖 / 在我工作里用得上吗。1-2 句。>
```

### 关于"Connect 跨 paper 关联" —— **v1.3 显式去掉**

之前 v1.2 有 §5 Connect 段(让 agent 把当前 paper 跟用户已读的 paper / 已知方向连起来)。**v1.3 显式移除**,因为:
- **跨 paper connect 是用户的认知工作**,agent 替他做反而会 inject agent 的判断而不是用户的 mental map
- 不同用户 mental map 不同;agent 假设 "用户读过 X paper" 会出错
- 特别地:**不要默认 connect 到任何用户在职公司的 paper**(SaiVLA / Synthoid 等)。用户自己 connect 即可,agent 不主动做

如果用户后续在 chat 里**主动**问 "这跟 X paper 怎么 connect",那是 Q&A,答案进 qa.md 作为追加 entry,**不进 paper-card**。

## 写作硬约定

1. **不要超过 1 屏 markdown**:paper-card 是查漏卡,不是 mini-note。如果 5 条 K 件事写到第 8 条,删
2. **必须有 agent 自己的判断**:脊椎不是 abstract 翻译,K 件事不是 paper 6 个 contribution bullet 抄一遍,批判要有自己的视角
3. **公式只列承重的**:不超过 5 条。其他公式在 note 里
4. **不复制 note.html 的内容**:任何想说"详见 note Sec X"的地方就这么写,不重复
5. **不做跨 paper connect**(v1.3):见上面"Connect 段移除"理由

## 跟 note.html / qa.md 的角色边界

| 问题 | 答案该在哪 |
|---|---|
| Paper 的 Sec 3 第 4 段说了什么? | **note.html**(完整转写) |
| 公式 (5) 里 $\alpha$ 是什么? | **qa.md**(符号表) |
| 这篇的 spine 是什么? | **paper-card** Sec 1 |
| 这篇 paper 我读完后该记住哪 5 件事? | **paper-card** Sec 2 |
| 这篇的批判点是什么? | **paper-card** Sec 4 |
| 这篇跟我之前读的 X paper 怎么 connect? | **不主动写**;用户问才答,进 qa.md 作 Q&A |

## 写完 self-check

- [ ] 脊椎复述不超过 3 句
- [ ] K 件事在 5-8 条之间
- [ ] 批判至少 3 条(🔴/🟠/🟡 至少各 1 条 ideally)
- [ ] 整个 card 不超过 1 屏(~80 行 markdown)
- [ ] 没有大段抄 note 的内容
- [ ] **没有跨 paper connect 段**(v1.3 移除)
