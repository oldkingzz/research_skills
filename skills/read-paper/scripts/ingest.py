#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "requests",
#   "pymupdf",
# ]
# ///
r"""
ingest.py — Download arxiv LaTeX source, flatten \input{}, extract figures.

LaTeX source ONLY. No PDF fallback. (Per user policy: arxiv 99% have source.)

Usage:
    uv run ingest.py <arxiv_id_or_url> [--out-dir <dir>]

Output structure:
    <out-dir>/<slug>/
        |-- main.tex          # flattened LaTeX (\input{} / \include{} resolved)
        |-- source/           # raw tarball contents
        |-- figs/             # png/jpg + pdf-figs converted to png (200dpi)
        +-- metadata.json     # arxiv id, slug, title, authors, url
"""
import argparse, json, re, shutil, sys, tarfile
from datetime import date
from pathlib import Path
import requests

ARXIV_RE = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")


def extract_arxiv_id(s: str) -> str:
    m = ARXIV_RE.search(s)
    if not m:
        sys.exit(f"ERR: cannot extract arxiv id from: {s}")
    return m.group(1)


def download_source(arxiv_id: str, tmp: Path) -> Path:
    url = f"https://arxiv.org/e-print/{arxiv_id}"
    print(f"→ {url}")
    r = requests.get(url, timeout=120, headers={"User-Agent": "read-paper-skill/1.0"})
    r.raise_for_status()
    tarball = tmp / f"{arxiv_id}.tar.gz"
    tarball.write_bytes(r.content)

    src = tmp / "source"
    src.mkdir(exist_ok=True)
    try:
        with tarfile.open(tarball, "r:gz") as t:
            t.extractall(src)
    except tarfile.TarError:
        # single-file submission (rare): treat as one .tex
        (src / "main.tex").write_bytes(r.content)
    tarball.unlink()
    return src


def find_main_tex(src: Path) -> Path:
    """Heuristic: file containing \\documentclass at the top."""
    candidates = list(src.rglob("*.tex"))
    if not candidates:
        sys.exit(f"ERR: no .tex files in {src}")
    for c in candidates:
        try:
            if "\\documentclass" in c.read_text(errors="ignore")[:8000]:
                return c
        except Exception:
            continue
    return max(candidates, key=lambda p: p.stat().st_size)


_INPUT_RE = re.compile(r"\\(?:input|include|subfile)\{([^}]+)\}")


def flatten(tex: str, base: Path, depth: int = 0) -> str:
    if depth > 6:
        return tex

    def rep(m: re.Match) -> str:
        fname = m.group(1).strip()
        if not fname.endswith(".tex"):
            fname += ".tex"
        try:
            sub = (base / fname).read_text(errors="ignore")
            return flatten(sub, (base / fname).parent, depth + 1)
        except FileNotFoundError:
            return m.group(0)
        except Exception:
            return m.group(0)

    return _INPUT_RE.sub(rep, tex)


def collect_figs(src: Path, figs: Path):
    figs.mkdir(exist_ok=True)
    for ext in (".png", ".jpg", ".jpeg"):
        for img in src.rglob(f"*{ext}"):
            if img.name.startswith(".") or "__MACOSX" in str(img):
                continue
            try:
                shutil.copy2(img, figs / img.name)
            except Exception:
                pass
    # pdf figures → png via pymupdf
    try:
        import pymupdf
    except ImportError:
        print("⚠ pymupdf not installed; skipping PDF→PNG conversion")
        return
    for pdf in src.rglob("*.pdf"):
        if pdf.name.startswith("."):
            continue
        try:
            doc = pymupdf.open(pdf)
            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=200)
                tag = f"_p{i}" if doc.page_count > 1 else ""
                pix.save(figs / f"{pdf.stem}{tag}.png")
            doc.close()
        except Exception as e:
            print(f"⚠ failed to convert {pdf.name}: {e}")


def strip_latex(s: str) -> str:
    """Strip LaTeX commands for use in plain-text contexts (slug, metadata)."""
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?\{([^}]*)\}", r"\2", s)  # \cmd{x} → x
    s = re.sub(r"\\[a-zA-Z]+\*?", "", s)  # bare \cmd
    s = re.sub(r"[{}]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_metadata(tex: str) -> dict:
    def grab(pattern: str) -> str:
        m = re.search(pattern, tex, re.DOTALL)
        return strip_latex(m.group(1).strip()) if m else ""

    return {
        "title": grab(r"\\title(?:\[[^\]]*\])?\{(.+?)\}"),
        "authors": grab(r"\\author(?:\[[^\]]*\])?\{(.+?)\}"),
    }


def slugify(title: str, arxiv_id: str) -> str:
    if not title:
        return arxiv_id
    s = re.sub(r"[^\w\s-]", "", title).strip().lower()
    s = re.sub(r"[-\s]+", "-", s)
    short = s[:40].rstrip("-")
    return f"{arxiv_id}-{short}" if short else arxiv_id


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="arxiv ID (e.g. 1706.03762) or any URL containing one")
    ap.add_argument("--out-dir", default=".", help="output base dir (default: cwd)")
    args = ap.parse_args()

    arxiv_id = extract_arxiv_id(args.input)
    out_base = Path(args.out_dir).resolve()
    tmp = out_base / f".tmp-{arxiv_id}"
    tmp.mkdir(parents=True, exist_ok=True)

    try:
        src = download_source(arxiv_id, tmp)
        main_tex = find_main_tex(src)
        flat = flatten(main_tex.read_text(errors="ignore"), main_tex.parent)
        meta = extract_metadata(flat)
        slug = slugify(meta["title"], arxiv_id)

        final = out_base / slug
        final.mkdir(parents=True, exist_ok=True)
        (final / "main.tex").write_text(flat)
        (final / "source").mkdir(exist_ok=True)
        for item in list(src.iterdir()):
            target = final / "source" / item.name
            if target.exists():
                shutil.rmtree(target) if target.is_dir() else target.unlink()
            shutil.move(str(item), str(target))
        collect_figs(final / "source", final / "figs")

        metadata = {
            "arxiv_id": arxiv_id,
            "slug": slug,
            "title": meta["title"],
            "authors": meta["authors"],
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "ingested": str(date.today()),
        }
        (final / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False))

        print(f"\n✓ {slug}")
        print(f"  dir:    {final}")
        print(f"  title:  {meta['title'][:80]}")
        print(f"  flat:   {len(flat):,} chars")
        print(f"  figs:   {len(list((final/'figs').iterdir()))}")
        print(f"\nNext steps (the agent does these):")
        print(f"  1. Read {final}/main.tex")
        print(f"  2. Write {final}/note.md following references/note_schema.md")
        print(f"  3. Write {final}/outline.json following references/slide_schema.md")
        print(f"  4. Run: uv run render_slides.py {final}")
        print(f"  5. Run: uv run update_queue.py <queue.md> mark {slug} READING")
    finally:
        if tmp.exists():
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
