# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 8 周第 37 章配图 1：间接法逐项桥（净利润 84.64 → 经营现金流 217.40）。

逐项取自伊利 2024 年报 page_217~218 的「现金流量表补充资料」。
净利润、折旧摊销、减值来自 data/yili2024.json；
补充资料里的其余调整项（财务费用、投资收益、递延所得税、营运资本三项）
只能来自 raw 年报 page_218，本脚本在此逐项列出并在文末注明页码。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, waterfall, C_BLUE, C_GREEN, C_RED, C_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
inc, cf = d["income"], d["cashflow"]
Y = lambda v: v / 1e8  # noqa: E731

np_ = Y(inc["net_profit"])
dep = Y(cf["depreciation"] + cf["rou_amortization"]
        + cf["intangible_amortization"] + cf["lt_prepaid_amortization"])
asset_imp = Y(-inc["asset_impairment"])
credit_imp = Y(-inc["credit_impairment"])
ocf = Y(cf["operating_net"])

# 以下逐项来自 page_218「将净利润调节为经营活动现金流量」
finance_cost = Y(1026190054.25)
investment_gain = Y(2417330849.26)
deferred_tax = Y(388802754.25 - 25513908.30)
inventory_down = Y(585324717.44)
receivable_down = Y(1824572724.85)
payable_up = Y(2611147936.03)
other = Y(15203668.87 + 42089507.17 + 28153114.85 + 81353918.71)

steps = [
    ("净利润\n（利润表末行）", np_, "total"),
    (f"＋ 折旧与摊销\n{dep:,.2f}", dep, "up"),
    (f"＋ 资产减值准备\n{asset_imp:,.2f}", asset_imp, "up"),
    (f"＋ 信用减值损失\n{credit_imp:,.2f}", credit_imp, "up"),
    (f"＋ 财务费用\n{finance_cost:,.2f}", finance_cost, "up"),
    (f"− 投资收益\n{investment_gain:,.2f}", investment_gain, "down"),
    (f"− 递延所得税\n{deferred_tax:,.2f}", deferred_tax, "down"),
    (f"＋ 存货减少\n{inventory_down:,.2f}", inventory_down, "up"),
    (f"＋ 经营性应收\n减少 {receivable_down:,.2f}", receivable_down, "up"),
    (f"＋ 经营性应付\n增加 {payable_up:,.2f}", payable_up, "up"),
    (f"＋ 其他\n{other:,.2f}", other, "up"),
    ("＝ 经营活动\n现金流净额", ocf, "total"),
]

total = np_ + dep + asset_imp + credit_imp + finance_cost - investment_gain \
    - deferred_tax + inventory_down + receivable_down + payable_up + other
assert abs(total - ocf) < 0.02, f"桥接不平：{total:.2f} vs {ocf:.2f}"

fig, ax = plt.subplots(figsize=(15.6, 7.6))
fig.subplots_adjust(left=0.062, right=0.988, top=0.885, bottom=0.255)

waterfall(ax, steps, unit="亿元", fmt="{:,.2f}", fontsize=10.4,
          total_color=C_BLUE, up_color=C_GREEN, down_color=C_RED,
          bar_width=0.54, label_gap_frac=0.020, ylim_head_frac=0.13,
          title="把 84.64 亿倒推到 217.40 亿：每一根柱子都能在 page_217~218 找到")
ax.set_ylabel("金额（亿元）", fontsize=12)
ax.tick_params(axis="x", labelsize=9.8)
ax.set_ylim(-8, 268)

fig.text(0.010, 0.088,
         "10 根调整柱（对应 17 个明细项）按原值加总，正好等于经营活动现金流量净额 217.40 亿元——这是「间接法」的自检；"
         "按图中四舍五入后的标注相加可能差 0.01，属进位误差。",
         ha="left", va="bottom", fontsize=10.3, color="#333333", weight="bold")
fig.text(0.010, 0.052,
         "折旧与摊销 = 固定资产折旧 40.56 + 使用权资产摊销 1.47 + 无形资产摊销 2.69 + 长期待摊费用摊销 1.41；"
         "资产减值准备 46.76 含商誉 30.75、存货 12.27、固定资产 3.67。",
         ha="left", va="bottom", fontsize=9.2, color=C_GRAY)
fig.text(0.010, 0.020,
         "「其他」= 处置长期资产损失 0.15 + 固定资产报废损失 0.42 + 公允价值变动损失 0.28 + 其他 0.81。",
         ha="left", va="bottom", fontsize=9.2, color=C_GRAY)
fig.text(0.988, 0.002,
         "数据来源：伊利 2024 年报 page_092、page_094、page_217、page_218；单位：亿元",
         ha="right", va="bottom", fontsize=9.2, color=C_GRAY)

save(fig, "w08d37_indirect_bridge.png")
