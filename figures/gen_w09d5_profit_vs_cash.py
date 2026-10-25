# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 9 周第 45 章配图之二：净利润 vs 经营活动现金流（伊利、蒙牛，2024）。

这张图专门点破「利润 ≠ 现金」：蒙牛这一年净利只剩 1.05 亿（归母），
但经营现金流还有 83.32 亿——主业还在造钱，只是账面被 39.81 亿减值吃掉了。
伊利的逻辑一样：净利 84.64 亿，现金流 217.40 亿。

所以每组画三根柱：净利润、经营现金流、两者之差（调节项）。
差额那根用灰色，明确表示「折旧、减值、营运资本变动」加回来的部分。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, C_PURPLE, C_GREEN, C_GRAY,
)
from figures._data import load  # noqa: E402

y = load("yili2024")
m = load("mengniu2024")
yi_ = 1e8

y_np = y["income"]["net_profit"] / yi_
y_ocf = y["cashflow"]["operating_net"] / yi_
y_gap = y_ocf - y_np

m_np = m["income"]["net_profit"] / yi_
m_ocf = m["cashflow"]["operating_net"] / yi_
m_gap = m_ocf - m_np

m_imp = m["goodwill_detail"]["bellamy"]["impairment_2024"]["total_impact"] / yi_
m_np_parent = m["income"]["net_profit_parent"] / yi_
y_imp = y["core_earnings"]["impairment_2024"] / yi_

fig, ax = plt.subplots(figsize=(12.4, 7.4))
fig.subplots_adjust(left=0.095, right=0.975, top=0.80, bottom=0.235)

x = np.arange(2)
w = 0.26
vals = [[y_np, y_ocf, y_gap], [m_np, m_ocf, m_gap]]
colors = [C_PURPLE, C_GREEN, "#bdbdbd"]
names = ["净利润", "经营活动现金流净额", "差额（折旧+减值+营运资本）"]

for k in range(3):
    bars = ax.bar(x + (k - 1) * w, [vals[0][k], vals[1][k]], w,
                  color=colors[k], zorder=3, label=names[k])
    for bb, v in zip(bars, [vals[0][k], vals[1][k]]):
        ax.text(bb.get_x() + bb.get_width() / 2, v + 4.0, f"{v:,.2f}",
                ha="center", va="bottom", fontsize=10.8, weight="bold",
                color="#1a1a1a", zorder=6)

ax.set_xticks(x)
ax.set_xticklabels(["伊利", "蒙牛"], fontsize=12.6)
ax.set_xlim(-0.62, 1.62)
ax.set_ylim(0, 292)
ax.set_ylabel("金额（亿元）", fontsize=11.6)
ax.tick_params(axis="y", labelsize=10.6)
ax.grid(axis="y", color="#ececec", lw=0.8, zorder=0)
clean_axes(ax)

# 图例横排放在标题下方（图内顶部），不压柱体
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.10), ncol=3,
          fontsize=10.0, frameon=False)

# 两组各补一条说明。不用引线——引线会穿过柱顶数值，改用白底注释框直接放在空白处。
ax.text(-0.03, 266,
        f"伊利：减值 {y_imp:,.2f} 亿\n净利仍守住 {y_np:,.2f} 亿",
        ha="center", va="center", fontsize=10.0, color="#6a51a3",
        weight="bold", linespacing=1.6, zorder=8,
        bbox=dict(boxstyle="round,pad=0.40", fc="white", ec="#6a51a3",
                  lw=1.1, alpha=0.97))
ax.text(1.02, 266,
        f"蒙牛：贝拉米减值影响 {m_imp:,.2f} 亿\n净利润只剩 {m_np:,.2f} 亿（归母 {m_np_parent:,.2f} 亿）",
        ha="center", va="center", fontsize=10.0, color="#c0392b",
        weight="bold", linespacing=1.6, zorder=8,
        bbox=dict(boxstyle="round,pad=0.40", fc="white", ec="#c0392b",
                  lw=1.1, alpha=0.97))

fig.suptitle(f"利润 $\\neq$ 现金：蒙牛归母净利只剩 {m_np_parent:,.2f} 亿，经营现金流仍有 {m_ocf:,.2f} 亿",
             fontsize=15.0, weight="bold", y=0.955)

fig.text(0.012, 0.132,
         "差额从哪来：折旧摊销不用付现、减值损失不用付现、营运资本变动（存货减少、应付增加）也会让现金多于利润。",
         fontsize=9.8, color="#333333")
fig.text(0.012, 0.088,
         f"蒙牛这组特别典型：商誉减值 {m['cashflow']['goodwill_impairment'] / yi_:.2f} 亿 + 商标减值 "
         f"{m['cashflow']['intangible_impairment'] / yi_:.2f} 亿，扣掉递延税转回后净影响 {m_imp:,.2f} 亿，"
         "全部在利润表上扣了钱，却一分现金没出去。",
         fontsize=9.8, color="#333333")
fig.text(0.012, 0.045,
         "数据来源：伊利 2024 年报 page_092、page_094、page_211；蒙牛 2024 年报 page_140、page_147、page_161。"
         f"柱状图用「净利润」而非「归母净利润」（蒙牛净利润 {m_np:,.2f} 亿，其中归母 {m_np_parent:,.2f} 亿），"
         "与各自现金流量表的调节起点一致。",
         fontsize=9.2, color=C_GRAY)
fig.text(0.012, 0.010,
         "所以看到「净利暴跌」先别下结论，翻到现金流量表看经营现金流——主业还在不在赚钱，那张表更诚实。",
         fontsize=9.4, color="#333333")

save(fig, "w09d5_profit_vs_cash.png")
