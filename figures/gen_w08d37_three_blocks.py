# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 8 周第 37 章配图 2：把间接法的桥拆成「三块」，看差额 132.76 亿从哪来。

三块：①不花现金的费用（折旧摊销 46.12 + 减值 52.31）；②非经营性损益的剔除（-15.88）；
③营运资本变动（+50.21）。三块加总 = 经营现金流 - 净利润 = 132.76 亿元。
数字全部来自 data/yili2024.json（折旧摊销、减值、净利润、经营现金流）。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, C_GREEN, C_ORANGE, C_BLUE, C_GRAY, C_PURPLE,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
inc, cf = d["income"], d["cashflow"]
Y = lambda v: v / 1e8  # noqa: E731

np_ = Y(inc["net_profit"])
ocf = Y(cf["operating_net"])
gap = ocf - np_

dep = Y(cf["depreciation"] + cf["rou_amortization"]
        + cf["intangible_amortization"] + cf["lt_prepaid_amortization"])
imp = Y(-(inc["asset_impairment"] + inc["credit_impairment"]))
block1 = dep + imp

# page_218 的其余调整项
block2 = Y(1026190054.25          # 财务费用
           - 2417330849.26        # 投资收益
           - 388802754.25         # 递延所得税资产减少
           + 25513908.30          # 递延所得税负债增加
           + 15203668.87          # 处置长期资产损失
           + 42089507.17          # 固定资产报废损失
           + 28153114.85          # 公允价值变动损失
           + 81353918.71)         # 其他
block3 = Y(585324717.44 + 1824572724.85 + 2611147936.03)  # 存货/应收/应付

assert abs(block1 + block2 + block3 - gap) < 0.02, "三块加总不等于差额"

fig, ax = plt.subplots(figsize=(13.2, 7.0))
fig.subplots_adjust(left=0.335, right=0.972, top=0.865, bottom=0.175)

labels = [
    f"① 不花现金的费用\n折旧摊销 {dep:,.2f} + 减值 {imp:,.2f}",
    "② 非经营性损益的剔除\n财务费用、投资收益、递延税",
    "③ 营运资本变动\n存货、经营性应收、应付",
    "三块合计\n= 现金流 - 净利润",
]
vals = [block1, block2, block3, gap]
colors = [C_GREEN, C_ORANGE, C_BLUE, C_PURPLE]
ys = [3, 2, 1, 0]
bars = ax.barh(ys, vals, height=0.50, color=colors, zorder=3,
               edgecolor="white", linewidth=0.8)

ax.set_yticks(ys)
ax.set_yticklabels(labels, fontsize=11.6, linespacing=1.6)
ax.set_xlim(-62, 168)
ax.set_ylim(-0.70, 3.60)
ax.set_xlabel("金额（亿元）", fontsize=12)
ax.axvline(0, color="#888888", lw=1.1, zorder=1)
ax.set_title("132.76 亿元的差额，其实是三块东西", fontsize=15.5, pad=12)

for b, v in zip(bars, vals):
    y = b.get_y() + b.get_height() / 2
    if v >= 0:
        ax.text(v + 3.0, y, f"{v:+,.2f}", ha="left", va="center",
                fontsize=12.5, weight="bold", color="#222222", zorder=6)
    else:
        ax.text(v / 2, y, f"{v:+,.2f}", ha="center", va="center",
                fontsize=12.5, weight="bold", color="white", zorder=6)

clean_axes(ax)

fig.text(0.012, 0.078,
         "读法：把桥拆成三块，比逐项背 13 个加减项有用得多。"
         "① 是「扣了但没花钱」，② 是「算在利润里但现金归投资/筹资活动」，③ 是「占用或释放上下游的钱」。",
         ha="left", va="bottom", fontsize=9.8, color="#333333")
fig.text(0.012, 0.033,
         f"验算：{block1:,.2f} - {abs(block2):,.2f} + {block3:,.2f} = {gap:,.2f}；"
         f"净利润 {np_:,.2f} + 差额 {gap:,.2f} = 经营现金流 {ocf:,.2f}。"
         "② 为负，是因为财务费用为负（利息收入大于利息支出）且投资收益 24.17 亿元要剔除。",
         ha="left", va="bottom", fontsize=9.2, color=C_GRAY)
fig.text(0.988, 0.002,
         "数据来源：伊利 2024 年报 page_092、page_094、page_217、page_218；单位：亿元",
         ha="right", va="bottom", fontsize=9.2, color=C_GRAY)

save(fig, "w08d37_three_blocks.png")
