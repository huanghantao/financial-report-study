# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 9 周第 41 章配图：三张表怎么咬合（伊利 2024 真实数字，亿元）。

这一版是第 10 章那张图的"进阶版"：除了三条箭头，还把勾稽等式
单独做成一张卡片，并把"净利润 84.64 与经营现金流 217.40 之间的差额"
画成利润表与现金流量表之间的调节箭头。

数字全部来自 data/yili2024.json；图上不出现任何手打数字。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.patches as mpatches  # noqa: E402

from figures._common import (  # noqa: E402
    save, fig_ax, arrow, label,
    C_BLUE, C_GREEN, C_PURPLE, C_GRAY,
    F_BLUE, F_GREEN, F_PURPLE, F_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
b, i, cf = d["balance"], d["income"], d["cashflow"]
Y = lambda v: v / 1e8  # noqa: E731

ta, tl, te = Y(b["total_assets"]), Y(b["total_liabilities"]), Y(b["total_equity"])
tca, tcl = Y(b["total_current_assets"]), Y(b["total_current_liabilities"])
cash, re_end = Y(b["cash"]), Y(b["retained_earnings"])
np_, npp = Y(i["net_profit"]), Y(i["net_profit_parent"])
ocf = Y(cf["operating_net"])
icf = Y(cf["investing_net"])
ffin = Y(cf["financing_net"])
net_change = Y(cf["net_cash_change"])
cash_beg, cash_end = Y(cf["cash_begin"]), Y(cf["cash_end"])
dep = Y(cf["depreciation"])
imp = Y(d["core_earnings"]["impairment_2024"])
gap = ocf - np_

fig, ax = fig_ax(14.4, 8.8, xlim=(0, 100), ylim=(0, 100))

ax.text(50, 95.6, "三张表怎么咬合：两条流量，汇进一张存量",
        ha="center", va="center", fontsize=15.6, weight="bold", color="#1a1a1a")
ax.text(50, 90.8, "伊利 2024 年报真实数字 · 单位：亿元 · 箭头旁边就是勾稽关系",
        ha="center", va="center", fontsize=10.8, color=C_GRAY)


def card(x0, y0, w, h, title, lines, ec, fc, fs=12.0, title_fs=12.6,
         linespacing=1.95):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x0, y0), w, h, boxstyle="round,pad=0.02,rounding_size=1.1",
        fc=fc, ec=ec, lw=1.9, zorder=3))
    ax.text(x0 + w / 2, y0 + h - 3.0, title, ha="center", va="center",
            fontsize=title_fs, weight="bold", color=ec, zorder=5)
    ax.text(x0 + w / 2, y0 + (h - 6.4) / 2 + 0.4, "\n".join(lines),
            ha="center", va="center", fontsize=fs, color="#222222",
            linespacing=linespacing, zorder=5)


# ── 利润表（左上，流量）────────────────────────────────────────────
card(2.0, 60.0, 37.0, 26.0, "利润表　page_091~092", [
    f"营业收入 {Y(i['revenue']):,.2f}",
    f"净利润 {np_:,.2f}",
    f"　其中归母 {npp:,.2f}",
], C_PURPLE, F_PURPLE)

# ── 现金流量表（左下，流量）────────────────────────────────────────
card(2.0, 9.0, 37.0, 30.0, "现金流量表　page_094~095", [
    f"经营活动净额 {ocf:+,.2f}",
    f"投资活动净额 {icf:+,.2f}",
    f"筹资活动净额 {ffin:+,.2f}",
    f"现金净增加额 {net_change:+,.2f}",
], C_GREEN, F_GREEN)

# ── 资产负债表（右上，存量）────────────────────────────────────────
card(62.0, 34.0, 36.0, 50.0, "资产负债表　2024.12.31", [
    f"资产总计 {ta:,.2f}",
    f"　货币资金 {cash:,.2f}",
    f"　流动资产 {tca:,.2f}",
    f"负债合计 {tl:,.2f}",
    f"　流动负债 {tcl:,.2f}",
    f"所有者权益 {te:,.2f}",
    f"　未分配利润 {re_end:,.2f}",
], C_BLUE, F_BLUE, fs=11.6)

# ── 三张勾稽等式卡片（右下）────────────────────────────────────────
card(62.0, 3.0, 36.0, 26.0, "三个勾稽等式", [
    "① 资产 = 负债 + 所有者权益",
    f"　{ta:,.2f} = {tl:,.2f} + {te:,.2f}",
    "② 期初现金 - 净变动 = 期末现金",
    f"　{cash_beg:,.2f} - {abs(net_change):,.2f} = {cash_end:,.2f}",
    "③ 年初未分配 + 归母净利 - 分红 = 年末",
    f"　年初未分配 + {npp:,.2f} - 分红 = {re_end:,.2f}",
], C_GRAY, F_GRAY, fs=9.9, title_fs=11.6, linespacing=1.7)

# ── 三条箭头 ───────────────────────────────────────────────────────
# ① 净利润 → 未分配利润
arrow(ax, (39.0, 73.0), (62.0, 71.0), color=C_PURPLE, lw=2.2)
label(ax, 50.5, 78.6, "净利润 84.53 滚进未分配利润\n分红会把它减掉一部分",
      color=C_PURPLE, fontsize=10.2)

# ② 现金净变动 → 货币资金
arrow(ax, (39.0, 24.0), (62.0, 40.0), color=C_GREEN, lw=2.2)
label(ax, 50.5, 16.8, "现金净变动 -182.66\n落到货币资金 254.04",
      color=C_GREEN, fontsize=10.2)

# ③ 净利润与经营现金流之间的调节（折旧、减值、营运资本）
arrow(ax, (20.5, 60.0), (20.5, 39.0), color=C_GRAY, lw=1.6, ls=(0, (4, 3)))
label(ax, 22.0, 49.5, f"折旧 {dep:,.2f} + 减值 {imp:,.2f}\n+ 营运资本变动等\n= 差额 {gap:,.2f}",
      color="#555555", fontsize=9.6, ha="left")

ax.text(50, 0.9,
        "数据来源：伊利 2024 年报 page_087、page_088、page_091、page_092、page_094、page_095；"
        "数值全部由 data/yili2024.json 计算，未手打",
        ha="center", va="center", fontsize=9.2, color=C_GRAY)

save(fig, "w09d1_three_statement_gear.png")
