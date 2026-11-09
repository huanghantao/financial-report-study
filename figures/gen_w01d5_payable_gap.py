# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 1 周第 5 章配图之一：应付账款的「时点差」长什么样。

3 月赊购 4 万元牛奶 → 4 月把奶茶卖掉、收到 10 万元、奶款未付 → 5 月才付奶款。
两条阶梯线分别是累计利润与累计经营现金，中间的阴影宽度就是应付账款余额。
示意数字，与正文那张三行时间线表一一对应。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, label, C_GREEN, C_PURPLE, C_GRAY,
)

F_GAP = "#fdf0d9"          # 差额带的浅橙底
C_GAP = "#c9711a"          # 差额带描边与文字

x = [0, 1, 2]
profit = [0, 6, 6]         # 3 月不动；4 月收 10、成本 4 → 利润 6；5 月不动
cash = [0, 10, 6]          # 3 月不动；4 月收到 10 万；5 月付奶款 4 万
ticks = [
    "3 月：赊购 4 万元牛奶\n存货 +4、应付 +4\n两张表都不动",
    "4 月：奶茶卖掉，收到 10 万\n收入 +10、成本 +4\n利润 6、现金 10",
    "5 月：付奶款 4 万\n应付 -4、现金 -4\n利润仍是 6",
]

fig, ax = plt.subplots(figsize=(10.6, 6.2))
fig.subplots_adjust(left=0.095, right=0.985, top=0.755, bottom=0.225)

ax.set_xlim(-0.24, 2.18)
ax.set_ylim(-1.2, 14.4)

ax.step(x, profit, where="post", color=C_PURPLE, lw=2.9, zorder=4,
        solid_capstyle="round")
ax.step(x, cash, where="post", color=C_GREEN, lw=2.9, zorder=4,
        solid_capstyle="round")
ax.plot(x, profit, "o", ms=8.5, color=C_PURPLE, mec="white", mew=1.6, zorder=6)
ax.plot(x, cash, "o", ms=8.5, color=C_GREEN, mec="white", mew=1.6, zorder=6)

# 差额带：4 月到 5 月之间，现金在上、利润在下
ax.fill_between([1, 2], [6, 6], [10, 10], color=F_GAP, zorder=2)
ax.plot([1, 2], [6, 6], color=C_GAP, lw=1.0, ls=(0, (3, 2)), zorder=3)
ax.plot([1, 2], [10, 10], color=C_GAP, lw=1.0, ls=(0, (3, 2)), zorder=3)
ax.annotate("", xy=(1.74, 10), xytext=(1.74, 6),
            arrowprops=dict(arrowstyle="<->", color=C_GAP, lw=1.7,
                            shrinkA=0, shrinkB=0), zorder=7)
label(ax, 1.30, 8.0, "差 4 万\n＝应付账款余额", color=C_GAP, fontsize=11.5,
      weight="bold", fc="white", alpha=0.95)

label(ax, 1.06, 11.2, "现金 10", color=C_GREEN, fontsize=12,
      weight="bold", ha="left")
label(ax, 1.06, 4.8, "利润 6", color=C_PURPLE, fontsize=12,
      weight="bold", ha="left")
label(ax, 2.16, 2.4, "5 月付清奶款\n两条线合并", color=C_GAP, fontsize=11,
      ha="right", va="center")
label(ax, 0.02, 12.7, "3 月这一格：两张表都不动，两条线都贴着 0",
      color=C_GRAY, fontsize=11, ha="left")

for _x in x:
    ax.axvline(_x, color="#e2e2e2", lw=0.9, ls=(0, (2, 3)), zorder=0)
ax.set_xticks(x)
ax.set_xticklabels(ticks, fontsize=10.6)
ax.set_ylabel("累计金额（万元）", fontsize=11.8)
ax.set_title("应付账款：先拿货、后付款，欠供应商的是钱", fontsize=13.5,
             pad=30, loc="left")
ax.legend(
    handles=[
        plt.Line2D([], [], color=C_PURPLE, lw=2.9, marker="o", ms=7.5,
                   mec="white", label="累计利润（利润表）"),
        plt.Line2D([], [], color=C_GREEN, lw=2.9, marker="o", ms=7.5,
                   mec="white", label="累计经营现金（现金流量表）"),
        plt.Rectangle((0, 0), 1, 1, fc=F_GAP, ec=C_GAP, lw=1.2,
                      label="阴影宽 = 应付账款余额"),
    ],
    loc="lower left", bbox_to_anchor=(0.0, 1.0), ncol=3, frameon=False,
    fontsize=10.8, handlelength=2.0, columnspacing=2.2, borderaxespad=0.2,
)
ax.axhline(0, color="#cccccc", lw=1.0, zorder=1)
ax.grid(axis="y", color="#eeeeee", lw=0.9, zorder=0)
clean_axes(ax)

save(fig, "w01d5_payable_gap.png")
