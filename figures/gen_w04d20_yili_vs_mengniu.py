# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 4 周第 20 章配图 2：同一年的两笔并购减值，把两家公司的利润吃成什么样（亿元）。

伊利：减值合计 52.31 亿，归母净利润 84.53 亿 —— 减值相当于利润的 61.9%。
蒙牛：贝拉米一项减值影响 39.81 亿，归母净利润只剩 1.05 亿 —— 减值相当于利润的 38 倍。

蒙牛「减值影响」= 商誉减值 11.55 亿 + 无限年期商标减值 34.90 亿 − 递延税项拨回 6.63 亿，
是年报管理层讨论与分析里给出的「综合对本集团业绩影响」39.81 亿元口径；
净利润是含少数股东的口径，本图统一用「归母净利润」。

数字全部来自 data/yili2024.json 与 data/mengniu2024.json。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, bar_labels, label, clean_axes, C_BLUE, C_RED, C_GREEN, C_GRAY,
)
from figures._data import load  # noqa: E402

y = load("yili2024")
m = load("mengniu2024")

y_np = y["income"]["net_profit_parent"] / 1e8          # 84.53
y_imp = ((y["notes"]["asset_impairment_total"]
          - y["income"]["credit_impairment"]) / 1e8)   # 52.31
m_np = m["income"]["net_profit_parent"] / 1e8          # 1.05
m_imp = m["goodwill_detail"]["bellamy"]["impairment_2024"]["total_impact"] / 1e8  # 39.81

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(15.0, 7.4), constrained_layout=True,
    gridspec_kw={"width_ratios": [1.0, 1.15]},
)

# ── 左：两家并排（注意蒙牛利润只有一根牙签） ─────────────────────
xs = [0, 1]
w = 0.30
b1 = ax1.bar([x - w / 2 - 0.01 for x in xs], [y_np, m_np], width=w,
             color=C_BLUE, label="归母净利润", zorder=3)
b2 = ax1.bar([x + w / 2 + 0.01 for x in xs], [y_imp, m_imp], width=w,
             color=C_RED, label="当年减值金额", zorder=3)
ax1.set_xticks(xs)
ax1.set_xticklabels(["伊利股份\n（A 股）", "蒙牛乳业\n（H 股）"], fontsize=12.2)
ax1.set_ylim(0, 108)
ax1.set_ylabel("金额（亿元）", fontsize=11.5)
ax1.set_title("蒙牛：39.81 亿减值 vs 1.05 亿利润", fontsize=13.4, pad=26, loc="left")
bar_labels(ax1, b1, [y_np, m_np], fmt=lambda v: f"{v:,.2f}", fontsize=11.4, inside=False)
bar_labels(ax1, b2, [y_imp, m_imp], fmt=lambda v: f"{v:,.2f}", fontsize=11.4)
ax1.legend(loc="upper left", bbox_to_anchor=(0.0, 1.16), ncol=2,
           frameon=False, fontsize=11)
label(ax1, 1.02, 60,
      "利润几乎被减值抹平：\n1.05 亿元还不到减值的 3%",
      fontsize=10.8, color=C_RED, ha="center")
clean_axes(ax1)

# ── 右：减值 ÷ 利润 的倍数 ───────────────────────────────────────
names = ["伊利\n52.31 ÷ 84.53", "蒙牛\n39.81 ÷ 1.05"]
vals = [y_imp / y_np, m_imp / m_np]
bars = ax2.barh([1, 0], vals, height=0.42, color=[C_BLUE, C_RED], zorder=3)
ax2.set_yticks([1, 0])
ax2.set_yticklabels(names, fontsize=11.6)
ax2.set_xlim(0, 40)
ax2.set_ylim(-0.62, 1.55)
ax2.set_xlabel("减值 ÷ 归母净利润（倍）", fontsize=11.5)
ax2.set_title("减值相当于几倍利润：伊利 0.62 倍，蒙牛约 38 倍", fontsize=13.4, pad=26, loc="left")
for b, v in zip(bars, vals):
    ax2.text(b.get_width() + 0.55, b.get_y() + b.get_height() / 2,
             f"{v:.2f} 倍", va="center", ha="left",
             fontsize=12.4, weight="bold", color="#333333")
ax2.text(4.0, 1.30, "0.62 倍 —— 还留得住六成利润", fontsize=10.8, color=C_BLUE, va="center")
clean_axes(ax2)

fig.text(0.012, -0.030,
         "数据来源：伊利 page_211、page_091；蒙牛 2024 年报 page_045、page_140。\n"
         "伊利减值 = 资产减值损失 46.76 亿 + 信用减值损失 5.55 亿；"
         "蒙牛为贝拉米商誉减值 11.55 亿 + 商标减值 34.90 亿 − 递延税项拨回 6.63 亿 = 39.81 亿的合并影响口径。",
         ha="left", va="top", fontsize=9.6, color=C_GRAY, linespacing=1.6)

save(fig, "w04d20_yili_vs_mengniu.png")
