# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 7 周第 31 章配图 2：24.17 亿元投资收益是怎么拼出来的（伊利 2024，亿元）。

处置长期股权投资 25.80，权益法核算联营企业 -2.15，交易性金融资产 0.53，
合计 24.17。数字全部来自 data/yili2024.json 的 income / notes 段。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, waterfall, label, C_GRAY, C_RED, C_GREEN,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
inc = d["income"]

disposal = d["notes"]["disposal_of_lt_equity_investment"] / 1e8  # 25.80
assoc = inc["share_of_associates"] / 1e8                         # -2.15
trading = inc["investment_income"] / 1e8 - disposal - assoc       # 0.53
total = inc["investment_income"] / 1e8                            # 24.17

fig, ax = plt.subplots(figsize=(12.0, 7.2))
steps = [
    ("处置长期股权投资\n（卖昌吉盛新）", disposal, "up"),
    ("权益法核算\n联营企业", assoc, "down"),
    ("交易性金融资产\n持有收益", trading, "up"),
    ("投资收益合计", total, "total"),
]
waterfall(ax, steps, unit="亿元", fmt="{:,.2f}", fontsize=11.5,
          up_color=C_GREEN, down_color=C_RED, total_color="#1f77b4",
          bar_width=0.52, title=None)
ax.set_ylim(-2.4, 36.0)
ax.set_xticklabels([s[0] for s in steps], fontsize=11.2)

label(ax, 0.0, 32.3, "卖子公司赚的 25.80 亿元，明年不会再有",
      fontsize=11.8, color=C_RED, weight="bold")
label(ax, 2.0, 28.6, "这一项才是「理财收益」",
      fontsize=10.8, color="#333333")

ax.set_title("24.17 亿元投资收益里，25.80 亿元是卖子公司赚的",
             fontsize=15.0, pad=16)

fig.text(
    0.012, -0.045,
    "数据来源：伊利 2024 年报 page_210（投资收益明细）、page_227（处置昌吉盛新实业股权）。\n"
    "图中「处置长期股权投资」25.80 亿元是利润表投资收益口径；page_227 披露的处置价款 26.47 亿元、\n"
    "合并层面差额 25.62 亿元，与 25.80 亿元相差约 0.17 亿元，属于合并层面的其他调整。",
    ha="left", va="top", fontsize=9.6, color=C_GRAY, linespacing=1.6,
)

save(fig, "w07d31_investment_bridge.png")
