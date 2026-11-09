# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 1 周第 5 章配图之二：合同负债（预收）的「时点差」长什么样。

4 月经销商先打 100 万元、5 月才发货。
两条阶梯线分别是累计利润与累计经营现金，中间的阴影宽度就是合同负债余额。
与应付账款那张图共用同一套图形语言：形状一样，只是一格欠钱、一格欠货。
示意数字，与正文那两行时间线表一一对应。
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

x = [0, 1]
profit = [0, 100]          # 4 月货没发，利润不动；5 月发货才确认收入 100
cash = [100, 100]          # 4 月收到 100 万；5 月发货不再有现金进出
ticks = [
    "4 月：经销商先打 100 万\n现金 +100、合同负债 +100\n利润表不动",
    "5 月：发货\n收入 +100、合同负债 -100\n利润 100、现金仍 100",
]

fig, ax = plt.subplots(figsize=(10.6, 6.2))
fig.subplots_adjust(left=0.095, right=0.985, top=0.755, bottom=0.225)

ax.set_xlim(-0.24, 1.18)
ax.set_ylim(-14, 140)

ax.step(x, profit, where="post", color=C_PURPLE, lw=2.9, zorder=4,
        solid_capstyle="round")
ax.step(x, cash, where="post", color=C_GREEN, lw=2.9, zorder=4,
        solid_capstyle="round")
ax.plot(x, profit, "o", ms=8.5, color=C_PURPLE, mec="white", mew=1.6, zorder=6)
ax.plot(x, cash, "o", ms=8.5, color=C_GREEN, mec="white", mew=1.6, zorder=6)

ax.fill_between([0, 1], [0, 0], [100, 100], color=F_GAP, zorder=2)
ax.plot([0, 1], [0, 0], color=C_GAP, lw=1.0, ls=(0, (3, 2)), zorder=3)
ax.plot([0, 1], [100, 100], color=C_GAP, lw=1.0, ls=(0, (3, 2)), zorder=3)
ax.annotate("", xy=(0.62, 100), xytext=(0.62, 0),
            arrowprops=dict(arrowstyle="<->", color=C_GAP, lw=1.7,
                            shrinkA=0, shrinkB=0), zorder=7)
label(ax, 0.30, 52, "差 100 万\n＝合同负债余额", color=C_GAP, fontsize=11.5,
      weight="bold", fc="white", alpha=0.95)

label(ax, 0.04, 112, "现金 100", color=C_GREEN, fontsize=12,
      weight="bold", ha="left")
label(ax, 0.04, 10, "利润 0：货还没发，一分收入都不算",
      color=C_PURPLE, fontsize=11.2, weight="bold", ha="left")
label(ax, 1.16, 126, "5 月发货后\n两条线合并", color=C_GAP, fontsize=11,
      ha="right", va="center")

for _x in x:
    ax.axvline(_x, color="#e2e2e2", lw=0.9, ls=(0, (2, 3)), zorder=0)
ax.set_xticks(x)
ax.set_xticklabels(ticks, fontsize=10.6)
ax.set_ylabel("累计金额（万元）", fontsize=11.8)
ax.set_title("合同负债（预收）：先收钱、后交货，欠客户的是货", fontsize=13.5,
             pad=30, loc="left")
ax.legend(
    handles=[
        plt.Line2D([], [], color=C_PURPLE, lw=2.9, marker="o", ms=7.5,
                   mec="white", label="累计利润（利润表）"),
        plt.Line2D([], [], color=C_GREEN, lw=2.9, marker="o", ms=7.5,
                   mec="white", label="累计经营现金（现金流量表）"),
        plt.Rectangle((0, 0), 1, 1, fc=F_GAP, ec=C_GAP, lw=1.2,
                      label="阴影宽 = 合同负债余额"),
    ],
    loc="lower left", bbox_to_anchor=(0.0, 1.0), ncol=3, frameon=False,
    fontsize=10.8, handlelength=2.0, columnspacing=2.2, borderaxespad=0.2,
)
ax.axhline(0, color="#cccccc", lw=1.0, zorder=1)
ax.grid(axis="y", color="#eeeeee", lw=0.9, zorder=0)
clean_axes(ax)

save(fig, "w01d5_advance_gap.png")
