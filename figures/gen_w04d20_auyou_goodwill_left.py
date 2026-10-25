# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 4 周第 20 章配图 3：澳优这笔商誉还剩多少（伊利，亿元）。

左：澳优商誉原值 51.92 亿元，已被减值 30.37 亿元（58.5%），只剩 21.55 亿元。
右：全公司商誉净值 23.37 亿元里，澳优占 92.2%，其余六家合计 1.82 亿元。

口径：
- 澳优原值、本期减值取自附注七(27) 商誉原值表与减值准备表（page_184）；
- 澳优剩余 = 原值 − 已计提减值（澳优期初减值准备为 0，本期计提就是累计数）；
- 「其余六家 1.82 亿」= 全公司商誉净值 23.37 亿 − 澳优 21.55 亿，是倒算的差额项。
数字全部来自 data/yili2024.json。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, label, clean_axes, C_BLUE, C_ORANGE, C_RED, C_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
g = d["goodwill_detail"]
auyou = g["by_entity"]["澳优乳业股份有限公司"]
auyou_gross = auyou["gross_end"] / 1e8            # 51.92
auyou_imp = auyou["impairment_added"] / 1e8       # 30.37
auyou_net = auyou_gross - auyou_imp                 # 21.55
net_total = d["balance"]["goodwill"] / 1e8        # 23.37
others = net_total - auyou_net                     # 1.82（倒算）

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.6, 6.8),
                               constrained_layout=True)

# ── 左：澳优原值 = 已减值 + 剩余 ──────────────────────────────────
ax1.barh([0], [auyou_imp], height=0.42, color=C_RED, zorder=3)
ax1.barh([0], [auyou_net], left=[auyou_imp], height=0.42,
         color=C_BLUE, zorder=3)
ax1.set_yticks([])
ax1.set_xlim(0, 66)
ax1.set_ylim(-0.95, 1.15)
ax1.set_xlabel("金额（亿元）", fontsize=11.5)
ax1.set_title(f"澳优商誉原值 {auyou_gross:,.2f} 亿元，已提减值 {auyou_imp/auyou_gross*100:.1f}%",
              fontsize=13.2, pad=14)

ax1.text(auyou_imp / 2, 0.0,
         f"已提减值\n{auyou_imp:,.2f} 亿（{auyou_imp/auyou_gross*100:.1f}%）",
         ha="center", va="center", color="white", fontsize=11.8,
         weight="bold", zorder=6)
ax1.text(auyou_imp + auyou_net / 2, 0.0,
         f"剩余净值\n{auyou_net:,.2f} 亿（{auyou_net/auyou_gross*100:.1f}%）",
         ha="center", va="center", color="white", fontsize=11.8,
         weight="bold", zorder=6)

ax1.annotate("", xy=(auyou_gross, 0.40), xytext=(0, 0.40),
             arrowprops=dict(arrowstyle="<|-|>", color=C_GRAY, lw=1.4,
                             shrinkA=0, shrinkB=0))
ax1.text(auyou_gross / 2, 0.50, f"原值 {auyou_gross:,.2f} 亿元",
         ha="center", va="bottom", fontsize=11.2, color="#333333")

label(ax1, 33.0, -0.62,
      "减值准备一旦计提，中国准则下不允许转回；\n"
      "剩下的 21.55 亿元往后每年仍要做减值测试",
      fontsize=11.0, color="#333333", ha="center")
clean_axes(ax1)

# ── 右：全公司商誉净值构成 ───────────────────────────────────────
ax2.barh([0], [auyou_net], height=0.42, color=C_BLUE, zorder=3)
ax2.barh([0], [others], left=[auyou_net], height=0.42,
         color=C_ORANGE, zorder=3)
ax2.set_yticks([])
ax2.set_xlim(0, 30)
ax2.set_ylim(-0.95, 1.15)
ax2.set_xlabel("金额（亿元）", fontsize=11.5)
ax2.set_title(f"伊利商誉净值 {net_total:,.2f} 亿元，澳优一家占 {auyou_net/net_total*100:.1f}%",
              fontsize=13.2, pad=14)

ax2.text(auyou_net / 2, 0.0,
         f"澳优 {auyou_net:,.2f} 亿（{auyou_net/net_total*100:.1f}%）",
         ha="center", va="center", color="white", fontsize=12.0,
         weight="bold", zorder=6)
ax2.annotate(f"其余六家 {others:,.2f} 亿（{others/net_total*100:.1f}%）",
             xy=(auyou_net + others / 2, 0.24), xytext=(auyou_net - 3.2, 0.72),
             ha="center", va="bottom", fontsize=10.8, color=C_ORANGE,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_ORANGE, lw=0.9),
             arrowprops=dict(arrowstyle="-", color=C_ORANGE, lw=1.0,
                             shrinkA=2, shrinkB=2))

label(ax2, 15.0, -0.62,
      "泰国 Chomthana 3.12 亿、新西兰 Westland 1.66 亿等；\n"
      "阿尔山、Oceania、康益佳三家商誉已全额提完减值",
      fontsize=11.0, color="#333333", ha="center")
clean_axes(ax2)

fig.text(0.012, -0.048,
         "数据来源：伊利 2024 年报 page_184（附注七(27) 商誉原值表、商誉减值准备表）、page_087（商誉净值）。\n"
         "左图「已提减值」用本期计提数（澳优期初减值准备为 0，本期计提即为累计数）；"
         "右图「其余六家」为倒算差额，四舍五入到 0.01 可能有尾差。",
         ha="left", va="top", fontsize=9.6, color=C_GRAY, linespacing=1.6)

save(fig, "w04d20_auyou_goodwill_left.png")
