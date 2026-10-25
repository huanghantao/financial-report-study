# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 4 周第 16 章配图 2：折旧 40.56 亿元到底有多重？

左图：折旧与净利润并排比两年——折旧相当于净利润的比例，从 37.9% 升到 47.9%。
右图：同一笔折旧，换成三把尺子（占收入、占营业成本、占固定资产净值）来量。

所有数字来自 data/yili2024.json。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, bar_labels, clean_axes, legend_outside,
    C_BLUE, C_ORANGE, C_GREEN, C_PURPLE, C_RED, C_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
dep = d["cashflow"]["depreciation"] / 1e8                # 40.56
dep_23 = d["compare_2023"]["cashflow"]["depreciation"] / 1e8   # 39.00
np_all = d["income"]["net_profit"] / 1e8                 # 84.64
np_23 = d["compare_2023"]["income"]["net_profit"] / 1e8   # 102.84
rev = d["income"]["revenue"] / 1e8                       # 1153.93
cost = d["income"]["cost_of_sales"] / 1e8                # 762.99
fa = d["balance"]["fixed_assets"] / 1e8                  # 346.19

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(14.6, 7.0), constrained_layout=True,
    gridspec_kw={"width_ratios": [1.0, 1.05]},
)

# ── 左：折旧 vs 净利润（两年分组） ────────────────────────────────
groups = ["2023 年", "2024 年"]
deps = [dep_23, dep]
nps = [np_23, np_all]
x = [0, 1.05]
w = 0.36

b1 = ax1.bar([i - w / 2 for i in x], deps, width=w, color=C_ORANGE,
             label="全年折旧", zorder=3)
b2 = ax1.bar([i + w / 2 for i in x], nps, width=w, color=C_PURPLE,
             label="净利润", zorder=3)
ax1.set_ylim(0, 128)
ax1.set_xticks(x)
ax1.set_xticklabels(groups, fontsize=12.5)
ax1.set_ylabel("金额（亿元）", fontsize=11.5)
ax1.set_title("折旧相当于净利润的几成：37.9% → 47.9%", fontsize=13.5, pad=14)
bar_labels(ax1, b1, deps, fmt=lambda v: f"{v:,.2f}", fontsize=11.5)
bar_labels(ax1, b2, nps, fmt=lambda v: f"{v:,.2f}", fontsize=11.5)
legend_outside(ax1, fontsize=11.5)

for i, (dd, nn) in enumerate(zip(deps, nps)):
    ax1.text(x[i], max(dd, nn) + 12.5, f"{dd/nn*100:.1f}%",
             ha="center", va="bottom", fontsize=13, weight="bold", color=C_RED)
clean_axes(ax1)

# ── 右：三把尺子量同一笔折旧 ──────────────────────────────────────
rows = [
    ("占营业收入\n（每 100 元收入含 3.5 元）", dep / rev * 100, C_BLUE),
    ("占营业成本\n（每 100 元成本含 5.3 元）", dep / cost * 100, C_ORANGE),
    ("占固定资产净值\n（一年折旧掉 11.7%）", dep / fa * 100, C_RED),
]
ys = [2, 1, 0]
bars2 = ax2.barh(ys, [r[1] for r in rows], height=0.42,
                 color=[r[2] for r in rows], zorder=3)
ax2.set_yticks(ys)
ax2.set_yticklabels([r[0] for r in rows], fontsize=11.2)
ax2.set_xlim(0, 15.5)
ax2.set_xlabel("比率（%）", fontsize=11.5)
ax2.set_title("同一笔折旧，三把尺子量出三种分量", fontsize=13.5, pad=14)
for b, r in zip(bars2, rows):
    ax2.text(b.get_width() + 0.28, b.get_y() + b.get_height() / 2,
             f"{r[1]:.1f}%", va="center", ha="left",
             fontsize=12.5, weight="bold", color="#333333")
clean_axes(ax2)

fig.text(0.012, -0.032,
         "数据来源：伊利 2024 年报 page_091（营业收入、营业成本、净利润）、page_087（固定资产净值）、"
         "page_217（折旧）。\n"
         "2024 年这个比例之所以从 37.9% 跳到 47.9%，一半因为折旧本身略增，一半因为净利润同比降了 17.7%。\n"
         "右图「占固定资产净值 11.7%」用的是现金流量表口径 40.56 亿 ÷ 346.19 亿；若只用固定资产附注口径 38.18 亿，则为 11.0%。",
         ha="left", va="top", fontsize=9.6, color=C_GRAY, linespacing=1.6)

save(fig, "w04d16_depreciation_weight.png")
