# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 10 周第 46 章配图：伊利 2024 年的四个「每股」价值锚（元/股）。

数字全部来自 data/yili2024.json：
- 每股净资产 = 归母权益 ÷ 总股本
- 每股收益 = 归母净利润 ÷ 总股本
- 每股经营现金流 = 经营活动现金流净额 ÷ 总股本
- 每股自由现金流 = 自由现金流 ÷ 总股本
这些是财报算出来的「锚」，不是股价；股价必须读者自己查最新行情。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, C_BLUE, C_GREEN, C_ORANGE, C_PURPLE, C_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
shares = d["balance"]["share_capital"] / 1e8
bvps = d["balance"]["equity_parent"] / 1e8 / shares
eps = d["income"]["net_profit_parent"] / 1e8 / shares
ocfps = d["cashflow"]["operating_net"] / 1e8 / shares
fcfps = d["ratios"]["free_cash_flow"] / 1e8 / shares
roe = d["ratios"]["roe_weighted_reported"]

items = [
    ("每股净资产", bvps, C_BLUE, "账上属于股东的钱"),
    ("每股经营现金流", ocfps, C_GREEN, "每股收回的现金"),
    ("每股自由现金流", fcfps, C_PURPLE, "扣资本开支后的钱"),
    ("每股收益", eps, C_ORANGE, "每股一年赚的利润"),
]
items = sorted(items, key=lambda z: z[1])  # 小的在下面，大的在上面

fig, ax = plt.subplots(figsize=(11.6, 6.8))
ys = list(range(len(items)))
ax.barh(ys, [it[1] for it in items], height=0.5,
        color=[it[2] for it in items], edgecolor="white", linewidth=1.2,
        zorder=3)

for y, (name, val, color, note) in zip(ys, items):
    ax.text(val + 0.13, y, f"{val:,.2f} 元", va="center", ha="left",
            fontsize=13.0, weight="bold", color=color, zorder=6)

ax.set_yticks(ys)
ax.set_yticklabels([f"{it[0]}\n{it[3]}" for it in items], fontsize=11.5,
                   linespacing=1.7)
ax.tick_params(axis="y", pad=10, length=0)
ax.set_xlim(0, 10.2)
ax.set_ylim(-0.62, len(items) - 0.32)
ax.set_xlabel("每股口径的金额（元/股）", fontsize=11.5)
ax.set_title("伊利 2024 年的四个「每股」价值锚：它们是估值的原材料，不是股价",
             fontsize=14.5, pad=16)

ax.text(0.98, 0.06,
        f"ROE {roe * 100:.2f}%：股东每投 1 元，一年赚回 {roe:.2f} 元",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=11.0,
        color="#333333",
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#cccccc", lw=0.9))
clean_axes(ax)

fig.text(0.012, -0.06,
         "数据来源：伊利 2024 年报 page_007（每股收益 1.33 元、加权平均 ROE 15.81%）、"
         "page_087 至 page_088（归母权益 531.80 亿元、总股本 63.66 亿股）、"
         "page_094 至 page_095（经营现金流 217.40 亿元、资本开支 39.78 亿元）；data/yili2024.json。\n"
         f"计算：每股净资产 {bvps:,.2f} = 531.80 ÷ 63.66；每股收益 {eps:,.2f} = 84.53 ÷ 63.66；"
         f"每股经营现金流 {ocfps:,.2f} = 217.40 ÷ 63.66；每股自由现金流 {fcfps:,.2f} = 177.61 ÷ 63.66。"
         "股价不在年报里，必须自己查最新行情；本图不含任何股价。",
         ha="left", va="top", fontsize=9.4, color=C_GRAY, linespacing=1.6)

save(fig, "w10d46_value_anchors.png")
