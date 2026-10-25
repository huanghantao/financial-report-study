# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 5 周第 25 章配图之一：伊利 vs 蒙牛，四组偿债与现金流指标对照。

上排：资产负债率、流动比率（越低越紧 / 越高越松）；
下排：经营现金流、归母权益。
每格都是两根柱，伊利在左、蒙牛在右，柱顶给数值，标题只在本子图内，不横跨。

数字全部来自 data/yili2024.json 与 data/mengniu2024.json（已核实），不手打。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import (
    save, clean_axes, C_BLUE, C_ORANGE, C_GRAY,
)
from figures._data import load
import matplotlib.pyplot as plt

y = load("yili2024")
m = load("mengniu2024")
yi = 1e8

yb, mb = y["balance"], m["balance"]
yr, mr = y["ratios"], m["ratios"]

debt_y = yb["total_liabilities"] / yb["total_assets"] * 100
debt_m = mb["total_liabilities"] / mb["total_assets"] * 100
cur_y = yb["total_current_assets"] / yb["total_current_liabilities"]
cur_m = mb["total_current_assets"] / mb["total_current_liabilities"]
ocf_y = y["cashflow"]["operating_net"] / yi
ocf_m = m["cashflow"]["operating_net"] / yi
eq_y = yb["equity_parent"] / yi
eq_m = mb["equity_parent"] / yi

panels = [
    ("资产负债率（%）", [debt_y, debt_m], lambda v: f"{v:.2f}%", 85),
    ("流动比率（倍）", [cur_y, cur_m], lambda v: f"{v:.2f}", 1.35),
    ("经营现金流（亿元）", [ocf_y, ocf_m], lambda v: f"{v:,.2f}", 265),
    ("归母权益（亿元）", [eq_y, eq_m], lambda v: f"{v:,.2f}", 640),
]

fig, axes = plt.subplots(2, 2, figsize=(13.2, 8.8))
fig.subplots_adjust(left=0.085, right=0.972, top=0.855, bottom=0.115,
                    hspace=0.44, wspace=0.24)
flat = list(axes.flat)

for ax, (title, vals, fmt, ymax) in zip(flat, panels):
    bars = ax.bar([0, 1], vals, width=0.42, color=[C_BLUE, C_ORANGE], zorder=3)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + ymax * 0.024,
                fmt(v), ha="center", va="bottom", fontsize=12.5,
                weight="bold", zorder=6)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["伊利", "蒙牛"], fontsize=12.5)
    ax.set_xlim(-0.62, 1.62)
    ax.set_ylim(0, ymax)
    ax.set_title(title, fontsize=13.2, pad=8)
    clean_axes(ax)

fig.suptitle("蒙牛负债率更低、流动比率更高，但伊利手里的现金和现金流厚得多",
             fontsize=15, weight="bold", y=0.962)
fig.text(0.02, 0.028,
         "数据来源：伊利 2024 年报 page_087、page_088、page_094；蒙牛 2024 年报 page_142~page_144、page_148。"
         "蒙牛为港股口径，原表单位「人民币千元」，已统一换算为元。",
         fontsize=9.6, color=C_GRAY)

save(fig, "w05d25_yili_vs_mengniu_debt.png")
