# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 2 周第 6 章配图：奶茶店开业三笔交易，怎么汇成一张「家底表」。

上半部分是三笔交易（每笔都同时动两个格子），下半部分是记完账后的左右两栏。
全部为教学示意数字（虚构奶茶店），不对应任何真实公司；真实公司数字见第 7 章起。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, fig_ax, box, label,
    C_BLUE, C_ORANGE, C_GREEN, C_PURPLE, C_GRAY,
    F_BLUE, F_ORANGE, F_PURPLE, F_GRAY,
)

fig, ax = fig_ax(13, 8.6, xlim=(0, 100), ylim=(0, 100))

# ── 标题 ────────────────────────────────────────────────────────────
ax.text(50, 96.2, "奶茶店开业三笔交易：每一笔都同时动两个格子",
        ha="center", va="center", fontsize=15.5, weight="bold", color="#1a1a1a")
ax.text(50, 91.2, "示意数字（虚构奶茶店，不对应任何真实公司）· 单位：万元",
        ha="center", va="center", fontsize=11, color=C_GRAY)

# ── 上半：三笔交易卡片 ──────────────────────────────────────────────
cards = [
    (3, "① 小满投入 20 万", "货币资金  ＋20", "所有者权益  ＋20",
     F_PURPLE, C_PURPLE),
    (36, "② 向银行借 40 万", "货币资金  ＋40", "短期借款  ＋40",
     F_ORANGE, C_ORANGE),
    (69, "③ 买设备装修 40 万", "固定资产  ＋40", "货币资金  −40",
     F_BLUE, C_BLUE),
]
for x, head, a, b, fc, ec in cards:
    box(ax, x, 72, 28, 13.5, "", fc=fc, ec=ec, lw=1.8)
    ax.text(x + 14, 81.6, head, ha="center", va="center",
            fontsize=11.5, weight="bold", color="#1a1a1a")
    ax.text(x + 14, 77.6, a, ha="center", va="center", fontsize=11, color=ec)
    ax.text(x + 14, 74.4, b, ha="center", va="center", fontsize=11, color=ec)

# ── 中间提示 ────────────────────────────────────────────────────────
ax.text(50, 66.4, "三笔记完，把每个格子剩下的余额抄到一张表上，就是「家底表」",
        ha="center", va="center", fontsize=11.5, color="#333333")

# ── 下半：左右两栏 ──────────────────────────────────────────────────
ROW_H = 8.0


def panel(x0, w, y_top, title, rows, ec, fc_head, last_ec=None):
    """画一个两列表格：左边科目名，右边金额。"""
    ax.add_patch(__import__("matplotlib").patches.Rectangle(
        (x0, y_top - 7), w, 7, facecolor=fc_head, edgecolor=ec, lw=1.6, zorder=3))
    ax.text(x0 + 2, y_top - 3.5, title, ha="left", va="center",
            fontsize=12, weight="bold", color=ec, zorder=5)
    for i, (name, val, strong) in enumerate(rows):
        y1 = y_top - 7 - i * ROW_H
        if strong:
            ax.add_patch(__import__("matplotlib").patches.Rectangle(
                (x0, y1 - ROW_H), w, ROW_H, facecolor=F_GRAY,
                edgecolor=ec, lw=1.4, zorder=3))
        else:
            ax.add_patch(__import__("matplotlib").patches.Rectangle(
                (x0, y1 - ROW_H), w, ROW_H, facecolor="white",
                edgecolor="#cccccc", lw=0.9, zorder=3))
        ax.text(x0 + 2, y1 - ROW_H / 2, name, ha="left", va="center",
                fontsize=12 if strong else 11.5,
                weight="bold" if strong else "normal",
                color="#1a1a1a" if not strong else ec, zorder=5)
        ax.text(x0 + w - 2, y1 - ROW_H / 2, val, ha="right", va="center",
                fontsize=12 if strong else 11.5,
                weight="bold" if strong else "normal",
                color="#1a1a1a" if not strong else ec, zorder=5)


panel(5, 41, 60, "资产（钱去哪儿了）", [
    ("货币资金", "20.0", False),
    ("设备与装修", "40.0", False),
    ("资产合计", "60.0", True),
], C_BLUE, F_BLUE)

panel(54, 41, 60, "负债 + 所有者权益（钱从哪儿来）", [
    ("银行借款", "40.0", False),
    ("小满投入", "20.0", False),
    ("合计", "60.0", True),
], C_PURPLE, F_PURPLE)

ax.text(50, 33.2, "=", ha="center", va="center", fontsize=30, weight="bold",
        color="#333333")
label(ax, 50, 26.4, "两边都是 60.0", color=C_GREEN, fontsize=10.5, weight="bold")

# ── 脚注 ────────────────────────────────────────────────────────────
ax.text(50, 15.0,
        "左边每一件东西，都能说清是「借来的」还是「自己的」；这就是资产负债表的分栏逻辑。",
        ha="center", va="center", fontsize=11.5, color="#333333")
ax.text(50, 7.6,
        "示意数字：一家虚构奶茶店开业当天的账；从第 7 章起换成伊利 2024 年报的真实数字。",
        ha="center", va="center", fontsize=10.5, color=C_GRAY)

save(fig, "w02d1_tea_shop_three_deals.png")
