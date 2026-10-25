# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 9 周第 42 章配图：杜邦树（伊利 2024，平均余额口径）。

ROE = 净利率 x 资产周转率 x 权益乘数。三层分解，每层把分子分母写出来。
数字全部来自 data/yili2024.json 的 dupont / income / balance 段。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.patches as mpatches  # noqa: E402

from figures._common import (  # noqa: E402
    save, fig_ax, label,
    C_BLUE, C_GREEN, C_ORANGE, C_PURPLE, C_GRAY,
    F_BLUE, F_GREEN, F_ORANGE, F_PURPLE,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
dp, i, b = d["dupont"], d["income"], d["balance"]
Y = lambda v: v / 1e8  # noqa: E731

roe = dp["roe"]
nm, at, em = dp["net_margin"], dp["asset_turnover"], dp["equity_multiplier"]
npp = Y(i["net_profit_parent"])
rev = Y(i["revenue"])
avg_ta = Y(dp["avg_total_assets"])
avg_eq = Y(dp["avg_equity_parent"])

fig, ax = fig_ax(14.6, 8.6, xlim=(0, 100), ylim=(0, 100))

ax.text(50, 96.0, "杜邦分解：ROE 15.84% 是这样乘出来的",
        ha="center", va="center", fontsize=16, weight="bold", color="#1a1a1a")
ax.text(50, 91.6, "伊利 2024 · 平均余额口径 · 三块各管一件事：卖得贵不贵、转得快不快、借得多不多",
        ha="center", va="center", fontsize=10.4, color=C_GRAY)


def node(x, y, w, h, head, big, sub, ec, fc, big_fs=15.5, head_fs=11.6,
         sub_fs=9.9):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.02,rounding_size=1.0",
        fc=fc, ec=ec, lw=2.0, zorder=3))
    ax.text(x, y + h / 2 - 3.0, head, ha="center", va="center",
            fontsize=head_fs, color=ec, weight="bold", zorder=5)
    ax.text(x, y + 0.6, big, ha="center", va="center",
            fontsize=big_fs, color="#1a1a1a", weight="bold", zorder=5)
    ax.text(x, y - h / 2 + 3.4, sub, ha="center", va="center",
            fontsize=sub_fs, color="#333333", linespacing=1.6, zorder=5)


# ── 第 1 层：ROE ───────────────────────────────────────────────────
node(50, 80.5, 40, 15.0, "净资产收益率 ROE", f"{roe * 100:.2f}%",
     "= 归母净利润 ÷ 平均归母权益", C_PURPLE, F_PURPLE, big_fs=17)

# ── 第 2 层：三块 ─────────────────────────────────────────────────
node(18, 50.0, 29, 22.0, "① 净利率", f"{nm * 100:.2f}%", "卖 100 元收入\n最后落下多少钱",
     C_GREEN, F_GREEN)
node(50, 50.0, 29, 22.0, "② 资产周转率", f"{at:.4f}", "一块钱资产\n一年做出几块钱收入",
     C_BLUE, F_BLUE)
node(82, 50.0, 29, 22.0, "③ 权益乘数", f"{em:.3f}", "总资产是净资产的\n几倍（杠杆）",
     C_ORANGE, F_ORANGE)

# ── 第 3 层：分子分母 ──────────────────────────────────────────────
ax.text(18, 32.6, f"归母净利 {npp:,.2f} 亿\n÷ 收入 {rev:,.2f} 亿",
        ha="center", va="center", fontsize=10.0, color="#333333",
        linespacing=1.7)
ax.text(50, 32.6, f"收入 {rev:,.2f} 亿\n÷ 平均总资产 {avg_ta:,.2f} 亿",
        ha="center", va="center", fontsize=10.0, color="#333333",
        linespacing=1.7)
ax.text(82, 32.6, f"平均总资产 {avg_ta:,.2f} 亿\n÷ 平均归母权益 {avg_eq:,.2f} 亿",
        ha="center", va="center", fontsize=10.0, color="#333333",
        linespacing=1.7)

# ── 连线：ROE 底 → 横向母线 → 三个子节点顶部 ───────────────────────
bus_y = 70.6
ax.plot([50, 50], [73.0, bus_y], color=C_GRAY, lw=1.6, zorder=2)
for x0, x1 in ((18, 31.4), (36.6, 63.4), (68.6, 82)):
    ax.plot([x0, x1], [bus_y, bus_y], color=C_GRAY, lw=1.6, zorder=2)
for x in (18, 50, 82):
    ax.plot([x, x], [bus_y, 61.4], color=C_GRAY, lw=1.6, zorder=2)

# 乘号放在母线两端，提示这是乘法关系
ax.text(34, bus_y, r"$\times$", ha="center", va="center", fontsize=14,
        color=C_GRAY, zorder=6)
ax.text(66, bus_y, r"$\times$", ha="center", va="center", fontsize=14,
        color=C_GRAY, zorder=6)

# ── 底部：把乘法写全 ───────────────────────────────────────────────
ax.text(50, 20.6,
        f"{nm * 100:.2f}%  $\\times$  {at:.4f}  $\\times$  {em:.3f}  =  {roe * 100:.2f}%",
        ha="center", va="center", fontsize=14.4, weight="bold", color="#1a1a1a")

ax.text(50, 13.6,
        "对照：年报口径（加权平均净资产收益率）15.81%，"
        "差 0.03 个百分点来自「平均余额」与「加权平均」两种算法的细节差异",
        ha="center", va="center", fontsize=10.0, color=C_GRAY)

ax.text(50, 7.0,
        "三块此消彼长：净利率高的生意通常周转慢（白酒），周转快的生意通常净利率薄（零售），"
        "杠杆高的生意（银行、地产）用别人的钱放大 ROE",
        ha="center", va="center", fontsize=9.6, color="#333333")

ax.text(50, 2.0,
        "数据来源：伊利 2024 年报 page_007（加权平均 ROE）、page_091~092、page_087~088；"
        "数值由 data/yili2024.json 的 dupont 段计算",
        ha="center", va="center", fontsize=9.0, color=C_GRAY)

save(fig, "w09d2_dupont_tree.png")
