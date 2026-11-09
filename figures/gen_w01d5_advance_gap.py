# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 1 周第 5 章配图之二：合同负债（预收）的「时点差」长什么样。

4 月经销商先打 100 万元，5 月发货（收入 100、成本 60，利润 40），6 月才付原料款。
两条阶梯线分别是累计利润与累计经营现金，中间的阴影宽度是"还没结清的那一格"：
4 月是合同负债 100 万元，5 月换成应付账款 60 万元，6 月付清才合并。
示意数字，与正文那三行时间线表一一对应。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, label, C_GREEN, C_PURPLE,
)

F_GAP = "#fdf0d9"          # 差额带的浅橙底
C_GAP = "#c9711a"          # 差额带描边与文字

x = [0, 1, 2]
profit = [0, 40, 40]       # 4 月货没发；5 月发货：收入 100 - 成本 60 = 利润 40
cash = [100, 100, 40]      # 4 月收 100 万；5 月原料钱还欠着；6 月付 60 万
ticks = [
    "4 月：经销商先打 100 万\n现金 +100、合同负债 +100\n利润表不动",
    "5 月：发货，原料钱还欠着\n收入 +100、成本 +60，利润 40\n现金不动",
    "6 月：付原料款 60 万\n应付 -60、现金 -60\n利润仍是 40",
]

fig, ax = plt.subplots(figsize=(10.6, 6.2))
fig.subplots_adjust(left=0.095, right=0.985, top=0.755, bottom=0.225)

ax.set_xlim(-0.24, 2.18)
ax.set_ylim(-14, 132)

ax.step(x, profit, where="post", color=C_PURPLE, lw=2.9, zorder=4,
        solid_capstyle="round")
ax.step(x, cash, where="post", color=C_GREEN, lw=2.9, zorder=4,
        solid_capstyle="round")
ax.plot(x, profit, "o", ms=8.5, color=C_PURPLE, mec="white", mew=1.6, zorder=6)
ax.plot(x, cash, "o", ms=8.5, color=C_GREEN, mec="white", mew=1.6, zorder=6)

# 第一段差额：4 月，合同负债 100 万元
ax.fill_between([0, 1], [0, 0], [100, 100], color=F_GAP, zorder=2)
ax.plot([0, 1], [0, 0], color=C_GAP, lw=1.0, ls=(0, (3, 2)), zorder=3)
ax.plot([0, 1], [100, 100], color=C_GAP, lw=1.0, ls=(0, (3, 2)), zorder=3)
ax.annotate("", xy=(0.50, 100), xytext=(0.50, 0),
            arrowprops=dict(arrowstyle="<->", color=C_GAP, lw=1.7,
                            shrinkA=0, shrinkB=0), zorder=7)
label(ax, 0.26, 56, "差 100 万\n＝合同负债", color=C_GAP, fontsize=11.5,
      weight="bold", fc="white", alpha=0.95)

# 第二段差额：5 月，换成应付账款 60 万元
ax.fill_between([1, 2], [40, 40], [100, 100], color=F_GAP, zorder=2)
ax.plot([1, 2], [40, 40], color=C_GAP, lw=1.0, ls=(0, (3, 2)), zorder=3)
ax.plot([1, 2], [100, 100], color=C_GAP, lw=1.0, ls=(0, (3, 2)), zorder=3)
ax.annotate("", xy=(1.72, 100), xytext=(1.72, 40),
            arrowprops=dict(arrowstyle="<->", color=C_GAP, lw=1.7,
                            shrinkA=0, shrinkB=0), zorder=7)
label(ax, 1.32, 70, "差 60 万\n＝应付账款", color=C_GAP, fontsize=11.5,
      weight="bold", fc="white", alpha=0.95)

label(ax, 0.04, 110, "现金 100", color=C_GREEN, fontsize=12,
      weight="bold", ha="left")
label(ax, 0.04, 9, "利润 0：货还没发，收入不算",
      color=C_PURPLE, fontsize=11, weight="bold", ha="left")
label(ax, 1.04, 31, "利润 40：100 收入减 60 成本", color=C_PURPLE,
      fontsize=11, weight="bold", ha="left")
label(ax, 2.14, 4.5, "6 月付清原料款\n两条线合并", color=C_GAP, fontsize=10.8,
      ha="right", va="center")

for _x in x:
    ax.axvline(_x, color="#e2e2e2", lw=0.9, ls=(0, (2, 3)), zorder=0)
ax.set_xticks(x)
ax.set_xticklabels(ticks, fontsize=10.6)
ax.set_ylabel("累计金额（万元）", fontsize=11.8)
ax.set_title("预收不是白赚：100 万收入里有 60 万成本，差额只是换了主人", fontsize=13,
             pad=30, loc="left")
ax.legend(
    handles=[
        plt.Line2D([], [], color=C_PURPLE, lw=2.9, marker="o", ms=7.5,
                   mec="white", label="累计利润（利润表）"),
        plt.Line2D([], [], color=C_GREEN, lw=2.9, marker="o", ms=7.5,
                   mec="white", label="累计经营现金（现金流量表）"),
        plt.Rectangle((0, 0), 1, 1, fc=F_GAP, ec=C_GAP, lw=1.2,
                      label="阴影宽 = 还没结清的那一格"),
    ],
    loc="lower left", bbox_to_anchor=(0.0, 1.0), ncol=3, frameon=False,
    fontsize=10.8, handlelength=2.0, columnspacing=2.2, borderaxespad=0.2,
)
ax.axhline(0, color="#cccccc", lw=1.0, zorder=1)
ax.grid(axis="y", color="#eeeeee", lw=0.9, zorder=0)
clean_axes(ax)

save(fig, "w01d5_advance_gap.png")
