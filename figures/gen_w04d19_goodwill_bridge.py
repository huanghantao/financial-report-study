# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 4 周第 19 章核心配图：伊利 2024 年商誉「净值桥」（亿元）。

51.60 亿 → 23.37 亿，一年砍掉 28.23 亿，其中 30.75 亿是自己主动计提的减值，
被收购澳优旗下 Amalthea 新增的 1.86 亿和汇率变动 0.66 亿抵掉一部分。

口径：
- 起点/终点净值 = 资产负债表商誉（page_087），等于附注七(27) 的原值减减值准备（page_184）；
- 减值 30.75 亿 = 澳优 30.37 亿 + 内蒙古康益佳 0.38 亿（page_184 商誉减值准备表）；
- 「汇率变动等」是倒算合并项：原值侧汇率 +0.72 与减少 0.04、减值准备侧汇率 +0.02 轧差后约 +0.66 亿。
所有数字来自 data/yili2024.json 的 goodwill_detail。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, waterfall, label, C_GRAY, C_RED, C_GREEN, C_BLUE, C_ORANGE,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
g = d["goodwill_detail"]
net_end = d["balance"]["goodwill"] / 1e8                        # 23.37
net_begin = d["balance"]["goodwill_2023"] / 1e8                 # 51.60
added = g["gross_added"] / 1e8                                  # 1.86
imp = g["impairment_added"] / 1e8                               # 30.75
fx_net = ((g["gross_fx"] - g["gross_disposal"] - g["impairment_fx"])
          / 1e8)                                                # 0.66

auyou = g["by_entity"]["澳优乳业股份有限公司"]
auyou_imp = auyou["impairment_added"] / 1e8                     # 30.37
kangyijia_imp = g["by_entity"]["内蒙古康益佳生物技术有限公司"]["impairment_added"] / 1e8  # 0.38

fig, ax = plt.subplots(figsize=(13.0, 6.6))

steps = [
    ("2023 年末\n商誉净额", net_begin, "total"),
    ("收购 Amalthea\n并入澳优", added, "up"),
    ("汇率变动等\n（倒算项）", fx_net, "up"),
    ("本期计提\n商誉减值", imp, "down"),
    ("2024 年末\n商誉净额", net_end, "total"),
]

waterfall(ax, steps, unit="亿元", fontsize=11.6, bar_width=0.50,
          label_gap_frac=0.018, ylim_head_frac=0.13,
          total_color=C_BLUE, up_color=C_GREEN, down_color=C_RED,
          title="商誉从 51.60 亿降到 23.37 亿：一年提掉 30.75 亿，其中 30.37 亿来自澳优")

ax.set_ylim(-6, 68)
ax.set_xlim(-0.6, 4.6)

# 三行注记放在坐标区左侧的空白带（第 1 根柱子右边、第 2~3 根柱子下方），不压任何柱子
label(ax, 0.42, 33.0,
      f"30.75 亿 = 澳优 {auyou_imp:,.2f} 亿 + 康益佳 {kangyijia_imp:,.2f} 亿",
      fontsize=11.2, color=C_RED, ha="left")
label(ax, 0.42, 25.0,
      "减值不花一分现金，\n但利润表要照扣",
      fontsize=11.2, color="#333333", ha="left")
label(ax, 0.42, 14.0,
      "剩下的 23.37 亿仍是\n「过去付贵了」的余额，不是能卖的资产",
      fontsize=11.2, color="#333333", ha="left")

fig.text(0.012, -0.028,
         "数据来源：伊利 2024 年报 page_087（商誉净值）、page_184（附注七(27) 商誉原值与减值准备明细）、page_211（资产减值损失）。\n"
         "四舍五入到 0.01，桥接两端可能有 0.01 的尾差；「汇率变动等」= 原值侧汇率变动 + 减少 − 减值准备侧汇率变动。",
         ha="left", va="top", fontsize=9.6, color=C_GRAY, linespacing=1.6)

save(fig, "w04d19_goodwill_bridge.png")
