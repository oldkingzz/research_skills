#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
update_queue.py — Manage the global reading queue.

Queue lives at a single user-specified path (typically <project>/queue.md).
Sections: TODO / READING / DONE / SHELVED.

Usage:
    uv run update_queue.py <queue> add <slug> <title> <arxiv_id> [--why "..."]
    uv run update_queue.py <queue> mark <slug> <status>
    uv run update_queue.py <queue> show
    uv run update_queue.py <queue> init
"""
import argparse, re, sys
from datetime import date
from pathlib import Path

SECTIONS = ["TODO", "READING", "DONE", "SHELVED"]


def init_queue(q: Path):
    if q.exists():
        sys.exit(f"queue already exists: {q}")
    q.write_text(
        "# Reading Queue\n\n"
        "Per-paper status: **TODO** → **READING** → **DONE** (or **SHELVED**).\n\n"
        "## TODO\n\n## READING\n\n## DONE\n\n## SHELVED\n"
    )
    print(f"✓ created {q}")


def _ensure(q: Path):
    if not q.exists():
        init_queue(q)


def _line_for(slug: str, title: str, arxiv_id: str, status: str, why: str = "") -> str:
    box = "x" if status == "DONE" else " "
    suffix = f" · _{why}_" if why else ""
    return (
        f"- [{box}] **{slug}** — [{title}](https://arxiv.org/abs/{arxiv_id}) "
        f"· {status} · {date.today()}{suffix}\n"
    )


def add_paper(q: Path, slug: str, title: str, arxiv_id: str, why: str = ""):
    _ensure(q)
    content = q.read_text()
    if re.search(rf"\*\*{re.escape(slug)}\*\*", content):
        print(f"already in queue: {slug}")
        return
    line = _line_for(slug, title, arxiv_id, "TODO", why)
    # insert after "## TODO" header
    content = re.sub(r"(## TODO\n)", rf"\1{line}", content, count=1)
    q.write_text(content)
    print(f"✓ added: {slug}")


def mark(q: Path, slug: str, status: str):
    if status not in SECTIONS:
        sys.exit(f"status must be one of: {SECTIONS}")
    _ensure(q)
    content = q.read_text()
    line_re = re.compile(rf"^- \[.\] \*\*{re.escape(slug)}\*\*.*$", re.MULTILINE)
    m = line_re.search(content)
    if not m:
        sys.exit(f"not found in queue: {slug}")
    old_line = m.group(0)
    # update status text + checkbox + date
    new_line = re.sub(r"· (TODO|READING|DONE|SHELVED)", f"· {status}", old_line)
    new_line = re.sub(r"^- \[.\]", f"- [{'x' if status == 'DONE' else ' '}]", new_line)
    new_line = re.sub(r"· \d{4}-\d{2}-\d{2}", f"· {date.today()}", new_line)
    # remove from current section
    content = content.replace(old_line + "\n", "")
    content = content.replace(old_line, "")
    # insert under target section
    content = re.sub(rf"(## {status}\n)", rf"\1{new_line}\n", content, count=1)
    # collapse extra blank lines
    content = re.sub(r"\n{3,}", "\n\n", content)
    q.write_text(content)
    print(f"✓ {slug} → {status}")


def show(q: Path):
    if not q.exists():
        sys.exit(f"queue not found: {q}")
    print(q.read_text())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("queue", help="path to queue.md")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init")
    sub.add_parser("show")

    a = sub.add_parser("add")
    a.add_argument("slug")
    a.add_argument("title")
    a.add_argument("arxiv_id")
    a.add_argument("--why", default="", help="one-line reason / context")

    m = sub.add_parser("mark")
    m.add_argument("slug")
    m.add_argument("status", choices=SECTIONS)

    args = ap.parse_args()
    q = Path(args.queue).expanduser().resolve()

    if args.cmd == "init":
        init_queue(q)
    elif args.cmd == "show":
        show(q)
    elif args.cmd == "add":
        add_paper(q, args.slug, args.title, args.arxiv_id, args.why)
    elif args.cmd == "mark":
        mark(q, args.slug, args.status)


if __name__ == "__main__":
    main()
