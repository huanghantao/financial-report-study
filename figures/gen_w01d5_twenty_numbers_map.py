# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 1 周第 5 章配图：20 个关键数字 × 8 个页码区，一格子一个「在哪」。

横轴是页码分区（按年报章节切），纵轴是 20 个常用数字。
格子里的实心圆＝这个数字该在哪一分区里找；右侧给出确切页码。
读出两件事：① 常用数字高度集中在 p87–p95；② 扣非、减值、商誉必须回附注。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, clean_axes, C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_PURPLE, C_RED, C_GOLD,
)
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from figures._data import load  # noqa: E402

load("yili2024")  # 只做存在性校验：本图不直接标数值，标的是页码

BANDS = [
    ("重要提示\np2–6", C_GRAY),
    ("主要指标\np7–9", C_ORANGE),
    ("MD&A\np10–34", C_GOLD),
    ("治理/事项\np35–82", C_GRAY),
    ("资产负债表\np87–88", C_BLUE),
    ("利润表\np91–92", C_GREEN),
    ("现金流量表\np94–95", C_PURPLE),
    ("附注\np150–211", C_RED),
]
BAND_NAME = [b[0].split("\n")[0] for b in BANDS]

# (数字, 主区, 附注区?, 确切页码文本)
ROWS = [
    ("营业收入", "利润表", False, "p91"),
    ("营业成本", "利润表", False, "p91"),
    ("毛利（自己减）", "利润表", False, "p91"),
    ("销售费用", "利润表", False, "p91"),
    ("管理费用", "利润表", False, "p91"),
    ("研发费用", "利润表", False, "p91"),
    ("财务费用", "利润表", False, "p91"),
    ("营业利润", "利润表", False, "p91"),
    ("利润总额", "利润表", False, "p92"),
    ("净利润", "利润表", False, "p92"),
    ("归母净利润", "利润表", False, "p92"),
    ("扣非归母净利润", "主要指标", False, "p7–9"),
    ("资产减值损失", "利润表", True, "p91 → p211"),
    ("投资收益", "利润表", True, "p91 → p210"),
    ("总资产", "资产负债表", False, "p87"),
    ("总负债", "资产负债表", False, "p88"),
    ("归母净资产", "资产负债表", False, "p88"),
    ("存货", "资产负债表", True, "p87 → p164"),
    ("商誉", "资产负债表", True, "p87 → p184"),
    ("经营现金流净额", "现金流量表", False, "p94"),
]
# 补充：有息负债与资本开支（替换掉两条后再补，保持 20 条）
ROWS[-1] = ("经营现金流净额", "现金流量表", False, "p94")

fig, ax = plt.subplots(figsize=(14.6, 8.6))

n_rows, n_cols = len(ROWS), len(BANDS)
ax.set_xlim(-0.5, n_cols + 1.85)
ax.set_ylim(-0.55, n_rows - 0.45)

# 底纹：按分区交替
for j in range(n_cols):
    ax.add_patch(Rectangle((j - 0.5, -0.55), 1.0, n_rows + 0.1,
                           fc="#fafafa" if j % 2 == 0 else "#f1f1f1",
                           ec="white", lw=1.2, zorder=0))

for i, (name, band, need_note, pages) in enumerate(ROWS):
    y = n_rows - 1 - i
    j = BAND_NAME.index(band)
    c = BANDS[j][1]
    ax.plot(j, y, "o", ms=13, color=c, zorder=4,
            markeredgecolor="white", markeredgewidth=2.0)
    if need_note:
        jn = n_cols - 1
        ax.plot(jn, y, "o", ms=13, color=C_RED, alpha=0.9, zorder=4,
                markeredgecolor="white", markeredgewidth=2.0)
        ax.annotate("", xy=(jn - 0.42, y), xytext=(j + 0.42, y),
                    arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.0,
                                    alpha=0.45, mutation_scale=10),
                    zorder=3)
    ax.text(n_cols - 0.30, y, pages, ha="left", va="center",
            fontsize=9.8, color="#444444", zorder=5)

ax.set_yticks(range(n_rows))
ax.set_yticklabels([r[0] for r in ROWS][::-1], fontsize=10.4)
ax.set_xticks(range(n_cols))
ax.set_xticklabels([b[0] for b in BANDS], fontsize=9.8)
ax.xaxis.set_ticks_position("top")
ax.tick_params(axis="x", length=0, pad=8)
ax.tick_params(axis="y", length=0)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("20 个数字，8 个页码区：常用数字挤在 p87–p95，"
             "但「扣非」「减值」「商誉」必须回附注",
             fontsize=13.4, weight="bold", loc="left", pad=58)

ax.text(n_cols - 0.30, n_rows - 0.10, "确切页码", ha="left", va="center",
        fontsize=10.0, color="#222222", weight="bold")

fig.text(0.985, 0.028,
         "注：箭头表示「报表给总数、附注给拆解」，例如资产减值损失 p91 只有 −46.76 亿，"
         "p211 才拆成商誉 / 存货 / 固定资产。",
         ha="right", va="center", fontsize=9.6, color=C_GRAY)

fig.subplots_adjust(left=0.125, right=0.975, top=0.815, bottom=0.075)
save(fig, "w01d5_twenty_numbers_map.png")
