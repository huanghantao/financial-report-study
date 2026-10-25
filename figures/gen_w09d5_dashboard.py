# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 9 周第 45 章配图之一：伊利 vs 蒙牛的四维仪表盘（8 个面板，每个面板一个指标）。

四个维度：成长 / 盈利 / 偿债 / 质量，各 2 个指标，共 8 个面板。
每个面板标题都带维度名，标题只在本面板内，不跨面板连成一句。
所有数字取自 data/yili2024.json 与 data/mengniu2024.json，现场计算，不手打。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, C_BLUE, C_ORANGE, C_GRAY,
)
from figures._data import load  # noqa: E402

y = load("yili2024")
m = load("mengniu2024")

yb, ycf, yi_, yr = y["balance"], y["cashflow"], y["income"], y["ratios"]
mb, mcf, mi_, mr = m["balance"], m["cashflow"], m["income"], m["ratios"]

y_rev_yoy = (yi_["revenue"] / yi_["revenue_2023"] - 1) * 100
m_rev_yoy = (mi_["revenue"] / mi_["revenue_2023"] - 1) * 100
y_np_yoy = (yi_["net_profit_parent"] / yi_["net_profit_parent_2023"] - 1) * 100
m_np_yoy = (mi_["net_profit_parent"] / mi_["net_profit_parent_2023"] - 1) * 100
y_gm, m_gm = yr["gross_margin"] * 100, mr["gross_margin"] * 100
y_nm, m_nm = yr["net_margin"] * 100, mr["net_margin"] * 100
y_debt, m_debt = yr["debt_ratio"] * 100, mr["debt_ratio"] * 100
y_cur, m_cur = yr["current_ratio"], mr["current_ratio"]
y_ocf = ycf["operating_net"] / 1e8
m_ocf = mcf["operating_net"] / 1e8
y_ocf_np = ycf["operating_net"] / yi_["net_profit"]
m_ocf_np = mcf["operating_net"] / mi_["net_profit"]

DIM_COLOR = {"成长": "#6a51a3", "盈利": "#2ca02c", "偿债": "#1f77b4", "质量": "#b8860b"}

panels = [
    ("成长", "营业收入同比", [y_rev_yoy, m_rev_yoy], "{:.2f}%", (-13.4, 4.2)),
    ("成长", "归母净利润同比", [y_np_yoy, m_np_yoy], "{:.1f}%", (-112.0, 30.0)),
    ("盈利", "毛利率", [y_gm, m_gm], "{:.2f}%", (0, 52)),
    ("盈利", "净利率", [y_nm, m_nm], "{:.2f}%", (0, 10.5)),
    ("偿债", "资产负债率", [y_debt, m_debt], "{:.2f}%", (0, 82)),
    ("偿债", "流动比率", [y_cur, m_cur], "{:.2f}", (0, 1.35)),
    ("质量", "经营现金流（亿元）", [y_ocf, m_ocf], "{:,.0f}", (0, 265)),
    ("质量", "经营现金流 / 净利润", [y_ocf_np, m_ocf_np], "{:.2f}", (0, 46)),
]

fig, axes = plt.subplots(2, 4, figsize=(15.8, 8.6))
fig.subplots_adjust(left=0.058, right=0.988, top=0.835, bottom=0.205,
                    hspace=0.52, wspace=0.30)

for ax, (dim, name, vals, fmt, (lo, hi)) in zip(axes.flat, panels):
    bars = ax.bar([0, 1], vals, width=0.46, color=[C_BLUE, C_ORANGE], zorder=3)
    span = hi - lo
    for bb, v in zip(bars, vals):
        va = "bottom" if v >= 0 else "top"
        off = span * 0.028 if v >= 0 else -span * 0.028
        ax.text(bb.get_x() + bb.get_width() / 2, v + off, fmt.format(v),
                ha="center", va=va, fontsize=11.4, weight="bold",
                color="#1a1a1a", zorder=6)

    ax.set_title(f"{dim}｜{name}", fontsize=11.2, pad=9, loc="left",
                 color=DIM_COLOR[dim], weight="bold")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["伊利", "蒙牛"], fontsize=11.2)
    ax.set_xlim(-0.66, 1.66)
    ax.set_ylim(lo, hi)
    ax.set_ylabel(name.replace("（亿元）", ""), fontsize=9.4, color="#555555")
    ax.tick_params(axis="y", labelsize=9.2)
    ax.axhline(0, color="#999999", lw=1.0, zorder=2)
    ax.grid(axis="y", color="#ececec", lw=0.8, zorder=0)
    clean_axes(ax)

fig.suptitle("伊利 vs 蒙牛 2024 仪表盘：伊利赢在「利润还在、现金厚」，蒙牛输在「利润被减值吃光」",
             fontsize=15.0, weight="bold", y=0.962)

fig.text(0.012, 0.132,
         f"陷阱一：蒙牛「经营现金流 / 净利润」{m_ocf_np:.1f} 倍不是现金好，是分母净利只有 "
         f"{(mi_['net_profit'] / 1e8):.2f} 亿——净利接近 0 时这个指标失真。\n"
         f"陷阱二：蒙牛毛利率 {m_gm:.2f}% 高于伊利，但销售费用率 "
         f"{mr['selling_expense_ratio'] * 100:.2f}% 也高得多（伊利 {yr['selling_expense_ratio'] * 100:.2f}%），"
         "毛利厚不等于净利厚。",
         fontsize=9.6, color="#333333", va="top", linespacing=1.7)
fig.text(0.012, 0.048,
         "数据来源：伊利 2024 年报 page_007、page_087、page_088、page_091、page_092、page_094；"
         "蒙牛 2024 年报 page_140、page_142、page_147。全部由 data/ 下两份 JSON 计算，未手打。",
         fontsize=9.0, color=C_GRAY)
fig.text(0.012, 0.012,
         "读法：八个指标没有一个「绝对好」或「绝对坏」，要结合商业模式和这一年发生了什么一起看。",
         fontsize=9.4, color="#333333")

save(fig, "w09d5_dashboard.png")
