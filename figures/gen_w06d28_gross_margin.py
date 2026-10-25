# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 6 周第 28 章配图 1：毛利率逆势上升，以及它为什么能上升。

左图：伊利 2023、2024 与蒙牛 2024 的毛利率对比，标出 +1.30 个百分点。
右图：2024 年营业收入 -8.24%、营业成本 -10.01%，成本降得比收入快，
      分母缩得比分子快，毛利率就上去了。

所有数字来自 data/yili2024.json 与 data/mengniu2024.json。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, bar_labels, label, clean_axes, C_BLUE, C_ORANGE, C_GRAY, C_GREEN,
)
from figures._data import load  # noqa: E402

y = load("yili2024")
m = load("mengniu2024")

gm24 = y["core_earnings"]["gross_margin_2024"] * 100
gm23 = y["core_earnings"]["gross_margin_2023"] * 100
gm_m = m["ratios"]["gross_margin"] * 100

rev24 = y["income"]["revenue"]
rev23 = y["compare_2023"]["income"]["revenue"]
cost24 = y["income"]["cost_of_sales"]
cost23 = y["compare_2023"]["income"]["cost_of_sales"]
rev_chg = (rev24 / rev23 - 1) * 100
cost_chg = (cost24 / cost23 - 1) * 100

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(15.2, 7.2), constrained_layout=True,
    gridspec_kw={"width_ratios": [1.25, 0.9]},
)

# ── 左：三家毛利率 ────────────────────────────────────────────
labels = ["伊利 2023", "伊利 2024", "蒙牛 2024"]
vals = [gm23, gm24, gm_m]
colors = [C_GRAY, C_BLUE, C_ORANGE]
bars = ax1.bar(range(3), vals, width=0.52, color=colors, zorder=3)
ax1.set_ylim(0, 50)
ax1.set_xticks(range(3))
ax1.set_xticklabels(labels, fontsize=12.5)
ax1.set_ylabel("毛利率（%）", fontsize=11.5, labelpad=8)
ax1.set_title("伊利毛利率 32.58% → 33.88%，收入下降时反而升了",
              fontsize=13.5, pad=14)
bar_labels(ax1, bars, vals, fmt=lambda v: f"{v:.2f}%", fontsize=12)

ax1.annotate("", xy=(0.93, gm24 + 2.6), xytext=(0.07, gm23 + 2.6),
             arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=2.0,
                             connectionstyle="arc3,rad=-0.25"))
label(ax1, 0.5, 43.0, "+1.30 个百分点", fontsize=13, weight="bold", color=C_GREEN)
clean_axes(ax1)

# ── 右：收入与成本的变动幅度 ──────────────────────────────────
rows = [("营业收入", rev_chg, C_BLUE), ("营业成本", cost_chg, C_ORANGE)]
ys = [1, 0]
bars2 = ax2.barh(ys, [r[1] for r in rows], height=0.42,
                 color=[r[2] for r in rows], zorder=3)
ax2.set_yticks(ys)
ax2.set_yticklabels([r[0] for r in rows], fontsize=12.5)
ax2.set_xlim(-13.5, 1.8)
ax2.axvline(0, color="#999999", lw=1.0, zorder=2)
ax2.set_xlabel("2024 年同比变动（%）", fontsize=11.5)
ax2.set_title("成本降 10.01%，收入降 8.24%：成本降得更快", fontsize=13, pad=14)
for b, r in zip(bars2, rows):
    ax2.text(b.get_width() - 0.35, b.get_y() + b.get_height() / 2,
             f"{r[1]:.2f}%", va="center", ha="right",
             fontsize=12.5, weight="bold", color="#333333")
ax2.text(-13.2, -0.72, "成本降幅比收入降幅大 1.77 个百分点",
         fontsize=10.8, color="#333333", ha="left", va="center")
ax2.set_ylim(-1.15, 1.75)
clean_axes(ax2)
ax2.spines["left"].set_visible(False)
ax2.tick_params(axis="y", length=0)

fig.text(
    0.012, -0.04,
    "数据来源：伊利 2024 年报 page_091、page_018（收入与成本变动）、data/yili2024.json；"
    "蒙牛 2024 年报 page_140、data/mengniu2024.json（收入 886.75 亿、成本 535.84 亿，毛利率 39.57%）。\n"
    "毛利率 =（营业收入 - 营业成本）÷ 营业收入。2024 年毛利额 390.94 亿元，比 2023 年的 409.70 亿元少 18.75 亿元；"
    "毛利率上升，是因为分母（收入）缩得比分子（毛利）更快。",
    ha="left", va="top", fontsize=9.4, color=C_GRAY, linespacing=1.6,
)

save(fig, "w06d28_gross_margin.png")
