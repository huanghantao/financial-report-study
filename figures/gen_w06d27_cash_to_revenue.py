# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 6 周第 27 章配图：营业收入 vs 销售商品收到的现金，以及合同负债。

左图：两年的收入与销售收现并排，柱顶标收现比（1.091 → 1.132）。
右图：合同负债从 86.96 亿增到 120.73 亿，解释"先收钱、后交货"。

数字全部来自 data/yili2024.json 的 income / cashflow / balance / compare_2023 段。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, bar_labels, label, clean_axes, legend_outside,
    C_BLUE, C_GREEN, C_ORANGE, C_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
rev24 = d["income"]["revenue"] / 1e8
rev23 = d["compare_2023"]["income"]["revenue"] / 1e8
cash24 = d["cashflow"]["cash_from_sales"] / 1e8
cash23 = d["compare_2023"]["cashflow"]["cash_from_sales"] / 1e8
cl24 = d["balance"]["contract_liabilities"] / 1e8
cl23 = d["compare_2023"]["balance"]["contract_liabilities"] / 1e8

ratio24 = cash24 / rev24
ratio23 = cash23 / rev23

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(15.0, 7.2), constrained_layout=True,
    gridspec_kw={"width_ratios": [1.35, 0.85]},
)

# ── 左：收入 vs 销售收现 ──────────────────────────────────────
x = [0, 1.5]
w = 0.52
b1 = ax1.bar([i - w / 2 for i in x], [rev23, rev24], width=w,
             color=C_BLUE, label="营业收入（报表确认）", zorder=3)
b2 = ax1.bar([i + w / 2 for i in x], [cash23, cash24], width=w,
             color=C_GREEN, label="销售商品、提供劳务收到的现金", zorder=3)
ax1.set_ylim(0, 1650)
ax1.set_xlim(-0.62, 3.62)
ax1.set_xticks(x)
ax1.set_xticklabels(["2023 年", "2024 年"], fontsize=13)
ax1.set_ylabel("金额（亿元）", fontsize=11.5)
ax1.set_title("收现比从 1.091 升到 1.132：收到的钱始终多于确认的收入",
              fontsize=13.5, pad=14)
bar_labels(ax1, b1, [rev23, rev24], fmt=lambda v: f"{v:,.2f}", fontsize=11)
bar_labels(ax1, b2, [cash23, cash24], fmt=lambda v: f"{v:,.2f}", fontsize=11)
legend_outside(ax1, fontsize=11)

label(ax1, 0.0, 1520, f"收现比 {ratio23:.3f}", fontsize=12.5, weight="bold",
      color=C_ORANGE)
label(ax1, 1.5, 1520, f"收现比 {ratio24:.3f}", fontsize=12.5, weight="bold",
      color=C_ORANGE)
ax1.text(2.40, 840,
         "收现比大于 1，钱从哪来\n\n"
         "① 售价里含 13% 增值税，\n    收到的现金天然比收入多\n"
         "② 预收货款先收钱、后交货\n    （合同负债 120.73 亿）",
         fontsize=10.6, color="#333333", ha="left", va="center",
         linespacing=1.65,
         bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=C_ORANGE, lw=1.0))
clean_axes(ax1)

# ── 右：合同负债 ──────────────────────────────────────────────
x2 = [0, 1]
b3 = ax2.bar(x2, [cl23, cl24], width=0.48, color=[C_GRAY, C_ORANGE], zorder=3)
ax2.set_ylim(0, 208)
ax2.set_xticks(x2)
ax2.set_xticklabels(["2023 年末", "2024 年末"], fontsize=12.5)
ax2.set_ylabel("合同负债（亿元）", fontsize=11.5)
ax2.set_title("合同负债一年增加 33.75 亿：先收钱、后交货", fontsize=13, pad=14)
bar_labels(ax2, b3, [cl23, cl24], fmt=lambda v: f"{v:,.2f}", fontsize=11.5)
label(ax2, 0.5, 150, "+38.8%", fontsize=13, weight="bold", color=C_ORANGE)
label(ax2, 0.5, 188,
      "这笔钱已经进了银行账户，但还没算成收入",
      fontsize=10.2, color="#333333")
clean_axes(ax2)

fig.text(
    0.012, -0.04,
    "数据来源：伊利 2024 年报 page_091（营业收入）、page_094（销售商品收到的现金）、"
    "page_191（合同负债期初 86.96 亿、期末 120.73 亿）。\n"
    "收现比 = 销售商品、提供劳务收到的现金 ÷ 营业收入。现金里含增值税，所以健康消费品的收现比通常略高于 1。",
    ha="left", va="top", fontsize=9.4, color=C_GRAY, linespacing=1.6,
)

save(fig, "w06d27_cash_to_revenue.png")
