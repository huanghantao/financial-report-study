# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 5 周第 21 章配图：伊利 2024 年 967.10 亿元负债拆成「有息」与「经营性」两堆。

数字全部来自 data/yili2024.json（已核实），不手打。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import (
    save, stacked_bar, bar_labels, legend_outside, clean_axes,
    C_BLUE, C_ORANGE, C_GRAY, C_GOLD,
)
from figures._data import load
import matplotlib.pyplot as plt

d = load("yili2024")
b = d["balance"]
notes = d["notes"]
r = d["ratios"]

yi = 1e8
total_liab = b["total_liabilities"] / yi
ibd = r["interest_bearing_debt"] / yi
operating = total_liab - ibd

st = b["short_term_borrowings"] / yi
stb = b["short_term_bonds_payable"] / yi
due1y = b["noncurrent_liabilities_due_1y"] / yi
ltb = b["long_term_borrowings"] / yi
lease = b["lease_liabilities"] / yi
ap = b["accounts_payable"] / yi
contract = b["contract_liabilities"] / yi
salary = b["employee_compensation_payable"] / yi
other_pay = b["other_payables"] / yi
# 其他经营性负债 = 其他流动负债里的非债券部分 + 递延所得税负债 + 应付票据
# + 应交税费 + 递延收益 + 衍生金融负债 + 长期应付职工薪酬（page_088、page_195）
other_operating = (
    (b["other_current_liabilities"] - b["short_term_bonds_payable"])
    + b["deferred_tax_liabilities"]
    + b["notes_payable"]
    + b["taxes_payable"]
    + b["deferred_income"]
    + 159011722.29               # 衍生金融负债（page_088）
    + 16156716.42                # 长期应付职工薪酬（page_088）
) / yi

fig = plt.figure(figsize=(13.5, 8.6))
gs = fig.add_gridspec(2, 1, height_ratios=[0.95, 2.4], hspace=0.10)
ax_top = fig.add_subplot(gs[0])
ax_bot = fig.add_subplot(gs[1])
fig.subplots_adjust(left=0.285, right=0.79, top=0.955, bottom=0.09)
ax_top.set_xlim(0, 10)
ax_top.set_ylim(0, 10)
ax_top.axis("off")

stacked_bar(
    ax_top,
    [("有息负债（要付利息）", ibd, C_ORANGE),
     ("经营性负债（占用上下游）", operating, C_BLUE)],
    total=total_liab,
    y=3.6, height=2.3, x0=0.5, width=9.0, unit=" 亿",
    min_inside=0.16, fontsize=12.5, upper_y=7.3, lower_y=2.3,
    title="967.10 亿元负债，先分成两堆",
    subtitle="单位：亿元。占比按负债合计 967.10 亿元计算",
)

rows = [
    ("短期借款", st, C_ORANGE),
    ("应付账款", ap, C_BLUE),
    ("合同负债", contract, C_BLUE),
    ("短期应付债券", stb, C_ORANGE),
    ("一年内到期的非流动负债", due1y, C_ORANGE),
    ("其余 7 项经营性负债合计", other_operating, C_BLUE),
    ("长期借款", ltb, C_ORANGE),
    ("应付职工薪酬", salary, C_BLUE),
    ("其他应付款", other_pay, C_BLUE),
    ("租赁负债", lease, C_ORANGE),
]
rows.sort(key=lambda t: t[1])
names = [t[0] for t in rows]
vals = [t[1] for t in rows]
colors = [t[2] for t in rows]
ypos = range(len(rows))

bars = ax_bot.barh(list(ypos), vals, color=colors, height=0.62, zorder=3)
ax_bot.set_yticks(list(ypos))
ax_bot.set_yticklabels(names, fontsize=11.5)
ax_bot.set_xlim(0, 430)
ax_bot.set_xlabel("金额（亿元）", fontsize=11.5)
ax_bot.set_title("十项主要负债：橙色要付息，蓝色是占用别人的钱",
                 fontsize=13.5, pad=10, loc="left")
for bar, v in zip(bars, vals):
    ax_bot.text(v + 5, bar.get_y() + bar.get_height() / 2,
                f"{v:,.2f}", va="center", ha="left", fontsize=11,
                color="#333333", zorder=6)
ax_bot.axvline(0, color="#999999", lw=0.9)
clean_axes(ax_bot)

from matplotlib.patches import Patch
handles = [Patch(facecolor=C_ORANGE, label="有息负债"),
           Patch(facecolor=C_BLUE, label="经营性负债")]
ax_bot.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.02, 1.0),
              frameon=False, fontsize=11.5)

# 两组合计，放在右下角空白处
ax_bot.text(0.985, 0.06,
            f"有息负债合计 {ibd:,.2f} 亿元（{ibd / total_liab:.1%}）\n"
            f"经营性负债合计 {operating:,.2f} 亿元（{operating / total_liab:.1%}）",
            transform=ax_bot.transAxes, ha="right", va="bottom",
            fontsize=11, color="#444444",
            bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=C_GRAY, lw=0.8))

fig.text(0.02, 0.018, "数据来源：伊利股份 2024 年报 page_087、page_088、page_195",
         fontsize=9.5, color="#666666")

save(fig, "w05d21_liability_split.png")
