# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 7 周第 34 章配图：利润总额 101.27 → 净利润 84.64 → 归母 84.53（伊利，亿元）。

两道关：所得税 16.63 亿元、少数股东损益 0.11 亿元。
数字全部来自 data/yili2024.json 的 income 段。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, waterfall, label, C_BLUE, C_GREEN, C_RED, C_GRAY, C_ORANGE,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
inc = d["income"]

pretax = inc["profit_before_tax"] / 1e8
tax = inc["income_tax"] / 1e8
net = inc["net_profit"] / 1e8
minority = inc["net_profit_minority"] / 1e8
parent = inc["net_profit_parent"] / 1e8
etr = tax / pretax * 100

fig, ax = plt.subplots(figsize=(12.4, 7.0))
steps = [
    ("利润总额", pretax, "total"),
    ("减：所得税费用", tax, "down"),
    ("净利润", net, "total"),
    ("减：少数股东损益", minority, "down"),
    ("归母净利润", parent, "total"),
]
waterfall(ax, steps, unit="亿元", fmt="{:,.2f}", fontsize=12.0,
          down_color=C_RED, total_color=C_BLUE, bar_width=0.50, title=None)
ax.set_ylim(-3, 128)
ax.set_xticklabels([s[0] for s in steps], fontsize=11.4)

ax.text(-0.45, 124.0,
        f"第一道关：所得税 {tax:,.2f} 亿元，有效税率 {etr:.2f}%（法定 25%）",
        fontsize=10.8, color="#333333", ha="left", va="center")
ax.text(-0.45, 114.0,
        f"第二道关：少数股东损益仅 {minority:,.2f} 亿元，归母与净利润几乎相等",
        fontsize=10.8, color="#333333", ha="left", va="center")

ax.set_title("101.27 亿利润总额，过两道关，股东拿到 84.53 亿",
             fontsize=14.8, pad=16)

fig.text(
    0.012, -0.035,
    "数据来源：伊利 2024 年报 page_092（合并利润表）、page_213（所得税费用调节表）。\n"
    f"有效税率 = {tax:,.2f} ÷ {pretax:,.2f} = {etr:.2f}%；2023 年有效税率仅 12.26%，"
    "税率回升本身也压低了 2024 年的净利润增速。",
    ha="left", va="top", fontsize=9.6, color=C_GRAY, linespacing=1.6,
)

save(fig, "w07d34_profit_layers.png")
