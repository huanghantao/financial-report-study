# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 10 周第 46 章配图：价格围绕价值波动 + 安全边际带（概念图）。

这张图里没有真实数字：内在价值区间（假设 32~40 元）、价格路径、时间轴全部是示意，
用来讲清三个概念：内在价值是一个区间、价格围绕它波动、价格跌到区间下方才是安全边际。
真实的「价值锚」见 gen_w10d46_value_anchors.py。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as mpatches  # noqa: E402

from figures._common import (  # noqa: E402
    save, fig_ax, C_BLUE, C_GREEN, C_ORANGE, C_GRAY, F_GREEN, F_ORANGE,
)

fig, ax = fig_ax(12.6, 7.2, xlim=(0, 13.4), ylim=(0, 10))

x0, x1 = 0.8, 9.9
band_lo, band_hi = 5.2, 6.3

# 安全边际区：价值下限以下
ax.add_patch(mpatches.Rectangle((x0, 2.0), x1 - x0, band_lo - 2.0,
                                facecolor=F_ORANGE, edgecolor="none", zorder=1))
ax.plot([x0, x1], [band_lo, band_lo], color=C_ORANGE, lw=1.2, ls=(0, (5, 3)),
        zorder=2)
# 内在价值区间
ax.add_patch(mpatches.Rectangle((x0, band_lo), x1 - x0, band_hi - band_lo,
                                facecolor=F_GREEN, edgecolor=C_GREEN,
                                lw=1.4, zorder=2))

# 价格路径（示意）
t = np.linspace(0, 9.1, 600)
price = 5.35 + 2.05 * np.sin(0.75 * t + 0.2) + 0.32 * np.sin(1.9 * t)
ax.plot(x0 + t, price, color=C_BLUE, lw=2.6, zorder=4, solid_capstyle="round")

i_hi = int(np.argmax(price))
i_lo = int(np.argmin(price))
x_hi, y_hi = x0 + t[i_hi], price[i_hi]
x_lo, y_lo = x0 + t[i_lo], price[i_lo]

ax.scatter([x_hi], [y_hi], s=95, color=C_BLUE, zorder=6,
           edgecolor="white", linewidth=1.6)
ax.scatter([x_lo], [y_lo], s=95, color=C_BLUE, zorder=6,
           edgecolor="white", linewidth=1.6)

# 两个极端点的注释都放在左侧空白处，避免压住曲线和右下角
ax.annotate("市场先生兴奋：报价远高于价值\n（这时该做的不是买）",
            xy=(x_hi, y_hi), xytext=(3.15, 8.85),
            ha="left", va="center", fontsize=11.4, color="#222222", zorder=7,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=C_BLUE, lw=1.0),
            arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=1.3,
                            shrinkA=4, shrinkB=7, mutation_scale=14))
ax.annotate("市场先生沮丧：报价掉进安全边际区\n（这才是该翻开年报的时候）",
            xy=(x_lo, y_lo), xytext=(2.05, 2.45),
            ha="left", va="center", fontsize=11.4, color="#222222", zorder=7,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=C_ORANGE, lw=1.0),
            arrowprops=dict(arrowstyle="-|>", color=C_ORANGE, lw=1.3,
                            shrinkA=4, shrinkB=7, mutation_scale=14))

# 右侧标签：全部放在坐标区外
ax.text(10.6, (band_lo + band_hi) / 2, "内在价值区间\n假设 32~40 元\n（算出来的）",
        ha="left", va="center", fontsize=11.2, color="#1a6b1a", weight="bold",
        linespacing=1.6)
ax.text(10.6, 3.55, "安全边际区\n价格低于 32 元\n（等出来的）", ha="left",
        va="center", fontsize=11.2, color=C_ORANGE, weight="bold",
        linespacing=1.6)

# 时间箭头（右下角空白区）
ax.annotate("", xy=(12.85, 1.05), xytext=(10.6, 1.05),
            arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.5,
                            mutation_scale=14))
ax.text(10.6, 1.28, "时间（示意）", ha="left", va="bottom", fontsize=10.4,
        color=C_GRAY)

ax.text(0.8, 9.55, "价格围绕价值波动：只有跌进安全边际区，才值得出手",
        fontsize=15.5, weight="bold", ha="left", va="center", color="#111111")
ax.text(0.8, 0.25,
        "本图纵轴未按比例，价格路径数值与价值区间均为示意；真实的价值锚见下一张图。",
        fontsize=9.8, color=C_GRAY, ha="left", va="bottom")

save(fig, "w10d46_price_value_band.png")
