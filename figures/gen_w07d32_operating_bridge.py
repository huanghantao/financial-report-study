# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 7 周第 32 章配图 2：营业利润少掉的 16.92 亿元，是怎么发生的（伊利，亿元）。

2023 年营业利润 118.73
  减值多提            -35.45
  投资收益增加（含卖子公司 +24.48）
  其他经营变化         -5.95
= 2024 年营业利润 101.82
数字全部来自 data/yili2024.json 的 income / compare_2023 / core_earnings 段。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, waterfall, C_GRAY, C_GREEN, C_RED, C_BLUE,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
inc = d["income"]
old = d["compare_2023"]["income"]
ce = d["core_earnings"]

op24 = inc["operating_profit"] / 1e8
op23 = old["operating_profit"] / 1e8
imp24 = ce["impairment_2024"] / 1e8
imp23 = ce["impairment_2023"] / 1e8
d_imp = imp24 - imp23
d_inv = (inc["investment_income"] - old["investment_income"]) / 1e8
residual = op24 - op23 + d_imp - d_inv

fig, ax = plt.subplots(figsize=(13.2, 7.2))
steps = [
    ("2023 年\n营业利润", op23, "total"),
    ("减值多提", d_imp, "down"),
    ("投资收益增加\n（含卖子公司 25.80）", d_inv, "up"),
    ("其他经营变化\n（毛利、费用等）", residual, "down"),
    ("2024 年\n营业利润", op24, "total"),
]
waterfall(ax, steps, unit="亿元", fmt="{:,.2f}", fontsize=11.8,
          down_color=C_RED, up_color=C_GREEN, total_color=C_BLUE,
          bar_width=0.54, title=None)
ax.set_ylim(-4, 138)
ax.set_xticklabels([s[0] for s in steps], fontsize=10.9)

ax.text(0.26, 0.30,
        f"营业利润一共少了 {op23 - op24:,.2f} 亿元：\n"
        f"减值多提 {d_imp:,.2f} 亿元是主因，\n"
        f"卖子公司 {d_inv:,.2f} 亿元把缺口补回大半，\n"
        f"真正的经营变化只有 {abs(residual):,.2f} 亿元。",
        transform=ax.transAxes, fontsize=11.6, color="#333333",
        ha="left", va="center", linespacing=1.7,
        bbox=dict(boxstyle="round,pad=0.45", fc="white", ec="#dddddd", lw=0.8))

ax.set_title(f"营业利润为什么少了 {op23 - op24:,.2f} 亿元：三块力量，两个是一次性的",
             fontsize=14.8, pad=16)

fig.text(
    0.012, -0.035,
    "数据来源：伊利 2024 年报 page_091、page_092（利润表）、page_211（减值明细）、page_210（投资收益）；"
    "data/yili2024.json 的 core_earnings 段。\n"
    "「其他经营变化」是倒算的差额：营业利润变动 + 减值变动 - 投资收益变动，"
    "它包含毛利额减少约 19 亿元、期间费用节省约 17 亿元等，正负相抵后为负。",
    ha="left", va="top", fontsize=9.5, color=C_GRAY, linespacing=1.6,
)

save(fig, "w07d32_operating_bridge.png")
