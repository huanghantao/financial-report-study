# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 2 周第 10 章配图：三张表怎么咬合成一台机器（带伊利 2024 真实数字）。

三个通道：
① 利润表净利润 → 资产负债表未分配利润；
② 现金流量表现金净增加额 → 资产负债表货币资金；
③ 资产 = 负债 + 所有者权益 始终成立。
数字全部来自 data/yili2024.json。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.patches as mpatches  # noqa: E402

from figures._common import (  # noqa: E402
    save, fig_ax, arrow, label,
    C_BLUE, C_GREEN, C_PURPLE, C_GRAY, C_RED,
    F_BLUE, F_GREEN, F_PURPLE,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
b, i, cf = d["balance"], d["income"], d["cashflow"]
Y = lambda v: v / 1e8  # noqa: E731

ta, tl, te = Y(b["total_assets"]), Y(b["total_liabilities"]), Y(b["total_equity"])
ep = Y(b["equity_parent"])
re_end = Y(b["retained_earnings"])                     # 322.29
cash_end, cash_beg = Y(b["cash"]), Y(b["cash_2023"])   # 254.04 / 433.72
np_, npp = Y(i["net_profit"]), Y(i["net_profit_parent"])   # 84.64 / 84.53
ocf, icf, ffin = Y(cf["operating_net"]), Y(cf["investing_net"]), Y(cf["financing_net"])
net_change = Y(cf["net_cash_change"])                  # −182.66
cashflow_end = Y(cf["cash_end"])                       # 245.47

fig, ax = fig_ax(14.6, 10.0, xlim=(0, 100), ylim=(0, 100))

ax.text(50, 97.2, "三张表是一台机器：利润表和现金流量表，最后都汇进资产负债表",
        ha="center", va="center", fontsize=15.4, weight="bold", color="#1a1a1a")
ax.text(50, 93.6, "伊利 2024 年报真实数字 · 单位：亿元",
        ha="center", va="center", fontsize=11, color=C_GRAY)


def card(x0, y0, w, h, title, lines, ec, fc, fs=11.2):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x0, y0), w, h, boxstyle="round,pad=0.02,rounding_size=1.0",
        fc=fc, ec=ec, lw=1.9, zorder=3))
    ax.text(x0 + w / 2, y0 + h - 2.8, title, ha="center", va="center",
            fontsize=12.4, weight="bold", color=ec, zorder=5)
    n = len(lines)
    ax.text(x0 + w / 2, y0 + (h - 6.0) / 2 + 0.2, "\n".join(lines),
            ha="center", va="center", fontsize=fs, color="#222222",
            linespacing=1.85, zorder=5)


# ── 资产负债表（左，主表）──────────────────────────────────────────
card(2.0, 24.0, 41.0, 62.0, "资产负债表　page_087~088", [
    f"资产总计 {ta:,.2f}",
    f"　货币资金 {cash_end:,.2f}",
    f"　流动资产 {Y(b['total_current_assets']):,.2f}",
    f"　非流动资产 {Y(b['total_noncurrent_assets']):,.2f}",
    "",
    f"负债合计 {tl:,.2f}",
    f"　未分配利润 {re_end:,.2f}",
    f"所有者权益 {te:,.2f}",
    f"　其中归母 {ep:,.2f}",
], C_BLUE, F_BLUE, fs=11.0)

# ── 利润表（右上）───────────────────────────────────────────────────
card(57.0, 62.0, 41.0, 20.0, "利润表　page_091~092", [
    f"营业收入 {Y(i['revenue']):,.2f}　营业成本 {Y(i['cost_of_sales']):,.2f}",
    f"净利润 {np_:,.2f}　其中归母 {npp:,.2f}",
], C_PURPLE, F_PURPLE, fs=11.0)

# ── 现金流量表（右下）───────────────────────────────────────────────
card(57.0, 22.0, 41.0, 34.0, "现金流量表　page_094~095", [
    f"经营活动净额 {ocf:+,.2f}",
    f"投资活动净额 {icf:+,.2f}",
    f"筹资活动净额 {ffin:+,.2f}",
    f"现金净增加额 {net_change:+,.2f}",
    f"期初 {Y(cf['cash_begin']):,.2f} → 期末 {cashflow_end:,.2f}",
], C_GREEN, F_GREEN, fs=11.0)

# ── 箭头 ① 净利润 → 未分配利润 ──────────────────────────────────────
arrow(ax, (56.4, 66.5), (43.4, 60.0), color=C_PURPLE, lw=2.4,
      connectionstyle="arc3,rad=0.22")
label(ax, 49.4, 70.6, f"① 净利润 {np_:,.2f}\n滚进未分配利润", color=C_PURPLE,
      fontsize=10.4, weight="bold")

# ── 箭头 ② 现金净增加额 → 货币资金 ──────────────────────────────────
arrow(ax, (56.4, 47.6), (43.6, 36.0), color="#1f7a1f", lw=2.4,
      connectionstyle="arc3,rad=-0.3")
label(ax, 50.0, 54.0, f"② 现金净增加\n{net_change:,.2f}\n落到货币资金", color="#1f7a1f",
      fontsize=10.2, weight="bold")

# ── 底部：三个通道的一句话 ──────────────────────────────────────────
label(ax, 21.0, 19.6,
      f"货币资金：年初 {cash_beg:,.2f} ＋ 净增加 {net_change:,.2f} ＝ 年末 {cash_end:,.2f}",
      color="#1f7a1f", fontsize=10.4, ha="center")

ax.text(2.0, 14.6, "通道 ①：利润表回答「赚了多少」，赚的钱滚进「未分配利润」这一格。",
        ha="left", va="center", fontsize=10.8, color="#333333")
ax.text(2.0, 10.6, "通道 ②：现金流量表回答「现金多了还是少了」，落点是「货币资金」这一格。",
        ha="left", va="center", fontsize=10.8, color="#333333")
ax.text(2.0, 6.6, "通道 ③：不论上面两条怎么流，资产 = 负债 + 所有者权益 永远成立。",
        ha="left", va="center", fontsize=10.8, color="#333333")

ax.text(2.0, 2.0,
        f"注意：现金流量表期末现金 {cashflow_end:,.2f} ≠ 资产负债表货币资金 {cash_end:,.2f}，"
        f"差 {cash_end - cashflow_end:,.2f} 亿元，是受限资金等不计入现金等价物的部分（page_150）。",
        ha="left", va="center", fontsize=9.8, color=C_RED)

save(fig, "w02d6_three_statement_link.png")
