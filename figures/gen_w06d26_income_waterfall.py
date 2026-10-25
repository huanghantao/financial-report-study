# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 6 周第 26 章配图：伊利 2024 年利润表瀑布（上半场 + 下半场放大）。

上半场：营业收入 1,153.93 亿，减成本、税金、销售、管理、研发，加回财务费用净收益，
        得到"经营利润（未计杂项）"116.36 亿。
下半场：从 116.36 亿出发，加减利息收入、其他收益、投资收益、公允价值、两项减值、
        资产处置，落到营业利润 101.82 亿。金额跨度大，所以下半场单独放大。

所有数字来自 data/yili2024.json 的 income 段，脚本内只做加减，不手打。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import save, waterfall, C_GRAY, C_BLUE, C_GREEN  # noqa: E402
from figures._data import load  # noqa: E402

d = load("yili2024")
inc = d["income"]

rev = inc["revenue"] / 1e8
cost = inc["cost_of_sales"] / 1e8
tax = inc["taxes_and_surcharges"] / 1e8
sell = inc["selling_expenses"] / 1e8
admin = inc["admin_expenses"] / 1e8
rd = inc["rd_expenses"] / 1e8
fin = inc["finance_expenses"] / 1e8          # 负数，表示净收益
gross = rev - cost
op_before = gross - tax - sell - admin - rd - fin

interest = inc["interest_income"] / 1e8       # 营业总收入里的利息收入（财务公司）
other = inc["other_income"] / 1e8
inv = inc["investment_income"] / 1e8
fair = inc["fair_value_change"] / 1e8         # 负数
credit = inc["credit_impairment"] / 1e8       # 负数
asset = inc["asset_impairment"] / 1e8         # 负数
disposal = inc["asset_disposal"] / 1e8        # 负数
op = inc["operating_profit"] / 1e8

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(17.0, 7.8), constrained_layout=True,
    gridspec_kw={"width_ratios": [1.32, 1.0]},
)

# ── 上半场：收入 → 经营利润 ─────────────────────────────────────
steps_left = [
    ("营业收入", rev, "total"),
    ("营业成本", -cost, "down"),
    ("毛利", gross, "total"),
    ("税金及附加", -tax, "down"),
    ("销售费用", -sell, "down"),
    ("管理费用", -admin, "down"),
    ("研发费用", -rd, "down"),
    ("财务费用", -fin, "up"),          # 费用为负，等于加回 5.92
    ("经营利润\n（未计杂项）", op_before, "total"),
]
waterfall(ax1, steps_left, unit="亿元", fontsize=10.5,
          total_color=C_BLUE, down_color="#d95f5f", up_color=C_GREEN,
          ylim_head_frac=0.16)
ax1.set_title("上半场：1,153.93 亿收入，减完成本费用，剩 116.36 亿",
              fontsize=14, pad=14)

# 在毛利柱上方补一句"这一行报表上没有"
ax1.annotate("毛利不是报表行项目，\n是收入减成本自己算的",
             xy=(2.30, 402), xytext=(4.65, 640),
             fontsize=10.2, color=C_GRAY, ha="center",
             bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#cccccc", lw=0.8),
             arrowprops=dict(arrowstyle="->", color=C_GRAY, lw=1.0,
                             connectionstyle="arc3,rad=0.15"))

# ── 下半场：经营利润 → 营业利润 ────────────────────────────────
steps_right = [
    ("经营利润\n（未计杂项）", op_before, "total"),
    ("利息收入", interest, "up"),
    ("其他收益", other, "up"),
    ("投资收益", inv, "up"),
    ("公允价值", -fair, "down"),
    ("信用减值", -credit, "down"),
    ("资产减值", -asset, "down"),
    ("资产处置", -disposal, "down"),
    ("营业利润", op, "total"),
]
waterfall(ax2, steps_right, unit="亿元", fontsize=9.8,
          total_color=C_BLUE, down_color="#d95f5f", up_color=C_GREEN,
          ylim_head_frac=0.18)
ax2.set_title("下半场（放大看）：杂项一进一出，落到 101.82 亿",
              fontsize=14, pad=14)

fig.text(
    0.012, -0.045,
    "数据来源：伊利 2024 年报 page_091、page_092（合并利润表）。\n"
    "左图把 762.99 亿营业成本、7.33 亿税金、219.82 亿销售费用、44.65 亿管理费用、"
    "8.70 亿研发费用一路减掉；财务费用是 -5.92 亿，减负数等于加回。\n"
    "右图里 3.86 亿利息收入是营业总收入里的那一笔（财务公司放贷收的息），"
    "与财务费用里的 24.55 亿利息收入不是同一个口径。",
    ha="left", va="top", fontsize=9.4, color=C_GRAY, linespacing=1.6,
)

save(fig, "w06d26_income_waterfall.png")
