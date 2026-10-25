# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 3 周第 1 章配图：伊利 2024 年资产按变现速度排队。

左图：流动资产 / 非流动资产 的占比条 + 四段变现速度阶梯；
右图：资产科目从「最快变成现金」到「最慢变成现金」依次排队。

口径说明：科目金额全部来自 data/yili2024.json。
JSON 里没有单列的零星科目（交易性金融资产以外的衍生金融资产、
其他权益工具投资、其他非流动金融资产、投资性房地产、长期待摊费用）
用「合计 − 已单列科目之和」轧差得到，脚本里不手打任何一个公司数字。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, stacked_bar,
    C_BLUE, C_ORANGE, C_GREEN, C_GRAY,
)
from figures._data import load  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as mpatches  # noqa: E402

d = load("yili2024")
B = d["balance"]
E = 1e8

cur = B["total_current_assets"] / E          # 666.19
noncur = B["total_noncurrent_assets"] / E    # 870.99
total = B["total_assets"] / E                # 1,537.18

# ── 流动资产：7 个单列科目 + 1 个轧差零星科目 ──────────────────
cur_items = [
    ("货币资金", B["cash"]),
    ("应收票据及应收账款", B["notes_receivable"] + B["accounts_receivable"]),
    ("预付款项", B["prepayments"]),
    ("其他应收款", B["other_receivables"]),
    ("存货", B["inventory"]),
    ("一年内到期的非流动资产", B["noncurrent_assets_due_1y"]),
    ("其他流动资产", B["other_current_assets"]),
]
cur_listed = sum(v for _, v in cur_items)
cur_minor = B["total_current_assets"] - cur_listed   # 衍生金融资产等零星科目
cur_items.insert(1, ("交易性金融资产等零星", cur_minor))

# ── 非流动资产：9 个单列科目 + 1 个轧差科目 ────────────────────
noncur_items = [
    ("长期股权投资", B["long_term_equity_investment"]),
    ("投资性房地产等零星（4 项）", None),
    ("固定资产", B["fixed_assets"]),
    ("在建工程", B["construction_in_progress"]),
    ("生产性生物资产", B["productive_biological_assets"]),
    ("使用权资产", B["right_of_use_assets"]),
    ("无形资产", B["intangible_assets"]),
    ("商誉", B["goodwill"]),
    ("递延所得税资产", B["deferred_tax_assets"]),
    ("其他非流动资产", B["other_noncurrent_assets"]),
]
noncur_listed = sum(v for _, v in noncur_items if v is not None)
noncur_minor = B["total_noncurrent_assets"] - noncur_listed
noncur_items[1] = (noncur_items[1][0], noncur_minor)

rows = [(n, v / E, True) for n, v in cur_items] + \
       [(n, v / E, False) for n, v in noncur_items]
vals = [v for _, v, _ in rows]
is_cur = [c for _, _, c in rows]

fig = plt.figure(figsize=(15.8, 8.8))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.38], wspace=0.34)

# ══════════════════ 左：占比条 + 四段阶梯 ══════════════════
ax1 = fig.add_subplot(gs[0])
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis("off")

ax1.text(0.4, 9.55, "一把尺子：一年内能不能变成现金", fontsize=14.5,
         weight="bold", ha="left", va="center", color="#1a1a1a")

stacked_bar(
    ax1,
    [("流动资产", cur, C_BLUE), ("非流动资产", noncur, C_ORANGE)],
    total=total, y=6.7, height=1.5, x0=0.4, width=9.2,
    min_inside=0.16, fontsize=11.5,
    upper_y=8.6, lower_y=4.2, show_value=False, show_pct=True,
)

ax1.annotate("", xy=(9.6, 8.42), xytext=(0.4, 8.42),
             arrowprops=dict(arrowstyle="<|-", color=C_GRAY, lw=1.3))
ax1.text(0.4, 8.60, "变现快", fontsize=10.5, color=C_GRAY,
         ha="left", va="bottom")
ax1.text(9.6, 8.60, "变现慢", fontsize=10.5, color=C_GRAY,
         ha="right", va="bottom")

ax1.text(0.4, 6.45,
         f"流动资产 {cur:,.2f} ＋ 非流动资产 {noncur:,.2f}\n＝ 资产总计 {total:,.2f} 亿元",
         fontsize=10.6, color="#333333", ha="left", va="top", linespacing=1.6)

steps = [
    ("① 现金", "货币资金、交易性金融资产", "今天就能用", C_BLUE),
    ("② 债权", "应收票据、应收账款、预付款项", "几天到几个月", C_BLUE),
    ("③ 实物", "存货：原奶、半成品、成品", "卖出去才变钱", C_GREEN),
    ("④ 长期", "固定资产、无形资产、商誉", "一年以上，甚至卖不掉", C_ORANGE),
]
ax1.text(0.4, 4.55, "资产内部的四个段位", fontsize=11.5, weight="bold",
         ha="left", va="center", color="#1a1a1a")
for i, (tag, what, when, color) in enumerate(steps):
    y = 3.72 - i * 0.95
    ax1.add_patch(mpatches.Rectangle((0.4, y - 0.03), 0.14, 0.42,
                                     facecolor=color, edgecolor="none"))
    ax1.text(0.75, y + 0.20, tag, fontsize=10.9, weight="bold", color=color,
             ha="left", va="center")
    ax1.text(0.75, y - 0.16, what, fontsize=9.8, color="#444444",
             ha="left", va="center")
    ax1.text(9.6, y + 0.02, when, fontsize=9.8, color=color, ha="right",
             va="center", weight="bold")

# ══════════════════ 右：科目排队 ══════════════════
ax2 = fig.add_subplot(gs[1])
ys = list(range(len(rows)))
colors = [C_BLUE if c else C_ORANGE for c in is_cur]
ax2.barh(ys, vals, height=0.64, color=colors,
         edgecolor="white", linewidth=0.6, zorder=3)

ax2.set_yticks(ys)
ax2.set_yticklabels([r[0] for r in rows], fontsize=9.4)
ax2.invert_yaxis()
ax2.set_xlim(0, 400)
ax2.set_xlabel("金额（亿元）", fontsize=11)
ax2.set_title("伊利 2024 年资产科目：从最快变成现金到最慢", fontsize=13.5,
              pad=10, weight="bold")
ax2.grid(axis="x", color="#e8e8e8", lw=0.8, zorder=0)
ax2.set_axisbelow(True)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

for y, v in zip(ys, vals):
    ax2.text(v + 4, y, f"{v:,.2f}", va="center", ha="left", fontsize=9.3,
             color="#333333", zorder=5)

n_cur = len(cur_items)
ax2.axhline(n_cur - 0.5, color=C_GRAY, lw=1.0, ls=(0, (5, 4)), zorder=4)

handles = [
    mpatches.Patch(color=C_BLUE, label=f"流动资产 {cur:,.2f} 亿元（一年内变现）"),
    mpatches.Patch(color=C_ORANGE, label=f"非流动资产 {noncur:,.2f} 亿元（一年以上）"),
]
ax2.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.01, 1.0),
           frameon=False, fontsize=10)

fig.text(0.99, 0.005, "数据来源：伊利 2024 年报 page_087（合并资产负债表）",
         ha="right", va="bottom", fontsize=9.5, color=C_GRAY)

save(fig, "w03d1_asset_liquidity.png")
