# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 3 周第 3 章配图：伊利 2024 年的赊账速度。

左图：三个周转天数（应收 9.1 天 / 存货 51.4 天 / 应付 58.9 天）——钱到得快、付得慢；
右图：应收账款按账龄分档的坏账计提比例——账龄越长，计提越狠。

口径：应收天数、存货周转次数、现金转换周期取自 data/yili2024.json 的 ratios；
应付天数由「现金转换周期 = 存货天数 + 应收天数 − 应付天数」反推；
分档计提比例取自附注七(5) page_154（data/yili2024_supplement.json）。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_RED, C_PURPLE,
)
from figures._data import load  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as mpatches  # noqa: E402

d = load("yili2024")
sup = load("yili2024_supplement")
R = d["ratios"]

ar_days = R["receivable_days"]                       # 9.1
inv_days = 365 / R["inventory_turnover"]             # 51.4
ccc = R["cash_conversion_cycle_days"]                # 1.6
ap_days = inv_days + ar_days - ccc                   # 58.9

fig, axes = plt.subplots(1, 2, figsize=(14.6, 7.0),
                         gridspec_kw={"width_ratios": [1.12, 1.0],
                                      "wspace": 0.30})

# ══════════════════ 左：三个周转天数 ══════════════════
ax = axes[0]
names = ["应收账款\n周转天数", "存货\n周转天数", "应付账款\n周转天数"]
vals = [ar_days, inv_days, ap_days]
colors = [C_BLUE, C_GREEN, C_ORANGE]
ys = [2, 1, 0]
bars = ax.barh(ys, vals, height=0.52, color=colors, edgecolor="white", lw=0.8)

ax.set_yticks(ys)
ax.set_yticklabels(names, fontsize=11.5)
ax.set_xlim(0, 78)
ax.set_xlabel("天数（天）", fontsize=11.5)
ax.set_title("伊利 2024 年：9.1 天收回货款，58.9 天才付给上游",
             fontsize=13.5, pad=12, weight="bold")
ax.grid(axis="x", color="#eaeaea", lw=0.8, zorder=0)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

for y, v, c in zip(ys, vals, colors):
    ax.text(v + 1.4, y, f"{v:,.1f} 天", va="center", ha="left",
            fontsize=13, weight="bold", color=c, zorder=6)

ax.text(0, 2.62, "钱到得快：卖出去到收到钱只隔 9 天",
        fontsize=10.8, color=C_BLUE, ha="left", va="center", weight="bold")
ax.text(0, -0.62, "钱付得慢：从上上游收到货到付钱隔了近两个月",
        fontsize=10.8, color=C_ORANGE, ha="left", va="center", weight="bold")

ax.text(0, -1.45,
        f"应收 {ar_days:.1f} 天 ＋ 存货 {inv_days:.1f} 天 − 应付 {ap_days:.1f} 天\n"
        f"＝ 现金转换周期 {ccc:.1f} 天（几乎不占自己的钱）",
        fontsize=10.8, color="#333333", ha="left", va="center", linespacing=1.7,
        bbox=dict(boxstyle="round,pad=0.40", fc="#f7f7f7", ec=C_GRAY, lw=0.9))
ax.set_ylim(-2.05, 2.95)

# ══════════════════ 右：分档计提比例 ══════════════════
ax2 = axes[1]
buckets = ["3个月以内", "4-6个月", "7-12个月", "1年以上"]
show_lbl = ["3 个月以内", "4-6 个月", "7-12 个月", "1 年以上"]
rates = [sup["accounts_receivable"]["by_bucket_2024"][b]["计提比例"] for b in buckets]
amounts = [sup["accounts_receivable"]["by_bucket_2024"][b]["应收账款"] / 1e8
           for b in buckets]

xs = list(range(len(buckets)))
bars2 = ax2.bar(xs, rates, width=0.56,
                color=[C_BLUE, C_GREEN, C_ORANGE, C_RED],
                edgecolor="white", lw=0.8)

ax2.set_xticks(xs)
ax2.set_xticklabels([f"{b}\n{amt:,.2f} 亿元" for b, amt in zip(show_lbl, amounts)],
                    fontsize=10.6)
ax2.set_ylim(0, 25)
ax2.set_ylabel("坏账计提比例（%）", fontsize=11.5)
ax2.set_title("账龄越长，计提越狠：1 年以上要打掉近两成",
              fontsize=13.5, pad=12, weight="bold")
ax2.grid(axis="y", color="#eaeaea", lw=0.8, zorder=0)
ax2.set_axisbelow(True)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

for x, v in zip(xs, rates):
    ax2.text(x, v + 0.45, f"{v:.2f}%", ha="center", va="bottom",
             fontsize=12, weight="bold", color="#222222")

ax2.text(0.02, 0.94,
         "同一笔货款，账龄每长一档，\n公司就多认一部分「可能收不回来」",
         transform=ax2.transAxes, fontsize=10.5, color="#333333",
         ha="left", va="top", linespacing=1.6,
         bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=C_GRAY, lw=0.9))

fig.text(0.99, 0.005,
         "数据来源：伊利 2024 年报 page_154、page_087、page_091；"
         "周转天数取自 data/yili2024.json 的 ratios",
         ha="right", va="bottom", fontsize=9.5, color=C_GRAY)

save(fig, "w03d3_receivable_days.png")
