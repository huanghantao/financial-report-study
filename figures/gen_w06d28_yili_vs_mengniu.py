# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 6 周第 28 章配图 2：高毛利不等于好生意，伊利 vs 蒙牛。

同一张图上并排三组比率：毛利率、销售费用率、净利率。
蒙牛毛利率更高，但销售费用率也更高，最后净利率几乎归零。

数字来自 data/yili2024.json 的 ratios 与 data/mengniu2024.json 的 ratios。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, label, clean_axes, legend_outside, C_BLUE, C_ORANGE, C_GRAY,
)
from figures._data import load  # noqa: E402

y = load("yili2024")
m = load("mengniu2024")

rows = ["毛利率", "销售费用率", "净利率"]
yili = [
    y["ratios"]["gross_margin"] * 100,
    y["ratios"]["selling_expense_ratio"] * 100,
    y["ratios"]["net_margin"] * 100,
]
meng = [
    m["ratios"]["gross_margin"] * 100,
    m["ratios"]["selling_expense_ratio"] * 100,
    m["ratios"]["net_margin"] * 100,
]

fig, ax = plt.subplots(figsize=(12.6, 7.4), constrained_layout=True)
ys = [2, 1, 0]
h = 0.34

b1 = ax.barh([i + h / 2 for i in ys], yili, height=h, color=C_BLUE,
             label="伊利 2024", zorder=3)
b2 = ax.barh([i - h / 2 for i in ys], meng, height=h, color=C_ORANGE,
             label="蒙牛 2024", zorder=3)
ax.set_yticks(ys)
ax.set_yticklabels(rows, fontsize=13)
ax.set_xlim(0, 48)
ax.set_ylim(-0.95, 2.55)
ax.set_xlabel("占营业收入的比例（%）", fontsize=11.5)
ax.set_title("蒙牛毛利率高 5.69 个百分点，净利率却只剩 0.12%",
             fontsize=14.5, pad=16)
legend_outside(ax, fontsize=11.5)

for b, vals in ((b1, yili), (b2, meng)):
    for bi, v in zip(b, vals):
        ax.text(bi.get_width() + 0.5, bi.get_y() + bi.get_height() / 2,
                f"{v:.2f}%", va="center", ha="left",
                fontsize=11.5, weight="bold", color="#333333")

ax.annotate("毛利高出来的 5.69 个点，被多出来的 6.99 个点销售费用吃掉，\n最后只剩 0.12% 净利率",
            xy=(meng[2] + 0.6, 0 - h / 2), xytext=(12.0, -0.62),
            fontsize=10.4, color="#333333", ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.42", fc="white", ec=C_ORANGE, lw=1.0),
            arrowprops=dict(arrowstyle="->", color=C_ORANGE, lw=1.2,
                            connectionstyle="arc3,rad=-0.2"))
label(ax, 27.0, 0.35, "净利率 = 归母净利润 ÷ 营业收入", fontsize=10.2, color=C_GRAY)
clean_axes(ax)

fig.text(
    0.012, -0.045,
    "数据来源：伊利 2024 年报 page_091（收入 1,153.93 亿、归母净利 84.53 亿）、page_018（销售费用 219.82 亿）；"
    "蒙牛 2024 年报 page_140（收入 886.75 亿、归母净利 1.05 亿）、销售及经销费用 230.93 亿。\n"
    "净利率这里用的是归母净利润，与 ratio 段的定义一致；蒙牛 2024 年净利润 2.25 亿，其中少数股东损益 1.20 亿。",
    ha="left", va="top", fontsize=9.4, color=C_GRAY, linespacing=1.6,
)

save(fig, "w06d28_yili_vs_mengniu.png")
