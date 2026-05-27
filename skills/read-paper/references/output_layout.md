# Output Layout —— 文件 / 目录约定

> agent 把 paper 产出物放在**哪里**、**怎么命名**。**所有 paper 共享同一份约定**,这样 cross-paper 找东西可预测。

## 1. 工作根目录

默认 `$CWD`,即 agent 当前工作目录。约定:**用户在某个父目录下开 Cursor / Codex,所有 paper 都进这个父目录的子目录**。

例:用户工作根 = `/Users/wangzesen/Documents/claude_sandbox/paper/`,跑所有命令都在这下面。

## 2. 单 paper 的目录结构

```
<paper-slug>/                          # 由 ingest.py 自动建,见下面 slug 规则
├── metadata.json                       # arxiv_id / slug / title / authors / url / ingested
├── main.tex                            # 扁平化后的 LaTeX 全文(\input{} 已解开)
├── source/                             # arxiv 原始 e-print tarball 解压结果
│   └── *.tex, *.bbl, *.sty, *.cls, ...
├── figs/                               # 所有图(.png/.jpg,以及 pdf-figs 已转 png 200dpi)
├── note.md                             # 主笔记,schema 见 note_schema.md
├── outline.json                        # slide 脚本输入,schema 见 slide_schema.md
├── slides.pptx                         # 渲染好的 deck (12 页默认)
├── qa.md                               # 滚动 Q&A(可选,只在 Teach mode 用)
└── paper-card.md                       # 耐久卡(可选,只在 Core / Teach mode 用)
```

## 3. slug 规则

**slug = `<arxiv-id>-<title-slug>[:40]`**

例(适用任何领域,不限 ML / robotics):
- arxiv `1706.03762` + title "Attention Is All You Need" → slug `1706.03762-attention-is-all-you-need`
- arxiv `1502.03167` + title "Batch Normalization: ..." → slug `1502.03167-batch-normalization`
- arxiv `2401.12345` + title "<任何 paper title>" → slug `2401.12345-<title-slug-up-to-40-chars>`

`ingest.py` 自动 slugify:lowercase + replace non-word with `-` + truncate at 40 chars。
完全 domain-agnostic —— 不论你读的是 ML / 物理 / 生物 / 数学 paper,只要是 arxiv 上的都按这套来。

## 4. 全局 queue

**位置:`<工作根>/queue.md`** —— 单一全局 queue,跨所有 paper。

格式见 `update_queue.py`(自动维护):
```markdown
# Reading Queue

## TODO
- [ ] **<slug>** — [<title>](https://arxiv.org/abs/<id>) · TODO · <date>

## READING
- [ ] **<slug>** — ... · READING · <date>

## DONE
- [x] **<slug>** — ... · DONE · <date>

## SHELVED
- [ ] **<slug>** — ... · SHELVED · <date> · _<why shelved>_
```

`update_queue.py` 自动维护四个 section + 检查重复 + 移动 line。

## 5. Cross-paper 资源(在工作根下,不进单 paper 子目录)

| 文件 | 用途 |
|---|---|
| `queue.md` | 全局 reading queue |
| `paper_candidates.md` | (paper #1 用)候选方向汇总 |
| `cross_notes/` | 跨 paper 比较 / 综合笔记 |
| `references/` | 共享的图、引用文件(可选) |

## 6. 临时 / 中间产物

- `ingest.py` 工作时建 `.tmp-<arxiv_id>/`,完成后**自动删除**
- 不留 `__pycache__`、`.DS_Store` 等(`.gitignore` 由你管,不在 skill 范围)
- **slides.pptx 是终产物**,不留 `.pdf` / intermediate marp HTML 之类

## 7. 命名硬规则

- 全部小写
- 用 `-` 不用 `_`
- 不带空格
- 不超过 40 char(slug 主体部分)
- arxiv id 在最前面,**永远可被 grep**

## 8. Disk 卫生(给 ingest.py 的约束)

- 一篇 paper 的 source/ 通常 5-50 MB(LaTeX + bib + 原始 figures)
- figs/ 通常 5-30 MB(png 200dpi)
- 一篇 paper 整个目录 < 100 MB
- **不在工作根目录乱写**,任何中间产物都进 `<slug>/` 或 `.tmp-*/`
- 不写超过 200 MB 单文件(防爆盘)
