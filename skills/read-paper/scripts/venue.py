# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""venue.py — 查一篇 arXiv 论文的录用情况(read-paper Step 3.6,2026-09-14 用户要求)。

Usage:
    python3 venue.py <arxiv-id> [--out <paper-dir>/venue.json]

做三件事,只报事实,不猜:
  1. arXiv API:标题、作者备注(comments,作者常写 "Accepted to CoRL 2025")、journal_ref、DOI、最新版本日期
  2. Semantic Scholar:venue / publicationVenue / 被引数
  3. 打印两条建议的网络搜索词(奖项只能靠搜:会议官网 awards 页、OpenReview、作者主页)
输出 JSON:{"ok":bool,"arxiv":{...},"s2":{...},"search_queries":[...],"award":null}
award 字段脚本永远写 null;agent 搜到有来源的奖项后手动填 {"name":..., "source":url}。
"""
import argparse, json, sys, re, urllib.request, urllib.parse, xml.etree.ElementTree as ET

UA = {"User-Agent": "read-paper-skill/1.0 (venue check)"}

def get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8")

def arxiv(aid):
    xml = get(f"http://export.arxiv.org/api/query?id_list={aid}")
    ns = {"a": "http://www.w3.org/2005/Atom", "ar": "http://arxiv.org/schemas/atom"}
    e = ET.fromstring(xml).find("a:entry", ns)
    if e is None: return {"error": "no entry"}
    def t(tag, nsk="a"):
        x = e.find(f"{nsk}:{tag}", ns); return x.text.strip() if x is not None and x.text else None
    return {"title": re.sub(r"\s+", " ", t("title") or ""), "published": t("published"), "updated": t("updated"),
            "comment": t("comment", "ar"), "journal_ref": t("journal_ref", "ar"), "doi": t("doi", "ar")}

def s2(aid):
    fields = "title,venue,publicationVenue,year,citationCount,externalIds,publicationTypes"
    try:
        d = json.loads(get(f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{aid}?fields={fields}"))
    except Exception as ex:
        return {"error": str(ex)}
    pv = d.get("publicationVenue") or {}
    return {"venue": d.get("venue"), "publicationVenue": pv.get("name"), "venue_type": pv.get("type"),
            "year": d.get("year"), "citationCount": d.get("citationCount"),
            "doi": (d.get("externalIds") or {}).get("DOI"), "publicationTypes": d.get("publicationTypes")}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("arxiv_id"); ap.add_argument("--out")
    a = ap.parse_args()
    out = {"ok": True, "arxiv_id": a.arxiv_id, "award": None}
    try: out["arxiv"] = arxiv(a.arxiv_id)
    except Exception as ex: out["arxiv"] = {"error": str(ex)}; out["ok"] = False
    out["s2"] = s2(a.arxiv_id)
    title = (out["arxiv"].get("title") or "")
    out["search_queries"] = [f'"{title}" accepted', f'"{title}" best paper award', f'"{title}" openreview']
    # 一行结论(只从字段里读,不推断)
    hints = []
    c = out["arxiv"].get("comment") or ""
    if re.search(r"accept|to appear|published|proceedings|camera[- ]ready", c, re.I): hints.append(f"arXiv 备注: {c}")
    if out["arxiv"].get("journal_ref"): hints.append(f"journal_ref: {out['arxiv']['journal_ref']}")
    if out["s2"].get("publicationVenue"): hints.append(f"S2 venue: {out['s2']['publicationVenue']}")
    elif out["s2"].get("venue"): hints.append(f"S2 venue: {out['s2']['venue']}")
    out["hints"] = hints or ["字段里没有录用信息;按 search_queries 搜,搜不到就写「未查到」"]
    s = json.dumps(out, ensure_ascii=False, indent=2)
    if a.out: open(a.out, "w", encoding="utf-8").write(s); print("ok ->", a.out)
    print(s)

if __name__ == "__main__":
    main()
