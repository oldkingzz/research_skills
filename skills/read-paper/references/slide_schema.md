# Slide Schema —— outline.json 的硬约定

> Agent 写完 `note.md` 之后,基于它**派生**一个 `outline.json`,然后跑 `render_slides.py` 出 `.pptx`。
> 默认 **12 页**(含 title),改长改短就调 `slides[]` 长度。

## 文件位置

`<paper-dir>/outline.json`,跟 `note.md` 同级。

## JSON schema

```json
{
  "title": "<原文标题或你重述的一句话>",
  "authors": "<First Author> et al. (<Affiliation>)",
  "subtitle": "arXiv <id> · <YYYY-MM> · read <YYYY-MM-DD>",
  "slides": [
    {
      "title": "Motivation",
      "bullets": [
        "...",
        "..."
      ],
      "figure": "figs/teaser.png"
    },
    ...
  ]
}
```

### 字段约定

| 字段 | 必填 | 约束 |
|---|---|---|
| `title` | ✓ | 顶层 paper title,会出现在 slide 1 |
| `authors` | ✓ | first author + et al. + 机构,不超过 100 char |
| `subtitle` | 选 | 一行,通常是 arxiv id + 日期 |
| `slides[]` | ✓ | 默认 11 条(+ 1 title slide = 12 总),可改 |
| `slides[].title` | ✓ | 单 slide 标题,≤ 6 个字最佳 |
| `slides[].bullets` | ✓ | **≤ 5 条**,每条 **≤ 110 字符**(渲染时会强制截断到 6 × 110) |
| `slides[].figure` | 选 | `figs/` 下某张图的文件名;不存在则跳过 |

---

## 默认 12 slides 模板(SKILL 让 agent 按这套生成)

```
Slide 1   Title                  (auto: title + authors + subtitle)
Slide 2   Motivation             领域为什么需要这个工作
Slide 3   Problem statement      具体问题定义 + 数学记号
Slide 4   Key idea               一句话核心 (spine 段升级版)
Slide 5   Method overview        架构图 + 数据流
Slide 6   Method details         承重组件 1-2 个
Slide 7   Math / loss            承重公式(渲不好就用图)
Slide 8   Experiments setup      benchmark + baseline
Slide 9   Key results            关键 table
Slide 10  Ablations              重要 ablation
Slide 11  Limitations            paper 自承 + 你看到的
Slide 12  Takeaways              中英双语 takeaways
```

不放 "Connect to my project" slide(用户 D 决策:**不自动加**)。

---

## Bullet 写作规则

- **≤ 5 bullet / slide**(超过就拆 slide 或重写)
- **≤ 110 char / bullet**(render 时会截断;别赌)
- 每个 bullet **必须是完整命题**,不是 keyword(❌ "flow matching" → ✅ "用 flow matching 替代 diffusion head 推理快 5x")
- **数学符号用 unicode**,不用 latex —— `θ`、`∇`、`ℒ`、`𝔼`、`α` 等(pptx 不会渲染 LaTeX 的 `$...$`)
- 复杂公式 → 截图 + 放图(不要 inline 公式)

## Figure 引用规则

- `figure` 字段填 `figs/` 下的**文件名**,不带路径(`render_slides.py` 自己拼路径)
- `ingest.py` 已经把 paper 的 png/jpg + 转好的 pdf-figs 都放到 `figs/` 了
- agent 写 outline 时**先 ls figs/**,挑跟该 slide 匹配的 figure 文件名
- 不要瞎填 `figure: "fig1.png"` 如果根本没这文件 —— render 会跳过但 deck 留空挺难看

## Title slide 美学

- 干净 white-background,左上角 accent color (default: 深蓝 #0E4D92)
- 用 Helvetica Neue(macOS 默认有)
- 不堆 logo / 不放装饰

## 自检 checklist(agent 写完 outline.json 后过一遍)

- [ ] slides 数 = 11(加上 title slide = 12)
- [ ] 每个 slide bullets ≤ 5
- [ ] 每个 bullet ≤ 110 char
- [ ] 至少 3 个 slide 有 figure(默认推荐:Motivation / Method overview / Key results)
- [ ] Takeaways slide 是中英双语
- [ ] 没有空 slide(bullets 必须有内容)
