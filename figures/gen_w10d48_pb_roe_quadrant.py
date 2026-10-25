# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 10 周第 48 章配图：PB-ROE 象限与伊利的位置。

假设股价 28 元（仅为演示，非真实报价）；每股净资产取 2024 年末 8.35 元（真实）。
PB = 28 ÷ 8.35；隐含要求回报率 = ROE ÷ PB。
图中两条虚线是「要求回报率 6% / 8%」的等值线（简化式 PB = ROE ÷ r），
不是精确定价公式，只用来判断「贵不贵」的方向。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, C_RED, C_GRAY, C_ORANGE,
)
from figures._data import load  # noqa: E402

PRICE = 28.0  # 假设股价，仅用于演示，非真实报价

d = load("yili2024")
shares = d["balance"]["share_capital"] / 1e8
bvps = d["balance"]["equity_parent"] / 1e8 / shares
roe = d["ratios"]["roe_weighted_reported"] * 100
pb = PRICE / bvps
implied = roe / pb

fig, ax = plt.subplots(figsize=(11.8, 7.4))

# 两条「要求回报率」等值线：PB = ROE / r（标签放在各自右端上方，避开圆点）
xs = np.linspace(0.4, 26.0, 300)
for r, lab in [(6.0, "要求回报率 6%"), (8.0, "要求回报率 8%")]:
    ax.plot(xs, xs / r, color=C_GRAY, lw=1.2, ls=(0, (4, 3)), zorder=2)
    ax.text(25.9, 25.9 / r + 0.30, lab, ha="right", va="bottom", fontsize=10.2,
            color=C_GRAY, zorder=6,
            bbox=dict(boxstyle="round,pad=0.26", fc="white", ec="none"))

# 象限线
ax.axvline(15.0, color="#bbbbbb", lw=1.0, zorder=1)
ax.axhline(3.0, color="#bbbbbb", lw=1.0, zorder=1)

quad = [
    (0.9, 4.95, "低 ROE + 高 PB\n最危险：贵，还不赚钱", "#b03a2e"),
    (15.8, 4.95, "高 ROE + 高 PB\n贵，但贵得有道理", "#1e6b34"),
    (0.9, 0.30, "低 ROE + 低 PB\n便宜，但没质量", "#7a5c00"),
    (15.8, 0.30, "高 ROE + 低 PB\n可能是机会", "#1f5c8b"),
]
for x, y, txt, color in quad:
    ax.text(x, y, txt, ha="left", va="bottom", fontsize=10.6, color=color,
            linespacing=1.5,
            bbox=dict(boxstyle="round,pad=0.32", fc="white", ec="none",
                      alpha=0.9))

# 伊利与它的隐含要求回报率，合成一个注释框放在左上空白区
ax.scatter([roe], [pb], s=250, color=C_RED, edgecolor="white", linewidth=2.0,
           zorder=8)
ax.annotate(
    f"伊利：ROE {roe:.2f}%，PB {pb:.2f} 倍\n"
    f"（假设股价 28 元 ÷ 每股净资产 {bvps:.2f} 元）\n"
    f"隐含要求回报率 = {roe:.2f}% ÷ {pb:.2f} = {implied:.1f}%",
    xy=(roe - 0.30, pb + 0.10), xytext=(1.6, 3.62),
    ha="left", va="center", fontsize=10.8, color="#222222", zorder=9,
    bbox=dict(boxstyle="round,pad=0.42", fc="white", ec=C_RED, lw=1.2),
    arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.3,
                    shrinkA=8, shrinkB=10, mutation_scale=15),
)

ax.set_xlim(0, 27.5)
ax.set_ylim(0, 5.45)
ax.set_xlabel("ROE：净资产收益率（%）", fontsize=11.5)
ax.set_ylabel("PB：市净率（倍）", fontsize=11.5)
ax.set_title("PB-ROE 象限：伊利落在「高 ROE、中高 PB」的右上区——贵不贵，要看 ROE 撑不撑得住",
             fontsize=13.6, pad=14)
clean_axes(ax)

fig.text(0.012, -0.06,
         f"假设股价 28 元（仅为演示，非真实报价）；每股净资产 {bvps:.2f} 元、ROE {roe:.2f}% 为伊利 2024 年报真实数据（page_007、page_088）。\n"
         "两条虚线是简化式 PB = ROE ÷ r 的等值线，只说明「同样的 PB，ROE 越高越便宜」这个方向，不是精确定价公式；"
         "真实估值还要看增长、分红与风险。",
         ha="left", va="top", fontsize=9.4, color=C_GRAY, linespacing=1.6)

save(fig, "w10d48_pb_roe_quadrant.png")
