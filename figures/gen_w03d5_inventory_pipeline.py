# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 3 周第 4 章配图：存货在流水线上的四站与"退路"。

概念图，不取数。四站依次是原材料 / 在产品 / 半成品 / 库存商品，
每站标清三件事：待在哪、投料了没有、出事时还能怎么处理。
重点在两个伊利专属的注记：第 2 站在伊利账上叫"半成品"（连续生产、
不设半成品仓），第 3 站伊利根本没有。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, fig_ax, box, arrow,
    C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_RED,
    F_BLUE, F_ORANGE, F_RED,
)

fig, ax = fig_ax(13.2, 5.7, xlim=(0, 13.2), ylim=(1.55, 6.55))

W, H = 2.45, 2.20
Y0 = 3.02
xs = [0.18, 3.58, 6.98, 10.38]

# 四站：名称、待在哪、投料状态、退路（出事时还能怎么处理）
stations = [
    ("原材料", "原料仓", "未投料", "退路：能退、能转卖",
     F_BLUE, C_BLUE, C_GREEN),
    ("在产品", "车间里", "已投料，工序没走完", "退路：基本只能报废",
     F_RED, C_RED, C_RED),
    ("半成品", "半成品仓", "已验收，能单独计价", "退路：能卖给别的厂",
     "white", C_GRAY, C_ORANGE),
    ("库存商品", "成品仓", "全部完工，可发货", "退路：只能打折促销",
     F_ORANGE, C_ORANGE, C_ORANGE),
]

ax.text(6.6, 6.24, "一箱奶出厂前，要走完四站",
        ha="center", va="center", fontsize=17, weight="bold", color="#1a1a1a")
ax.text(6.6, 5.78, "四站的边界只看两件事：有没有投料、有没有入库并且能单独计价",
        ha="center", va="center", fontsize=12.5, color="#555555")

for x, (name, place, feed, exit_, fc, ec, tc) in zip(xs, stations):
    rect = box(ax, x, Y0, W, H, "", fc=fc, ec=ec, lw=1.9)
    if name == "半成品":
        rect.set_linestyle((0, (5, 4)))  # 虚线：伊利没有这一站

    cx = x + W / 2
    ax.text(cx, Y0 + H - 0.44, name, ha="center", va="center",
            fontsize=15, weight="bold",
            color=C_RED if name == "在产品" else "#1a1a1a", zorder=6)
    ax.text(cx, Y0 + H - 0.96, place, ha="center", va="center",
            fontsize=12.5, color="#444444", zorder=6)
    ax.text(cx, Y0 + H - 1.40, feed, ha="center", va="center",
            fontsize=11.8, color="#444444", zorder=6)
    ax.text(cx, Y0 + 0.36, exit_, ha="center", va="center",
            fontsize=12, weight="bold",
            color=C_RED if name == "在产品" else tc, zorder=6)

for i in range(3):
    arrow(ax, (xs[i] + W, Y0 + H / 2), (xs[i + 1], Y0 + H / 2),
          color=C_GRAY, lw=2.0)

# ── 伊利的两条注记 ────────────────────────────────────────────────
cx2 = xs[1] + W / 2   # 在产品
cx3 = xs[2] + W / 2   # 半成品

arrow(ax, (cx2, 2.48), (cx2, Y0 - 0.04), color=C_ORANGE, lw=1.6)
ax.text(cx2, 2.10, "伊利：这一格叫「半成品」", ha="center", va="center",
        fontsize=12, weight="bold", color=C_ORANGE)

arrow(ax, (cx3, Y0 - 0.04), (cx3, 2.48), color=C_GRAY, lw=1.4, ls=(0, (3, 3)))
ax.text(cx3, 2.10, "乳业连续生产，伊利不设这一站", ha="center", va="center",
        fontsize=12, color="#666666")

save(fig, "w03d5_inventory_pipeline.png")
