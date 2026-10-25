# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 3 周第 2 章核心配图：伊利 2023 → 2024 的「钱搬家」。

两组堆叠条，每组三段：货币资金 / 其他流动资产里的大额存单 / 其他非流动资产里的大额存单。
看完这张图，你会明白「货币资金少 179.68 亿」并不是钱没了，而是换了科目住。

口径：data/yili2024.json 的 balance.cash、notes.time_deposits_* 、
compare_2023.balance；2023 年「其他流动资产里的大额存单」原文为空（0）。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, label,
    C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_RED,
)
from figures._data import load  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as mpatches  # noqa: E402

d = load("yili2024")
sup = load("yili2024_supplement")
B = d["balance"]
C23 = d["compare_2023"]["balance"]
N = d["notes"]
E = 1e8

cash24 = B["cash"] / E
cash23 = C23["cash"] / E
dep_cur24 = N["time_deposits_in_other_current_assets"] / E
dep_cur23 = 0.0
dep_non24 = N["time_deposits_in_other_noncurrent_assets"] / E
# 2023 年其他非流动资产中的大额存单：page_188「期初余额」列，见 data/yili2024_supplement.json
dep_non23 = sup["other_noncurrent_breakdown"]["y2023"]["time_deposits"] / E

tot24 = cash24 + dep_cur24 + dep_non24
tot23 = cash23 + dep_cur23 + dep_non23
delta = tot24 - tot23

fig, ax = plt.subplots(figsize=(12.6, 8.2))

xs = [1.0, 2.6]
w = 0.78

segs = [
    ("货币资金", C_BLUE),
    ("其他流动资产里的大额存单及定期存款", C_GREEN),
    ("其他非流动资产里的大额存单及定期存款", C_ORANGE),
]
data = [
    (cash23, dep_cur23, dep_non23),
    (cash24, dep_cur24, dep_non24),
]

# 先把坐标范围定死，柱顶留白的比例才算得准
ax.set_xlim(0.2, 4.3)
ax.set_ylim(0, 880)
TOP_GAP = (880 - 0) * 0.022

for xi, (x, vals) in enumerate(zip(xs, data)):
    bottom = 0.0
    for (name, color), v in zip(segs, vals):
        if v <= 0:
            continue
        ax.bar(x, v, width=w, bottom=bottom, color=color,
               edgecolor="white", linewidth=1.6, zorder=3)
        if v > 60:
            ax.text(x, bottom + v / 2, f"{v:,.2f}", ha="center", va="center",
                    color="white", fontsize=13, weight="bold", zorder=6)
        else:
            ax.annotate(f"{v:,.2f}", xy=(x + w / 2, bottom + v / 2),
                        xytext=(x + w / 2 + 0.30, bottom + v / 2),
                        ha="left", va="center", fontsize=11.5,
                        color=color, weight="bold", zorder=6,
                        bbox=dict(boxstyle="round,pad=0.28", fc="white",
                                  ec=color, lw=0.9, alpha=0.95),
                        arrowprops=dict(arrowstyle="-", color=color, lw=0.9,
                                        shrinkA=2, shrinkB=2))
        bottom += v
    # 柱顶总量：固定在柱顶之上 TOP_GAP，zorder=8 压过柱体
    ax.text(x, bottom + TOP_GAP, f"{bottom:,.2f}", ha="center", va="bottom",
            fontsize=15, weight="bold", color="#1a1a1a", zorder=8)

ax.set_xticks(xs)
ax.set_xticklabels(["2023 年末", "2024 年末"], fontsize=13.5, weight="bold")
ax.set_ylabel("类现金金额（亿元）", fontsize=12)
ax.set_title(f"货币资金少了 {cash23 - cash24:,.2f} 亿，类现金反而多了 {delta:,.2f} 亿：\n"
             f"钱只是换了个科目住",
             fontsize=14.5, pad=16, weight="bold")
ax.grid(axis="y", color="#ececec", lw=0.8, zorder=0)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# 2023 年的水平参考线（不写字，避免和柱顶数字打架；含义由右侧「净增」箭头说明）
ax.axhline(tot23, color=C_GRAY, lw=1.2, ls=(0, (6, 4)), zorder=2)

# 总量变化箭头：从 2023 年水位指向 2024 年柱顶
ax.annotate("", xy=(3.42, tot24), xytext=(3.42, tot23),
            arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=2.4,
                            mutation_scale=22))
ax.text(3.56, tot24 + 26,
        f"类现金净增\n＋{delta:,.2f} 亿元", fontsize=12, color=C_RED,
        weight="bold", ha="left", va="bottom", linespacing=1.6,
        bbox=dict(boxstyle="round,pad=0.32", fc="white", ec=C_RED, lw=1.1))

# 结构变化说明
label(ax, 1.95, 800,
      f"货币资金 {cash23:,.2f} → {cash24:,.2f}（{cash24 - cash23:+,.2f}）\n"
      f"两张「存单」科目 {dep_cur23 + dep_non23:,.2f} → "
      f"{dep_cur24 + dep_non24:,.2f}（{dep_cur24 + dep_non24 - dep_cur23 - dep_non23:+,.2f}）",
      fontsize=11.2, color="#333333", ha="center", va="center")

handles = [mpatches.Patch(color=c, label=n) for n, c in segs]
ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.01, 1.0),
          frameon=False, fontsize=11, handlelength=1.6,
          title="钱存在哪个科目里", title_fontsize=11.5)

fig.text(0.99, 0.005,
         "数据来源：伊利 2024 年报 page_087、page_166、page_188",
         ha="right", va="bottom", fontsize=9.5, color=C_GRAY)

save(fig, "w03d2_cash_relocation.png")
