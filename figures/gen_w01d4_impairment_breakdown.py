# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 1 周第 4 章配图：报表上的一个总数，在附注里被拆成几块。

以伊利 2024 年「资产减值损失 −46.76 亿元」为例：
利润表 page_091 只给一个数，附注七(73) page_211 才说清每一块是什么。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.patches as mpatches  # noqa: E402

from figures._common import (  # noqa: E402
    save, fig_ax, box, arrow, label,
    C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_RED,
    F_BLUE, F_GRAY, F_RED,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
total = d["notes"]["asset_impairment_total"] / 1e8   # 46.76
gw = d["notes"]["goodwill_impairment_loss"] / 1e8   # 30.75
inv = d["notes"]["inventory_writedown"] / 1e8       # 12.27
fa = d["notes"]["fixed_asset_impairment"] / 1e8     # 3.67
other = total - gw - inv - fa                       # 约 0.07

fig, ax = fig_ax(13.8, 8.4, xlim=(0, 100), ylim=(0, 100))

ax.text(50, 96.0, "利润表给你一个 −46.76 亿，附注才告诉你这 46.76 亿是什么",
        ha="center", va="center", fontsize=14.8, weight="bold", color="#1a1a1a")
ax.text(50, 91.4, "同一个数字，两处出现：一处是结论，一处是解释。读财报的功夫，大半花在后者。",
        ha="center", va="center", fontsize=11.2, color=C_GRAY)

# ── 左：利润表那一行 ────────────────────────────────────────
box(ax, 3.0, 53.0, 32.0, 29.0, "", fc=F_RED, ec=C_RED, lw=1.8)
ax.text(19.0, 78.2, "利润表（page_091）", ha="center", va="center",
        fontsize=11.6, weight="bold", color=C_RED)
ax.text(19.0, 71.4, "资产减值损失", ha="center", va="center",
        fontsize=11.2, color="#333333")
ax.text(19.0, 63.2, f"−{total:,.2f} 亿元", ha="center", va="center",
        fontsize=16.0, weight="bold", color=C_RED)
ax.text(19.0, 56.6, "附注列写着：七(73)", ha="center", va="center",
        fontsize=10.2, color=C_GRAY)

arrow(ax, (35.8, 67.5), (43.8, 67.5), color=C_GRAY, lw=2.4)
label(ax, 39.8, 72.2, "顺着\n七(73) 翻", fontsize=9.8, color=C_GRAY)

# ── 右：附注拆解 ────────────────────────────────────────────
box(ax, 44.6, 53.0, 52.4, 29.0, "", fc=F_GRAY, ec=C_GRAY, lw=1.6)
ax.text(70.8, 78.4, "附注七(73)（page_211）", ha="center", va="center",
        fontsize=11.4, weight="bold", color="#333333")

parts = [
    ("商誉减值损失", gw, C_RED),
    ("存货跌价损失", inv, C_ORANGE),
    ("固定资产减值损失", fa, C_GREEN),
    ("工程物资减值损失", other, C_GRAY),
]
y = 72.6
for name, v, c in parts:
    ax.plot([47.2, 48.6], [y, y], color=c, lw=6, solid_capstyle="round", zorder=4)
    ax.text(49.6, y, name, ha="left", va="center", fontsize=10.5, color="#333333")
    ax.text(94.4, y, f"{v:,.2f} 亿元", ha="right", va="center",
            fontsize=10.8, color=c, weight="bold")
    y -= 5.2

# ── 下半：100% 堆叠条 ───────────────────────────────────────
ax.text(50, 45.5, "按金额占比看：一块商誉减值，就占了三分之二",
        ha="center", va="center", fontsize=12.2, weight="bold", color="#1a1a1a")

bar_y, bar_h = 35.5, 6.4
x0, width = 4.0, 90.0
cur = x0
for name, v, c in parts:
    w = v / total * width
    ax.add_patch(mpatches.Rectangle((cur, bar_y), w, bar_h, fc=c,
                                    ec="white", lw=1.4, zorder=3))
    if w > 8:
        ax.text(cur + w / 2, bar_y + bar_h / 2, f"{v / total * 100:.0f}%",
                ha="center", va="center", fontsize=11.0, color="white",
                weight="bold", zorder=5)
    cur += w

label(ax, 50, bar_y - 5.8,
      f"占比：商誉 {gw / total * 100:.0f}%　·　存货 {inv / total * 100:.0f}%　·　"
      f"固定资产 {fa / total * 100:.0f}%　·　工程物资不足 1%",
      fontsize=10.4, color="#333333")

label(ax, 50, 23.6,
      f"四块相加：{gw:,.2f} + {inv:,.2f} + {fa:,.2f} + {other:,.2f} = {total:,.2f} 亿元，与利润表那一行完全对上。",
      fontsize=10.8, color="#333333")

box(ax, 6, 5.4, 88, 11.4,
    "为什么要拆？「商誉减值 30.75 亿」是一次性的、不耗现金的；「存货跌价 12.27 亿」跟真实经营有关。\n"
    "混在一个 46.76 里，你没法判断明年还会不会再来一次。",
    fc=F_BLUE, ec=C_BLUE, fontsize=10.8)

ax.text(99, 1.0, "数据来源：伊利 2024 年报 page_091（利润表）、page_211（附注七(73)）",
        ha="right", va="center", fontsize=9.3, color=C_GRAY)

save(fig, "w01d4_impairment_breakdown.png")
