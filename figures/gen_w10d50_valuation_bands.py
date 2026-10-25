# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 10 周第 50 章配图：三种估值方法的区间带对比（元/股）。

- PE 法：假设 17~30 倍，分别乘扣非 EPS 0.94 元与归母 EPS 1.33 元；
- PB 法：假设 2.5~4.0 倍，乘每股净资产 8.35 元；
- DCF 法：第 49 章敏感性表的 9 个结果，取最低~最高。
所有「倍数」「折现率」「增速」都是假设，不是真实报价，也不是目标价。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, C_BLUE, C_GREEN, C_ORANGE, C_GRAY, C_RED,
)
from figures._data import load  # noqa: E402

PE_LO, PE_HI = 17.0, 30.0
PB_LO, PB_HI = 2.5, 4.0
GROWTH = [0.00, 0.03, 0.05]
DISCOUNT = [0.08, 0.10, 0.12]
TERMINAL, YEARS = 0.02, 5

d = load("yili2024")
shares = d["balance"]["share_capital"] / 1e8
bvps = d["balance"]["equity_parent"] / 1e8 / shares
eps_parent = round(d["income"]["net_profit_parent"] / 1e8 / shares, 2)
eps_ded = round(d["nonrecurring"]["net_profit_deducted"] / 1e8 / shares, 2)
fcf0 = d["ratios"]["free_cash_flow"] / 1e8


def dcf_ps(g, r):
    pv, f = 0.0, fcf0
    for t in range(1, YEARS + 1):
        f *= (1 + g)
        pv += f / (1 + r) ** t
    pv += (f * (1 + TERMINAL) / (r - TERMINAL)) / (1 + r) ** YEARS
    return pv / shares


dcf_vals = [dcf_ps(g, r) for g in GROWTH for r in DISCOUNT]

bands = [
    ("PE 法（最保守）\n30 倍 × 扣非 EPS 0.94 元", PE_HI * eps_ded, PE_HI * eps_ded,
     C_ORANGE),
    ("PE 法（最乐观）\n17 倍 × 归母 EPS 1.33 元", PE_LO * eps_parent,
     PE_LO * eps_parent, C_ORANGE),
    ("PB 法：2.5~4.0 倍\n× 每股净资产 8.35 元", PB_LO * bvps, PB_HI * bvps,
     C_BLUE),
    ("DCF 法：9 组假设\n的每股价值", min(dcf_vals), max(dcf_vals), C_GREEN),
]

# 为了画成「区间带」，把 PE 的四个角按方法归成两条：扣非口径与归母口径
bands = [
    ("PE 法：17~30 倍\n× 扣非 EPS 0.94 元", PE_LO * eps_ded, PE_HI * eps_ded,
     C_ORANGE),
    ("PE 法：17~30 倍\n× 归母 EPS 1.33 元", PE_LO * eps_parent,
     PE_HI * eps_parent, C_ORANGE),
    ("PB 法：2.5~4.0 倍\n× 每股净资产 8.35 元", PB_LO * bvps, PB_HI * bvps,
     C_BLUE),
    ("DCF 法：9 组假设\n的每股价值", min(dcf_vals), max(dcf_vals), C_GREEN),
]

lows = [b[1] for b in bands]
highs = [b[2] for b in bands]
lo_all, hi_all = max(lows), min(highs)

fig, ax = plt.subplots(figsize=(12.6, 7.0))
ys = [len(bands) - 1 - i for i in range(len(bands))]

ax.axvspan(lo_all, hi_all, color="#fff2cc", zorder=1)
for y, (name, lo, hi, color) in zip(ys, bands):
    ax.plot([lo, hi], [y, y], color=color, lw=15, solid_capstyle="round",
            alpha=0.20, zorder=3)
    ax.plot([lo, hi], [y, y], color=color, lw=2.8, solid_capstyle="round",
            zorder=4)
    ax.scatter([lo, hi], [y, y], s=68, color=color, zorder=6,
               edgecolor="white", linewidth=1.4)
    ax.text(lo - 0.8, y, f"{lo:,.1f}", ha="right", va="center", fontsize=11.4,
            color=color, weight="bold", zorder=7)
    ax.text(hi + 0.8, y, f"{hi:,.1f}", ha="left", va="center", fontsize=11.4,
            color=color, weight="bold", zorder=7)
    ax.text(hi + 3.4, y, f"宽 {hi - lo:,.1f} 元", ha="left", va="center",
            fontsize=10.0, color=C_GRAY, zorder=7)

# 重叠区标注放在图顶部，箭头指下来，避免压住任何一条带子
ax.annotate(f"四个区间都覆盖的只有\n{lo_all:.1f}~{hi_all:.1f} 元这一小段",
            xy=((lo_all + hi_all) / 2, len(bands) - 0.42),
            xytext=((lo_all + hi_all) / 2 - 18.0, len(bands) + 0.10),
            ha="center", va="bottom", fontsize=10.8, color=C_RED,
            weight="bold", zorder=9, linespacing=1.6,
            bbox=dict(boxstyle="round,pad=0.38", fc="white", ec=C_RED, lw=1.1),
            arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.2,
                            shrinkA=5, shrinkB=2, mutation_scale=13))

ax.set_yticks(ys)
ax.set_yticklabels([b[0] for b in bands], fontsize=10.8, linespacing=1.55)
ax.set_ylim(-0.6, len(bands) + 0.95)
ax.set_xlim(0, 62)
ax.set_xlabel("每股价值（元/股）：全部是假设情景，不是真实股价，也不是目标价",
              fontsize=11.4)
ax.set_title("三种方法、四个区间：重叠的部分很窄——这就是估值必须给区间的理由",
             fontsize=13.6, pad=16)
clean_axes(ax)

fig.text(0.012, -0.085,
         f"EPS 与每股净资产为真实数据（归母 EPS {eps_parent:.2f} 元、扣非 EPS {eps_ded:.2f} 元、每股净资产 {bvps:.2f} 元）；"
         "PE 倍数、PB 倍数、DCF 的增速与折现率全部是假设。\n"
         f"DCF 基期自由现金流 {fcf0:,.2f} 亿元（page_094~095），前 5 年增速 0%/3%/5%、折现率 8%/10%/12%、永续增长 {TERMINAL * 100:.0f}%，"
         f"9 组结果从 {min(dcf_vals):.1f} 元到 {max(dcf_vals):.1f} 元。本图演示「交叉验证」的方法，不构成投资建议。",
         ha="left", va="top", fontsize=9.4, color=C_GRAY, linespacing=1.6)

save(fig, "w10d50_valuation_bands.png")
