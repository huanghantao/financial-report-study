# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 1 周第 1 章配图：清偿顺序，以及伊利 2024 年 1,537.18 亿元最后归谁。

上半部分是「谁先拿」的顺序阶梯，下半部分是「扣完还剩多少」的减法链。
所有公司数字来自 data/yili2024.json；页码是 raw 年报的文件编号。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, fig_ax, box, arrow, label,
    C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_PURPLE, C_RED,
    F_BLUE, F_ORANGE, F_GREEN, F_GRAY, F_PURPLE, F_RED,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
assets = d["balance"]["total_assets"] / 1e8          # 1,537.18
liab = d["balance"]["total_liabilities"] / 1e8       # 967.10
equity_parent = d["balance"]["equity_parent"] / 1e8  # 531.80
minority = d["balance"]["minority_interest"] / 1e8   # 38.28
equity_total = d["balance"]["total_equity"] / 1e8    # 570.08
wage = d["balance"]["employee_compensation_payable"] / 1e8  # 37.77
tax = d["balance"]["taxes_payable"] / 1e8                   # 8.50

fig, ax = fig_ax(13, 8.8, xlim=(0, 100), ylim=(0, 100))

ax.text(50, 96.5, "1,537.18 亿元先分给谁：员工和税在前，股东排最后",
        ha="center", va="center", fontsize=15.5, weight="bold", color="#1a1a1a")
ax.text(50, 91.8,
        "上半：清偿顺序（越靠上越先拿）　　下半：扣掉所有欠款之后，才轮到股东",
        ha="center", va="center", fontsize=11.5, color=C_GRAY)

# ── 上半：四级阶梯 ────────────────────────────────────────────────
rows = [
    ("①  员工工资与社保", f"账面还欠 {wage:,.2f} 亿元", F_ORANGE, C_ORANGE),
    ("②  各项税款", f"账面还欠 {tax:,.2f} 亿元", F_ORANGE, C_ORANGE),
    ("③  债权人本息", f"负债合计 {liab:,.2f} 亿元", F_RED, C_RED),
    ("④  全体股东", f"所有者权益 {equity_total:,.2f} 亿元", F_PURPLE, C_PURPLE),
]
top = 86.0
h = 9.2
for i, (name, amount, fc, ec) in enumerate(rows):
    y = top - i * 12.2
    box(ax, 20, y - h, 60, h, "", fc=fc, ec=ec, lw=1.8)
    ax.text(23, y - h / 2, name, ha="left", va="center",
            fontsize=13, weight="bold", color="#1a1a1a")
    ax.text(77, y - h / 2, amount, ha="right", va="center",
            fontsize=12.5, color=ec, weight="bold")
    if i < 3:
        arrow(ax, (50, y - h - 0.4), (50, y - 12.2 + 0.4), color=C_GRAY, lw=1.6)

ax.text(20, top + 2.0, "先拿 →", ha="left", va="center", fontsize=11, color=C_GRAY)
ax.text(80, top + 2.0, "最后拿、拿剩的", ha="right", va="center", fontsize=11, color=C_GRAY)

# ── 下半：减法链 ────────────────────────────────────────────────
ax.text(50, 33.5, "账面「净资产」是这么剩下的", ha="center", va="center",
        fontsize=12.5, weight="bold", color="#1a1a1a")

box(ax, 4, 12, 25, 15,
    f"公司全部资产\n{assets:,.2f} 亿元", fc=F_BLUE, ec=C_BLUE, fontsize=12.5)
arrow(ax, (30.2, 19.5), (36.6, 19.5), color=C_RED, lw=2.0)
label(ax, 33.4, 24.0, f"减 负债\n{liab:,.2f}", color=C_RED, fontsize=10.5)

box(ax, 37.8, 12, 24, 15,
    f"净资产\n{equity_total:,.2f} 亿元", fc=F_GREEN, ec=C_GREEN, fontsize=12.5)
arrow(ax, (63.0, 19.5), (69.4, 19.5), color=C_GRAY, lw=2.0)
label(ax, 66.2, 24.0, f"减 少数股东\n{minority:,.2f}", color=C_GRAY, fontsize=10.5)

box(ax, 70.6, 12, 25, 15,
    f"归母权益\n{equity_parent:,.2f} 亿元", fc=F_PURPLE, ec=C_PURPLE,
    fontsize=12.5, weight="bold")

label(ax, 50, 6.2,
      "① ② 是账面「还欠着」的数，已经包含在 ③ 的 967.10 亿元里，不能和 ③ 相加；"
      "④ 排最后，因为它是「剩下的」。",
      fontsize=10.8, color="#333333", ha="center")

ax.text(99, 1.2, "数据来源：伊利 2024 年报 page_087、page_088",
        ha="right", va="center", fontsize=9.5, color=C_GRAY)

save(fig, "w01d1_priority_waterfall.png")
