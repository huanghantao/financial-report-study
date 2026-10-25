# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 9 周第 44 章配图之二：大存大贷的对照（伊利、蒙牛）。

一组两根柱：左手"账上有多少类现金"，右手"欠了多少有息负债"，
再在旁边标出净有息负债（负数＝现金比债多）。

伊利的口径来自 data/yili2024.json 的 ratios 段（已核实，含大额存单）；
蒙牛的类现金按 page_048 的管理层披露口径：现金 + 长期定期存款（page_244）。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, C_BLUE, C_ORANGE, C_GREEN, C_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
m = load("mengniu2024")

yi_ = 1e8
y_cash = d["ratios"]["cash_and_deposits"] / yi_
y_debt = d["ratios"]["interest_bearing_debt"] / yi_
y_net = d["ratios"]["net_interest_bearing_debt"] / yi_

m_lt_deposit = 14_006_079_000.0     # 蒙牛 page_244：长期定期存款
m_cash = (m["balance"]["cash"] + m_lt_deposit) / yi_
m_debt = (m["balance"]["borrowings_current"]
          + m["balance"]["borrowings_noncurrent"]) / yi_
m_net = (m["balance"]["borrowings_current"] + m["balance"]["borrowings_noncurrent"]) / yi_ \
        - m_cash
# 蒙牛自己在 page_048 披露的「净借贷」：借款减现金，但不减长期定期存款
m_net_official = 17_298_000_000.0 / yi_

y_assets = d["balance"]["total_assets"] / yi_
m_assets = m["balance"]["total_assets"] / yi_

fig, ax = plt.subplots(figsize=(12.6, 7.2))
fig.subplots_adjust(left=0.10, right=0.975, top=0.795, bottom=0.215)

x = np.arange(2)
w = 0.34
cash_vals = [y_cash, m_cash]
debt_vals = [y_debt, m_debt]

b1 = ax.bar(x - w / 2, cash_vals, w, color=C_BLUE, zorder=3,
            label="类现金（货币资金 + 大额存单 / 长期定期存款）")
b2 = ax.bar(x + w / 2, debt_vals, w, color=C_ORANGE, zorder=3,
            label="有息负债（短期借款、债券、一年内到期、长期借款）")

for bars, vals in ((b1, cash_vals), (b2, debt_vals)):
    for bb, v in zip(bars, vals):
        ax.text(bb.get_x() + bb.get_width() / 2, v + 12, f"{v:,.0f}",
                ha="center", va="bottom", fontsize=12.6, weight="bold",
                color="#1a1a1a", zorder=6)

# 净有息负债 / 净现金：标在每组两根柱的正上方，不压柱体
nets = [("净现金 46 亿", C_GREEN), ("净负债 33 亿", C_ORANGE)]
for k, (txt, col) in enumerate(nets):
    ax.text(k, max(cash_vals[k], debt_vals[k]) + 72, txt, ha="center",
            va="bottom", fontsize=11.6, weight="bold", color=col, zorder=7)

ax.set_xticks(x)
ax.set_xticklabels([f"伊利（总资产 {y_assets:,.0f} 亿）",
                    f"蒙牛（总资产 {m_assets:,.0f} 亿）"], fontsize=12.2)
ax.set_ylabel("金额（亿元）", fontsize=11.6)
ax.set_ylim(0, 800)
ax.tick_params(axis="y", labelsize=10.6)
ax.grid(axis="y", color="#e8e8e8", lw=0.8, zorder=0)
clean_axes(ax)
ax.legend(loc="upper right", bbox_to_anchor=(1.0, 1.0), fontsize=10.0,
          frameon=True, framealpha=0.96, edgecolor="#dddddd")

fig.suptitle("两家都是「账上钱多、同时借得多」：伊利净现金 46 亿，蒙牛净负债 33 亿",
             fontsize=14.8, weight="bold", y=0.955)

fig.text(0.012, 0.115,
         "伊利：类现金 652.07 亿（货币资金 254.04 + 大额存单 118.26 + 定期存款 279.77），"
         "有息负债 605.58 亿，两边几乎相等——所以这条红旗是「必须问清楚」，不是「一定有问题」。",
         fontsize=9.6, color="#333333")
fig.text(0.012, 0.070,
         "蒙牛：现金 173.39 亿 + 长期定期存款 140.06 亿 = 313.45 亿；有息负债 346.37 亿；"
         "两边相减净负债 33 亿。注意蒙牛 page_048 自己披露的净借贷是 172.98 亿——"
         "它的口径不减长期定期存款，两个数都对，只是问的问题不同。",
         fontsize=9.6, color="#333333")
fig.text(0.012, 0.024,
         "数据来源：伊利 2024 年报 page_087、page_088、page_166、page_188、page_195；"
         "蒙牛 2024 年报 page_048、page_142、page_244。"
         "蒙牛有息负债 = 流动借款 166.62 + 非流动借款 179.76；总资产相差 474 亿，看比率比看绝对额更有意义。",
         fontsize=9.0, color=C_GRAY)

save(fig, "w09d4_cash_vs_debt.png")
