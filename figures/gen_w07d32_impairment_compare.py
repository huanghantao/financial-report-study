# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 7 周第 32 章配图 1：减值两年对比 + 2024 年构成（伊利，亿元）。

左：2024 年减值构成（商誉 30.75、存货 12.27、信用 5.55、固定 3.67、工程物资 0.07）；
右：2024 年合计 52.31 = 与 2023 年持平部分的 16.86 + 多提的 35.45。
数字全部来自 data/yili2024.json 的 notes / income / core_earnings 段。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, C_BLUE, C_ORANGE, C_RED, C_BROWN, C_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
n = d["notes"]
inc = d["income"]

goodwill = n["goodwill_impairment_loss"] / 1e8       # 30.75
inventory = n["inventory_writedown"] / 1e8           # 12.27
fixed = n["fixed_asset_impairment"] / 1e8            # 3.67
material = n["asset_impairment_total"] / 1e8 - goodwill - inventory - fixed  # 0.07
credit = -inc["credit_impairment"] / 1e8             # 5.55
total_2024 = goodwill + inventory + fixed + material + credit
total_2023 = d["core_earnings"]["impairment_2023"] / 1e8
delta = total_2024 - total_2023

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(14.8, 7.4), constrained_layout=True,
    gridspec_kw={"width_ratios": [1.46, 1.0]},
)

# ── 左：2024 年构成 ─────────────────────────────────────────
rows = [
    ("商誉减值", goodwill, C_RED),
    ("存货跌价", inventory, C_ORANGE),
    ("信用减值", credit, C_BLUE),
    ("固定资产减值", fixed, C_BROWN),
    ("工程物资减值", material, C_GRAY),
]
ys = list(range(len(rows)))[::-1]
bars = ax1.barh(ys, [r[1] for r in rows], height=0.50,
                color=[r[2] for r in rows], zorder=3)
ax1.set_yticks(ys)
ax1.set_yticklabels([r[0] for r in rows], fontsize=11.8)
ax1.set_xlim(0, 39)
ax1.set_ylim(-0.75, 5.10)
ax1.set_xlabel("金额（亿元）", fontsize=11.3)
ax1.set_title("2024 年：52.31 亿元减值，商誉一项占 58.8%",
              fontsize=13.6, pad=14)

for b, r in zip(bars, rows):
    pct = r[1] / total_2024 * 100
    ax1.text(b.get_width() + 0.5, b.get_y() + b.get_height() / 2,
             f"{r[1]:,.2f} 亿元（{pct:.1f}%）", va="center", ha="left",
             fontsize=11.4, weight="bold", color="#333333", zorder=6)

ax1.text(0.0, 4.86,
         "前四项 = 资产减值损失 46.76 亿元；信用减值 5.55 亿元在利润表另一行",
         fontsize=10.4, color="#555555", ha="left", va="center")
clean_axes(ax1)

# ── 右：两年对比，2024 年拆成「持平」+「多提」─────────────
ax2.bar([0], [total_2023], width=0.46, color=C_GRAY, zorder=3)
ax2.bar([1], [total_2023], width=0.46, color=C_GRAY, zorder=3)
ax2.bar([1], [delta], bottom=[total_2023], width=0.46, color=C_RED,
        zorder=3)

ax2.set_xticks([0, 1])
ax2.set_xticklabels(["2023 年", "2024 年"], fontsize=12.4)
ax2.set_ylim(0, 67)
ax2.set_xlim(-0.66, 1.66)
ax2.set_ylabel("减值合计（亿元）", fontsize=11.3)
ax2.set_title("两年合计：从 16.86 涨到 52.31", fontsize=13.6, pad=14)

ax2.text(0, total_2023 + 1.4, f"{total_2023:,.2f}", ha="center", va="bottom",
         fontsize=12.2, weight="bold", color="#333333", zorder=6)
ax2.text(1, total_2023 + delta + 1.4, f"{total_2024:,.2f}", ha="center",
         va="bottom", fontsize=12.2, weight="bold", color="#333333", zorder=6)
ax2.text(1, total_2023 + delta / 2, f"多提\n{delta:,.2f}", ha="center",
         va="center", fontsize=11.6, weight="bold", color="white", zorder=6)
ax2.text(1, total_2023 / 2, f"{total_2023:,.2f}", ha="center", va="center",
         fontsize=11.0, color="white", weight="bold", zorder=6)

ax2.annotate("这 16.86 亿元\n两年都有，是「常态」",
             xy=(-0.235, total_2023 / 2), xytext=(-0.62, 34.0),
             fontsize=10.4, color="#444444", ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color=C_GRAY, lw=1.2,
                             shrinkA=2, shrinkB=3,
                             connectionstyle="arc3,rad=0.18"))
clean_axes(ax2)

fig.text(
    0.012, -0.040,
    "数据来源：伊利 2024 年报 page_211（资产减值损失、信用减值损失明细）、page_091（利润表）、"
    "data/yili2024.json 的 notes 与 core_earnings 段。\n"
    "2023 年细项：存货跌价 12.22 亿元、生产性生物资产 2.34 亿元、固定资产 0.69 亿元、信用减值 1.60 亿元，"
    "合计 16.86 亿元（page_211）。右图灰段为「与 2023 年持平」的部分，红段为「多提」的 35.45 亿元。",
    ha="left", va="top", fontsize=9.5, color=C_GRAY, linespacing=1.6,
)

save(fig, "w07d32_impairment_compare.png")
