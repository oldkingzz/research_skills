# 讲义课的写法与交互组件规范（v1.8，2026-09-18）

> 起因：用户读 Belkhale 2306.02437 第 4 课（转移多样性）时说「云里雾里，核心问题在于我不理解这个实在干什么」，并要求「耐心一点，辅以大量例子，最好能用上 HTML 的丰富特性，用一些图片和交互，token 无限」。按本规范重写后用户评价「非常非常好」，随即要求把其余各课全部按此重构。**本文件是那次重写的可复用提炼。**
>
> 适用范围：`note.html` 的**讲义 tab**。原文对照 tab 不适用（它要的是忠实转写，不是教学）。

---

## 1. 一课的固定骨架（八段，顺序固定）

| 段 | 内容 | 载体 |
|---|---|---|
| ① | **本课要回答的 2–4 个问题**，外加一句读法建议 | `askbox` |
| ② | **零符号的物理直觉**：一个生活化例子，把这一课的核心概念讲清楚，**一个数学符号都不出现** | `exbox` |
| ③ | **交互组件**：让读者拖滑块，亲眼看见②说的那个东西在动 | `lab` |
| ④ | **易混概念辨析**：凡是有两个以上长得像的词，必须给一张对照表 + 一张并排 SVG | `tblwrap` + `svgwrap` |
| ⑤ | **定义 / 定理**，逐项拆解每个符号 | `box` |
| ⑥ | **推导，每一步都写「为什么这么走」**，不是只写「这一步做了什么」 | `dvbox` |
| ⑦ | **带真实数字走一遍**（手算表或交互组件实时算） | `exbox` / `lab` |
| ⑧ | **证据边界**：这一课的结论假设了什么、什么没被验过 | `warnbox` |
| — | 回到原文 | `backbox` |

**②必须在⑤之前。** 用户卡住的根因几乎总是「先看到符号，没看到东西」。

### 关于⑥「为什么这么走」

这是本规范最核心的一条，也是旧版讲义最大的缺陷。每一步推导后面用 `<span class="muted"><b>为什么</b>：…</span>` 补一句，说明**这一步是为了解决什么障碍**。示例（取自第 3 课）：

> **用 log-sum 不等式把两个积分号从 log 里提到外面**，等号变 ≤。
> *为什么*：只要积分还困在 log 里面，就没法把「状态部分」和「动作部分」分开。这一步是整条推导的关键动作，代价就是从此只有不等号。

推导末尾再加一句「把 N 步压成一句话」。

---

## 2. 主场 / 非主场：解释到什么程度

沿用 SKILL.md 硬规矩 10。本文件补一条**可操作的判据**：

> **写完一课后，把所有非主场词列出来，逐个问「我在第一次出现的地方解释了吗」。** 概率论、统计、信息论、优化、控制的术语**全部**算非主场——用户明确说过「我连 marginal 是什么都不知道」「只要进入连续概率论我就没法转过来」。

必须从零讲起的例子（这些在 Belkhale 一篇里就全遇到了）：边缘分布（并说清「边缘」这个名字来自把联合分布表的行加总写在纸的**边缘**上）、期望就是加权平均、KL 散度、熵、erf、无穷范数、支撑集、示性函数、标准误、log-sum 不等式、「intractable」。

**积分号的通用交代**：告诉读者 `∫` 当 `∑` 读，它本身就是拉长的 S（Sum）；离散是可数格子，连续是无限细的格子，动作完全相同。一篇论文里这句话说一次就够。

---

## 3. 交互组件：什么时候做，做什么

### 3.1 判据

做交互组件的唯一理由是：**这个概念「动起来」才说得清**。典型场景四种：

1. **参数扫描**：某个量变大变小会发生什么（σ 拖到 0，落点重叠成一个点）。
2. **两个量的赛跑**：结论取决于比值而非绝对值（系统噪声掩护学生抖动）。
3. **反直觉的极端情形**：把滑块推到端点，看到一个和直觉相反的结果（环境完全确定时覆盖最差）。
4. **公式 vs 实测**：让读者跑蒙特卡洛，和闭式解对一对（P_S 的 2000 次实测）。

**不要为了有交互而做交互。** 静态 SVG 能说清的就用静态 SVG（如三个概念的并排对比图）。

### 3.2 HTML 骨架（照抄）

```html
<div class="lab"><div class="hd"><span class="tag">交互 N</span>一句话说明这个组件在干嘛</div><div class="bd">
<div class="svgwrap"><svg id="xNa_svg" viewBox="0 0 720 300" role="img" aria-label="…"></svg></div>
<div class="ctl">
  <label>参数名</label><input id="xNa_p" type="range" min="0" max="100" value="20"><span class="v" id="xNa_pv">0.20</span>
</div>
<div class="btnrow"><button id="xNa_go">按钮</button></div>
<div class="out">
  <div class="cell hi"><div class="k">读数标题</div><div class="n" id="xNa_out">—</div><div class="meter"><i id="xNa_bar"></i></div></div>
</div>
<div class="rd"><b>做这三件事</b>：① … ② … ③ …<br><span class="muted">诚实标注：哪些是论文的、哪些是我为讲清楚编的模型。</span></div>
</div></div>
```

`rd` 那一段**必须**给出「亲手验这几件事」的具体操作，否则读者不知道该拖什么。

### 3.3 可用 CSS 类（不要自创）

`askbox` `box` `exbox` `dvbox` `warnbox` `backbox` `tblwrap` `svgwrap` `muted` `lbl`
`lab` `hd` `tag` `bd` `ctl` `btnrow` `out` `cell`（+`hi`/`good`/`bad`）`k` `n` `meter`（+`g`/`r`/`p`）`rd` `v`
`num`（编号圆点）`quote`（原文引用块）`lb`（课号标签）`where`（夯实条目的出处行）

**动手前先 `grep -o '^  \.[a-z]*{' note.html` 把该页真实的类名列出来**，不要凭这份清单猜——这份清单本身就漏过 `num` 和 `quote`。

**自创类名没有 CSS，会渲染成裸块。** 第 4 课第一版用了不存在的 `keybox`，就是这么踩的。

### 3.4 JS 硬规矩

1. **每课所有 JS 放在该课末尾的唯一一个 `<script>` 里，包在一个 IIFE 中**；每个组件再各自一个内层 IIFE。
2. **元素 id 一律加课号前缀**（第 3 课 `x3…`，第 5 课 `x5…`），否则跨课撞名。
3. **不要定义或使用 `$`**，页面底部脚本自己有。
4. **SVG 用 `document.createElementNS`**，固定 `viewBox`，**不要测量布局**（组件可能在隐藏的 tab 里，`getBoundingClientRect` 会拿到 0）。
5. **SVG 文本节点里不放 LaTeX**，只用普通字符（σ ε ρ π 直接写）。Q 块标题同理，见 `note_schema_v2.md` §3。
6. **不要用单字母变量名遮蔽外层辅助函数**。第 3 课踩过：内层 `var T = 步数` 把画文字的 `T()` 遮蔽掉，运行时抛异常，**连带把后面所有组件都打断了**（同一个外层 IIFE）。
7. 需要正态随机数就 Box–Muller；需要 `erf` 就用 Abramowitz–Stegun 7.1.26（误差 <1.5e-7），JS 没有内置。

### 3.5 数值必须先在 node 里验过再写进页面

写进页面的每个公式，先用 `node -e` 独立算一遍，和论文的数字或已知真值对照。第 4 课就是这样发现论文那个积分**有闭式解**的（两个独立正态之比服从柯西分布，`q=(2/π)arctan(r)`，与数值积分吻合到 13 位）。

**尤其要检查「界 vs 真实值」这类对比**：第 3 课第一版把**单步**的 KL 和**时间平均**的界放在一起比，结果「上界」比被界住的量还小，等于教错。**两边必须是定理里那两个对象。**

---

## 4. 证据强度分级板（收口课的推荐产物）

最后一课建议做一块「证据强度分级板」：把这篇的**每一条主张**列出来，各自标上它实际靠什么站着，可筛选，带计数。四档：

| 档 | 含义 |
|---|---|
| **定理** | 有证明。但要注明是无条件的，还是建在玩具模型上的 |
| **隔离实验** | 有受控对照，其他变量被固定 |
| **相关观察** | 只是一起变，没有控制变量，不能推因果 |
| **未验证** | 一次实验都没做过 |

每行必须带出处。分级本身标注为 agent 判断。

**这块板子是这套讲义的「taste 层」**：用户要的不只是看懂一篇，而是学会分清「作者说的」和「作者证明的」。Belkhale 那篇 13 条主张里有 4 条属于「未验证」，其中包括它的招牌建议之一。

---

## 5. 验证：每课写完必做

### 5.1 结构（脚本，秒级）

```bash
python3 -c "
s=open('note.html',encoding='utf-8').read()
for t in ['div','svg','table','li','script']:
    print(t, s.count('<'+t)-s.count('</'+t+'>'))"
```
全为 0 才算过。

### 5.2 JS 语法

```bash
python3 -c "
import re;s=open('note.html',encoding='utf-8').read()
open('/tmp/all.js','w').write(''.join(re.findall(r'<script>(.*?)</script>',s,re.S)))"
node --check /tmp/all.js
```

### 5.3 运行时（headless Chrome 探针，比截图可靠）

截图只能看到「长什么样」，看不到「有没有抛异常」。**在页面里注入一段探针，把结果写进 `document.title`，再用 `--dump-dom` 把标题抓出来**：

```js
window.__errs=[];addEventListener("error",e=>__errs.push(e.message+"@"+e.lineno));
addEventListener('load',()=>setTimeout(()=>{
  var ids=[...所有 svg 的 id];
  var empty=ids.filter(i=>!document.getElementById(i)||!document.getElementById(i).childNodes.length);
  var bad=[...document.querySelectorAll('body *')].filter(e=>{
    var r=e.getBoundingClientRect(); if(!(r.width>0&&r.right>innerWidth+2))return false;
    for(var p=e.parentElement;p;p=p.parentElement){var o=getComputedStyle(p).overflowX;
      if(o==='auto'||o==='scroll')return false;}
    return !['path','polyline','polygon','text','rect','line','circle','ellipse','svg','tspan'].includes(e.tagName);});
  document.title='P|err='+(__errs[0]||'none')+'|empty='+(empty.join()||'none')
    +'|Q='+document.getElementById('qlist').children.length
    +'|overflow='+bad.length+'|doc='+document.documentElement.scrollWidth+'/'+innerWidth
    +'|katexErr='+document.querySelectorAll('.katex-error').length;
},5000));   // 至少 5000ms：KaTeX 的 display 公式会二次重排，4200ms 时量到过 doc=720/500 的假阳性
```

```bash
chrome --headless=new --disable-gpu --virtual-time-budget=26000 --window-size=1280,1200 \
  --dump-dom "file://$PWD/probe.html" | grep -o "<title>[^<]*</title>"
```

**两个宽度都要跑：1280 和 500**（headless Chrome 的最小窗宽约 500，比 390 窄的测不了，如实说明即可）。

合格线：`err=none`、`empty=none`、`overflow=0`、`doc` 两个数字相等、`katexErr=0`。

**过滤掉 SVG 内部元素**（path/polyline/text/rect/g/marker/defs…）**和 MathML 节点**（semantics/mrow/math/annotation），它们在 `svgwrap` / `katex-display` 里超出是正常的，否则会刷出一堆假阳性。

**等待时间不能短于 5 秒。** KaTeX 渲染完 display 公式后还会二次重排；在 4.2 秒量到过 `doc=720/500` 的溢出，5 秒后同一页面是 `500/500`。**报溢出之前先加长等待重测一次**，否则会去修一个不存在的 bug。

### 5.4 目视

只在结构和运行时都过了之后再截图。想单看某一课，注入一段脚本把其余 `h2` 及其后续兄弟节点 `display:none`，再整页截图。

---

## 6. 并行重构多课时的工作方式

一次要重写多课时，可以派子代理并行起草，但：

- **子代理绝不直接编辑 `note.html`**（会互相覆盖）。让它们各自把成品写到 scratchpad 下的独立文件，主 agent 负责拼接。
- 简报里必须给全：模板课的位置、可用 CSS 类清单、id 前缀、JS 硬规矩、**必须回 `main.tex` 核对每一个数字**、出处标签纪律、以及「篇幅对齐模板课而不是简报里的估值」。
- 拼接前跑一遍 §5.1 的标签平衡和 class 白名单检查。
- 子代理报告里要求列出：**它核对过的每个数字及其表号、它无法核实因而标成 agent 判断的条目、node --check 结果**。

---

## 7. 这次重写里被推翻的两个做法（别再犯）

1. **「按论文结构写讲义」**。论文的结构是为审稿人写的，不是为初学者写的。讲义必须按**理解的顺序**重排：概念 → 直觉 → 例子 → 定义 → 推导 → 边界。Belkhale 第 4 课原版直接从引理跳到定理，用户完全读不下去。
2. **「把推导写对就够了」**。写对只是及格线。**每一步为什么这么走**才是讲义的价值；缺了这一层，读者只能验证你没算错，学不到怎么自己走一遍。
