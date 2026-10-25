# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 5 周第 23 章配图之二：有息负债的期限结构，以及「借新还旧」的滚动规模。

左边：605.58 亿元有息负债里，556.08 亿元一年内要还或续借，只有 49.49 亿元在一年以上；
      竖线是货币资金 254.04 亿元——短债比手上的现金多出 302.05 亿元。
右边：2024 年取得借款 2,188.31 亿元、偿还债务 2,162.98 亿元，一年滚了近 2,200 亿元。

数字全部来自 data/yili2024.json（已核实），不手打。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import (
    save, clean_axes, C_BLUE, C_ORANGE, C_RED, C_GREEN, C_GRAY,
)
from figures._data import load
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

d = load("yili2024")
b, cf = d["balance"], d["cashflow"]
yi = 1e8

st = b["short_term_borrowings"] / yi
stb = b["short_term_bonds_payable"] / yi
due1y = b["noncurrent_liabilities_due_1y"] / yi
ltb = b["long_term_borrowings"] / yi
lease = b["lease_liabilities"] / yi
# 竖排「长期借款 46.87」需要约 7.5 亿数据宽度；租赁负债 2.63 亿的色块只有这么宽
LT_LABEL_SPACE = 8.0
cash = b["cash"] / yi

within1y = st + stb + due1y
beyond1y = ltb + lease
gap = within1y - cash

borrow = cf["borrowings_received"] / yi
repay = cf["borrowings_repaid"] / yi
net_borrow = borrow - repay

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.0, 7.0),
                               gridspec_kw={"width_ratios": [1.45, 1.0],
                                            "wspace": 0.26})
fig.subplots_adjust(left=0.075, right=0.975, top=0.83, bottom=0.155)

# ── 左：期限结构 ───────────────────────────────────────────────
ypos = [1, 0]
h = 0.36
segs_1y = [("短期借款", st, C_ORANGE), ("短期应付债券", stb, C_ORANGE),
           ("一年内到期的非流动负债", due1y, C_ORANGE)]

left = 0.0
for name, v, col in segs_1y:
    ax1.barh(ypos[0], v, left=left, height=h, color=col, zorder=3,
             edgecolor="white", linewidth=0.9)
    ax1.text(left + v / 2, ypos[0], f"{v:,.2f}", ha="center", va="center",
             color="white", fontsize=11, weight="bold", zorder=6)
    left += v

ax1.barh(ypos[1], ltb, left=0, height=h, color=C_BLUE, zorder=3,
         edgecolor="white", linewidth=0.9)
ax1.text(ltb + 3, ypos[1], f"长期借款 {ltb:,.2f}", ha="left",
         va="center", color="#333333", fontsize=11, weight="bold", zorder=6)
ax1.barh(ypos[1], lease, left=ltb, height=h, color=C_BLUE, zorder=3,
         edgecolor="white", linewidth=0.9)
ax1.text(ltb + lease + LT_LABEL_SPACE, ypos[1] - 0.30,
         f"租赁负债 {lease:,.2f}", ha="left", va="center",
         color="#333333", fontsize=11, weight="bold", zorder=6)

ax1.axvline(cash, color=C_RED, lw=1.8, ls="--", zorder=4)
ax1.text(cash + 8, 1.50, f"货币资金 {cash:,.2f}", color=C_RED, fontsize=11.5,
         ha="left", va="center", weight="bold", zorder=6,
         bbox=dict(boxstyle="round,pad=0.28", fc="white", ec="none", alpha=0.92))

ax1.set_yticks(ypos)
ax1.set_yticklabels(["1 年内要还\n或需续借", "1 年以上"], fontsize=12.5)
ax1.set_ylim(-0.62, 1.72)
ax1.set_xlim(0, 640)
ax1.set_xlabel("金额（亿元）", fontsize=11.5)
ax1.set_title("605.58 亿元有息负债的期限结构", fontsize=13.5, pad=10)
ax1.text(within1y - 10, 1.29, f"合计 {within1y:,.2f}", ha="right", va="center",
         fontsize=12, weight="bold", color=C_ORANGE, zorder=6)
ax1.text(ltb + lease + LT_LABEL_SPACE, -0.42, f"合计 {beyond1y:,.2f}", ha="left", va="center",
         fontsize=12, weight="bold", color=C_BLUE, zorder=6)
clean_axes(ax1)

handles = [Patch(facecolor=C_ORANGE, label="一年内到期"),
           Patch(facecolor=C_BLUE, label="一年以上到期")]
ax1.legend(handles=handles, loc="lower right", bbox_to_anchor=(0.99, 0.02),
           frameon=False, fontsize=11.5)

# ── 右：借新还旧的滚动规模 ──────────────────────────────────────
names = ["取得借款\n收到的现金", "偿还债务\n支付的现金"]
vals = [borrow, repay]
bars = ax2.bar([0, 1], vals, width=0.46, color=[C_GREEN, C_GRAY], zorder=3)
for bar, v in zip(bars, vals):
    ax2.text(bar.get_x() + bar.get_width() / 2, v + 55, f"{v:,.2f}",
             ha="center", va="bottom", fontsize=13.5, weight="bold", zorder=6)
ax2.set_xticks([0, 1])
ax2.set_xticklabels(names, fontsize=12.5)
ax2.set_ylim(0, 2950)
ax2.set_xlim(-0.62, 1.62)
ax2.set_ylabel("2024 年发生额（亿元）", fontsize=11.5)
ax2.set_title("一年借进来 2,188 亿，还出去 2,163 亿", fontsize=13.5, pad=10)
ax2.text(0.5, 2760, f"净增只有 {net_borrow:,.2f} 亿元", ha="center", va="center",
         fontsize=12.5, weight="bold", color="#222222", zorder=6,
         bbox=dict(boxstyle="round,pad=0.34", fc="white", ec="#cccccc", lw=0.8))
ax2.text(0.5, 2520, "规模几乎全部是「借新还旧」", ha="center", va="center",
         fontsize=11.5, color="#444444", zorder=6)
clean_axes(ax2)

fig.suptitle(f"短期债务 {within1y:,.2f} 亿元，手上现金只有 {cash:,.2f} 亿元，缺口 {gap:,.2f} 亿元",
             fontsize=15.5, weight="bold", y=0.935)
fig.text(0.075, 0.030,
         "数据来源：伊利 2024 年报 page_087、page_088（负债科目）、page_095（筹资活动现金流）。"
         "短期应付债券 100.24 亿元列在「其他流动负债」中（page_195）。分项相加与合计的 0.01 尾差来自四舍五入。",
         fontsize=9.6, color=C_GRAY)

save(fig, "w05d23_debt_maturity.png")
