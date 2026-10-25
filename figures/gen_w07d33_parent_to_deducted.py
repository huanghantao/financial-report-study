# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 7 周第 33 章配图：归母净利润 84.53 → 扣非归母净利润 60.11（伊利，亿元）。

中间减掉的是非经常性损益 24.42 亿元（税后、扣少数股东后）。
数字全部来自 data/yili2024.json 的 income / nonrecurring 段。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, waterfall, label, C_BLUE, C_GREEN, C_RED, C_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
inc = d["income"]
nr = d["nonrecurring"]

parent = inc["net_profit_parent"] / 1e8
nonrec = nr["total"] / 1e8
deducted = nr["net_profit_deducted"] / 1e8

fig, ax = plt.subplots(figsize=(11.8, 7.2))
steps = [
    ("归母净利润", parent, "total"),
    ("减：非经常性损益\n（税后、扣少数股东）", nonrec, "down"),
    ("扣非归母净利润", deducted, "total"),
]
waterfall(ax, steps, unit="亿元", fmt="{:,.2f}", fontsize=12.2,
          down_color=C_RED, total_color=C_BLUE, bar_width=0.46, title=None)
ax.set_ylim(-3, 112)
ax.set_xticklabels([s[0] for s in steps], fontsize=11.8)

label(ax, 1.0, 46.0,
      f"减掉的 {nonrec:,.2f} 亿元\n= 归母净利润的 {nonrec / parent * 100:.1f}%\n"
      "主要是处置昌吉盛新股权的收益",
      fontsize=11.2, color="#333333")
label(ax, 2.0, 74.0, "这才是「卖牛奶」赚的钱",
      fontsize=11.8, color=C_GREEN, weight="bold")

ax.set_title("84.53 亿归母净利润，剔掉 24.42 亿一次性收益，只剩 60.11 亿",
             fontsize=14.6, pad=16)

fig.text(
    0.012, -0.040,
    "数据来源：伊利 2024 年报 page_007（主要会计数据）、page_008 至 page_009（非经常性损益明细）、page_092（利润表）。\n"
    "扣非归母净利润 60.11 亿元，同比下降 40.04%（2023 年 100.26 亿元）；非经常性损益 24.42 亿元，"
    "2023 年仅 4.02 亿元。",
    ha="left", va="top", fontsize=9.6, color=C_GRAY, linespacing=1.6,
)

save(fig, "w07d33_parent_to_deducted.png")
