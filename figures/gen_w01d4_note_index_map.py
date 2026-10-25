# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 1 周第 4 章配图：三张报表的行，怎么顺着「附注」列找到解释。

左列是报表上的行（带页码），中间是附注编号，右列是附注页码与那一页能读到什么。
所有编号与页码都来自伊利 2024 年报 raw 原文。
"""
import sys
import pathlib

import matplotlib.patches as mpatches  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, fig_ax, box, arrow, label,
    C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_PURPLE,
    F_BLUE, F_ORANGE, F_GREEN, F_GRAY, F_PURPLE,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
cash = d["balance"]["cash"] / 1e8
gw = d["balance"]["goodwill"] / 1e8
asset_imp = d["notes"]["asset_impairment_total"] / 1e8

fig, ax = fig_ax(14.0, 8.6, xlim=(0, 100), ylim=(0, 100))

ax.text(50, 96.5, "报表上「附注」那两个字，是通往另外 168 页的门",
        ha="center", va="center", fontsize=14.8, weight="bold", color="#1a1a1a")
ax.text(50, 91.8, "沿着它翻过去，你会看到同一个数字被拆开、被解释、被追溯",
        ha="center", va="center", fontsize=11.2, color=C_GRAY)

# ── 表头 ────────────────────────────────────────────────────
ax.text(2.0, 86.0, "报表上的行", ha="left", va="center",
        fontsize=11.2, weight="bold", color="#555555")
ax.text(45.0, 86.0, "附注编号", ha="center", va="center",
        fontsize=11.2, weight="bold", color="#555555")
ax.text(56.0, 86.0, "翻到哪一页 · 能读到什么", ha="left", va="center",
        fontsize=11.2, weight="bold", color="#555555")

# ── 六行映射 ────────────────────────────────────────────────
rows = [
    ("资产负债表 · 货币资金（p87）", f"{cash:,.2f} 亿", "七(1)", "p150", "库存现金、银行存款、其他货币资金的拆分", C_BLUE, F_BLUE),
    ("资产负债表 · 商誉（p87）", f"{gw:,.2f} 亿", "七(27)", "p184", "每个被收购公司的商誉原值、减值准备", C_BLUE, F_BLUE),
    ("资产负债表 · 其他非流动资产（p87）", "292.59 亿", "七(30)", "p188", "大额存单及定期存款 279.77 亿藏在这一行", C_BLUE, F_BLUE),
    ("资产负债表 · 合同负债（p88）", "120.73 亿", "七(38)", "p191", "预收经销商的货款，是「欠货」不是「欠钱」", C_BLUE, F_BLUE),
    ("利润表 · 营业收入（p91）", "1,153.93 亿", "七(61)", "p206", "按产品、按地区拆开的收入与成本", C_GREEN, F_GREEN),
    ("利润表 · 资产减值损失（p91）", f"−{asset_imp:,.2f} 亿", "七(73)", "p211", "商誉 30.75、存货 12.27、固定资产 3.67", C_GREEN, F_GREEN),
]

y = 78.2
for name, value, note_no, page, desc, c, fc in rows:
    ax.add_patch(mpatches.FancyBboxPatch(
        (1.6, y - 3.4), 40.0, 6.8, boxstyle="round,pad=0.02,rounding_size=0.3",
        fc=fc, ec=c, lw=1.2, zorder=3))
    ax.text(3.0, y, name, ha="left", va="center", fontsize=10.4, color="#222222")
    ax.text(40.0, y, value, ha="right", va="center", fontsize=10.4,
            color=c, weight="bold")

    arrow(ax, (42.0, y), (49.6, y), color=C_GRAY, lw=1.4, shrinkA=2, shrinkB=2)

    ax.text(52.4, y, note_no, ha="center", va="center", fontsize=11.2,
            color=C_PURPLE, weight="bold",
            bbox=dict(boxstyle="round,pad=0.35", fc=F_PURPLE, ec=C_PURPLE, lw=1.2))
    ax.text(57.6, y, f"{page}　{desc}", ha="left", va="center",
            fontsize=10.3, color="#333333")
    y -= 8.6

# ── 说明 ────────────────────────────────────────────────────
ax.plot([1.6, 98.4], [30.2, 30.2], color="#dddddd", lw=1.0, zorder=1)

box(ax, 2.0, 10.5, 46.0, 16.4,
    "「七」＝第十节财务报告里的第七部分：\n"
    "七、合并财务报表项目注释（起于 page_150）\n\n"
    "括号里的数字＝这一部分的第几项，1 到 82。",
    fc=F_PURPLE, ec=C_PURPLE, fontsize=10.8)

box(ax, 52.0, 10.5, 46.0, 16.4,
    "编号跟着报表顺序走，不是随手编的：\n"
    "资产 1–31　负债 32–52　权益 53–60\n"
    "利润表 61–78　现金流 79–80",
    fc=F_GRAY, ec=C_GRAY, fontsize=10.8)

label(ax, 50, 6.0,
      "所以顺序永远是：报表上看到不懂的一行 → 看「附注」列 → 翻到对应页码 → 读数字背后的解释。",
      fontsize=10.8, color="#333333")

ax.text(99, 1.0, "数据来源：伊利 2024 年报 page_087、page_088、page_091、page_150、page_184、page_188、page_191、page_206、page_211",
        ha="right", va="center", fontsize=8.8, color=C_GRAY)

save(fig, "w01d4_note_index_map.png")
