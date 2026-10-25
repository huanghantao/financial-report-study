# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 10 周第 47 章配图：同一假设股价下，三种利润口径给出三个 PE。

假设股价 28 元（仅为演示，非真实报价）。三个分母都来自 data/yili2024.json：
- 归母净利润 84.53 亿元；
- 扣非归母净利润 60.11 亿元；
- 剔除减值后的经营性归母利润 ≈ 103.83 亿元（扣非 + 减值 × (1 - 有效税率)，粗算）。
EPS = 各口径利润 ÷ 总股本 63.66 亿股；PE = 28 ÷ EPS。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, C_BLUE, C_ORANGE, C_PURPLE, C_GRAY,
)
from figures._data import load  # noqa: E402

PRICE = 28.0  # 假设股价，仅用于演示，非真实报价

d = load("yili2024")
inc = d["income"]
shares = d["balance"]["share_capital"] / 1e8
etr = inc["income_tax"] / inc["profit_before_tax"]

np_parent = inc["net_profit_parent"] / 1e8
deducted = d["nonrecurring"]["net_profit_deducted"] / 1e8
impair = -(inc["asset_impairment"] + inc["credit_impairment"]) / 1e8
adjusted = deducted + impair * (1 - etr)

rows = [
    ("扣非归母净利润", deducted, C_ORANGE),
    ("归母净利润", np_parent, C_PURPLE),
    ("剔除减值后（粗算）", adjusted, C_BLUE),
]

fig, ax = plt.subplots(figsize=(12.2, 6.4))
ys = [2, 1, 0]
pe_vals = []
for y, (name, profit, color) in zip(ys, rows):
    eps = round(profit / shares, 2)   # 展示用两位小数，PE 也用这个 EPS 算，读者能对上
    pe = PRICE / eps
    pe_vals.append(pe)
    ax.barh(y, pe, height=0.5, color=color, edgecolor="white", linewidth=1.2,
            zorder=3)
    ax.text(pe - 0.55, y, f"收益率 {100 / pe:.1f}%", ha="right", va="center",
            fontsize=10.4, color="white", weight="bold", zorder=5)
    ax.text(pe + 0.45, y, f"PE {pe:.1f} 倍", ha="left", va="center",
            fontsize=13.0, color=color, weight="bold", zorder=6)
    ax.text(pe + 6.4, y, f"{profit:,.2f} 亿元 ÷ 63.66 亿股 = EPS {eps:.2f} 元",
            ha="left", va="center", fontsize=10.6, color="#333333", zorder=6)

ax.set_yticks(ys)
ax.set_yticklabels([f"{name}\n{profit:,.2f} 亿元" for name, profit, _ in rows],
                   fontsize=12.0)
ax.tick_params(axis="y", pad=10, length=0)
ax.set_ylim(-0.6, 2.65)
ax.set_xlim(0, 42)
ax.set_xlabel("市盈率 PE（倍）", fontsize=11.5)
ax.set_title("假设股价 28 元（非真实报价）：同一只股票，PE 可以是 17 倍，也可以是 30 倍",
             fontsize=14.5, pad=14)

ax.text(0.6, 2.52, "分母不同，尺子就不同：变的不是市场，是你用哪个利润",
        fontsize=11.0, color="#555555", ha="left", va="center", zorder=7)
clean_axes(ax)

fig.text(0.012, -0.07,
         f"假设股价 28 元（仅为演示，非真实报价，年报中没有股价）。EPS 由各口径利润 ÷ 63.66 亿股得到；"
         f"扣非 EPS {deducted / shares:.2f} 元（年报披露的扣非基本每股收益为 0.95 元，因加权平均股数略少，差 1 分钱，不影响结论）。\n"
         f"剔除减值口径 = 扣非 {deducted:,.2f} + 减值 {impair:,.2f} × (1 - 有效税率 {etr * 100:.2f}%) = {adjusted:,.2f} 亿元，是粗算上限，"
         "详见第 35 章；数据来源：page_007、page_008、page_091 至 page_092、page_211。",
         ha="left", va="top", fontsize=9.4, color=C_GRAY, linespacing=1.6)

save(fig, "w10d47_pe_three_eps.png")
