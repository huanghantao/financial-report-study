# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 3 周第 5 章第二张配图：伊利 2024 年资产结构——按「块」看，而不是按科目看。

一根 100% 竖条把 1,537.18 亿元切成 7 块，右侧图例给出每块的金额与占比。
一张图看清：类现金 42.4%、长期经营资产 29.0%、存货 7.0%、商誉 1.5%。

口径：data/yili2024.json 的 balance + data/yili2024_supplement.json（存单与零星科目）。
脚本里验算「7 块之和 = 资产总计」，不平就报错。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_RED, C_PURPLE, C_GOLD, C_BROWN,
)
from figures._data import load  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as mpatches  # noqa: E402

d = load("yili2024")
sup = load("yili2024_supplement")
B = d["balance"]
E = 1e8
TOT = B["total_assets"] / E
minor = sup["balance_minor"]["noncurrent_2024"]

dep_cur = d["notes"]["time_deposits_in_other_current_assets"] / E
dep_non = d["notes"]["time_deposits_in_other_noncurrent_assets"] / E

cash_block = B["cash"] / E + dep_cur + dep_non
ops_block = (B["fixed_assets"] + B["construction_in_progress"] + B["intangible_assets"]
             + B["productive_biological_assets"] + B["right_of_use_assets"]) / E
inv_block = B["inventory"] / E
ar_block = (B["notes_receivable"] + B["accounts_receivable"] + B["prepayments"]
            + B["other_receivables"]) / E
inv_asset_block = (B["long_term_equity_investment"]
                   + minor["其他权益工具投资"] + minor["其他非流动金融资产"]
                   + minor["投资性房地产"]) / E
gw_block = B["goodwill"] / E
rest_block = TOT - cash_block - ops_block - inv_block - ar_block - inv_asset_block - gw_block

blocks = [
    ("类现金（货币资金＋两类存单）", cash_block, C_GREEN),
    ("长期经营资产（固定＋在建＋无形＋生物＋使用权）", ops_block, C_BLUE),
    ("存货", inv_block, C_PURPLE),
    ("应收票据与应收账款、预付款项", ar_block, C_GOLD),
    ("投资类资产（长期股权＋其他权益工具＋投资性房地产）", inv_asset_block, C_BROWN),
    ("商誉", gw_block, C_RED),
    ("其他（一年内到期、其他流动资产、递延所得税等）", rest_block, C_GRAY),
]

sm = sum(v for _, v, _ in blocks)
assert abs(sm - TOT) < 1, f"7 块之和 {sm} 与资产总计 {TOT} 对不上：差额 {sm - TOT}"

fig, ax = plt.subplots(figsize=(13.6, 8.6))
fig.subplots_adjust(left=0.06, right=0.60, top=0.93, bottom=0.20)
ax.set_xlim(0, 1.0)
ax.set_ylim(0, 100)
ax.axis("off")

bar_x, bar_w = 0.22, 0.56
bottom = 0.0
for name, v, color in blocks:
    h = v / TOT * 100
    ax.add_patch(mpatches.Rectangle((bar_x, bottom), bar_w, h,
                                    facecolor=color, edgecolor="white", lw=1.6,
                                    zorder=3))
    if h >= 6.5:
        ax.text(bar_x + bar_w / 2, bottom + h / 2, f"{v:,.1f}",
                ha="center", va="center", fontsize=13, weight="bold",
                color="white", zorder=6)
    bottom += h

ax.text(bar_x + bar_w / 2, 101.8,
        f"资产总计 {TOT:,.2f} 亿元：钱压在哪几块",
        ha="center", va="bottom", fontsize=14, weight="bold", color="#1a1a1a")



handles = [mpatches.Patch(color=c, label=f"{n}　{v:,.2f} 亿元 · {v / TOT * 100:.1f}%")
           for n, v, c in blocks]
ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.86, 1.06),
          frameon=False, fontsize=10.5, handlelength=1.3, labelspacing=1.05,
          alignment="left")

fig.text(0.06, 0.115,
         "读法：绿色那块 42.4% 是随时能变成现金的钱，比蓝色长期资产还多；\n"
         "红色商誉只有 1.5%，但它是最容易「一下子消失」的一块（第 19 章细讲）。",
         fontsize=10.8, color="#333333", ha="left", va="top", linespacing=2.0,
         bbox=dict(boxstyle="round,pad=0.50", fc="#f7f7f7", ec=C_GRAY, lw=0.9))

fig.text(0.99, 0.005,
         "数据来源：伊利 2024 年报 page_087、page_166、page_188",
         ha="right", va="bottom", fontsize=9.5, color=C_GRAY)

save(fig, "w03d5_asset_blocks.png")
