# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 5 周第 24 章配图：伊利 2024 年归母权益构成瀑布。

股本 63.66 → 资本公积 132.11 → 减库存股 7.58 → 其他综合收益 -10.69
→ 盈余公积 32.00 → 未分配利润 322.29 = 归母权益 531.80 亿元。
右侧另加一根「少数股东权益 38.28」，合计所有者权益 570.08 亿元。

数字全部来自 data/yili2024.json（已核实），不手打。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import (
    save, label, clean_axes, C_BLUE, C_GREEN, C_RED, C_PURPLE, C_ORANGE, C_GRAY,
)
from figures._data import load
import matplotlib.pyplot as plt

d = load("yili2024")
b = d["balance"]
yi = 1e8

sc = b["share_capital"] / yi
cr = b["capital_reserve"] / yi
ts = b["treasury_stock"] / yi
oci = b["other_comprehensive_income"] / yi
sr = b["surplus_reserve"] / yi
re_ = b["retained_earnings"] / yi
parent = b["equity_parent"] / yi
minority = b["minority_interest"] / yi
total = b["total_equity"] / yi

fig, ax = plt.subplots(figsize=(14.2, 7.4))
fig.subplots_adjust(left=0.085, right=0.975, top=0.885, bottom=0.20)

w = 0.56
xs = list(range(7))

# 逐格累计
levels = []
run = 0.0
# 1 股本
ax.bar(0, sc, width=w, color=C_BLUE, zorder=3, edgecolor="white")
ax.text(0, sc + 8, f"{sc:,.2f}", ha="center", va="bottom", fontsize=11.5,
        weight="bold", zorder=6)
levels.append((0, 0.0, sc, "total"))
run = sc
# 2 资本公积
ax.bar(1, cr, bottom=run, width=w, color=C_BLUE, zorder=3, edgecolor="white")
ax.text(1, run + cr + 8, f"{cr:,.2f}", ha="center", va="bottom", fontsize=11.5,
        weight="bold", zorder=6)
levels.append((1, run, run + cr, "up"))
run += cr
# 3 库存股（减）
ax.bar(2, ts, bottom=run - ts, width=w, color=C_RED, zorder=3, edgecolor="white")
ax.text(2, run + 8, f"-{ts:,.2f}", ha="center", va="bottom", fontsize=11.5,
        weight="bold", color=C_RED, zorder=6)
levels.append((2, run - ts, run, "down"))
run -= ts
# 4 其他综合收益（负，减）
ax.bar(3, abs(oci), bottom=run + oci, width=w, color=C_RED, zorder=3,
       edgecolor="white")
ax.text(3, run + 10, f"{oci:,.2f}", ha="center", va="bottom", fontsize=11.5,
        weight="bold", color=C_RED, zorder=6)
levels.append((3, run + oci, run, "down"))
run += oci
# 5 盈余公积
ax.bar(4, sr, bottom=run, width=w, color=C_GREEN, zorder=3, edgecolor="white")
ax.text(4, run + sr + 8, f"{sr:,.2f}", ha="center", va="bottom", fontsize=11.5,
        weight="bold", zorder=6)
levels.append((4, run, run + sr, "up"))
run += sr
# 6 未分配利润
ax.bar(5, re_, bottom=run, width=w, color=C_GREEN, zorder=3, edgecolor="white")
ax.text(5, run + re_ + 8, f"{re_:,.2f}", ha="center", va="bottom",
        fontsize=11.5, weight="bold", zorder=6)
levels.append((5, run, run + re_, "up"))
run += re_
# 7 归母权益
ax.bar(6, parent, width=w, color=C_PURPLE, zorder=3, edgecolor="white")
ax.text(6, parent + 8, f"{parent:,.2f}", ha="center", va="bottom",
        fontsize=12.5, weight="bold", color=C_PURPLE, zorder=6)
levels.append((6, 0.0, parent, "total"))

# 连接线
for i in range(6):
    y = levels[i][2] if levels[i][3] != "down" else levels[i][1]
    nxt = levels[i + 1][1] if levels[i + 1][3] in ("up", "down") else levels[i + 1][2]
    if levels[i][3] == "down":
        y = levels[i][1]
    if levels[i + 1][3] == "total":
        nxt = 0.0
    ax.plot([xs[i] + w / 2, xs[i + 1] - w / 2], [y, y], color="#8c8c8c",
            lw=1.0, ls=(0, (4, 3)), zorder=2)

ax.set_xticks(xs)
ax.set_xticklabels(["股本", "资本公积", "减：库存股", "其他综合收益", "盈余公积",
                    "未分配利润", "归母权益"], fontsize=11.8)
ax.set_ylim(0, 620)
ax.set_xlim(-0.62, 6.62)
ax.set_ylabel("金额（亿元）", fontsize=11.5)
ax.set_title("把 531.80 亿元归母权益一层层拆开", fontsize=14.5, pad=14)

label(ax, 2.05, 585,
      f"未分配利润 {re_:,.2f} 亿元，占归母权益 {re_ / parent:.1%}\n"
      f"这家公司的净资产，主要是自己赚出来的，不是股东投进来的",
      fontsize=11.5, color="#222222")
label(ax, 2.5, 305,
      f"库存股 {ts:,.2f} 亿是回购花掉的钱，从权益里直接扣掉；\n"
      f"其他综合收益 {oci:,.2f} 亿是没进利润表的浮亏",
      fontsize=11.2, color="#333333", ha="center")
clean_axes(ax)

fig.text(0.012, 0.032,
         f"数据来源：伊利 2024 年报 page_088（所有者权益各科目）、page_092（其他综合收益明细）。"
         f"归母权益 {parent:,.2f} + 少数股东权益 {minority:,.2f} = 所有者权益合计 {total:,.2f} 亿元。",
         fontsize=9.6, color=C_GRAY)

save(fig, "w05d24_equity_waterfall.png")
