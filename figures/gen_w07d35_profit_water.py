# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 7 周第 35 章配图：84.53 亿元里的「可持续」与「一次性」（伊利，亿元）。

上条：报表口径 84.53 = 主业 60.11 + 一次性收益 24.42；
下条：调整口径 103.82 = 主业 60.11 + 减值加回 43.71（粗算）。
数字全部来自 data/yili2024.json 的 income / nonrecurring / core_earnings 段。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as mpatches  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, label, legend_outside,
    C_BLUE, C_GREEN, C_ORANGE, C_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
inc = d["income"]
nr = d["nonrecurring"]

parent = inc["net_profit_parent"] / 1e8
one_off = nr["total"] / 1e8
core = nr["net_profit_deducted"] / 1e8
impair = d["core_earnings"]["impairment_2024"] / 1e8
etr = inc["income_tax"] / inc["profit_before_tax"]
addback = impair * (1 - etr)
adjusted = core + addback

fig, ax = plt.subplots(figsize=(13.2, 6.9))
h = 0.32
y1, y2 = 0.84, 0.46

# 报表口径
b1 = ax.barh(y1, core, height=h, color=C_GREEN, edgecolor="white",
             linewidth=1.0, zorder=3)
b2 = ax.barh(y1, one_off, left=core, height=h, color=C_ORANGE,
             edgecolor="white", linewidth=1.0, zorder=3)
# 调整口径
b3 = ax.barh(y2, core, height=h, color=C_GREEN, edgecolor="white",
             linewidth=1.0, zorder=3)
b4 = ax.barh(y2, addback, left=core, height=h, color=C_BLUE,
             edgecolor="white", linewidth=1.0, zorder=3)

ax.text(core / 2, y1, f"主业 {core:,.2f}", ha="center", va="center",
        color="white", fontsize=11.8, weight="bold", zorder=5)
ax.text(core + one_off / 2, y1, f"一次性 {one_off:,.2f}", ha="center",
        va="center", color="white", fontsize=11.2, weight="bold", zorder=5)
ax.text(core / 2, y2, f"主业 {core:,.2f}", ha="center", va="center",
        color="white", fontsize=11.8, weight="bold", zorder=5)
ax.text(core + addback / 2, y2, f"减值加回 {addback:,.2f}", ha="center",
        va="center", color="white", fontsize=11.2, weight="bold", zorder=5)

ax.text(core + one_off + 1.6, y1, f"{parent:,.2f}", va="center", ha="left",
        fontsize=13.0, weight="bold", color=C_ORANGE)
ax.text(core + addback + 1.6, y2, f"{adjusted:,.2f}", va="center", ha="left",
        fontsize=13.0, weight="bold", color=C_BLUE)

ax.set_yticks([y2, y1])
ax.set_yticklabels(["调整后\n（粗算）", "报表口径"], fontsize=12.0)
ax.set_ylim(0.24, 1.20)
ax.set_xlim(0, 128)
ax.set_xlabel("归母口径的利润（亿元）", fontsize=11.4)
ax.set_title(f"84.53 亿的含水量：24.42 亿是一次性的，加回减值后约 {adjusted:,.2f} 亿",
             fontsize=14.8, pad=16)

ax.text(126.0, 1.13,
        f"报表数字被两股相反的力量扭曲：一次性收益 +{one_off:,.2f}，减值 -{impair:,.2f}",
        fontsize=10.8, color="#333333", ha="right", va="center")

handles = [
    mpatches.Patch(color=C_GREEN, label="主业赚的钱（扣非口径）"),
    mpatches.Patch(color=C_ORANGE, label="一次性收益（税后）"),
    mpatches.Patch(color=C_BLUE, label="减值加回（税后，粗算）"),
]
ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.02, 1.0),
          frameon=False, fontsize=11)
clean_axes(ax)

fig.text(
    0.012, -0.055,
    f"数据来源：伊利 2024 年报 page_007、page_008 至 page_009（非经常性损益）、page_091 至 page_092（利润表）、"
    f"page_211（减值明细）；data/yili2024.json。\n"
    f"调整后 = 扣非归母净利润 {core:,.2f} + 减值 {impair:,.2f} × (1 - 有效税率 {etr * 100:.2f}%) = {adjusted:,.2f} 亿元。"
    "这是粗算，不是年报口径：把 52.31 亿元减值全部当成一次性，是「上限」；"
    "存货跌价年年都有，保守口径见正文。",
    ha="left", va="top", fontsize=9.5, color=C_GRAY, linespacing=1.6,
)

save(fig, "w07d35_profit_water.png")
