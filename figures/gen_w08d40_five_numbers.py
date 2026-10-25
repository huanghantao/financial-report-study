# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 8 周第 40 章配图：利润与现金的五个数字。

归母净利润 84.53 / 扣非归母 60.11 / 净利润 84.64 / 经营现金流 217.40 / 自由现金流 177.61。
横向条形，从「会计口径最严」到「现金口径最宽」排列。
数字全部来自 data/yili2024.json 的 income、cashflow、nonrecurring、ratios 段。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, label, C_BLUE, C_GREEN, C_PURPLE, C_ORANGE, C_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
Y = lambda v: v / 1e8  # noqa: E731

items = [
    ("扣非归母净利润\n只算主业、剔掉一次性", Y(d["nonrecurring"]["net_profit_deducted"]), C_ORANGE),
    ("归母净利润\n股东实际分到的那份", Y(d["income"]["net_profit_parent"]), C_BLUE),
    ("净利润\n含少数股东损益", Y(d["income"]["net_profit"]), C_PURPLE),
    ("自由现金流\n经营现金流减资本开支", Y(d["ratios"]["free_cash_flow"]), C_GRAY),
    ("经营活动现金流净额\n这一年真正收回来的钱", Y(d["cashflow"]["operating_net"]), C_GREEN),
]

fig, ax = plt.subplots(figsize=(13.4, 7.4))
fig.subplots_adjust(left=0.335, right=0.955, top=0.880, bottom=0.190)

ys = list(range(len(items)))[::-1]
bars = ax.barh(ys, [x[1] for x in items], height=0.52,
               color=[x[2] for x in items], zorder=3,
               edgecolor="white", linewidth=0.9)
ax.set_yticks(ys)
ax.set_yticklabels([x[0] for x in items], fontsize=11.6, linespacing=1.7)
ax.set_xlim(0, 275)
ax.set_ylim(-0.70, 4.70)
ax.set_xlabel("金额（亿元）", fontsize=12)
ax.set_title("同样一年，五个数字：每个回答不同的问题", fontsize=15.5, pad=14)

for b, (_, v, _) in zip(bars, items):
    y = b.get_y() + b.get_height() / 2
    ax.text(v + 4, y, f"{v:,.2f}", ha="left", va="center",
            fontsize=13, weight="bold", color="#222222", zorder=6)

clean_axes(ax)

fig.text(0.012, 0.090,
         "从下往上看是「越算越宽」：扣非 60.11 只算主业；归母 84.53 加上一次性收益；"
         "净利润 84.64 再加上少数股东；自由现金流 177.61 换成现金视角；经营现金流 217.40 是现金流的最宽口径。",
         ha="left", va="bottom", fontsize=9.6, color="#333333")
fig.text(0.012, 0.044,
         "五个数字都对，没有一个是「假的」。区别只在口径——"
         "所以引用任何一个之前，先问一句：它回答的是「赚了多少」还是「收到多少」。",
         ha="left", va="bottom", fontsize=9.4, color=C_GRAY)
fig.text(0.985, 0.002,
         "数据来源：伊利 2024 年报 page_008、page_092、page_094、page_095；单位：亿元",
         ha="right", va="bottom", fontsize=9.2, color=C_GRAY)

save(fig, "w08d40_five_numbers.png")
