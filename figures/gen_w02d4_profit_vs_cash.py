# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 2 周第 9 章配图：同一年、同一家公司，净利润 84.64 亿，经营现金流 217.40 亿。

两根柱：利润表算出的「账面利润」与现金流量表收到的「真金白银」，比值 2.57 倍。
数字全部来自 data/yili2024.json。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, bar_labels, label, C_BLUE, C_GREEN, C_GRAY, C_ORANGE,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
net_profit = d["income"]["net_profit"] / 1e8        # 84.64
ocf = d["cashflow"]["operating_net"] / 1e8          # 217.40
ratio = d["ratios"]["ocf_to_net_profit"]            # 2.5686
np_2023 = d["compare_2023"]["income"]["net_profit"] / 1e8       # 102.84
ocf_2023 = d["compare_2023"]["cashflow"]["operating_net"] / 1e8  # 182.90

fig, ax = plt.subplots(figsize=(12.2, 7.6))
fig.subplots_adjust(left=0.085, right=0.975, top=0.87, bottom=0.17)

vals = [net_profit, ocf]
bars = ax.bar([0, 1], vals, width=0.44, color=[C_BLUE, C_GREEN],
              edgecolor="white", lw=1.2, zorder=3)
ax.set_xticks([0, 1])
ax.set_xticklabels(["净利润\n（利润表算出来的账面利润）",
                    "经营活动现金流量净额\n（现金流量表真正收到的钱）"],
                   fontsize=12)
ax.set_ylabel("金额（亿元）", fontsize=12)
ax.set_ylim(0, 288)
ax.set_xlim(-0.62, 1.62)
ax.set_title("同一年、同一家公司：利润表说赚了 84.64 亿，现金流量表说收到 217.40 亿",
             fontsize=14.6, pad=16)
ax.grid(axis="y", color="#ebebeb", lw=0.9, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

bar_labels(ax, bars, vals, fmt=lambda v: f"{v:,.2f} 亿元", fontsize=12.6)

# 绿色柱内：把「2.57 倍」写在柱子里，白字，不压任何线条
ax.text(1.0, 108, f"是净利润的\n{ratio:.2f} 倍", ha="center", va="center",
        fontsize=13.4, color="white", weight="bold", linespacing=1.7, zorder=6)

# 两根柱顶之间：一条水平双箭头，标出差额
y_arrow = 255
ax.annotate("", xy=(0.94, y_arrow), xytext=(0.06, y_arrow),
            arrowprops=dict(arrowstyle="<|-|>", color=C_ORANGE, lw=1.9,
                            mutation_scale=15))
label(ax, 0.5, y_arrow + 11, f"两者的差：{ocf - net_profit:,.2f} 亿元", color=C_ORANGE,
      fontsize=12.2, weight="bold")

# 左侧柱子上方的空白：一句提示
label(ax, -0.02, 150,
      "钱比利润多 133 亿，\n不代表利润造假：\n折旧、减值不花现金，\n却已从利润里扣掉。",
      color="#333333", fontsize=10.6, ha="center")

fig.text(0.975, 0.045,
         f"2023 年同口径：净利润 {np_2023:,.2f} 亿元，经营现金流 {ocf_2023:,.2f} 亿元，"
         f"比值 {ocf_2023 / np_2023:.2f} 倍。净利润为合并报表净利润（含少数股东损益）。",
         ha="right", va="bottom", fontsize=9.4, color=C_GRAY)
fig.text(0.975, 0.013, "数据来源：伊利 2024 年报 page_092、page_094；单位：亿元",
         ha="right", va="bottom", fontsize=9.4, color=C_GRAY)

save(fig, "w02d4_profit_vs_cash.png")
