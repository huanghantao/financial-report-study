# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 4 周第 17 章配图：capex 与折旧的两年对照（伊利，亿元）。

capex 是「今年往长期资产里投了多少钱」；折旧是「往年投下的资产今年被消耗掉多少」。
把两条线放在一起看，就能判断这家公司是在扩张、维持，还是在收缩：
2023 年 capex 69.56 亿 > 折旧 39.00 亿（净增投入 30.56 亿）；
2024 年 capex 39.78 亿 < 折旧 40.56 亿（净投入为负 0.78 亿）——从铺摊子转向守摊子。

所有数字来自 data/yili2024.json。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, bar_labels, label, clean_axes, legend_outside,
    C_BLUE, C_ORANGE, C_GREEN, C_RED, C_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
capex = d["cashflow"]["capex"] / 1e8                    # 39.78
capex_23 = d["compare_2023"]["cashflow"]["capex"] / 1e8  # 69.56
dep = d["cashflow"]["depreciation"] / 1e8               # 40.56
dep_23 = d["compare_2023"]["cashflow"]["depreciation"] / 1e8  # 39.00

cip = d["balance"]["construction_in_progress"] / 1e8     # 29.55
cip_23 = d["compare_2023"]["balance"]["construction_in_progress"] / 1e8  # 43.37
fa = d["balance"]["fixed_assets"] / 1e8                  # 346.19
fa_23 = d["compare_2023"]["balance"]["fixed_assets"] / 1e8  # 352.42

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(14.8, 7.2), constrained_layout=True,
    gridspec_kw={"width_ratios": [1.15, 1.0]},
)

# ── 左：capex vs 折旧，两年分组 ───────────────────────────────────
x = [0, 1.1]
w = 0.34
b1 = ax1.bar([i - w / 2 for i in x], [capex_23, capex], width=w,
             color=C_BLUE, label="资本开支（购建长期资产付现）", zorder=3)
b2 = ax1.bar([i + w / 2 for i in x], [dep_23, dep], width=w,
             color=C_ORANGE, label="全年折旧", zorder=3)
ax1.set_ylim(0, 92)
ax1.set_xticks(x)
ax1.set_xticklabels(["2023 年", "2024 年"], fontsize=12.5)
ax1.set_ylabel("金额（亿元）", fontsize=11.5)
ax1.set_title("2024 年 capex 首次低于折旧：净投入由 +30.56 亿转为 −0.78 亿",
              fontsize=13.2, pad=14)
bar_labels(ax1, b1, [capex_23, capex], fmt=lambda v: f"{v:,.2f}", fontsize=11.5)
bar_labels(ax1, b2, [dep_23, dep], fmt=lambda v: f"{v:,.2f}", fontsize=11.5)
legend_outside(ax1, fontsize=11)

label(ax1, x[0], 82, "净投入 +30.56 亿元\n（扩张期）", fontsize=11, color=C_GREEN,
      ha="center")
label(ax1, x[1], 82, "净投入 −0.78 亿元\n（维持/收缩期）", fontsize=11, color=C_RED,
      ha="center")
clean_axes(ax1)

# ── 右：两张长期资产表的同比降幅 ─────────────────────────────────
cats = ["固定资产净值", "在建工程"]
v23 = [fa_23, cip_23]
v24 = [fa, cip]
chg = [(v24[i] - v23[i]) / v23[i] * 100 for i in range(2)]

yy = [1, 0]
bars2 = ax2.barh(yy, chg, height=0.40, color=[C_BLUE, C_RED], zorder=3)
ax2.set_yticks(yy)
ax2.set_yticklabels(cats, fontsize=12)
ax2.set_xlim(-42, 22)
ax2.set_ylim(-0.75, 1.75)
ax2.axvline(0, color="#999999", lw=1.0, zorder=1)
ax2.set_xlabel("同比变化（%）", fontsize=11.5)
ax2.set_title("两张长期资产表同时缩水：在建工程降 31.9%", fontsize=13.2, pad=14)

notes = [f"{v23[0]:,.2f} 亿 → {v24[0]:,.2f} 亿", f"{v23[1]:,.2f} 亿 → {v24[1]:,.2f} 亿"]
for b, c, note in zip(bars2, chg, notes):
    ymid = b.get_y() + b.get_height() / 2
    if abs(c) < 4:
        # 柱体太薄，字写不进柱内：挪到柱子左边，深色
        ax2.text(c - 2.2, ymid, f"{c:+.1f}%", va="center", ha="right",
                 fontsize=12.4, weight="bold", color="#333333")
    else:
        ax2.text(c + 1.6, ymid, f"{c:+.1f}%", va="center", ha="left",
                 fontsize=12.6, weight="bold", color="white")
    ax2.text(1.6, ymid, note, va="center", ha="left",
             fontsize=10.8, color="#555555")

label(ax2, -20.0, 1.44,
      "在建工程下降主因：\n部分在建项目转入固定资产（page_176）",
      fontsize=10.0, color=C_GRAY, ha="center", va="center")
clean_axes(ax2)

fig.text(0.012, -0.030,
         "数据来源：伊利 2024 年报 page_095（购建固定资产、无形资产和其他长期资产支付的现金）、"
         "page_217（折旧）、page_087（固定资产、在建工程）。\n"
         "「净投入」= 资本开支 − 折旧，是用现金流口径粗算的「这一年往里添了还是只够维持」，"
         "不是会计科目；在建工程下降的主因是部分在建项目转入固定资产（page_176）。",
         ha="left", va="top", fontsize=9.6, color=C_GRAY, linespacing=1.6)

save(fig, "w04d17_capex_vs_depreciation.png")
