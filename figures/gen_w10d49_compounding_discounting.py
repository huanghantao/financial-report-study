# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 10 周第 49 章配图：复利曲线（左）与贴现示意（右）。

左右两张图用同一组示意参数：100 元、年化 10%、10 年。
左图把 100 元滚成 259.37 元；右图把 259.37 元按 10% 折回今天，得到 100 元。
这两个数字是教科书算例（示意），不是伊利数据。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, C_BLUE, C_ORANGE, C_GREEN, C_GRAY,
)

PV, RATE, YEARS = 100.0, 0.10, 10  # 示意算例
years = list(range(YEARS + 1))
fv = [PV * (1 + RATE) ** n for n in years]
end = fv[-1]

fig, axes = plt.subplots(1, 2, figsize=(14.2, 6.8), constrained_layout=True)

# ── 左：复利 ──────────────────────────────────────────────
ax = axes[0]
ax.bar(years, fv, color=[C_BLUE if n < YEARS else C_ORANGE for n in years],
       width=0.62, edgecolor="white", linewidth=1.0, zorder=3)
ax.plot(years, fv, color=C_ORANGE, lw=1.6, ls=(0, (4, 3)), zorder=4)
for n in (0, 5, 10):
    ax.text(n, fv[n] + 7.0, f"{fv[n]:,.2f}", ha="center", va="bottom",
            fontsize=11.2, weight="bold", color="#222222", zorder=6)
ax.set_ylim(0, 330)
ax.set_xlim(-0.7, 10.7)
ax.set_xticks(years)
ax.set_xlabel("年数（年）", fontsize=11.5)

ax.yaxis.set_label_coords(-0.105, 0.5)
ax.set_title("复利：100 元按 10% 滚 10 年，变成 259.37 元\n（纵轴单位：元）",
             fontsize=13.2, pad=12)
ax.text(0.03, 0.97,
        "FV = PV × (1 + r)$^n$\n100 × 1.10$^{10}$ = 259.37",
        transform=ax.transAxes, ha="left", va="top", fontsize=11.8,
        color="#222222", linespacing=1.8,
        bbox=dict(boxstyle="round,pad=0.42", fc="white", ec=C_BLUE, lw=1.0))
ax.text(0.98, 0.95, "10 年 2.59 倍\n按 72 法则，约 7.2 年翻一番",
        transform=ax.transAxes, ha="right", va="top", fontsize=10.4,
        color=C_ORANGE, linespacing=1.6,
        bbox=dict(boxstyle="round,pad=0.34", fc="white", ec=C_ORANGE, lw=0.9))
clean_axes(ax)

# ── 右：贴现 ──────────────────────────────────────────────
ax = axes[1]
pv_path = [end / (1 + RATE) ** n for n in years]
ax.fill_between(years, 0, pv_path, color="#eef7ee", zorder=1)
ax.plot(years, pv_path, color=C_GREEN, lw=2.6, zorder=4,
        marker="o", markersize=5.5, markerfacecolor="white",
        markeredgecolor=C_GREEN, markeredgewidth=1.6)
for n in (5, 10):
    ax.text(n, pv_path[n] + 8.0, f"{pv_path[n]:,.2f}", ha="center", va="bottom",
            fontsize=11.2, weight="bold", color="#1a6b1a", zorder=6)
ax.set_ylim(0, 330)
ax.set_xlim(-0.7, 10.7)
ax.set_xticks(years)
ax.set_xlabel("这笔钱距离今天还有几年（年）", fontsize=11.5)

ax.yaxis.set_label_coords(-0.115, 0.5)
ax.set_title("贴现：10 年后的 259.37 元，按 10% 折回今天只值 100 元\n（纵轴单位：元）",
             fontsize=13.2, pad=12)
ax.text(0.03, 0.97,
        "PV = FV ÷ (1 + r)$^n$\n259.37 ÷ 1.10$^{10}$ = 100.00",
        transform=ax.transAxes, ha="left", va="top", fontsize=11.8,
        color="#222222", linespacing=1.8,
        bbox=dict(boxstyle="round,pad=0.42", fc="white", ec=C_GREEN, lw=1.0))
ax.text(0.97, 0.10, "曲线越往右越低：同样的钱，越晚拿到越不值钱",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=10.4,
        color="#1a6b1a",
        bbox=dict(boxstyle="round,pad=0.34", fc="white", ec=C_GREEN, lw=0.9))
clean_axes(ax)

fig.text(0.008, -0.055,
         "示例参数：本金 100 元、年化收益率 10%、10 年，均为示意算例，与伊利无关。"
         "左图与右图是同一件事的两个方向：乘 (1 + r)$^n$ 是复利，除以 (1 + r)$^n$ 是贴现。"
         "注意两张图的横轴含义不同：左图是「过去滚了几年」，右图是「未来还有几年」。",
         ha="left", va="top", fontsize=9.4, color=C_GRAY, linespacing=1.6)

save(fig, "w10d49_compounding_discounting.png")
