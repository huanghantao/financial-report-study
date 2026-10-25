# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 10 周第 50 章配图：一份分析报告的八段骨架。

概念图：左边是八段结构（①~⑧），右边写「这一段要回答什么问题」和「主要看哪几个数字」。
读者可以照着这张图，把任何一家公司的年报写成一份 3,000 字的报告。
图中所有真实数字都由 figures._data.load("yili2024") 现算，不手打。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, fig_ax, box,
    C_BLUE, C_GREEN, C_ORANGE, C_PURPLE, C_RED, C_GRAY,
    F_BLUE, F_GREEN, F_ORANGE, F_PURPLE, F_RED,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
r = d["ratios"]
shares = d["balance"]["share_capital"] / 1e8
bvps = d["balance"]["equity_parent"] / 1e8 / shares
eps = d["income"]["net_profit_parent"] / 1e8 / shares
eps_ded = round(d["nonrecurring"]["net_profit_deducted"] / 1e8 / shares, 2)
fcf = r["free_cash_flow"] / 1e8
ocf = d["cashflow"]["operating_net"] / 1e8
debt = r["interest_bearing_debt"] / 1e8
goodwill = d["balance"]["goodwill"] / 1e8
inventory = d["balance"]["inventory"] / 1e8
impair = d["core_earnings"]["impairment_2024"] / 1e8

PE_LO, PE_HI = 17.0, 30.0   # 假设倍数（与第 47 章一致）
PB_LO, PB_HI = 2.5, 4.0     # 假设倍数（与第 48 章一致）

fig, ax = fig_ax(13.6, 9.2, xlim=(0, 13.6), ylim=(0.55, 9.75))

rows = [
    ("① 生意是什么", "它靠什么赚钱？卖给谁？", "分产品收入、毛利率、主要子公司",
     F_BLUE, C_BLUE),
    ("② 赚钱能力", "股东的钱一年能赚回多少？",
     f"ROE {r['roe_weighted_reported'] * 100:.2f}%、毛利率 {r['gross_margin'] * 100:.2f}%、"
     f"净利率 {r['net_margin'] * 100:.2f}%",
     F_GREEN, C_GREEN),
    ("③ 资产质量", "账上的资产值这个钱吗？",
     f"商誉 {goodwill:.2f} 亿、存货 {inventory:.2f} 亿、减值 {impair:.2f} 亿",
     F_GREEN, C_GREEN),
    ("④ 负债与风险", "欠的钱要不要付息？还得上吗？",
     f"有息负债 {debt:.2f} 亿、流动比率 {r['current_ratio']:.2f}",
     F_ORANGE, C_ORANGE),
    ("⑤ 现金流质量", "利润有没有变成现金？",
     f"经营现金流 {ocf:.2f} 亿、FCF {fcf:.2f} 亿、净现比 {r['ocf_to_net_profit']:.2f}",
     F_GREEN, C_GREEN),
    ("⑥ 红旗扫描", "有没有让我睡不着的信号？", "20 条红旗清单逐条过，记录命中几条",
     F_RED, C_RED),
    ("⑦ 估值区间", "它大概值多少钱？",
     f"PE {PE_LO:.0f}~{PE_HI:.0f} 倍、PB {PB_LO:.1f}~{PB_HI:.1f} 倍、DCF 另见敏感性表",
     F_PURPLE, C_PURPLE),
    ("⑧ 结论与安全边际", "什么价格我才动手？", "区间下沿再打折，写下「不买的条件」",
     F_PURPLE, C_PURPLE),
]

row_h = 0.80
gap = 0.155
y_start = 7.30
for i, (title, question, data, fc, ec) in enumerate(rows):
    y = y_start - i * (row_h + gap)
    box(ax, 0.45, y, 2.45, row_h, title, fc=fc, ec=ec, fontsize=12.4, lw=1.5)
    ax.text(3.18, y + row_h * 0.66, question, ha="left", va="center",
            fontsize=11.8, color="#222222", weight="bold")
    ax.text(3.18, y + row_h * 0.25, data, ha="left", va="center",
            fontsize=10.5, color=C_GRAY)

# 右侧竖排提示
ax.plot([12.62, 12.62], [0.62, 8.02], color="#dddddd", lw=1.4, zorder=1)
ax.text(12.80, 4.30, "八段写完，\n就是一份\n可以给别人\n看的报告", ha="left",
        va="center", fontsize=11.0, color=C_GRAY, linespacing=1.9)

ax.text(0.45, 9.45, "一份分析报告的八段骨架：每段只回答一个问题",
        fontsize=16.5, weight="bold", ha="left", va="center", color="#111111")
ax.text(0.45, 8.98,
        "① 先说生意，② 再说能力，③④ 看家底，⑤⑥ 验真假，⑦⑧ 才谈价格。",
        fontsize=11.2, color="#555555", ha="left", va="center")
ax.text(0.45, 8.58,
        "顺序反了，报告就会变成「先有结论、再找理由」。",
        fontsize=11.2, color="#555555", ha="left", va="center")

fig.text(0.012, -0.035,
         "图中数字均为伊利 2024 年报真实数据（page_007、page_087~088、page_091~092、page_094~095、page_211）；"
         "PE/PB 倍数与 DCF 结果为第 47~49 章的假设情景，不是真实股价、不是目标价。"
         f"参考：每股收益 {eps:.2f} 元、扣非每股收益 {eps_ded:.2f} 元、每股净资产 {bvps:.2f} 元。",
         ha="left", va="top", fontsize=9.4, color=C_GRAY, linespacing=1.6)

save(fig, "w10d50_report_skeleton.png")
