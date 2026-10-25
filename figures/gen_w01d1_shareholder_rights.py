# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 1 周第 1 章配图：一股股票拆开看——三项权利，三个「每股」数字。

左：股东的三项权利（投票 / 分红 / 剩余索取）。
右：伊利 2024 年把归母净利润、归母权益、现金分红摊到 63.66 亿股上。
数字全部来自 data/yili2024.json 与年报 page_002、page_007。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, box, label, clean_axes,
    C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_PURPLE,
    F_BLUE, F_ORANGE, F_PURPLE,
)
from figures._data import load  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

d = load("yili2024")
shares = d["balance"]["share_capital"] / 1e8         # 63.66 亿股
equity_parent = d["balance"]["equity_parent"] / 1e8  # 531.80 亿元
eps = d["income"]["eps_basic"]                       # 1.33 元/股
bps = d["ratios"]["book_value_per_share"]            # 8.35 元/股
dps = 1.22                                           # 年报 page_002 每股派现
payout = 0.9140                                      # 年报 page_002 分红占归母净利

fig = plt.figure(figsize=(15.4, 7.6))
ax1 = fig.add_axes([0.025, 0.12, 0.38, 0.74])
ax2 = fig.add_axes([0.51, 0.17, 0.45, 0.66])
ax1.axis("off")

# ── 左：三项权利 ──────────────────────────────────────────────
ax1.set_xlim(0, 100)
ax1.set_ylim(0, 100)
ax1.text(50, 96, "买一股，买到的是三项权利", ha="center", va="center",
         fontsize=14.5, weight="bold", color="#1a1a1a")

box(ax1, 4, 68, 92, 17,
    "① 投票权（voting right）\n股东大会上选举董事、表决重大事项",
    fc=F_BLUE, ec=C_BLUE, fontsize=11.5)
box(ax1, 4, 45, 92, 17,
    "② 分红权（dividend right）\n公司决定分钱时，按股数分",
    fc=F_ORANGE, ec=C_ORANGE, fontsize=11.5)
box(ax1, 4, 22, 92, 17,
    "③ 剩余索取权（residual claim）\n还完债、交完税，剩下的归股东",
    fc=F_PURPLE, ec=C_PURPLE, fontsize=11.5)

label(ax1, 50, 10,
      "三项里最要紧的是顺序：前两项要等\n公司「有得给」，第三项决定\n「剩下的有多少」。",
      fontsize=10.5, color="#333333")

# ── 右：三个「每股」数字 ───────────────────────────────────────
names = ["每股净资产\n（归母权益 ÷ 总股本）",
         "每股收益\n（归母净利 ÷ 总股本）",
         "每股分红\n（2024 年度预案）"]
vals = [bps, eps, dps]
colors = [C_PURPLE, C_GREEN, C_ORANGE]

bars = ax2.barh(names, vals, color=colors, height=0.46, zorder=3)
ax2.invert_yaxis()
ax2.set_xlim(0, 10.3)
ax2.set_ylim(2.62, -0.62)
ax2.set_xlabel("元 / 股", fontsize=11.5)
ax2.set_title(f"摊到 {shares:.2f} 亿股上，一股各是多少", fontsize=13.5,
              weight="bold", loc="left", pad=14)
ax2.tick_params(axis="y", labelsize=10.5)
ax2.tick_params(axis="x", labelsize=10.5)
ax2.grid(axis="x", color="#e3e3e3", lw=0.9, zorder=0)
clean_axes(ax2)

for b, v in zip(bars, vals):
    y = b.get_y() + b.get_height() / 2
    label(ax2, v + 0.18, y, f"{v:.2f} 元", ha="left", va="center",
          fontsize=11.5, weight="bold", color="#222222")

np_parent = d["income"]["net_profit_parent"] / 1e8  # 84.53

fig.text(0.51, 0.048,
         f"每股收益 ＝ 归母净利 {np_parent:.2f} 亿元 ÷ {shares:.2f} 亿股 ＝ {eps:.2f} 元；"
         f"每股净资产 ＝ 归母权益 {equity_parent:.2f} 亿元 ÷ {shares:.2f} 亿股 ＝ {bps:.2f} 元；\n"
         f"每股分红 1.22 元（含税），合计约 77.26 亿元，占归母净利润 {payout * 100:.1f}%。",
         fontsize=10.0, color=C_GRAY, va="bottom")

save(fig, "w01d1_shareholder_rights.png")
