# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 4 周第 20 章配图 1：2024 年 52.31 亿元减值都是什么牌子（伊利，亿元）。

上面四项合起来是利润表里的「资产减值损失」46.76 亿元；
「信用减值损失」5.55 亿元单列——它在利润表里是另一行，
两者一起才是这一年「因为资产不值钱了」而扣掉的利润总额。

数字全部来自 data/yili2024.json（notes 段）。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, label, C_BLUE, C_ORANGE, C_RED,
    C_GRAY, C_BROWN,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
n = d["notes"]
gw = n["goodwill_impairment_loss"] / 1e8         # 30.75
inv = n["inventory_writedown"] / 1e8             # 12.27
fa = n["fixed_asset_impairment"] / 1e8           # 3.67
asset_total = n["asset_impairment_total"] / 1e8  # 46.76
other = asset_total - gw - inv - fa              # 0.07（工程物资减值）
credit = -d["income"]["credit_impairment"] / 1e8  # 5.55
np_parent = d["income"]["net_profit_parent"] / 1e8  # 84.53
total = asset_total + credit                     # 52.31

rows = [
    ("商誉减值\n（澳优 + 康益佳）", gw, C_RED),
    ("存货跌价", inv, C_ORANGE),
    ("固定资产减值", fa, C_BROWN),
    ("工程物资减值\n（倒算的差额项）", other, C_GRAY),
    ("信用减值\n（另一行，不在 46.76 里）", credit, C_BLUE),
]

fig, ax = plt.subplots(figsize=(13.0, 7.6))
ys = list(range(len(rows)))[::-1]
bars = ax.barh(ys, [r[1] for r in rows], height=0.50,
               color=[r[2] for r in rows], zorder=3)

ax.set_yticks(ys)
ax.set_yticklabels([r[0] for r in rows], fontsize=11.4)
ax.set_xlim(0, 46)
ax.set_ylim(-0.85, 4.9)
ax.set_xlabel("金额（亿元）", fontsize=11.5)
ax.set_title("2024 年一共减值 52.31 亿元，商誉一项占 58.8%", fontsize=14.2, pad=30)

ax.text(0, 4.72,
        "前四项相加 = 46.76 亿元，正是利润表「资产减值损失」那一行；"
        "信用减值 5.55 亿元在另一行，要单独加。",
        fontsize=10.8, color="#444444", ha="left", va="bottom")

for b, r in zip(bars, rows):
    share = r[1] / total * 100
    ax.text(b.get_width() + 0.55, b.get_y() + b.get_height() / 2,
            f"{r[1]:,.2f} 亿元 · 占 {share:.1f}%",
            va="center", ha="left", fontsize=11.6, weight="bold")

# 注记放在「存货跌价」右侧的空白里（第 2 行右侧 x 约 14~42 全是空的）
label(ax, 15.0, 3.44,
      f"这 {total:,.2f} 亿元（税前）相当于归母净利润 {np_parent:,.2f} 亿元的 {total/np_parent*100:.1f}%，\n"
      f"而归母净利润同比 -18.94%（2023 年是 104.29 亿元）",
      fontsize=11.2, color="#333333", ha="left")

clean_axes(ax)
fig.text(0.012, -0.028,
         "数据来源：伊利 2024 年报 page_211（资产减值损失、信用减值损失明细）、page_091（利润表）、page_007（同比数据）。\n"
         "「工程物资减值」= 资产减值损失合计 − 商誉 − 存货 − 固定资产，由已核实数据倒算；"
         "年报附注原文为 6,618,814.46 元。",
         ha="left", va="top", fontsize=9.6, color=C_GRAY, linespacing=1.6)

save(fig, "w04d20_impairment_breakdown.png")
