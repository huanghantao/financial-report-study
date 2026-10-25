# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 8 周第 39 章配图 2：伊利 vs 蒙牛的自由现金流。

左：经营现金流、资本开支、自由现金流（亿元）；
右：自由现金流 ÷ 营业收入（每 100 元收入留下多少自由现金）。
伊利数字来自 data/yili2024.json，蒙牛来自 data/mengniu2024.json。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, bar_labels, label, clean_axes, legend_outside,
    C_BLUE, C_ORANGE, C_GREEN, C_GRAY,
)
from figures._data import load  # noqa: E402

y = load("yili2024")
m = load("mengniu2024")
Y = lambda v: v / 1e8  # noqa: E731

names = ["伊利\n2024 年", "蒙牛\n2024 年"]
ocf = [Y(y["cashflow"]["operating_net"]), Y(m["cashflow"]["operating_net"])]
capex = [Y(y["cashflow"]["capex"]), Y(m["cashflow"]["capex"])]
fcf = [Y(y["ratios"]["free_cash_flow"]), Y(m["ratios"]["free_cash_flow"])]
rev = [Y(y["income"]["revenue"]), Y(m["income"]["revenue"])]
fcf_margin = [f / r for f, r in zip(fcf, rev)]

for i in range(2):
    assert abs(ocf[i] - capex[i] - fcf[i]) < 0.05, "FCF 与 OCF-capex 不一致"

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(15.2, 7.2), constrained_layout=True,
    gridspec_kw={"width_ratios": [1.55, 1.0]},
)

# ── 左：三项金额分组柱 ─────────────────────────────────
w = 0.25
xs = [0, 1]
b1 = ax1.bar([x - w for x in xs], ocf, width=w, color=C_BLUE,
             label="经营活动现金流", zorder=3)
b2 = ax1.bar(xs, capex, width=w, color=C_ORANGE,
             label="资本开支", zorder=3)
b3 = ax1.bar([x + w for x in xs], fcf, width=w, color=C_GREEN,
             label="自由现金流", zorder=3)

ax1.set_ylim(0, 280)
ax1.set_xlim(-0.62, 1.62)
ax1.set_xticks(xs)
ax1.set_xticklabels(names, fontsize=12.5)
ax1.set_ylabel("金额（亿元）", fontsize=11.8)
ax1.set_title("经营现金流、资本开支与自由现金流（亿元）", fontsize=14, pad=10)
bar_labels(ax1, b1, ocf, fmt=lambda v: f"{v:,.2f}", fontsize=10.4)
bar_labels(ax1, b2, capex, fmt=lambda v: f"{v:,.2f}", fontsize=10.4)
bar_labels(ax1, b3, fcf, fmt=lambda v: f"{v:,.2f}", fontsize=11.2)
legend_outside(ax1, fontsize=11)
clean_axes(ax1)

# ── 右：FCF 占收入的比重 ────────────────────────────────
b4 = ax2.bar(xs, [v * 100 for v in fcf_margin], width=0.44,
             color=[C_GREEN, C_GRAY], zorder=3)
ax2.set_ylim(0, 22)
ax2.set_xlim(-0.68, 1.68)
ax2.set_xticks(xs)
ax2.set_xticklabels(names, fontsize=12.5)
ax2.set_ylabel("FCF ÷ 营业收入（%）", fontsize=11.8)
ax2.set_title("每 100 元收入留下多少自由现金", fontsize=14, pad=10)
bar_labels(ax2, b4, [v * 100 for v in fcf_margin],
           fmt=lambda v: f"{v:,.1f}%", fontsize=12.5)
clean_axes(ax2)

fig.suptitle("伊利每 100 元收入留下 15.4 元自由现金，蒙牛留下 5.5 元",
             fontsize=16.2, weight="bold", y=1.045)
fig.text(0.012, -0.045,
         f"数据来源：伊利 2024 年报 page_094、page_095（经营现金流 {ocf[0]:,.2f} 亿、"
         f"资本开支 {capex[0]:,.2f} 亿）；蒙牛 2024 年报 page_147、page_148（经营现金流 "
         f"{ocf[1]:,.2f} 亿、资本开支 {capex[1]:,.2f} 亿）。两家都用「经营现金流 − 购建长期资产支付的现金」。\n"
         f"蒙牛的自由现金流只有伊利的 {fcf[1] / fcf[0] * 100:.0f}%，不是因为它不赚钱，"
         f"而是因为它的经营现金流（{ocf[1]:,.2f} 亿）本就不到伊利的一半，"
         f"资本开支占经营现金流的比重还更高（{capex[1] / ocf[1] * 100:.0f}% 对 {capex[0] / ocf[0] * 100:.0f}%）。",
         ha="left", va="top", fontsize=9.3, color=C_GRAY, linespacing=1.7)

save(fig, "w08d39_yili_vs_mengniu_fcf.png")
