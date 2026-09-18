# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""card_svg.py — 一屏卡图片版生成器(read-paper v1.7.1;09-12 第二版:860 宽、字 14、高度按内容算)。规范见 references/card_image_schema.md。

Usage:
    python3 card_svg.py card.json --out card.svg

card.json 字段(全部为字符串,除非注明):
{
  "title": "中文标题(≤30 字)",
  "meta": "作者 · 发表 · 读于",
  "stand": "AI 镜",            # 主要成立于哪一镜
  "empty": "ML 镜",            # 哪一镜空;没有空镜时改用 "badge": "主要成立于 AI + ML 镜 · Robotics 镜软" 整句
  "spine": "≤100 字",
  "lineage": [                 # 恰好 5 项,顺序固定
    {"k": "来处", "t": "≤52 字", "src": "[原句 Sec 1]"},
    {"k": "当时的极限", ...}, {"k": "弊病", ...}, {"k": "动作与代价", ...}, {"k": "去处", ...}
  ],
  "lenses": [                  # 恰好 3 项
    {"k": "Robotics", "t": "≤64 字", "v": "硬"},   # v ∈ 硬/软/空
    {"k": "AI", ...}, {"k": "ML", ...}
  ],
  "grid_names": ["监督从哪来","teacher 给什么","student 怎么学","部署差距"],
  "grid": ["≤40 字", "…", "…", "…"],
  "bounds": ["≤34 字", "…", "…"],   # ≤3 条
  "verdict": "≤70 字",
  "nail": "≤160 字(脚本自动补「候选,未验证」)",
  "terms": [{"k": "RRT", "t": "≤110 字白话解释"}, ...]   # 卡上出现的每个缩写 / 专有名词都要有
}
超出字数或行数直接报错,不缩字号。
"""
import argparse, json, sys
from xml.sax.saxutils import escape

INK, SUB, LINE = "#1a1d23", "#5a6270", "#e3e6eb"
BLUE, BLUE_S = "#0f62fe", "#eef4ff"
GREEN, GREEN_S = "#0e6027", "#e9f6ec"
YEL, YEL_S = "#8a6a00", "#fff8e1"
RED, RED_S = "#a2191f", "#ffefef"
PUR, PUR_S = "#8a3ffc", "#f6f0ff"
FONT = '-apple-system, "PingFang SC", "Hiragino Sans GB", sans-serif'
VERDICT_COLOR = {"硬": (GREEN, GREEN_S), "软": (YEL, YEL_S), "空": (RED, RED_S)}

def em(ch):
    return 1.0 if ord(ch) > 0x2E7F else 0.55

def count(s):
    return sum(em(c) for c in s)

NO_HEAD = set(",.;:!?)]}%,。;:!?)】”』」、")   # 不能出现在行首的标点
NO_TAIL = set("「『“(([【")                      # 不能落在行尾的开引号 / 开括号

def _tokens(text):
    """中文逐字成 token;连续的 ASCII 字母数字(含 - / . %)整词成 token;空格独立。"""
    toks, cur = [], ""
    for ch in text:
        if ch.isascii() and (ch.isalnum() or ch in "-./%_+"):
            cur += ch
        else:
            if cur: toks.append(cur); cur = ""
            toks.append(ch)
    if cur: toks.append(cur)
    return toks

def wrap(text, width_px, size):
    """greedy wrap by estimated glyph width; ASCII words are not split; no leading punctuation."""
    max_em = width_px / size
    lines, cur, cur_w = [], "", 0.0
    for tk in _tokens(text):
        w = count(tk)
        if cur and cur_w + w > max_em and tk not in NO_HEAD:
            carry = ""
            if cur and cur[-1] in NO_TAIL:      # 行尾的开引号带到下一行
                carry = cur[-1]; cur = cur[:-1]
            lines.append(cur.rstrip()); cur, cur_w = carry, count(carry)
            if tk == " ": continue
        cur += tk; cur_w += w
    if cur.strip(): lines.append(cur.rstrip())
    return lines

def text_block(x, y, text, width, size, max_lines, fill=INK, weight="normal", lh=1.45, what=""):
    lines = wrap(text, width, size)
    if len(lines) > max_lines:
        raise SystemExit(f"[card_svg] '{what}' 需要 {len(lines)} 行,上限 {max_lines} 行({count(text):.0f} 字)。删字,不缩字号。")
    out = []
    for i, ln in enumerate(lines):
        out.append(f'<text x="{x}" y="{y + i*size*lh:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(ln)}</text>')
    return "\n".join(out), y + len(lines)*size*lh

def check(name, text, limit):
    c = count(text)
    if c > limit:
        raise SystemExit(f"[card_svg] '{name}' {c:.0f} 字,上限 {limit}。")

def rect(x, y, w, h, fill, stroke, r=8, sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def badge(x, y, label, color, bg):
    w = count(label) * 12 + 16
    return (f'<rect x="{x}" y="{y-13}" width="{w:.0f}" height="20" rx="10" fill="{bg}" stroke="{color}"/>'
            f'<text x="{x+8}" y="{y+1}" font-size="12" font-weight="700" fill="{color}">{escape(label)}</text>'), w


W, M = 860, 16          # 画布宽、外边距;内容栏 851 px 时约 1:1 显示
BODY, LAB, SRC = 14, 13.5, 11.5
LH = 1.45

def lineh(size): return size * LH

def build(d):
    # ---- limits(见 card_image_schema.md §2)
    check("title", d["title"], 30); check("spine", d["spine"], 150)
    assert len(d["lineage"]) == 5 and len(d["lenses"]) == 3 and len(d["grid"]) == 4 and len(d["bounds"]) <= 3
    for n in d["lineage"]: check("脉络·"+n["k"], n["t"], 100); check("出处", n.get("src",""), 12)
    for l in d["lenses"]: check("三镜·"+l["k"], l["t"], 120); assert l["v"] in VERDICT_COLOR
    for i, g in enumerate(d["grid"]): check(f"四格{i+1}", g, 90)
    for b in d["bounds"]: check("边界", b, 60)
    check("verdict", d["verdict"], 120); check("nail", d["nail"], 160)
    for t in d.get("terms", []): check("名词·"+t["k"], t["t"], 110)

    S = []  # body; header appended at the end once height is known
    inner = W - 2*M
    # ① 标题带
    lab = d.get("badge") or f'主要成立于 {d["stand"]} · {d["empty"]}空'   # 没有空镜时用 badge 字段直接给整句
    bw = count(lab)*12.5 + 20
    S.append(f'<text x="{M}" y="32" font-size="21" font-weight="800">{escape(d["title"])}</text>')
    S.append(rect(W-M-bw, 13, bw, 27, BLUE_S, BLUE, r=13))
    S.append(f'<text x="{W-M-bw+10}" y="31" font-size="12.5" font-weight="700" fill="{BLUE}">{escape(lab)}</text>')
    t, y = text_block(M, 57, d["meta"], inner, 12, 2, fill=SUB, what="meta"); S.append(t)
    y += 8
    # ② 脊椎带
    lines = wrap(d["spine"], inner-72, 15)
    if len(lines) > 5: raise SystemExit("[card_svg] spine 超过 5 行,删字。")
    h = 16 + len(lines)*lineh(15) + 10
    S.append(rect(M, y, inner, h, BLUE_S, BLUE))
    S.append(f'<text x="{M+12}" y="{y+25}" font-size="{LAB}" font-weight="800" fill="{BLUE}">脊椎</text>')
    t, _ = text_block(M+60, y+25, d["spine"], inner-72, 15, 5, what="spine"); S.append(t)
    y += h + 14
    # ③ 双栏带:左 脉络 / 右 三镜 + 钉子候选
    top = y
    LW = 404; RX = M + LW + 12; RW = inner - LW - 12
    L = []; ly = top + 48
    L.append(f'<text x="{M+12}" y="{top+22}" font-size="{LAB}" font-weight="800" fill="{BLUE}">脉络</text>')
    for n in d["lineage"]:
        L.append(f'<circle cx="{M+28}" cy="{ly-5}" r="5" fill="{BLUE}"/>')
        L.append(f'<text x="{M+42}" y="{ly}" font-size="{BODY}" font-weight="700">{escape(n["k"])}</text>')
        kx = M+42 + count(n["k"])*BODY + 8
        L.append(f'<text x="{kx:.0f}" y="{ly}" font-size="{SRC}" fill="{SUB}">{escape(n.get("src",""))}</text>')
        t, y2 = text_block(M+42, ly+20, n["t"], LW-42-24, BODY, 6, what="脉络·"+n["k"]); L.append(t)
        ly = y2 + 12
    left_end = ly - 2
    L.insert(1, f'<line x1="{M+28}" y1="{top+36}" x2="{M+28}" y2="{left_end-22}" stroke="{BLUE}" stroke-width="2"/>')
    R = []; ry = top + 36
    R.append(f'<text x="{RX+12}" y="{top+22}" font-size="{LAB}" font-weight="800" fill="{BLUE}">三镜</text>')
    for l in d["lenses"]:
        col, bg = VERDICT_COLOR[l["v"]]
        lines = wrap(l["t"], RW-48, BODY)
        if len(lines) > 6: raise SystemExit(f"[card_svg] 三镜·{l['k']} 超过 6 行,删字。")
        h = 32 + len(lines)*lineh(BODY) + 8
        R.append(rect(RX+12, ry, RW-24, h, bg, col, r=6))
        R.append(f'<text x="{RX+24}" y="{ry+21}" font-size="{BODY}" font-weight="700" fill="{col}">{escape(l["k"])}</text>')
        b, _ = badge(RX+24 + count(l["k"])*BODY + 10, ry+18, l["v"], col, "#fff"); R.append(b)
        t, _ = text_block(RX+24, ry+44, l["t"], RW-48, BODY, 6, what="三镜·"+l["k"]); R.append(t)
        ry += h + 8
    R.append(f'<text x="{RX+12}" y="{ry+12}" font-size="{LAB}" font-weight="700" fill="{BLUE}">{escape(lab)}</text>')
    ry += 30
    nail = d["nail"].rstrip("。") + "。候选,未验证。"
    lines = wrap(nail, RW-48, LAB)
    if len(lines) > 8: raise SystemExit("[card_svg] nail 超过 8 行,删字。")
    h = 32 + len(lines)*lineh(LAB) + 8
    R.append(rect(RX+12, ry, RW-24, h, RED_S, RED, r=6, sw=1.5))
    R.append(f'<text x="{RX+24}" y="{ry+21}" font-size="{BODY}" font-weight="700" fill="{RED}">钉子候选</text>')
    t, _ = text_block(RX+24, ry+44, nail, RW-48, LAB, 8, what="nail"); R.append(t)
    ry += h
    right_end = ry
    bh = max(left_end, right_end) - top + 14
    S.append(rect(M, top, LW, bh, "#fff", LINE)); S.append(rect(RX, top, RW, bh, "#fff", LINE))
    S.extend(L); S.extend(R)
    y = top + bh + 14
    # ④ 四格带
    S.append(f'<text x="{M}" y="{y+14}" font-size="{LAB}" font-weight="800" fill="{PUR}">四格地图</text>')
    gy = y + 24; gw = (inner - 3*12) / 4
    gl = [wrap(g, gw-20, LAB) for g in d["grid"]]
    if max(len(x) for x in gl) > 8: raise SystemExit("[card_svg] 四格某格超过 8 行,删字。")
    gh = 34 + max(len(x) for x in gl)*lineh(LAB) + 8
    for i in range(4):
        x = M + i*(gw+12)
        S.append(rect(x, gy, gw, gh, PUR_S, PUR, r=6))
        S.append(f'<text x="{x+10}" y="{gy+21}" font-size="{LAB}" font-weight="700" fill="{PUR}">{"①②③④"[i]} {escape(d["grid_names"][i])}</text>')
        t, _ = text_block(x+10, gy+43, d["grid"][i], gw-20, LAB, 8, what=f"四格{i+1}"); S.append(t)
    y = gy + gh + 14
    # ⑤ 底带:边界 / 一句话裁决
    bl = [wrap("· "+b, LW-24, LAB) for b in d["bounds"]]
    if any(len(x) > 3 for x in bl): raise SystemExit("[card_svg] 边界某条超过 3 行,删字。")
    vl = wrap(d["verdict"], RW-24, BODY)
    if len(vl) > 6: raise SystemExit("[card_svg] verdict 超过 6 行,删字。")
    hb = 32 + sum(len(x) for x in bl)*lineh(LAB) + 8
    hv = 32 + len(vl)*lineh(BODY) + 8
    h = max(hb, hv)
    S.append(rect(M, y, LW, h, YEL_S, YEL, r=6))
    S.append(f'<text x="{M+12}" y="{y+21}" font-size="{BODY}" font-weight="700" fill="{YEL}">边界</text>')
    by = y + 44
    for b in d["bounds"]:
        t, by = text_block(M+12, by, "· "+b, LW-24, LAB, 3, what="边界"); S.append(t)
    S.append(rect(RX, y, RW, h, GREEN_S, GREEN, r=6))
    S.append(f'<text x="{RX+12}" y="{y+21}" font-size="{BODY}" font-weight="700" fill="{GREEN}">一句话裁决</text>')
    t, _ = text_block(RX+12, y+44, d["verdict"], RW-24, BODY, 6, what="verdict"); S.append(t)
    y = y + h + 14
    # ⑥ 名词带:卡上出现的每一个缩写 / 专有名词,一行白话解释;两栏
    terms = d.get("terms", [])
    if terms:
        S.append(f'<text x="{M}" y="{y+14}" font-size="{LAB}" font-weight="800" fill="{SUB}">名词(卡上出现过的词,默认你没见过)</text>')
        ty0 = y + 24; cw = (inner - 12) / 2
        cols = [[], []]; cy = [ty0 + 26, ty0 + 26]
        for i, t in enumerate(terms):
            c = i % 2; x = M + c*(cw+12) + 12
            lines = wrap(t["t"], cw-24-count(t["k"])*LAB-8, LAB) if False else None
            cols[c].append(f'<text x="{x}" y="{cy[c]}" font-size="{LAB}" font-weight="700">{escape(t["k"])}</text>')
            kx = x + count(t["k"])*LAB + 8
            first_w = cw - 24 - (kx - x)
            # 第一行接在词后面,后续行回到左边
            toks = wrap(t["t"], first_w, LAB)
            first = toks[0] if toks else ""
            rest = "".join(toks[1:])
            cols[c].append(f'<text x="{kx:.0f}" y="{cy[c]}" font-size="{LAB}" fill="{INK}">{escape(first)}</text>')
            yy = cy[c] + lineh(LAB)
            if rest:
                tb, yy = text_block(x, yy, rest, cw-24, LAB, 5, what="名词·"+t["k"])
                cols[c].append(tb)
            cy[c] = yy + 6
        th = max(cy) - ty0 + 4
        S.append(rect(M, ty0, cw, th, "#fff", LINE, r=6)); S.append(rect(M+cw+12, ty0, cw, th, "#fff", LINE, r=6))
        S.extend(cols[0]); S.extend(cols[1])
        y = ty0 + th
    H = int(y + M)
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family=\'{FONT}\' fill="{INK}">',
            f'<rect width="{W}" height="{H}" fill="#fbfbfc"/>']
    return "\n".join(head + S + ["</svg>"])

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("json"); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = json.load(open(a.json, encoding="utf-8"))
    svg = build(d)
    open(a.out, "w", encoding="utf-8").write(svg)
    print("ok ->", a.out, f"({len(svg)} bytes)")

if __name__ == "__main__":
    main()
