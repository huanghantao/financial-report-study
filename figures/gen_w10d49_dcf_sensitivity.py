# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 10 周第 49 章配图：DCF 敏感性热力图——折现率 × 前 5 年增速 → 每股价值（元）。

基期自由现金流 177.61 亿元（伊利 2024 年报真实数字，page_094~095 计算）。
其余全部是假设：前 5 年 FCF 增速 0% / 3% / 5%，折现率 8% / 10% / 12%，
第 6 年起永续增长 2%。股本 63.66 亿股。
这张图想说明的是：假设动一格，结论动一大截——所以 DCF 给的是区间，不是点。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

from figures._common import save, C_GRAY  # noqa: E402
from figures._data import load  # noqa: E402

GROWTH = [0.00, 0.03, 0.05]      # 假设：前 5 年 FCF 增速
DISCOUNT = [0.08, 0.10, 0.12]    # 假设：折现率
TERMINAL = 0.02                  # 假设：永续增长率
YEARS = 5

d = load("yili2024")
fcf0 = d["ratios"]["free_cash_flow"] / 1e8
shares = d["balance"]["share_capital"] / 1e8


def dcf_per_share(g: float, r: float) -> tuple:
    pv_stage = 0.0
    f = fcf0
    for t in range(1, YEARS + 1):
        f = f * (1 + g)
        pv_stage += f / (1 + r) ** t
    tv = f * (1 + TERMINAL) / (r - TERMINAL)
    pv_tv = tv / (1 + r) ** YEARS
    ev = pv_stage + pv_tv
    return ev / shares, pv_tv / ev


vals = np.array([[dcf_per_share(g, r)[0] for g in GROWTH] for r in DISCOUNT])
tv_share = np.array([[dcf_per_share(g, r)[1] for g in GROWTH]
                     for r in DISCOUNT])

fig, ax = plt.subplots(figsize=(11.4, 6.9))
im = ax.imshow(vals, cmap="YlGnBu", aspect="auto", origin="upper")

for i in range(len(DISCOUNT)):
    for j in range(len(GROWTH)):
        v = vals[i, j]
        txt_color = "white" if v > vals.mean() + 4 else "#1a1a1a"
        ax.text(j, i - 0.10, f"{v:,.1f} 元", ha="center", va="center",
                fontsize=14.0, weight="bold", color=txt_color, zorder=5)
        ax.text(j, i + 0.24, f"终值占 {tv_share[i, j] * 100:.0f}%", ha="center",
                va="center", fontsize=9.8, color=txt_color, zorder=5)

ax.set_xticks(range(len(GROWTH)))
ax.set_xticklabels([f"{g * 100:.0f}%" for g in GROWTH], fontsize=13)
ax.set_yticks(range(len(DISCOUNT)))
ax.set_yticklabels([f"{r * 100:.0f}%" for r in DISCOUNT], fontsize=13)
ax.set_xlabel("假设：前 5 年自由现金流增速", fontsize=12.0, labelpad=10)
ax.set_ylabel("假设：折现率", fontsize=12.0, labelpad=14)
ax.set_title(f"同一份 177.61 亿元的自由现金流，假设动一动，每股价值从 "
             f"{vals.min():.0f} 元到 {vals.max():.0f} 元",
             fontsize=14.2, pad=14)
ax.set_xticks(np.arange(-0.5, len(GROWTH), 1), minor=True)
ax.set_yticks(np.arange(-0.5, len(DISCOUNT), 1), minor=True)
ax.grid(which="minor", color="white", linewidth=2.2)
ax.tick_params(which="minor", length=0)
for spine in ax.spines.values():
    spine.set_visible(False)

cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.03)
cbar.set_label("每股价值（元，假设价格）", fontsize=10.5)
cbar.ax.tick_params(labelsize=9.5)

fig.text(0.008, -0.075,
         f"基期自由现金流 {fcf0:,.2f} 亿元（伊利 2024 年报真实数字：经营现金流 217.40 - 资本开支 39.78）；"
         f"前 5 年增速、折现率、永续增长 {TERMINAL * 100:.0f}% 全部是假设，每股价值 = 企业价值 ÷ {shares:.2f} 亿股。\n"
         "单元格上方小字是「终值占企业价值的比例」——它越高，说明估值越依赖 5 年以后的假设，越不可靠。"
         "本图是教学演示，不是投资建议；任何 DCF 的结论都随假设变化，请自己动手换参数重算。",
         ha="left", va="top", fontsize=9.4, color=C_GRAY, linespacing=1.6)

save(fig, "w10d49_dcf_sensitivity.png")
