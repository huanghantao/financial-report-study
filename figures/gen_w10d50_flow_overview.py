# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 10 周第 50 章配图：十周流程总装图（从找年报到做决策）。

概念图：十个步骤分四段（找数据 / 拆三表 / 查质量 / 定价格），
每一步下面写「在哪几章学会」，最后用四条说明收束四段的含义。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, fig_ax, box, arrow,
    C_BLUE, C_GREEN, C_ORANGE, C_PURPLE,
    F_BLUE, F_GREEN, F_ORANGE, F_PURPLE,
)

fig, ax = fig_ax(13.6, 8.8, xlim=(0, 13.6), ylim=(0, 8.8))

stages = [
    ("① 找年报", "第 1~5 章", F_BLUE, C_BLUE),
    ("② 读三表", "第 2、6 章", F_BLUE, C_BLUE),
    ("③ 拆资产", "第 3~4 章", F_GREEN, C_GREEN),
    ("④ 拆负债", "第 5 章", F_GREEN, C_GREEN),
    ("⑤ 读利润", "第 6~7 章", F_GREEN, C_GREEN),
    ("⑥ 查现金", "第 8 章", F_GREEN, C_GREEN),
    ("⑦ 算比率", "第 9 章", F_ORANGE, C_ORANGE),
    ("⑧ 扫红旗", "第 9 章", F_ORANGE, C_ORANGE),
    ("⑨ 估值", "第 10 章", F_PURPLE, C_PURPLE),
    ("⑩ 决策", "第 10 章", F_PURPLE, C_PURPLE),
]

W, H = 2.05, 1.12
GAP_X = 0.48
X0 = 0.55
Y_ROW1, Y_ROW2 = 5.58, 3.62
PITCH = W + GAP_X

pos = {}
for i, (name, chap, fc, ec) in enumerate(stages):
    row, col = divmod(i, 5)
    x = X0 + col * PITCH
    y = Y_ROW1 if row == 0 else Y_ROW2
    box(ax, x, y, W, H, f"{name}\n{chap}", fc=fc, ec=ec, fontsize=11.4, lw=1.5)
    pos[i] = (x, y)

# 第一行 → 右
for i in range(4):
    x1 = pos[i][0] + W
    x2 = pos[i + 1][0]
    y = Y_ROW1 + H / 2
    arrow(ax, (x1 + 0.04, y), (x2 - 0.04, y), color="#9a9a9a", lw=1.6)

# 换行：从第 5 格底部下到两行之间的空隙，横穿到第 6 格上方，再向下进入
x5 = pos[4][0] + W / 2
x6 = pos[5][0] + W / 2
y_mid = (Y_ROW2 + H + Y_ROW1) / 2
ax.plot([x5, x5], [Y_ROW1, y_mid], color="#9a9a9a", lw=1.6,
        solid_capstyle="butt", zorder=2)
ax.plot([x5, x6], [y_mid, y_mid], color="#9a9a9a", lw=1.6,
        solid_capstyle="butt", zorder=2)
ax.annotate("", xy=(x6, Y_ROW2 + H + 0.04), xytext=(x6, y_mid + 0.02),
            arrowprops=dict(arrowstyle="-|>", color="#9a9a9a", lw=1.6,
                            mutation_scale=15, shrinkA=0, shrinkB=0))

# 第二行 → 右
for i in range(5, 9):
    x1 = pos[i][0] + W
    x2 = pos[i + 1][0]
    y = Y_ROW2 + H / 2
    arrow(ax, (x1 + 0.04, y), (x2 - 0.04, y), color="#9a9a9a", lw=1.6)

# 四段说明
notes = [
    (C_BLUE, "找数据：知道每一页在讲什么，比背下任何一个数字都重要。"),
    (C_GREEN, "拆三表：资产有没有水分、负债要不要付息、利润是谁赚的。"),
    (C_ORANGE, "查质量：现金流是验钞机，红旗清单是排雷器。"),
    (C_PURPLE, "定价格：三把尺子量同一家公司，重叠的那一段才是结论。"),
]
note_y = [2.80, 2.22, 1.64, 1.06]
for (col, txt), y in zip(notes, note_y):
    ax.plot([0.60, 0.90], [y + 0.14, y + 0.14], color=col, lw=3.4,
            solid_capstyle="round", zorder=3)
    ax.text(1.10, y + 0.14, txt, ha="left", va="center", fontsize=11.2,
            color="#333333", zorder=3)

ax.text(0.55, 8.35, "从一份年报到一个价格：十周学到的十个步骤",
        fontsize=16.5, weight="bold", ha="left", va="center", color="#111111")
ax.text(0.55, 7.78,
        "蓝色＝拿到数据，绿色＝拆开报表，橙色＝检验质量，紫色＝给公司定价。"
        "顺序不能乱：没有前八步，第九步就是猜。",
        fontsize=11.2, color="#555555", ha="left", va="center")

save(fig, "w10d50_flow_overview.png")
