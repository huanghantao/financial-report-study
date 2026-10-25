# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 8 周第 38 章配图 2：借款 2,188 亿、还款 2,163 亿，净融资只有 +25 亿。

左：2024 年取得借款收到的现金 2,188.31 亿元 vs 偿还债务支付的现金 2,162.98 亿元；
右：筹资活动净额 2023 年 +72.58 亿元、2024 年 -72.78 亿元。
数字全部来自 data/yili2024.json 的 cashflow 与 compare_2023.cashflow 段。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, bar_labels, label, clean_axes, C_BLUE, C_ORANGE, C_GREEN, C_RED,
    C_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
cf = d["cashflow"]
Y = lambda v: v / 1e8  # noqa: E731

borrow24 = Y(cf["borrowings_received"])
repay24 = Y(cf["borrowings_repaid"])
net_debt24 = borrow24 - repay24
fin24 = Y(cf["financing_net"])
fin23 = Y(d["compare_2023"]["cashflow"]["financing_net"])

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(14.6, 7.2), constrained_layout=True,
    gridspec_kw={"width_ratios": [1.25, 1.0]},
)

# ── 左：总额对比（只放 2024 年） ─────────────────────────
b1 = ax1.bar([0, 1], [borrow24, repay24], width=0.46,
             color=[C_BLUE, C_ORANGE], zorder=3)
ax1.set_ylim(0, 2700)
ax1.set_xlim(-0.72, 1.72)
ax1.set_xticks([0, 1])
ax1.set_xticklabels(["取得借款收到的现金", "偿还债务支付的现金"], fontsize=11.8)
ax1.set_ylabel("金额（亿元）", fontsize=11.8)
ax1.set_title("2024 年：借进来 2,188 亿，还出去 2,163 亿", fontsize=14, pad=10)
bar_labels(ax1, b1, [borrow24, repay24], fmt=lambda v: f"{v:,.2f}", fontsize=12.5)
label(ax1, 0.5, 2400, f"净融资额只有 {net_debt24:+,.2f} 亿元",
      fontsize=12.8, weight="bold", color=C_GREEN)
clean_axes(ax1)

# ── 右：筹资活动净额两年对比 ────────────────────────────
b2 = ax2.bar([0, 1], [fin23, fin24], width=0.46,
             color=[C_GREEN, C_RED], zorder=3)
ax2.set_ylim(-110, 110)
ax2.set_xlim(-0.72, 1.72)
ax2.set_xticks([0, 1])
ax2.set_xticklabels(["2023 年", "2024 年"], fontsize=12.5)
ax2.set_ylabel("筹资活动净额（亿元）", fontsize=11.8)
ax2.set_title("筹资活动净额：从净流入转为净流出", fontsize=14, pad=10)
ax2.axhline(0, color="#888888", lw=1.0, zorder=1)
for b, v in zip(b2, [fin23, fin24]):
    x = b.get_x() + b.get_width() / 2
    ax2.text(x, v + (5 if v >= 0 else -5), f"{v:+,.2f}",
             ha="center", va="bottom" if v >= 0 else "top",
             fontsize=12.5, weight="bold", color="#222222", zorder=6)
clean_axes(ax2)

fig.suptitle("借 2,188 亿、还 2,163 亿：不是危机，是资金池在滚动",
             fontsize=16.5, weight="bold", y=1.04)
fig.text(0.012, -0.048,
         f"数据来源：伊利 2024 年报 page_095。左图是「总额」，右图是「净额」。"
         f"总额 2,188 亿元看着吓人，但扣掉当年偿还的 2,163 亿元，净融资只有 {net_debt24:+,.2f} 亿元——"
         f"相当于用新债换旧债，规模几乎没变。",
         ha="left", va="top", fontsize=9.4, color=C_GRAY, linespacing=1.7)

save(fig, "w08d38_borrow_repay.png")
