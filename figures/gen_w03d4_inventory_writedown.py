# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 3 周第 4 章配图：伊利的存货与跌价准备。

左图：2023 / 2024 两年存货拆成「账面价值 + 跌价准备」，柱高就是账面余额；
右图：四类存货的跌价计提比例（跌价准备 ÷ 账面余额），看哪一类最容易坏。

口径：金额取自 data/yili2024_supplement.json 的 inventory 段（附注七(10)，page_164）；
跌价损失取自 data/yili2024.json 的 notes.inventory_writedown（page_211）。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_RED,
)
from figures._data import load  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as mpatches  # noqa: E402

d = load("yili2024")
sup = load("yili2024_supplement")["inventory"]
E = 1e8

net = {y: sup[y]["合计"]["账面价值"] / E for y in ("y2023", "y2024")}
prov = {y: sup[y]["合计"]["跌价准备"] / E for y in ("y2023", "y2024")}
gross = {y: sup[y]["合计"]["账面余额"] / E for y in ("y2023", "y2024")}
writedown = d["notes"]["inventory_writedown"] / E

fig, axes = plt.subplots(1, 2, figsize=(14.8, 7.0),
                         gridspec_kw={"width_ratios": [1.0, 1.18],
                                      "wspace": 0.32})

# ══════════════════ 左：两年存货 = 净值 + 跌价准备 ══════════════════
ax = axes[0]
xs = [0, 1]
labels = ["2023 年末", "2024 年末"]

for x, y in zip(xs, ("y2023", "y2024")):
    ax.bar(x, net[y], width=0.52, color=C_BLUE, edgecolor="white",
           linewidth=1.4, zorder=3)
    ax.bar(x, prov[y], width=0.52, bottom=net[y], color=C_RED,
           edgecolor="white", linewidth=1.4, zorder=3)
    ax.text(x, net[y] / 2, f"账面价值\n{net[y]:,.2f}", ha="center", va="center",
            fontsize=12.5, weight="bold", color="white", zorder=6)
    ax.text(x, net[y] + prov[y] / 2, f"跌价 {prov[y]:,.2f}", ha="center",
            va="center", fontsize=11, weight="bold", color="white", zorder=6)
    ax.text(x, gross[y] + 3.6, f"账面余额 {gross[y]:,.2f}",
            ha="center" if y == "y2023" else "left", va="bottom",
            fontsize=12.5, weight="bold", color="#1a1a1a", zorder=8)

ax.set_xlim(-0.62, 1.62)
ax.set_ylim(0, 202)
ax.set_xticks(xs)
ax.set_xticklabels(labels, fontsize=13, weight="bold")
ax.set_ylabel("金额（亿元）", fontsize=11.5)
ax.set_title(f"存货账面价值两年下降：{net['y2023']:,.2f} → {net['y2024']:,.2f} 亿元",
             fontsize=13.5, pad=16, weight="bold")
ax.grid(axis="y", color="#ececec", lw=0.8, zorder=0)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.text(0.5, 188,
        f"柱高 ＝ 账面余额；红色一段 ＝ 已计提的跌价准备\n"
        f"2024 年新计提的存货跌价损失 {writedown:,.2f} 亿元，直接进利润表",
        ha="center", va="center", fontsize=10.6,
        color="#333333", linespacing=1.8,
        bbox=dict(boxstyle="round,pad=0.42", fc="#fbeaea", ec=C_RED, lw=1.0))

handles = [
    mpatches.Patch(color=C_BLUE, label="账面价值（真正记在资产里的数）"),
    mpatches.Patch(color=C_RED, label="存货跌价准备（已经认掉的损失）"),
]
ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, -0.13),
          frameon=False, fontsize=10, ncol=1)

# ══════════════════ 右：四类存货的计提比例 ══════════════════
ax2 = axes[1]
cats = ["原材料", "库存商品", "半成品", "包装材料"]
rate23 = [sup["y2023"][c]["跌价准备"] / sup["y2023"][c]["账面余额"] * 100
          for c in cats]
rate24 = [sup["y2024"][c]["跌价准备"] / sup["y2024"][c]["账面余额"] * 100
          for c in cats]

ys = list(range(len(cats)))
h = 0.34
ax2.barh([y + h / 2 for y in ys], rate23, height=h, color="#b9cfe4",
         edgecolor="white", label="2023 年末")
ax2.barh([y - h / 2 for y in ys], rate24, height=h, color=C_BLUE,
         edgecolor="white", label="2024 年末")

ax2.set_yticks(ys)
ax2.set_yticklabels(cats, fontsize=12)
ax2.invert_yaxis()
ax2.set_xlim(0, 33)
ax2.set_xlabel("跌价准备 ÷ 账面余额（%）", fontsize=11.5)
ax2.set_title("半成品最需要盯：每 4 元账面值里就有 1 元被计提",
              fontsize=13.5, pad=14, weight="bold")
ax2.grid(axis="x", color="#ececec", lw=0.8, zorder=0)
ax2.set_axisbelow(True)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

for y, a, b in zip(ys, rate23, rate24):
    ax2.text(a + 0.45, y + h / 2, f"{a:.2f}%", va="center", ha="left",
             fontsize=10.5, color="#5a7590")
    ax2.text(b + 0.45, y - h / 2, f"{b:.2f}%", va="center", ha="left",
             fontsize=10.5, color=C_BLUE, weight="bold")

ax2.legend(loc="lower right", frameon=False, fontsize=10.5)

fig.text(0.99, 0.005,
         "数据来源：伊利 2024 年报 page_164、page_165、page_211",
         ha="right", va="bottom", fontsize=9.5, color=C_GRAY)

save(fig, "w03d4_inventory_writedown.png")
