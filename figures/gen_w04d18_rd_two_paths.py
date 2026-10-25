# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 4 周第 18 章配图：研发支出的两条路——费用化 vs 资本化（概念图）。

同一个「今年花了 8.70 亿元研发」的事实，走两条不同的会计路线，
会得到两张不同的利润表和两张不同的资产负债表。
左边的数字是伊利的真实选择：全部费用化，开发支出余额为 0。

伊利数字来自 data/yili2024.json（研发费用、净利润、无形资产）。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, fig_ax, box, arrow, label,
    C_BLUE, C_GREEN, C_ORANGE, C_GRAY,
    F_BLUE, F_GREEN, F_ORANGE, F_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
rd = d["income"]["rd_expenses"] / 1e8          # 8.70
npp = d["income"]["net_profit_parent"] / 1e8   # 84.53
rev = d["income"]["revenue"] / 1e8             # 1153.93
ia = d["balance"]["intangible_assets"] / 1e8   # 47.80

fig, ax = fig_ax(14.4, 9.0, xlim=(0, 100), ylim=(0, 100))

ax.text(50, 96.6, "同一笔 8.70 亿元研发支出，两条路走出两张报表",
        ha="center", va="center", fontsize=16.5, weight="bold", color="#1a1a1a")
ax.text(50, 91.6,
        "伊利选的是左边那条：全部计入当期费用，报表上不留「开发支出」余额",
        ha="center", va="center", fontsize=12.0, color=C_GRAY)

# 起点
box(ax, 30, 81.0, 40, 7.0,
    f"今年实际投入研发 {rd:,.2f} 亿元\n（钱已经花出去了，这点两条路一样）",
    fc=F_GRAY, ec=C_GRAY, fontsize=12.4)

arrow(ax, (39, 80.4), (24, 72.0), color=C_GREEN, lw=2.2)
arrow(ax, (61, 80.4), (76, 72.0), color=C_ORANGE, lw=2.2)

# 左路：费用化
box(ax, 2, 64.6, 46, 6.8, "路 A：全部费用化（伊利的选择）",
    fc=F_GREEN, ec=C_GREEN, fontsize=13.6, weight="bold")
box(ax, 2, 44.6, 46, 18.4,
    "利润表：研发费用 +8.70 亿元\n→ 当年利润立刻少 8.70 亿元\n\n"
    "资产负债表：无形资产不变\n不新增任何资产",
    fc="#ffffff", ec=C_GREEN, fontsize=11.8)
box(ax, 2, 31.4, 46, 10.6,
    "结果：利润更「难看」，资产更「瘦」\n但没有一个数字靠假设撑着",
    fc=F_GREEN, ec=C_GREEN, fontsize=11.8, weight="bold")

# 右路：资本化
box(ax, 52, 64.6, 46, 6.8, "路 B：符合条件的部分资本化",
    fc=F_ORANGE, ec=C_ORANGE, fontsize=13.6, weight="bold")
box(ax, 52, 44.6, 46, 18.4,
    "利润表：研发费用只记一部分\n→ 当年利润比路 A 好看\n\n"
    "资产负债表：差额挂成「开发支出」\n→ 将来转无形资产，逐年摊销",
    fc="#ffffff", ec=C_ORANGE, fontsize=11.8)
box(ax, 52, 31.4, 46, 10.6,
    "结果：利润更「漂亮」，资产更「胖」\n但多出来的资产靠一句话撑着：\n「符合资本化条件」",
    fc=F_ORANGE, ec=C_ORANGE, fontsize=11.8, weight="bold")

# 底部：这道选择题的实质
box(ax, 2, 16.0, 96, 11.6,
    "本质：资本化不是「多赚了钱」，只是把今天的费用推到未来几年。\n"
    "总费用一分不少，变的只是费用落在哪一年；而「哪一年算符合条件」，是管理层说了算。",
    fc=F_BLUE, ec=C_BLUE, fontsize=12.2)

label(ax, 25, 8.6,
      f"伊利 2024：研发费用 {rd:,.2f} 亿元，全部费用化；\n"
      f"无形资产 {ia:,.2f} 亿元中，内部研发形成的占比是 0",
      fontsize=10.9, color=C_GREEN)
label(ax, 75, 8.6,
      f"假如当年资本化一半（约 {rd/2:,.2f} 亿元），\n"
      f"归母净利润会从 {npp:,.2f} 亿变成约 {npp + rd/2:,.2f} 亿",
      fontsize=10.9, color=C_ORANGE)

ax.text(99.2, 1.6,
        f"数据来源：伊利 2024 年报 page_091（研发费用、净利润）、page_183（无形资产明细）、page_022（研发投入情况表）。"
        f"研发费用率仅 {rd/rev*100:.2f}%，是乳业这类快消公司的常态，不是「不重视研发」。",
        ha="right", va="center", fontsize=9.4, color=C_GRAY)

save(fig, "w04d18_rd_two_paths.png")
