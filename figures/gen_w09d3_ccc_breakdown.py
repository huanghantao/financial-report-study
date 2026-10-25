# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 9 周第 43 章配图：现金转换周期 CCC 的三段拆解 + 两个口径对照。

左图：平均余额口径。应付账款往下画（占用供应商的钱），存货与应收往上画
      （自己垫的钱），净额就是 CCC = 2.6 天。
右图：同一家公司、同一年，期末余额口径与平均余额口径的差异。

数字全部来自 data/yili2024.json 的 working_capital / ratios /
income / balance / compare_2023 段。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, C_BLUE, C_GREEN, C_ORANGE, C_PURPLE, C_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
wc, r = d["working_capital"], d["ratios"]
inc, bal, bal23 = d["income"], d["balance"], d["compare_2023"]["balance"]

cost = inc["cost_of_sales"]
rev = inc["revenue"]
DAYS = 365.0

# ── 平均余额口径（左图）────────────────────────────────────────────
inv_d = wc["inventory_days"]
rec_d = wc["receivable_days"]
pay_d = wc["payable_days"]
ccc = wc["cash_conversion_cycle_days"]

# ── 期末余额口径（右图，复算 ratios 里的旧口径）─────────────────────
inv_d_end = bal["inventory"] / cost * DAYS
rec_d_end = bal["accounts_receivable"] / rev * DAYS
pay_d_end = bal["accounts_payable"] / cost * DAYS
ccc_end = inv_d_end + rec_d_end - pay_d_end

fig, axes = plt.subplots(1, 2, figsize=(14.4, 7.2),
                         gridspec_kw={"width_ratios": [1.12, 1.0]})
fig.subplots_adjust(left=0.115, right=0.975, top=0.775, bottom=0.235,
                    wspace=0.30)

# ════════════════════ 左：CCC 三段横向条形 ════════════════════════
ax = axes[0]
items = [
    ("应付账款\n（占用供应商）", -pay_d, C_GREEN),
    ("存货\n（躺在仓库）", inv_d, C_BLUE),
    ("应收账款\n（卖完等钱）", rec_d, C_ORANGE),
]
for k, (name, val, color) in enumerate(items):
    ax.barh(k, val, height=0.52, color=color, zorder=3)
    off = 1.6 if val >= 0 else -1.6
    ax.text(val + off, k, f"{abs(val):.1f} 天", va="center",
            ha="left" if val >= 0 else "right",
            fontsize=12.4, weight="bold", color="#1a1a1a", zorder=6)

ax.axvline(0, color="#666666", lw=1.2, zorder=4)
ax.set_yticks(range(3))
ax.set_yticklabels([it[0] for it in items], fontsize=11.2, linespacing=1.5)
ax.set_xlim(-92, 78)
ax.set_xlabel("天数（负数＝占用别人的钱，正数＝自己的钱被占用）", fontsize=11.0)
ax.set_title(f"三段一抵，CCC 只有 {ccc:.1f} 天", fontsize=13.4, pad=12)
ax.set_xticks([-60, -40, -20, 0, 20, 40, 60])
ax.tick_params(axis="x", labelsize=10.4)
ax.grid(axis="x", color="#e6e6e6", lw=0.8, zorder=0)
clean_axes(ax)

# 净额标注放在条形下方，避开柱体
ax.annotate(f"净额 CCC = {inv_d:.1f} + {rec_d:.1f} - {pay_d:.1f} = {ccc:.1f} 天",
            xy=(ccc, -0.62), xytext=(6, -0.86), fontsize=11.4,
            color=C_PURPLE, weight="bold", ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.34", fc="white", ec=C_PURPLE,
                      lw=1.2, alpha=0.96),
            arrowprops=dict(arrowstyle="-|>", color=C_PURPLE, lw=1.4,
                            shrinkA=2, shrinkB=3))
ax.set_ylim(-1.05, 2.62)

# ════════════════ 右：两个口径的差异 ════════════════════════════
ax2 = axes[1]
labels = ["存货\n周转天数", "应收账款\n天数", "应付账款\n天数", "CCC"]
end_vals = [inv_d_end, rec_d_end, pay_d_end, ccc_end]
avg_vals = [inv_d, rec_d, pay_d, ccc]

x = np.arange(len(labels))
w = 0.36
b1 = ax2.bar(x - w / 2, end_vals, w, color="#9ecae1", edgecolor=C_BLUE,
             lw=1.1, zorder=3, label="期末余额口径（年报比率表常用）")
b2 = ax2.bar(x + w / 2, avg_vals, w, color=C_BLUE, zorder=3,
             label="平均余额口径（本学期末+期初）÷2")

for bars, vals in ((b1, end_vals), (b2, avg_vals)):
    for bb, v in zip(bars, vals):
        ax2.text(bb.get_x() + bb.get_width() / 2, v + 1.4, f"{v:.1f}",
                 ha="center", va="bottom", fontsize=11.2, weight="bold",
                 color="#1a1a1a", zorder=6)

ax2.set_xticks(x)
ax2.set_xticklabels(labels, fontsize=11.0, linespacing=1.5)
ax2.set_ylim(0, 76)
ax2.set_ylabel("天数", fontsize=11.2)
ax2.set_title("同一家公司同一年，两个口径差 1.0 天", fontsize=13.4, pad=12)
ax2.tick_params(axis="y", labelsize=10.4)
ax2.grid(axis="y", color="#e6e6e6", lw=0.8, zorder=0)
clean_axes(ax2)
ax2.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0), fontsize=9.6,
           frameon=False, ncol=1)

# 差异来源的注释：放在画布底部，不压任何柱体
fig.text(0.505, 0.135,
         f"差在哪：2023 年末存货 {bal23['inventory'] / 1e8:.2f} 亿 > 2024 年末 "
         f"{bal['inventory'] / 1e8:.2f} 亿，一平均就比期末高，周转天数变长；"
         f"应付账款同理（{bal23['accounts_payable'] / 1e8:.2f} 亿降到 "
         f"{bal['accounts_payable'] / 1e8:.2f} 亿）。\n"
         f"所以 CCC 从 {r['cash_conversion_cycle_days']:.1f} 天变成 {ccc:.1f} 天，"
         "不是生意变差，是算法换了。",
         fontsize=9.4, color="#333333", va="top", ha="left", linespacing=1.7)

fig.suptitle("伊利 2024 年的现金转换周期只有 2.6 天：付原料钱到收回货款，几乎不占钱",
             fontsize=15.2, weight="bold", y=0.955)
fig.text(0.012, 0.070,
         "数据来源：伊利 2024 年报 page_087（存货、应收账款）、page_088（应付账款）、page_091（营业成本、营业收入）；"
         "计算口径见 data/yili2024.json 的 working_capital 段。周转天数 = 平均余额 ÷ 对应流量 × 365。",
         fontsize=9.2, color=C_GRAY)
fig.text(0.012, 0.024,
         "读法：CCC 越短越好。CCC 为负，说明做生意不但不垫钱，还先收了别人的钱——那是产业链上最强势的位置。",
         fontsize=9.6, color="#333333")

save(fig, "w09d3_ccc_breakdown.png")
