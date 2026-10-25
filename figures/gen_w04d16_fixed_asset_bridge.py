# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 4 周第 16 章配图 1：伊利 2024 年固定资产「净值桥」（亿元）。

净值从 352.42 亿走到 346.19 亿：中间被折旧 40.56 亿和减值 3.67 亿
往下拽，又被当年新投入 37.99 亿往上托，最后只降了 6.24 亿。

口径说明：
- 期初/期末净值、全年折旧、固定资产减值，全部来自 data/yili2024.json；
- 「购置与转固等净增」是倒算项：期末 − 期初 + 折旧 + 减值；
  它在附注七(21)（page_174）里被拆成购置 2.59 亿、在建工程转入 42.49 亿、
  处置与转出 23.27 亿等，本章正文用表格讲；
- 折旧取现金流量表补充资料口径（page_217），含生产性生物资产与投资性房地产折旧，
  所以和固定资产附注里的 38.18 亿略有差异（正文 16.5 节专门解释这两个数）。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, waterfall, label, C_GRAY, C_RED, C_GREEN, C_BLUE,
)
from figures._data import load  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402

d = load("yili2024")
fa_end = d["balance"]["fixed_assets"] / 1e8           # 346.19
fa_beg = d["compare_2023"]["balance"]["fixed_assets"] / 1e8  # 352.42
dep = d["cashflow"]["depreciation"] / 1e8             # 40.56
imp = d["notes"]["fixed_asset_impairment"] / 1e8      # 3.67
added = fa_end - fa_beg + dep + imp                   # 37.99（倒算）

fig, ax = plt.subplots(figsize=(12.4, 7.2))

steps = [
    ("2023 年末\n固定资产净值", fa_beg, "total"),
    ("全年折旧\n（不花现金）", dep, "down"),
    ("固定资产减值\n（也不花现金）", imp, "down"),
    ("购置、在建工程\n转固等净增", added, "up"),
    ("2024 年末\n固定资产净值", fa_end, "total"),
]

waterfall(ax, steps, unit="亿元", fontsize=11.5, bar_width=0.52,
          rotate_labels=0, label_gap_frac=0.020, ylim_head_frac=0.12,
          total_color=C_BLUE, up_color=C_GREEN, down_color=C_RED,
          title="折旧与减值往下拽 44.23 亿，新投入往上托 37.99 亿：净值一年只降 6.24 亿")

ax.set_ylim(-38, 395)
ax.set_xlim(-0.62, 4.62)

# 注记放在坐标区左中部（第 1 根柱右侧、第 2 根柱下方的整片空白），不压任何柱子
label(ax, 0.55, 216,
      "折旧 + 减值合计 44.23 亿元，\n是这一年被「用旧、用坏」的部分",
      fontsize=11.4, color=C_RED, ha="left")

label(ax, 0.55, 130,
      "净值只降 6.24 亿元 ——\n但 44.23 亿元的代价\n已经在利润表里扣过了",
      fontsize=11.4, color="#333333", ha="left")

fig.text(0.01, 0.005,
         "数据来源：伊利 2024 年报 page_087（净值）、page_174（附注七(21)）、page_217（折旧）。"
         "「净增」为倒算项；各数四舍五入到 0.01，合计可能有末位差。",
         ha="left", va="bottom", fontsize=9.6, color=C_GRAY)

save(fig, "w04d16_fixed_asset_bridge.png")
