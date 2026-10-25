# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 2 周第 7 章配图：伊利 2024 年资产负债表的左右结构（真实数字）。

左柱是「钱去哪儿了」（资产），右柱是「钱从哪儿来」（负债 + 所有者权益）。
高度按金额等比缩放，两柱同高即恒等式成立。数字全部来自 data/yili2024.json。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.patches as mpatches  # noqa: E402

from figures._common import (  # noqa: E402
    save, fig_ax, label,
    C_BLUE, C_ORANGE, C_GREEN, C_PURPLE, C_GRAY, C_GOLD,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
b = d["balance"]

ca = b["total_current_assets"] / 1e8            # 666.19
nca = b["total_noncurrent_assets"] / 1e8        # 870.99
ta = b["total_assets"] / 1e8                    # 1,537.18
cl = b["total_current_liabilities"] / 1e8       # 899.25
ncl = b["total_noncurrent_liabilities"] / 1e8   # 67.86
tl = b["total_liabilities"] / 1e8               # 967.10
ep = b["equity_parent"] / 1e8                   # 531.80
mi = b["minority_interest"] / 1e8               # 38.28
te = b["total_equity"] / 1e8                    # 570.08

fig, ax = fig_ax(13.6, 9.4, xlim=(0, 100), ylim=(0, 100))

ax.text(50, 96.6, "伊利 2024 年末：左边 1,537.18 亿元，右边也是 1,537.18 亿元",
        ha="center", va="center", fontsize=15.5, weight="bold", color="#1a1a1a")
ax.text(50, 92.4,
        "柱高按金额等比缩放；左右两柱一样高，就是「资产 = 负债 + 所有者权益」",
        ha="center", va="center", fontsize=11.2, color=C_GRAY)

BASE = 19.0                 # 柱底 y
SCALE = 57.0 / ta           # 亿元 → 画布高度


def bar(x0, x1, segs, top_label):
    """从柱底向上堆叠 segs=[(名称, 金额, 颜色)]，返回柱顶 y。"""
    y = BASE
    for name, val, color in segs:
        h = val * SCALE
        ax.add_patch(mpatches.Rectangle((x0, y), x1 - x0, h, facecolor=color,
                                        edgecolor="white", lw=1.6, zorder=3))
        if h >= 6:
            ax.text((x0 + x1) / 2, y + h / 2,
                    f"{name}\n{val:,.2f} 亿元 · {val / ta * 100:.1f}%",
                    ha="center", va="center", fontsize=11.8, color="white",
                    weight="bold", linespacing=1.65, zorder=5)
        y += h
    ax.plot([x0 - 0.4, x1 + 0.4], [y + 0.4, y + 0.4], color="#333333",
            lw=2.4, zorder=4, solid_capstyle="butt")
    ax.text((x0 + x1) / 2, y + 2.6, top_label, ha="center", va="bottom",
            fontsize=12.2, weight="bold", color="#1a1a1a", zorder=5)
    return y


# ── 左柱：资产（下→上：流动资产、非流动资产）────────────────────────
LX0, LX1 = 8.0, 29.0
bar(LX0, LX1, [
    ("流动资产", ca, "#5b9bd5"),
    ("非流动资产", nca, C_BLUE),
], f"资产总计 {ta:,.2f} 亿元")
ax.text((LX0 + LX1) / 2, BASE - 5.0, "资产：钱去哪儿了",
        ha="center", va="top", fontsize=12.2, weight="bold", color=C_BLUE)

# ── 右柱：负债 + 所有者权益（下→上：流动负债、非流动负债、归母、少数）
RX0, RX1 = 62.0, 83.0
bar(RX0, RX1, [
    ("流动负债", cl, C_ORANGE),
    ("非流动负债", ncl, "#f5c08a"),
    ("归母所有者权益", ep, C_PURPLE),
    ("少数股东权益", mi, C_GOLD),
], f"负债和所有者权益总计 {ta:,.2f} 亿元")
ax.text((RX0 + RX1) / 2, BASE - 5.0, "负债 + 所有者权益：钱从哪儿来",
        ha="center", va="top", fontsize=12.2, weight="bold", color=C_ORANGE)

# 两个窄分段：标签放进中间的空白区，两行写法，避免标签过长
y_ncl = BASE + (cl + ncl / 2) * SCALE
y_mi = BASE + (cl + ncl + ep + mi / 2) * SCALE
label(ax, RX0 - 1.2, y_ncl, f"非流动负债\n{ncl:,.2f} 亿元", color="#b5651d",
      fontsize=10.6, ha="right")
ax.plot([RX0 - 1.0, RX0], [y_ncl, y_ncl], color="#b5651d", lw=1.0, zorder=4)

# 少数股东权益在最顶端，标签往下挪，用折线引到色块，避免撞上柱顶总计
y_mi_lab = y_mi - 4.2
label(ax, RX0 - 1.6, y_mi_lab, f"少数股东权益\n{mi:,.2f} 亿元", color="#8a6d1f",
      fontsize=10.6, ha="right")
ax.plot([RX0 - 1.4, RX0], [y_mi_lab + 0.6, y_mi], color="#8a6d1f", lw=1.0, zorder=4)

# ── 右侧小计括号 ────────────────────────────────────────────────────
BX = 85.6


def bracket(y_lo, y_hi, text, color):
    ax.plot([BX, BX], [y_lo, y_hi], color=color, lw=1.8, zorder=4)
    for yy in (y_lo, y_hi):
        ax.plot([BX - 1.3, BX], [yy, yy], color=color, lw=1.8, zorder=4)
    ax.text(BX + 1.6, (y_lo + y_hi) / 2, text, ha="left", va="center",
            fontsize=11, color=color, weight="bold", zorder=5, linespacing=1.6)


bracket(BASE, BASE + tl * SCALE,
        f"负债合计\n{tl:,.2f} 亿\n占 {tl / ta * 100:.1f}%", C_ORANGE)
bracket(BASE + tl * SCALE, BASE + ta * SCALE,
        f"所有者权益\n{te:,.2f} 亿\n占 {te / ta * 100:.1f}%", C_PURPLE)

# ── 中间的等号 ──────────────────────────────────────────────────────
ymid = BASE + ta * SCALE / 2
ax.text(44, ymid + 3.4, "=", ha="center", va="center", fontsize=32,
        weight="bold", color="#333333", zorder=5)
ax.text(44, ymid - 3.2, "两边永远相等", ha="center", va="top",
        fontsize=10.4, color=C_GREEN, weight="bold", zorder=5)

# ── 底部口径提示 ────────────────────────────────────────────────────
ax.text(50, 5.6,
        f"归母权益 {ep:,.2f} 亿 + 少数股东权益 {mi:,.2f} 亿 = 所有者权益 {te:,.2f} 亿；"
        f"流动负债 {cl:,.2f} 亿 + 非流动负债 {ncl:,.2f} 亿 = 负债 {tl:,.2f} 亿",
        ha="center", va="center", fontsize=10.8, color="#333333")
ax.text(99, 1.8, "数据来源：伊利 2024 年报 page_087、page_088；单位：亿元",
        ha="right", va="center", fontsize=9.6, color=C_GRAY)

save(fig, "w02d2_yili_balance_structure.png")
