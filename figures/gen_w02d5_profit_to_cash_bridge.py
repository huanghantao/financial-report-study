# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 2 周第 9 章配图：净利润 84.64 亿 → 经营现金流 217.40 亿 的桥（间接法）。

用年报 page_217~218 的「现金流量表补充资料」逐项搭桥，加总正好等于经营现金流净额。
数字全部来自 data/yili2024.json（折旧摊销、减值由利润表/现金流补充资料合成）。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, waterfall, C_BLUE, C_GREEN, C_RED, C_GRAY, C_ORANGE,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
inc, cf = d["income"], d["cashflow"]
Y = lambda v: v / 1e8  # noqa: E731

np_ = Y(inc["net_profit"])                                   # 84.64
dep = Y(cf["depreciation"] + cf["rou_amortization"]
        + cf["intangible_amortization"] + cf["lt_prepaid_amortization"])  # 46.12
imp = Y(-(inc["asset_impairment"] + inc["credit_impairment"]))          # 52.31
ocf = Y(cf["operating_net"])                                 # 217.40

# 其余调整项（page_218）与营运资本变动，逐项加总后归成两组
other_adj = Y(28153114.85          # 公允价值变动损失
              + 1026190054.25      # 财务费用
              - 2417330849.26      # 投资损失（收益以负号填列）
              - 388802754.25       # 递延所得税资产减少
              + 25513908.30        # 递延所得税负债增加
              + 42089507.17        # 固定资产报废损失
              + 15203668.87        # 处置长期资产损失
              + 81353918.71)       # 其他
working_capital = Y(cf.get("inventory_decrease", 585324717.44)
                    + 1824572724.85    # 经营性应收项目的减少
                    + 2611147936.03)   # 经营性应付项目的增加

assert abs((np_ + dep + imp + other_adj + working_capital) - ocf) < 0.02, "桥接不平"

fig, ax = plt.subplots(figsize=(13.2, 7.6))
fig.subplots_adjust(left=0.085, right=0.985, top=0.885, bottom=0.235)

steps = [
    ("净利润\n（利润表）", np_, "total"),
    ("＋ 折旧与摊销\n不花现金", dep, "up"),
    ("＋ 计提减值\n不花现金", imp, "up"),
    ("－ 财务费用、投资\n收益等调整", abs(other_adj), "down"),
    ("＋ 营运资本变动\n存货、应收、应付", working_capital, "up"),
    ("＝ 经营活动\n现金流净额", ocf, "total"),
]

waterfall(ax, steps, unit="亿元", fmt="{:,.2f}", fontsize=10.8,
          total_color=C_BLUE, up_color=C_GREEN, down_color=C_RED,
          bar_width=0.52, label_gap_frac=0.028, ylim_head_frac=0.12,
          title="从净利润 84.64 亿到经营现金流 217.40 亿：每一格都能对上年报")
ax.set_ylabel("金额（亿元）", fontsize=11.8)
ax.tick_params(axis="x", labelsize=10.8)
ax.set_ylim(-6, 262)

fig.text(0.012, 0.055,
         "折旧摊销 = 固定资产折旧 40.56 + 使用权资产摊销 1.47 + 无形资产摊销 2.69 + 长期待摊费用摊销 1.41；"
         "减值 = 资产减值 46.76 + 信用减值 5.55。",
         ha="left", va="bottom", fontsize=9.3, color=C_GRAY)
fig.text(0.012, 0.024,
         "「其它调整」含财务费用 +10.26、投资收益 −24.17、递延所得税 −3.63、报废与处置损失 +0.57、其他 +0.81；"
         "「营运资本变动」= 存货 +5.85、经营性应收 +18.25、经营性应付 +26.11。",
         ha="left", va="bottom", fontsize=9.3, color=C_GRAY)
fig.text(0.985, 0.001, "数据来源：伊利 2024 年报 page_092、page_094、page_217、page_218；单位：亿元",
         ha="right", va="bottom", fontsize=9.3, color=C_GRAY)

save(fig, "w02d5_profit_to_cash_bridge.png")
