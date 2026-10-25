# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 1 周第 3 章配图：270 页年报的「章节—页码」地图。

横向条形从每章起始页延伸到下一章起始页；页数与占比标在条形右侧。
页码全部来自伊利 2024 年报 raw 原文（page_NNN.md 的 NNN）。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, clean_axes, C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_PURPLE, C_RED, C_GOLD,
)
import matplotlib.pyplot as plt  # noqa: E402

# (章节名, 起始页, 结束页)
blocks = [
    ("重要提示与释义", 2, 6),
    ("公司简介和主要财务指标", 7, 9),
    ("管理层讨论与分析（MD&A）", 10, 34),
    ("公司治理", 35, 49),
    ("环境与社会责任", 50, 60),
    ("重要事项", 61, 70),
    ("股份变动及股东情况", 71, 75),
    ("优先股 / 债券相关情况", 76, 82),
    ("审计报告", 83, 86),
    ("四张报表（合并 + 母公司）", 87, 102),
    ("财务报表附注（含会计政策）", 103, 270),
]

TOTAL = 270
colors = [C_GRAY, C_BLUE, C_ORANGE, C_GREEN, C_GOLD, C_RED, C_PURPLE,
          C_GRAY, C_RED, C_GREEN, C_BLUE]

fig, ax = plt.subplots(figsize=(13.8, 8.0))
ys = list(range(len(blocks)))[::-1]

for y, (name, start, end), c in zip(ys, blocks, colors):
    n = end - start + 1
    ax.barh(y, n, left=start - 1, height=0.5, color=c, alpha=0.92,
            edgecolor="white", lw=1.2, zorder=3)
    ax.text(end + 3.0, y, f"p{start}–{end}　{n} 页　{n / TOTAL * 100:.0f}%",
            ha="left", va="center", fontsize=10.4, color="#333333", zorder=6)

ax.set_yticks(ys)
ax.set_yticklabels([b[0] for b in blocks], fontsize=10.8)
ax.set_xlim(0, TOTAL + 78)
ax.set_ylim(-0.75, len(blocks) + 0.75)
ax.set_xticks([1, 50, 100, 150, 200, 250, 270])
ax.set_xlabel("年报页码（共 270 页）", fontsize=11.5)
ax.set_title("270 页里，真正的「账」只有 16 页，其余 168 页都在解释它",
             fontsize=14, weight="bold", loc="left", pad=30)
ax.tick_params(axis="x", labelsize=10.5)
ax.grid(axis="x", color="#e6e6e6", lw=0.9, zorder=0)
clean_axes(ax)

# 两个关键锚点：虚线 + 顶部错开的注释，互不遮挡
for page, note, ha, dx in [(87, "p87：三张表从这里开始", "right", -2.5),
                           (103, "p103：附注从这里开始", "left", 2.5)]:
    ax.axvline(page - 1, color=C_RED, lw=1.3, ls=(0, (4, 3)), zorder=2, alpha=0.6)
    ax.text(page - 1 + dx, len(blocks) + 0.30, note, ha=ha, va="center",
            fontsize=10.2, color=C_RED, weight="bold", zorder=7)

fig.text(0.99, 0.035,
         "注：页码为 raw 目录中 page_NNN.md 的编号；「四张报表」含合并与母公司两套，"
         "母公司表在 page_089–102。",
         ha="right", va="center", fontsize=9.6, color=C_GRAY)

fig.subplots_adjust(left=0.225, right=0.985, top=0.855, bottom=0.115)
save(fig, "w01d3_report_map.png")
