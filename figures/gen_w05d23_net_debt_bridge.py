# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 5 周第 23 章核心配图：伊利 2024 年「净有息负债桥」。

605.58 亿元有息负债，减掉货币资金 254.04 亿、其他流动资产里的大额存单 118.26 亿、
其他非流动资产里的大额存单 279.77 亿，得到 -46.50 亿元——账上的类现金比有息负债还多。

口径：
- 有息负债 = 短期借款 + 短期应付债券 + 一年内到期的非流动负债 + 长期借款 + 租赁负债（page_088、page_195）；
- 类现金 = 货币资金 + 大额存单及定期存款（其他流动资产 + 其他非流动资产，page_087、page_166、page_188）。
数字全部来自 data/yili2024.json（已核实），不手打。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import (
    save, label, clean_axes, C_GRAY, C_RED, C_GREEN, C_BLUE, C_ORANGE, C_GOLD,
)
from figures._data import load
import matplotlib.pyplot as plt

d = load("yili2024")
b, r, n = d["balance"], d["ratios"], d["notes"]
yi = 1e8

ibd = r["interest_bearing_debt"] / yi
cash = b["cash"] / yi
td_cur = n["time_deposits_in_other_current_assets"] / yi
td_non = n["time_deposits_in_other_noncurrent_assets"] / yi
net = r["net_interest_bearing_debt"] / yi
cash_all = r["cash_and_deposits"] / yi

# 逐步累计
lvl0 = ibd
lvl1 = lvl0 - cash
lvl2 = lvl1 - td_cur
lvl3 = lvl2 - td_non

fig, ax = plt.subplots(figsize=(14.0, 7.4))
fig.subplots_adjust(left=0.095, right=0.975, top=0.855, bottom=0.17)

xs = [0, 1, 2, 3, 4]
w = 0.52

# 起点：有息负债整根
ax.bar(xs[0], ibd, width=w, color=C_ORANGE, zorder=3,
       edgecolor="white", linewidth=0.8)
# 三个减项：从累计线往下掉
ax.bar(xs[1], cash, bottom=lvl1, width=w, color=C_GREEN, zorder=3,
       edgecolor="white", linewidth=0.8)
ax.bar(xs[2], td_cur, bottom=lvl2, width=w, color=C_GREEN, zorder=3,
       edgecolor="white", linewidth=0.8)
ax.bar(xs[3], td_non, bottom=lvl3, width=w, color=C_GREEN, zorder=3,
       edgecolor="white", linewidth=0.8)
# 终点：净有息负债为负，从 0 往下画
ax.bar(xs[4], abs(net), bottom=net, width=w, color=C_RED, zorder=3,
       edgecolor="white", linewidth=0.8)

# 连接线
for i, lvl in enumerate([ibd, lvl1, lvl2, lvl3]):
    ax.plot([xs[i] + w / 2, xs[i + 1] - w / 2], [lvl, lvl],
            color="#8c8c8c", lw=1.0, ls=(0, (4, 3)), zorder=2)

# 柱顶/柱内标注
ax.text(xs[0], ibd + 14, f"{ibd:,.2f}", ha="center", va="bottom",
        fontsize=13.5, weight="bold", color="#222222", zorder=6)
for xi, v, top, bot in [(xs[1], cash, lvl0, lvl1),
                        (xs[2], td_cur, lvl1, lvl2),
                        (xs[3], td_non, lvl2, lvl3)]:
    ax.text(xi, (top + bot) / 2, f"-{v:,.2f}", ha="center", va="center",
            fontsize=12.5, weight="bold", color="white", zorder=6)
ax.text(xs[4], net - 16, f"{net:,.2f}", ha="center", va="top",
        fontsize=14, weight="bold", color=C_RED, zorder=6)

# 累计落点：写在绿色柱体右侧、紧贴虚线下方，不压柱体
for xi, lvl in [(xs[1], lvl1), (xs[2], lvl2)]:
    ax.text(xi + w / 2 + 0.10, lvl - 8, f"余 {lvl:,.2f}", ha="left", va="top",
            fontsize=10.2, color="#666666", zorder=6)

ax.set_xticks(xs)
ax.set_xticklabels(["有息负债\n合计", "减：\n货币资金", "减：大额存单\n（其他流动资产）",
                    "减：大额存单\n（其他非流动资产）", "净有息负债"], fontsize=12)
ax.set_ylim(-175, 700)
ax.set_xlim(-0.6, 4.62)
ax.set_ylabel("金额（亿元）", fontsize=11.5)
ax.axhline(0, color="#999999", lw=1.0, zorder=1)
ax.set_title("伊利 2024 年净有息负债：605.58 亿元有息负债，对上 652.07 亿元类现金",
             fontsize=14.5, pad=14)
clean_axes(ax)

label(ax, 1.05, -80,
      f"类现金合计 {cash_all:,.2f} 亿元 > 有息负债 {ibd:,.2f} 亿元\n"
      f"净有息负债 {net:,.2f} 亿元：不是「没有债」，是「债被现金盖住了」",
      fontsize=11.8, color="#222222", ha="center", va="center")

fig.text(0.012, 0.030,
         "数据来源：伊利 2024 年报 page_087（货币资金、其他流动资产、其他非流动资产）、"
         "page_088（短期借款、一年内到期、长期借款、租赁负债）、page_166、page_188（大额存单明细）、page_195（短期应付债券）。",
         fontsize=9.6, color=C_GRAY)

save(fig, "w05d23_net_debt_bridge.png")
