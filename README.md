# research-skills

读 / 写学术论文（主要 ML/AI，英文）的个人技能集，配合 Claude Code 使用。

## 为什么存在

主要在 VSCode 里读论文。Claude 侧边栏不渲染 LaTeX，所以**所有含数学公式的回答都写进一个 markdown 文件（`qa.md`），靠 VSCode 预览渲染**。这是整个技能集的核心约定。

## 结构

```
.
├── SKILL.md                  # 总入口 + qa.md 输出约定
├── skills/
│   ├── read-paper/           # ★ 原创：「先赌后验」式深读方法论
│   │   ├── SKILL.md
│   │   ├── references/critique-rubric.md   # 6 维批判 rubric
│   │   └── templates/paper-card.md
│   └── ml-paper-writing/     # 来自 Orchestra-Research（MIT），见其 NOTICE.md
├── templates/qa.template.md
└── references/
```

### `read-paper` 的核心想法
不是让 AI 把论文讲给你听（那只会制造"我懂了"的错觉），而是**先赌后验**：在每个承重点先押一个答案再揭晓，**你押错的地方就是对你个人真正值得较真的那 1%**。详见 `skills/read-paper/SKILL.md`。

## 许可

本仓库 MIT。`skills/ml-paper-writing/` 派生自 [Orchestra-Research/AI-research-SKILLs](https://github.com/Orchestra-Research/AI-research-SKILLs)（MIT），署名见该目录 `LICENSE` 与 `NOTICE.md`。
