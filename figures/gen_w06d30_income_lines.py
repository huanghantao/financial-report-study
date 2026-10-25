# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 6 周第 30 章配图 2：利润表八行关键项目，2024 vs 2023。

横向分组条：同一行两个年度并排，右边标出变动幅度。
选八行：营业收入、营业成本、毛利、销售费用、管理费用、研发费用、资产减值、营业利润。

数字来自 data/yili2024.json 的 income 与 compare_2023.income 段；毛利由收入减成本算出。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, legend_outside, C_BLUE, C_GRAY, C_RED, C_GREEN,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
a = d["income"]
b = d["compare_2023"]["income"]

rows = [
    ("营业收入", a["revenue"], b["revenue"]),
    ("营业成本", a["cost_of_sales"], b["cost_of_sales"]),
    ("毛利", a["revenue"] - a["cost_of_sales"],
     b["revenue"] - b["cost_of_sales"]),
    ("销售费用", a["selling_expenses"], b["selling_expenses"]),
    ("管理费用", a["admin_expenses"], b["admin_expenses"]),
    ("研发费用", a["rd_expenses"], b["rd_expenses"]),
    ("资产减值", -a["asset_impairment"], -b["asset_impairment"]),
    ("营业利润", a["operating_profit"], b["operating_profit"]),
]
rows_yi = [(name, v24 / 1e8, v23 / 1e8) for name, v24, v23 in rows]

fig, ax = plt.subplots(figsize=(13.6, 8.4), constrained_layout=True)
ys = list(range(len(rows_yi)))[::-1]
h = 0.40

b24 = ax.barh([i - h / 2 for i in ys], [r[1] for r in rows_yi], height=h,
              color=C_BLUE, label="2024 年", zorder=3)
b23 = ax.barh([i + h / 2 for i in ys], [r[2] for r in rows_yi], height=h,
              color=C_GRAY, label="2023 年", zorder=3)
ax.set_yticks(ys)
ax.set_yticklabels([r[0] for r in rows_yi], fontsize=12.5)
ax.tick_params(axis="y", pad=6)
ax.set_xlim(0, 1660)
ax.set_xlabel("金额（亿元）", fontsize=11.5)
ax.set_title("八行关键项目：收入、成本、费用、减值、营业利润两年对照",
             fontsize=14, pad=16)
legend_outside(ax, fontsize=11.5)

for bi, v in zip(b24, [r[1] for r in rows_yi]):
    ax.text(bi.get_width() + 8, bi.get_y() + bi.get_height() / 2,
            f"{v:,.2f}", va="center", ha="left", fontsize=10.5, color="#333333")
for bi, v in zip(b23, [r[2] for r in rows_yi]):
    ax.text(bi.get_width() + 8, bi.get_y() + bi.get_height() / 2,
            f"{v:,.2f}", va="center", ha="left", fontsize=10.5, color="#555555")

# 右侧单独一列：同比变动幅度（减值增加是坏事，用红色）
ax.axvline(1345, color="#cccccc", lw=1.0, ls=(0, (4, 3)), zorder=2)
for i, (name, v24, v23) in zip(ys, rows_yi):
    chg = (v24 / v23 - 1) * 100 if v23 else 0
    if name == "资产减值":
        color = C_RED if chg > 0 else C_GREEN
    else:
        color = C_RED if chg < 0 else C_GREEN
    ax.text(1372, i, f"{chg:+.1f}%", va="center", ha="left",
            fontsize=11, weight="bold", color=color)
ax.text(1372, len(rows_yi) - 0.42, "同比变动", va="center", ha="left",
        fontsize=10.5, color="#333333")

clean_axes(ax)

fig.text(
    0.012, -0.035,
    "数据来源：伊利 2024 年报 page_091、page_092（合并利润表）。资产减值在利润表里是负数（损失），"
    "图中取绝对值画成正数，方便和费用放在同一把尺子上。\n"
    "毛利 = 营业收入 - 营业成本，是算出来的，不是报表行项目。",
    ha="left", va="top", fontsize=9.4, color=C_GRAY, linespacing=1.6,
)

save(fig, "w06d30_income_lines.png")
