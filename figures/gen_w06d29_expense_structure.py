# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 6 周第 29 章配图：毛利率减三项费用和税金，还剩多少；费用率两年对比。

左图：把毛利率 33.88% 一层层减到经营利润率 10.08%（百分点瀑布）。
右图：销售、管理、研发三项费用率的两年对比，销售费用率是唯一明显上升的。

数字来自 data/yili2024.json 的 income / core_earnings 段，脚本内只做除法与加减。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, waterfall, bar_labels, label, clean_axes, legend_outside,
    C_BLUE, C_GRAY, C_GREEN, C_ORANGE,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
inc = d["income"]
rev = inc["revenue"]
rev23 = d["compare_2023"]["income"]["revenue"]

gm = d["core_earnings"]["gross_margin_2024"] * 100
sell = inc["selling_expenses"] / rev * 100
admin = inc["admin_expenses"] / rev * 100
rd = inc["rd_expenses"] / rev * 100
fin = inc["finance_expenses"] / rev * 100          # 负数
tax = inc["taxes_and_surcharges"] / rev * 100
op_margin = gm - sell - admin - rd - fin - tax

sell23 = d["core_earnings"]["selling_ratio_2023"] * 100
admin23 = d["core_earnings"]["admin_ratio_2023"] * 100
rd23 = d["compare_2023"]["income"]["rd_expenses"] / rev23 * 100
fin23 = d["compare_2023"]["income"]["finance_expenses"] / rev23 * 100

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(15.6, 7.3), constrained_layout=True,
    gridspec_kw={"width_ratios": [1.15, 1.0]},
)

# ── 左：毛利率 → 经营利润率 ──────────────────────────────────
steps = [
    ("毛利率", gm, "total"),
    ("销售费用", -sell, "down"),
    ("管理费用", -admin, "down"),
    ("研发费用", -rd, "down"),
    ("财务费用", -fin, "up"),          # 负数费用，等于加分
    ("税金及附加", -tax, "down"),
    ("经营利润率", op_margin, "total"),
]
waterfall(ax1, steps, unit="百分点", fmt="{:,.2f}%", fontsize=9.6,
          total_color=C_BLUE, down_color="#d95f5f", up_color=C_GREEN,
          ylim_head_frac=0.18)
ax1.set_title("33.88% 的毛利率，减完费用和税金，剩 10.08%", fontsize=13.0, pad=14)
ax1.set_ylabel("占营业收入的比重（百分点）", fontsize=10.5, labelpad=12)
ax1.yaxis.set_label_coords(-0.115, 0.5)

ax1.text(4.35, 25.2,
         "三项费用合计 23.67%，再加税金 0.63%\n"
         "33.88% - 24.30% = 9.58 个百分点",
         fontsize=10.2, color="#333333", ha="left", va="center",
         linespacing=1.7,
         bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=C_GRAY, lw=0.9))

# ── 右：三项费用率两年对比 ────────────────────────────────────
cats = ["销售费用率", "管理费用率", "研发费用率"]
v23 = [sell23, admin23, rd23]
v24 = [sell, admin, rd]
ys = [2, 1, 0]
h = 0.34
b1 = ax2.barh([i + h / 2 for i in ys], v23, height=h, color=C_GRAY,
              label="2023 年", zorder=3)
b2 = ax2.barh([i - h / 2 for i in ys], v24, height=h, color=C_BLUE,
              label="2024 年", zorder=3)
ax2.set_yticks(ys)
ax2.set_yticklabels(cats, fontsize=12.5)
ax2.set_xlim(0, 22.5)
ax2.set_xlabel("费用率（%）", fontsize=11.5)
ax2.set_title("只有销售费用率明显上升：17.95% → 19.05%", fontsize=13, pad=14)
legend_outside(ax2, fontsize=11)
for b, vals in ((b1, v23), (b2, v24)):
    for bi, v in zip(b, vals):
        ax2.text(bi.get_width() + 0.3, bi.get_y() + bi.get_height() / 2,
                 f"{v:.2f}%", va="center", ha="left",
                 fontsize=11, weight="bold", color="#333333")
label(ax2, 8.6, -0.62,
      "财务费用率：-0.12% → -0.51%（负数是净利息收入，给利润加分）",
      fontsize=10.0, color="#333333")
clean_axes(ax2)
ax2.set_ylim(-1.05, 2.55)

fig.text(
    0.012, -0.045,
    "数据来源：伊利 2024 年报 page_091（销售费用 219.82 亿、管理费用 44.65 亿、研发费用 8.70 亿、"
    "财务费用 -5.92 亿、税金及附加 7.33 亿）、data/yili2024.json 的 income 与 core_earnings 段。\n"
    "经营利润率 = 毛利率 - 销售费用率 - 管理费用率 - 研发费用率 - 财务费用率 - 税金及附加率；"
    "财务费用为负，减负数等于加回 0.51 个百分点。",
    ha="left", va="top", fontsize=9.4, color=C_GRAY, linespacing=1.6,
)

save(fig, "w06d29_expense_structure.png")
