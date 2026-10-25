# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 1 周第 3 章配图：三张表在年报里的位置，以及它们各自回答什么问题。

左侧是一条「时间轴—页码」标尺，右侧三个方框分别对应资产负债表 / 利润表 / 现金流量表，
框里给出页码、第一行、末行和伊利 2024 年的关键数字。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, fig_ax, box, arrow, label,
    C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_PURPLE,
    F_BLUE, F_ORANGE, F_GREEN, F_GRAY, F_PURPLE,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
assets = d["balance"]["total_assets"] / 1e8
np_parent = d["income"]["net_profit_parent"] / 1e8
ocf = d["cashflow"]["operating_net"] / 1e8

fig, ax = fig_ax(13.8, 8.4, xlim=(0, 100), ylim=(0, 100))

ax.text(50, 96.0, "三张表挨着放，从 page_087 到 page_095",
        ha="center", va="center", fontsize=15, weight="bold", color="#1a1a1a")
ax.text(50, 91.3, "它们三个连起来回答一个问题：这家公司一年下来，家底变厚了没有、为什么",
        ha="center", va="center", fontsize=11.2, color=C_GRAY)

# ── 页码标尺 ────────────────────────────────────────────────
def page_x(p):
    return 8 + (p - 80) / 20 * 84

ax.plot([page_x(80), page_x(97)], [83.5, 83.5], color=C_GRAY, lw=1.6, zorder=2)
for p in (80, 85, 87, 90, 92, 95, 97):
    ax.plot([page_x(p), page_x(p)], [82.3, 84.7], color=C_GRAY, lw=1.4, zorder=2)
    ax.text(page_x(p), 87.2, f"p{p}", ha="center", va="center",
            fontsize=9.8, color=C_GRAY)

# 三张表在标尺上的区间
spans = [(87, 88, C_BLUE, "资产负债表 p87–88"),
         (91, 92, C_GREEN, "利润表 p91–92"),
         (94, 95, C_ORANGE, "现金流量表 p94–95")]
for start, end, c, name in spans:
    x0, x1 = page_x(start - 0.6), page_x(end + 0.6)
    ax.plot([x0, x1], [80.6, 80.6], color=c, lw=7, solid_capstyle="round", zorder=4)
    ax.text((x0 + x1) / 2, 78.2, name, ha="center", va="center",
            fontsize=10.2, color=c, weight="bold")

# ── 三张表详情 ──────────────────────────────────────────────
cards = [
    (2.5, "资产负债表（balance sheet）", "page_087–088",
     "2024 年 12 月 31 日这一天\n公司有多少东西、欠多少、剩多少",
     f"资产总计 {assets:,.2f} 亿元", C_BLUE, F_BLUE),
    (34.5, "利润表（income statement）", "page_091–092",
     "2024 年 1—12 月这一年\n收入减成本费用，赚了多少",
     f"归母净利润 {np_parent:,.2f} 亿元", C_GREEN, F_GREEN),
    (66.5, "现金流量表（cash flow statement）", "page_094–095",
     "2024 年这一年\n钱实际进出了多少",
     f"经营现金流净额 {ocf:,.2f} 亿元", C_ORANGE, F_ORANGE),
]
for x, title, page, what, key, c, fc in cards:
    box(ax, x, 30.0, 30.5, 40.0, "", fc=fc, ec=c, lw=1.7)
    ax.text(x + 15.25, 65.0, title, ha="center", va="center",
            fontsize=11.4, weight="bold", color=c)
    ax.text(x + 15.25, 60.6, page, ha="center", va="center",
            fontsize=10.5, color=C_GRAY)
    ax.text(x + 15.25, 51.5, what, ha="center", va="center",
            fontsize=10.4, color="#333333", linespacing=1.7)
    ax.plot([x + 3, x + 27.5], [44.0, 44.0], color=c, lw=1.0, alpha=0.45, zorder=4)
    ax.text(x + 15.25, 37.6, key, ha="center", va="center",
            fontsize=11.0, color=c, weight="bold")

for x in (17.75, 49.75):
    arrow(ax, (x + 8.6, 24.0), (x + 13.4, 24.0), color=C_GRAY, lw=1.8)

# ── 底部：报表末页的签名行 ───────────────────────────────────
label(ax, 50, 19.6,
      "每张表末页都有一行签名：公司负责人 潘刚 · 主管会计工作负责人 赵成霞 · 会计机构负责人 邹赢",
      fontsize=10.6, color="#333333")

box(ax, 8, 5.2, 84, 10.6,
    "看不清就先记住这个顺序：先看利润表（赚没赚）→ 再看资产负债表（家底厚不厚）"
    "→ 最后看现金流量表（利润是不是真的）",
    fc=F_GRAY, ec=C_GRAY, fontsize=11.0)

ax.text(99, 1.2, "数据来源：伊利 2024 年报 page_087、page_091、page_092、page_094",
        ha="right", va="center", fontsize=9.3, color=C_GRAY)

save(fig, "w01d3_three_statements_position.png")
