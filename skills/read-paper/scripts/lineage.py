# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "requests",
# ]
# ///
"""lineage.py — read-paper v1.7 Step 3.5.

Fetch a paper's references and citations from the Semantic Scholar Graph API and
write <out>/lineage.json. Intermediate artifact for the agent (not a user-facing file).

Usage:
    uv run lineage.py <arxiv-id> --out <paper-dir>/lineage.json [--top 15]

Behaviour:
    - No API key required (public rate limit; retries once on 429).
    - Top-N references and citations ranked by citationCount.
    - On any failure writes {"ok": false, "error": "..."} so the agent can report it.
"""
import argparse, json, sys, time
import requests

API = "https://api.semanticscholar.org/graph/v1"
FIELDS = "title,year,venue,citationCount,externalIds,authors"

def get(url, params, tries=2):
    for i in range(tries):
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 429 and i + 1 < tries:
            time.sleep(3); continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("rate limited")

def compact(p):
    p = p or {}
    ext = p.get("externalIds") or {}
    return {
        "title": p.get("title"),
        "year": p.get("year"),
        "venue": p.get("venue"),
        "citationCount": p.get("citationCount"),
        "arxiv": ext.get("ArXiv"),
        "doi": ext.get("DOI"),
        "firstAuthor": ((p.get("authors") or [{}])[0].get("name")),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arxiv_id")
    ap.add_argument("--out", required=True)
    ap.add_argument("--top", type=int, default=15)
    a = ap.parse_args()
    out = {"ok": False, "arxiv_id": a.arxiv_id, "fetched": time.strftime("%Y-%m-%d")}
    try:
        pid = f"arXiv:{a.arxiv_id}"
        me = get(f"{API}/paper/{pid}", {"fields": FIELDS})
        out["paper"] = compact(me)
        refs = get(f"{API}/paper/{pid}/references", {"fields": FIELDS, "limit": 500}).get("data", [])
        cits = get(f"{API}/paper/{pid}/citations", {"fields": FIELDS, "limit": 500}).get("data", [])
        refs = [compact(x.get("citedPaper")) for x in refs]
        cits = [compact(x.get("citingPaper")) for x in cits]
        key = lambda p: -(p.get("citationCount") or 0)
        out["references_total"] = len(refs)
        out["citations_total"] = len(cits)
        out["references_top"] = sorted([r for r in refs if r.get("title")], key=key)[: a.top]
        out["citations_top"] = sorted([c for c in cits if c.get("title")], key=key)[: a.top]
        out["ok"] = True
    except Exception as e:  # noqa: BLE001
        out["error"] = f"{type(e).__name__}: {e}"
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(("ok" if out["ok"] else "FAILED: " + out.get("error", "")), "->", a.out)
    sys.exit(0 if out["ok"] else 1)

if __name__ == "__main__":
    main()
