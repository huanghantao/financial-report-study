# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 8 周第 36 章配图：净利润与经营现金流两个方向，以及净现比。

左图：2023 / 2024 两年的净利润与经营现金流（亿元）；
右图：净现比（经营现金流 ÷ 净利润），2023 年 1.78 倍、2024 年 2.57 倍。
数字全部来自 data/yili2024.json。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, bar_labels, label, clean_axes, legend_outside,
    C_GREEN, C_PURPLE, C_BLUE, C_RED, C_GRAY,
)
from matplotlib.lines import Line2D  # noqa: E402
from figures._data import load  # noqa: E402

d = load("yili2024")
inc, cf, c23 = d["income"], d["cashflow"], d["compare_2023"]
np24 = inc["net_profit"] / 1e8
np23 = c23["income"]["net_profit"] / 1e8
ocf24 = cf["operating_net"] / 1e8
ocf23 = cf["operating_net_2023"] / 1e8
r24 = ocf24 / np24
r23 = ocf23 / np23
gap = ocf24 - np24

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(14.8, 7.2), constrained_layout=True,
    gridspec_kw={"width_ratios": [1.5, 1.0]},
)

# ── 左：净利润 vs 经营现金流 ─────────────────────────────
w = 0.34
b1 = ax1.bar([-w / 2, 1 - w / 2], [np23, np24], width=w,
             color=C_PURPLE, label="净利润", zorder=3)
b2 = ax1.bar([w / 2, 1 + w / 2], [ocf23, ocf24], width=w,
             color=C_GREEN, label="经营活动现金流净额", zorder=3)
ax1.set_ylim(0, 320)
ax1.set_xlim(-0.85, 1.85)
ax1.set_xticks([0, 1])
ax1.set_xticklabels(["2023 年", "2024 年"], fontsize=12.5)
ax1.set_ylabel("金额（亿元）", fontsize=11.8)
ax1.set_title("净利润与经营现金流（亿元）", fontsize=14.5, pad=10)
bar_labels(ax1, b1, [np23, np24], fmt=lambda v: f"{v:,.2f}", fontsize=11.5)
bar_labels(ax1, b2, [ocf23, ocf24], fmt=lambda v: f"{v:,.2f}", fontsize=11.5)
label(ax1, 1.0, 268, f"2024 年两者相差 {gap:,.2f} 亿元",
      fontsize=12.5, weight="bold", color=C_RED)
legend_outside(ax1, fontsize=11.5)
clean_axes(ax1)

# ── 右：净现比 ────────────────────────────────────────
b3 = ax2.bar([0, 1], [r23, r24], width=0.5, color=[C_GRAY, C_BLUE], zorder=3)
ax2.set_ylim(0, 3.25)
ax2.set_xlim(-0.8, 1.8)
ax2.set_xticks([0, 1])
ax2.set_xticklabels(["2023 年", "2024 年"], fontsize=12.5)
ax2.set_ylabel("净现比（倍）", fontsize=11.8)
ax2.set_title("净现比：经营现金流 ÷ 净利润", fontsize=14.5, pad=10)
bar_labels(ax2, b3, [r23, r24], fmt=lambda v: f"{v:,.2f}", fontsize=12.5)
ax2.axhline(1.0, color=C_RED, lw=1.3, ls=(0, (5, 3)), zorder=2)
legend_outside(
    ax2, fontsize=11,
    handles=[Line2D([], [], color=C_RED, lw=1.3, ls=(0, (5, 3)),
                    label="1 倍 = 长期健康线")],
    handlelength=2.0,
)
clean_axes(ax2)

fig.suptitle("归母净利润 -18.9%，经营现金流 +18.9%：同一家公司、同一年的两个方向",
             fontsize=16.5, weight="bold", y=1.075)
fig.text(0.012, -0.035,
         f"数据来源：伊利 2024 年报 page_092（净利润 {np24:,.2f} 亿元）、page_094（经营现金流 {ocf24:,.2f} 亿元）、"
         f"page_007（2023 年数据）。净现比 = 经营现金流 ÷ 净利润，"
         f"2023 年 {r23:,.2f} 倍、2024 年 {r24:,.2f} 倍。",
         ha="left", va="top", fontsize=9.5, color=C_GRAY)

save(fig, "w08d36_profit_vs_ocf.png")
