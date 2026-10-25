# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 9 周第 44 章配图：20 条财务红旗的命中矩阵（伊利 vs 蒙牛，2024）。

这是一张「热力表」：三种状态一目了然。
- 命中（红）：触发了追问，需要翻附注解释——命中不等于有问题；
- 未命中（绿）：这一年没触发；
- 数据不足（灰）：年报没披露到能判断的颗粒度，老实标出来，不硬判。

判定依据（金额、页码）写在正文第 44 章的表里；本图不放长注释，只放结论。
金额与比值全部由 data/yili2024.json、data/mengniu2024.json 现场计算。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.patches as mpatches  # noqa: E402

from figures._common import save, fig_ax, C_GRAY  # noqa: E402
from figures._data import load  # noqa: E402

d = load("yili2024")
m = load("mengniu2024")

# ── 先算几条关键比值，判定才有依据 ─────────────────────────────────
yb, ycf, yi_ = d["balance"], d["cashflow"], d["income"]
mb = m["balance"]

y_gw = yb["goodwill"] / yb["equity_parent"]
y_nr = d["nonrecurring"]["total"] / yi_["net_profit_parent"]
y_ocf_np = ycf["operating_net"] / yi_["net_profit"]
y_cash = d["ratios"]["cash_and_deposits"] / 1e8
y_ibd = d["ratios"]["interest_bearing_debt"] / 1e8

m_gw = mb["goodwill"] / mb["equity_parent"]
m_cash = (mb["cash"] + 14_006_079_000.0) / 1e8

RED, GREEN, GRAY = "#c0392b", "#1e8449", "#8a8a8a"
FRED, FGREEN, FGRAY = "#fbeaea", "#eef7ee", "#f2f2f2"

HIT, MISS, NA = "命中", "未命中", "数据不足"
STYLE = {HIT: (RED, FRED), MISS: (GREEN, FGREEN), NA: (GRAY, FGRAY)}

flags = [
    ("① 经营现金流长期显著低于净利润", MISS, MISS),
    ("② 应收账款增速远超收入增速", MISS, MISS),
    ("③ 存货增速远超收入增速", MISS, MISS),
    ("④ 毛利率显著高于同行且无法解释", MISS, HIT),
    ("⑤ 商誉占净资产比例过高", HIT, HIT),
    ("⑥ 频繁并购", MISS, HIT),
    ("⑦ 大存大贷（账上钱多还大量借钱）", HIT, HIT),
    ("⑧ 其他应收款异常大", MISS, MISS),
    ("⑨ 预付账款异常大", MISS, MISS),
    ("⑩ 在建工程长期不转固", MISS, MISS),
    ("⑪ 研发资本化率突然升高", MISS, NA),
    ("⑫ 非经常性损益占利润比重高", HIT, HIT),
    ("⑬ 第四季度利润异常", HIT, NA),
    ("⑭ 审计意见非标或更换审计师", MISS, MISS),
    ("⑮ 关联交易占比高", HIT, NA),
    ("⑯ 控股股东高比例质押", MISS, MISS),
    ("⑰ 频繁更换财务总监", MISS, NA),
    ("⑱ 应付账款周转天数异常拉长", MISS, MISS),
    ("⑲ 递延所得税资产异常增长", MISS, MISS),
    ("⑳ 报表勾稽不平", MISS, MISS),
]

n_y_hit = sum(1 for f in flags if f[1] == HIT)
n_m_hit = sum(1 for f in flags if f[2] == HIT)
n_m_na = sum(1 for f in flags if f[2] == NA)

fig, ax = fig_ax(13.2, 10.2, xlim=(0, 100), ylim=(0, 100))

ax.text(50, 97.4,
        f"20 条红旗扫描：伊利命中 {n_y_hit} 条、蒙牛命中 {n_m_hit} 条，"
        "没有一条能单独定罪",
        ha="center", va="center", fontsize=14.6, weight="bold", color="#1a1a1a")
ax.text(50, 93.9, "「命中」只代表需要追问一句；能不能解释，才决定它是噪声还是警报",
        ha="center", va="center", fontsize=10.2, color=C_GRAY)

# ── 表头 ───────────────────────────────────────────────────────────
x_name = 4.0
x_y, w_y = 57.0, 17.0
x_m, w_m = 77.0, 17.0
head_y = 89.4
ax.text(x_name, head_y, "红旗信号", ha="left", va="center",
        fontsize=11.4, weight="bold", color="#333333")
ax.text(x_y + w_y / 2, head_y, "伊利 2024", ha="center", va="center",
        fontsize=11.4, weight="bold", color="#333333")
ax.text(x_m + w_m / 2, head_y, "蒙牛 2024", ha="center", va="center",
        fontsize=11.4, weight="bold", color="#333333")
ax.plot([4, 96], [87.0, 87.0], color="#c8c8c8", lw=1.3)

row_h = 3.62
top = 85.0
for k, (name, ys, ms) in enumerate(flags):
    yc = top - k * row_h - row_h / 2
    if k % 2 == 0:
        ax.add_patch(mpatches.Rectangle((4.0, yc - row_h / 2), 92.0, row_h,
                                        fc="#fbfbfb", ec="none", zorder=0))
    ax.text(x_name, yc, name, ha="left", va="center", fontsize=10.0,
            color="#1a1a1a", zorder=4)

    for x0, w0, st in ((x_y, w_y, ys), (x_m, w_m, ms)):
        ec, fc = STYLE[st]
        ax.add_patch(mpatches.FancyBboxPatch(
            (x0, yc - 1.35), w0, 2.7,
            boxstyle="round,pad=0.02,rounding_size=0.55",
            fc=fc, ec=ec, lw=1.25, zorder=2))
        ax.text(x0 + w0 / 2, yc, st, ha="center", va="center",
                fontsize=9.6, weight="bold", color=ec, zorder=4)



# ── 图例（图外下方，横排）──────────────────────────────────────────
ly = 3.4
lx = 4.0
for st in (HIT, MISS, NA):
    ec, fc = STYLE[st]
    ax.add_patch(mpatches.FancyBboxPatch(
        (lx, ly - 1.05), 7.6, 2.1,
        boxstyle="round,pad=0.02,rounding_size=0.45",
        fc=fc, ec=ec, lw=1.25, zorder=3))
    ax.text(lx + 3.8, ly, st, ha="center", va="center", fontsize=9.4,
            weight="bold", color=ec, zorder=5)
    lx += 9.0

ax.text(96.0, 8.4,
        f"伊利命中 {n_y_hit} 条：⑤商誉 4.4%、⑦大存大贷、⑫非经常 28.9%、⑬Q4 亏损 24.16 亿、⑮关联采购 19.8%",
        ha="right", va="center", fontsize=8.8, color="#333333")
ax.text(96.0, 6.3,
        f"蒙牛命中 {n_m_hit} 条、{n_m_na} 条数据不足；港股披露口径与 A 股不同，缺数据就标缺，不硬判",
        ha="right", va="center", fontsize=8.8, color="#333333")
ax.text(50.0, 0.7,
        "数据：伊利 2024 年报 page_007~095、page_210、page_227；蒙牛 2024 年报 page_048、page_131、page_140~148、page_244",
        ha="center", va="center", fontsize=8.2, color=C_GRAY)

save(fig, "w09d4_flag_matrix.png")
