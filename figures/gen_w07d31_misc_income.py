# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 7 周第 31 章配图 1：营业利润里的三项「杂项」有多大（伊利 2024，亿元）。

其他收益 10.16 + 投资收益 24.17 + 公允价值变动 -0.28 = 34.06 亿元，
相当于营业利润 101.82 亿元的 33.4%。数字全部来自 data/yili2024.json。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_RED,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
inc = d["income"]

other = inc["other_income"] / 1e8
inv = inc["investment_income"] / 1e8
fv = inc["fair_value_change"] / 1e8
total = other + inv + fv
op = inc["operating_profit"] / 1e8
share = total / op * 100

rows = [
    ("三项合计", total, C_GREEN),
    ("投资收益", inv, C_ORANGE),
    ("其他收益", other, C_BLUE),
    ("公允价值变动", fv, C_RED),
]

fig, ax = plt.subplots(figsize=(12.4, 7.0))
ys = [3, 2, 1, 0]
bars = ax.barh(ys, [r[1] for r in rows], height=0.52,
               color=[r[2] for r in rows], zorder=3)

ax.set_yticks(ys)
ax.set_yticklabels([r[0] for r in rows], fontsize=12.2)
ax.set_xlim(-6.5, 41)
ax.set_ylim(-0.72, 4.78)
ax.set_xlabel("金额（亿元）", fontsize=11.5)
ax.axvline(0, color="#666666", lw=1.1, zorder=1)
ax.axhline(2.55, color="#bbbbbb", lw=1.0, ls=(0, (4, 3)), zorder=1)

for b, r in zip(bars, rows):
    v = r[1]
    if v >= 0:
        ax.text(b.get_width() + 0.7, b.get_y() + b.get_height() / 2,
                f"{v:,.2f} 亿元", va="center", ha="left",
                fontsize=12.2, weight="bold", color="#222222", zorder=6)
    else:
        ax.text(b.get_width() - 0.7, b.get_y() + b.get_height() / 2,
                f"{v:,.2f} 亿元", va="center", ha="right",
                fontsize=12.2, weight="bold", color=C_RED, zorder=6)

ax.text(0.0, 4.50,
        f"三项合计 {total:,.2f} 亿元，相当于营业利润 {op:,.2f} 亿元的 {share:.1f}%",
        fontsize=12.0, color="#333333", ha="left", va="center")
ax.text(0.0, 4.08,
        "虚线以上是合计，虚线以下是三项明细；三项里只有投资收益是大额正数",
        fontsize=10.6, color=C_GRAY, ha="left", va="center")

ax.set_title("利润里的杂项：34.06 亿元，占营业利润 33.4%",
             fontsize=15.0, pad=16)
clean_axes(ax)

fig.text(
    0.012, -0.035,
    "数据来源：伊利 2024 年报 page_091（利润表）、page_209（其他收益）、page_210（投资收益、公允价值变动）。\n"
    "投资收益 24.17 亿元中，25.80 亿元来自处置昌吉盛新股权，权益法核算的联营企业收益为 -2.15 亿元；"
    "公允价值变动为 -0.28 亿元。",
    ha="left", va="top", fontsize=9.6, color=C_GRAY, linespacing=1.6,
)

save(fig, "w07d31_misc_income.png")
