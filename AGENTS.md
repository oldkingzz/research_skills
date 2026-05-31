# research_skills — Agent-readable instructions

This repo is a **skill set for reading and writing academic papers**. It targets:
- **Anthropic Claude Code** (reads `.claude/skills/` symlink-aware)
- **OpenAI Codex CLI** (reads `.agents/skills/` natively)
- **Cursor** (reads `.cursor/skills/` and `.agents/skills/`)

The same `SKILL.md` files work across all three platforms — they share the open
[agentskills.io](https://agentskills.io/) format.

## Repo layout

```
research_skills/
├── SKILL.md                          # set-level entrypoint + qa.md convention
├── AGENTS.md                          # this file (project-level always-on context)
├── CLAUDE.md → AGENTS.md              # symlink so Claude Code reads this too
├── skills/
│   ├── read-paper/                    # main reading skill (Teach/Core/Skim modes)
│   │   ├── SKILL.md                   # complete spec including execution workflow
│   │   ├── scripts/                   # uv-runnable Python (PEP 723 inline deps)
│   │   │   ├── ingest.py              # arxiv → LaTeX source → flattened main.tex
│   │   │   ├── render_slides.py       # outline.json + figs → slides.pptx
│   │   │   └── update_queue.py        # queue.md state machine
│   │   ├── references/
│   │   │   ├── note_schema.md         # note.md required structure
│   │   │   ├── slide_schema.md        # outline.json format + 12-slide template
│   │   │   ├── output_layout.md       # file/dir naming conventions
│   │   │   └── critique-rubric.md     # 6-dim critique rubric
│   │   └── templates/
│   │       ├── paper-card.md
│   │       └── note.template.md
│   └── ml-paper-writing/              # writing skill (Orchestra-derived)
├── templates/qa.template.md
└── references/
```

## Key conventions

1. **One source of truth, multi-platform access.** `skills/read-paper/` is the
   canonical home. Project-level installs symlink `.agents/skills/read-paper` and
   `.claude/skills/read-paper` to this dir.
2. **Scripts use `uv run` with PEP 723 inline metadata.** No `requirements.txt`,
   no `pyproject.toml` needed — every script declares its own deps in the file
   header. uv handles ephemeral venvs.
3. **LaTeX source only, never PDF.** Paper ingestion uses arxiv `e-print`
   endpoint and processes flattened `.tex` files. PDF parsing is fragile for
   math-heavy papers; we don't fall back to it.
4. **Outputs are `.pptx`, never `.pdf`.** Slide generation is python-pptx
   direct, no PDF intermediate.
5. **Single global `queue.md`** at the project working root, NOT per-paper.
   Tracks TODO / READING / DONE / SHELVED across all papers.
6. **Notes are Chinese (mother tongue for depth thinking), Key Takeaways are
   bilingual (CN + EN)** — EN takeaways are polish enough to paste into a
   related-work section.
7. **Three reading modes**: Skim (旁支三行裁决) / Core (核心领域先赌后验) /
   Teach (Claude 出主讲稿,用户问问题) — see `skills/read-paper/SKILL.md`.

## Invocation (auto-trigger, no explicit skill name needed)

Modern LLM-backed agents (Claude Opus 4.x, GPT-5.x, Gemini 2.x) match user intent
against skill `description` fields and auto-load the right skill. **The user does
NOT need to say "use read-paper skill"** — natural language works:

- "读这篇 https://arxiv.org/abs/<any-arxiv-id>"
- "看下 1706.03762" (any arxiv ID, any field — ML / physics / biology / math)
- "summarize this paper: <url>"
- "解释一下这篇 paper 的方法"
- "/arxiv <id>" (slash style also fine)

The skill is **domain-agnostic** — it works for any arxiv paper, not just ML /
robotics. The `description` field includes those trigger phrases up front so
auto-matching works across Claude Code / Codex CLI / Cursor without ceremony.

## What the agent does once triggered (v1.3 — three-artifact pipeline, slides on demand)

1. `uv run skills/read-paper/scripts/ingest.py <arxiv-id> --out-dir <CWD>`
   — downloads arxiv LaTeX source, flattens `\input{}`, extracts figures
2. `uv run skills/read-paper/scripts/update_queue.py <CWD>/queue.md add <slug> "<title>" <id>`
   `uv run skills/read-paper/scripts/update_queue.py <CWD>/queue.md mark <slug> READING`
3. Agent reads `<slug>/main.tex` end-to-end
4. Agent writes `<slug>/note.md` per `references/note_schema.md`
   — **exhaustive faithful PDF → markdown transcription**, follows paper's own
   section order, no compression, no agent opinions (those go in paper-card)
5. Agent writes `<slug>/qa.md` per `references/qa_schema.md`
   — **default content is just Q1 = symbol / formula / abbreviation table**;
   no Q2+ yet (those are added later when user asks follow-ups)
6. Agent writes `<slug>/paper-card.md` per `references/paper-card_schema.md`
   — **canonical 1-screen self-check card, 5 sections** (spine, K must-know
   items, key math, critique, verdict); user uses this AFTER reading note to
   find gaps. **No "Connect to other papers" section** (v1.3 removed) —
   cross-paper connect is the user's cognitive work, not the agent's
7. `uv run skills/read-paper/scripts/update_queue.py <CWD>/queue.md mark <slug> DONE`
8. (**on demand only**) If user explicitly asks for slides, write
   `<slug>/outline.json` per `references/slide_schema.md` then run
   `uv run skills/read-paper/scripts/render_slides.py <CWD>/<slug>/` →
   `<slug>/slides.pptx`. Slides are NOT in the default pipeline.

The three artifacts have **strict role boundaries** (no content duplication):
- note.md = what the paper says (faithful)
- qa.md = symbol lookup (just Q1 by default)
- paper-card.md = canonical opinionated takeaways for post-study self-check

## Iteration policy

This is `v1.x` — actively being iterated. When a workflow improvement is
discovered, fold it back into the SKILL.md / references/ here (do NOT just
leave it in agent memory). Memory is a workaround; this repo is the durable home.
