# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 8 周第 38 章配图 1：三类现金流与现金净变动。

经营 +217.40、投资 -327.09、筹资 -72.78、汇率 -0.18，合计现金净减少 182.66 亿元。
数字全部来自 data/yili2024.json 的 cashflow 段。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, C_GREEN, C_BLUE, C_ORANGE, C_GRAY, C_PURPLE,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
cf = d["cashflow"]
Y = lambda v: v / 1e8  # noqa: E731

items = [
    ("经营活动", Y(cf["operating_net"]), C_GREEN),
    ("投资活动", Y(cf["investing_net"]), C_BLUE),
    ("筹资活动", Y(cf["financing_net"]), C_ORANGE),
    ("汇率影响", Y(cf["fx_effect"]), C_GRAY),
    ("现金净变动", Y(cf["net_cash_change"]), C_PURPLE),
]
names = [x[0] for x in items]
vals = [x[1] for x in items]
colors = [x[2] for x in items]

fig, ax = plt.subplots(figsize=(12.6, 6.8))
fig.subplots_adjust(left=0.16, right=0.965, top=0.875, bottom=0.185)

ys = list(range(len(items)))[::-1]
bars = ax.barh(ys, vals, height=0.52, color=colors, zorder=3,
               edgecolor="white", linewidth=0.8)
ax.set_yticks(ys)
ax.set_yticklabels(names, fontsize=13)
ax.set_xlim(-400, 300)
ax.set_ylim(-0.72, 4.72)
ax.set_xlabel("金额（亿元）", fontsize=12)
ax.axvline(0, color="#888888", lw=1.1, zorder=1)
ax.set_title("伊利 2024 年：经营赚进来 217 亿，投资花出去 327 亿",
             fontsize=15, pad=14)
ax.tick_params(axis="y", pad=8)

for b, v in zip(bars, vals):
    y = b.get_y() + b.get_height() / 2
    if abs(v) >= 60:
        ax.text(v + (10 if v >= 0 else -10), y, f"{v:+,.2f}",
                ha="left" if v >= 0 else "right", va="center",
                fontsize=12.5, weight="bold", color="#222222", zorder=6)
    else:
        ax.text(v + (-10 if v < 0 else 10), y, f"{v:+,.2f}",
                ha="right" if v < 0 else "left", va="center",
                fontsize=11.5, weight="bold", color="#222222", zorder=6)

clean_axes(ax)

fig.text(0.012, 0.085,
         "经营现金流 217.40 亿元是「做生意收回来的钱」；投资 -327.09 亿元主要是买大额存单与理财（投资支付的现金 342.54 亿元）；"
         "筹资 -72.78 亿元是还债与分红的结果。",
         ha="left", va="bottom", fontsize=9.6, color="#333333")
fig.text(0.012, 0.038,
         "四行相加：217.40 - 327.09 - 72.78 - 0.18 = -182.66 亿元，与报表「现金及现金等价物净增加额」一致。",
         ha="left", va="bottom", fontsize=9.4, color=C_GRAY)
fig.text(0.985, 0.002,
         "数据来源：伊利 2024 年报 page_094、page_095；单位：亿元",
         ha="right", va="bottom", fontsize=9.2, color=C_GRAY)

save(fig, "w08d38_three_flows.png")
