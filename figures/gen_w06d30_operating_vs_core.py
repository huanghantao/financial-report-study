# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 6 周第 30 章配图 1：报表营业利润 vs 剔除减值后的经营性利润。

同一家公司、同一年，两个视角给出方向相反的结论：
报表口径 118.73 → 101.82（-14.2%）；剔除减值 135.59 → 154.13（+13.7%）。

数字来自 data/yili2024.json 的 core_earnings 段。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, bar_labels, label, clean_axes, C_BLUE, C_GREEN, C_GRAY, C_RED,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
ce = d["core_earnings"]
op24 = ce["operating_profit_2024"] / 1e8
op23 = ce["operating_profit_2023"] / 1e8
core24 = ce["core_operating_profit_2024"] / 1e8
core23 = ce["core_operating_profit_2023"] / 1e8
imp24 = ce["impairment_2024"] / 1e8
imp23 = ce["impairment_2023"] / 1e8
op_chg = (op24 / op23 - 1) * 100
core_chg = (core24 / core23 - 1) * 100

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(14.4, 7.4), constrained_layout=True, sharey=True,
)

# ── 左：报表口径 ──────────────────────────────────────────────
b1 = ax1.bar([0, 1], [op23, op24], width=0.52, color=[C_GRAY, C_RED], zorder=3)
ax1.set_ylim(0, 216)
ax1.set_xlim(-0.65, 1.65)
ax1.set_xticks([0, 1])
ax1.set_xticklabels(["2023 年", "2024 年"], fontsize=12.5)
ax1.set_ylabel("营业利润（亿元）", fontsize=11.5)
ax1.set_title("报表口径：营业利润", fontsize=15, pad=10)
bar_labels(ax1, b1, [op23, op24], fmt=lambda v: f"{v:,.2f}", fontsize=12)
ax1.annotate("", xy=(0.86, 112), xytext=(0.14, 132),
             arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=2.2,
                             connectionstyle="arc3,rad=-0.18", mutation_scale=22))
label(ax1, 0.5, 152, f"{op24 - op23:+,.2f} 亿（{op_chg:+.1f}%）",
      fontsize=13.5, weight="bold", color=C_RED)
clean_axes(ax1)

# ── 右：剔除减值 ──────────────────────────────────────────────
b2 = ax2.bar([0, 1], [core23, core24], width=0.52, color=[C_GRAY, C_GREEN],
             zorder=3)
ax2.set_xlim(-0.65, 1.65)
ax2.set_xticks([0, 1])
ax2.set_xticklabels(["2023 年", "2024 年"], fontsize=12.5)
ax2.set_title("剔除减值：经营性利润", fontsize=15, pad=10)
bar_labels(ax2, b2, [core23, core24], fmt=lambda v: f"{v:,.2f}", fontsize=12)
ax2.annotate("", xy=(0.86, 176), xytext=(0.14, 152),
             arrowprops=dict(arrowstyle="-|>", color=C_GREEN, lw=2.2,
                             connectionstyle="arc3,rad=0.18", mutation_scale=22))
label(ax2, 0.5, 198, f"{core24 - core23:+,.2f} 亿（{core_chg:+.1f}%）",
      fontsize=13.5, weight="bold", color=C_GREEN)
clean_axes(ax2)

fig.suptitle("同一家公司、同一年，两个方向相反的结论",
             fontsize=17.5, weight="bold", y=1.045)
fig.text(
    0.012, -0.045,
    f"数据来源：伊利 2024 年报 page_091（营业利润）、page_211（资产减值 46.76 亿、信用减值 5.55 亿）、"
    f"data/yili2024.json 的 core_earnings 段。\n"
    f"左图是利润表最后几行的口径；右图把资产减值与信用减值加回营业利润："
    f"2024 年加回 {imp24:.2f} 亿，2023 年加回 {imp23:.2f} 亿。减值是会计判断，不花现金，也不代表当年主业变差。",
    ha="left", va="top", fontsize=9.4, color=C_GRAY, linespacing=1.6,
)

save(fig, "w06d30_operating_vs_core.png")
