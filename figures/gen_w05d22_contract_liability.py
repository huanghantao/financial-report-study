# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 5 周第 22 章配图：伊利合同负债 86.96 → 120.73 亿元，与收入 -8.24% 反向。

数字全部来自 data/yili2024.json（已核实），不手打。

注意：2023 年「预收款项 26.47 亿元」在附注七(37) 里写明是**股权转让款**，
不是货款，所以不与合同负债加总——本图只画合同负债本身。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import (
    save, label, clean_axes, legend_outside,
    C_BLUE, C_ORANGE, C_GRAY, C_RED, C_GREEN,
)
from figures._data import load
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

d = load("yili2024")
b, c23 = d["balance"], d["compare_2023"]["balance"]
inc, inc23 = d["income"], d["compare_2023"]["income"]
yi = 1e8

contract24 = b["contract_liabilities"] / yi
contract23 = c23["contract_liabilities"] / yi
rev24 = inc["revenue"] / yi
rev23 = inc23["revenue"] / yi
rev_yoy = (rev24 / rev23 - 1) * 100
contract_yoy = (contract24 / contract23 - 1) * 100
cover24 = contract24 / (rev24 / 12)
cover23 = contract23 / (rev23 / 12)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.6, 7.2),
                               gridspec_kw={"width_ratios": [1.0, 1.0],
                                            "wspace": 0.34})
fig.subplots_adjust(left=0.085, right=0.965, top=0.845, bottom=0.185)

# ── 左：合同负债两年 + 能覆盖几个月的收入 ──────────────────────────
x = [0, 1]
bars = ax1.bar(x, [contract23, contract24], width=0.44, color=C_BLUE, zorder=3)
for bar, v, cv in zip(bars, [contract23, contract24], [cover23, cover24]):
    cx = bar.get_x() + bar.get_width() / 2
    ax1.text(cx, v * 0.52, f"{v:,.2f}",
             ha="center", va="center", color="white", fontsize=14,
             weight="bold", zorder=5)
ax1.annotate("", xy=(0.90, contract24 + 16), xytext=(0.10, contract23 + 16),
             arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.8,
                             shrinkA=6, shrinkB=6,
                             connectionstyle="arc3,rad=-0.18"))
label(ax1, 0.5, 146, f"一年增加 {contract24 - contract23:,.2f} 亿元（{contract_yoy:+.1f}%）",
      fontsize=12.5, color=C_RED, weight="bold")
ax1.set_xticks(x)
ax1.set_xticklabels([f"2023 年末\n可覆盖 {cover23:.2f} 个月收入",
                     f"2024 年末\n可覆盖 {cover24:.2f} 个月收入"], fontsize=12.5)
ax1.set_ylim(0, 158)
ax1.set_xlim(-0.55, 1.55)
ax1.set_ylabel("合同负债（亿元）", fontsize=11.5)
ax1.set_title("合同负债：86.96 亿 → 120.73 亿", fontsize=13.5, pad=10)
clean_axes(ax1)

# ── 右：收入在跌，应收在缩，合同负债却在涨 ────────────────────────
ar24 = b["accounts_receivable"] / yi
ar23 = c23["accounts_receivable"] / yi
ar_yoy = (ar24 / ar23 - 1) * 100

items = [("合同负债", contract_yoy, C_ORANGE),
         ("营业收入", rev_yoy, C_GRAY),
         ("应收账款", ar_yoy, C_BLUE)]
names = [i[0] for i in items][::-1]
vals = [i[1] for i in items][::-1]
cols = [i[2] for i in items][::-1]
bars2 = ax2.barh(range(len(vals)), vals, color=cols, height=0.46, zorder=3)
ax2.set_yticks(range(len(vals)))
ax2.set_yticklabels(names, fontsize=13)
ax2.set_ylim(-0.65, 2.75)
ax2.set_xlim(-24, 52)
ax2.axvline(0, color="#888888", lw=1.0, zorder=2)
ax2.set_xlabel("2024 年同比增速（%）", fontsize=11.5)
ax2.set_title("收入在跌、应收在缩，只有合同负债在涨", fontsize=13.5, pad=10)
for bar, v in zip(bars2, vals):
    if v >= 0:
        ax2.text(v + 1.5, bar.get_y() + bar.get_height() / 2, f"{v:+.1f}%",
                 va="center", ha="left", fontsize=13, weight="bold",
                 color="#222222", zorder=6)
    else:
        ax2.text(v - 1.5, bar.get_y() + bar.get_height() / 2, f"{v:+.1f}%",
                 va="center", ha="right", fontsize=13, weight="bold",
                 color="#222222", zorder=6)
label(ax2, 14, -0.42,
      "应收在缩 = 不是靠赊销冲收入\n压货嫌疑降低，但要等 2025 一季报验证",
      fontsize=10.5, ha="center", va="center", color="#333333")
clean_axes(ax2)

fig.suptitle("收入下滑 8.24% 的一年，伊利合同负债反而涨了 38.8%",
             fontsize=15.5, weight="bold", y=0.955)
fig.text(0.085, 0.030,
         "数据来源：伊利股份 2024 年报 page_007、page_088、page_191。"
         "2023 年「预收款项 26.47 亿元」经附注七(37) 核实为股权转让款，与卖奶无关，未并入上图。",
         fontsize=9.5, color="#666666")

save(fig, "w05d22_contract_liability.png")
