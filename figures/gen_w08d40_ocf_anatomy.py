# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 8 周第 40 章配图：217.40 亿经营现金流从哪来。

上条：经营活动现金流入 1,352.77 亿元（销售商品收现 1,306.52 亿元占 96.6%）；
下条：经营活动现金流出 1,135.37 亿元（购买商品 912.54 亿元占 80.4%）；
两条之差 217.40 亿元就是经营活动现金流量净额。
数字全部来自 data/yili2024.json 的 cashflow 段。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, clean_axes, C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_PURPLE,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
cf = d["cashflow"]
inc = d["income"]
Y = lambda v: v / 1e8  # noqa: E731

inflow = Y(cf["operating_inflow"])
outflow = Y(cf["operating_outflow"])
net = Y(cf["operating_net"])
sales = Y(cf["cash_from_sales"])
goods = Y(cf["purchase_cash"])
staff = Y(cf["employee_cash"])
tax = Y(cf["tax_cash"])
other_in = inflow - sales
other_out = outflow - goods - staff - tax
rev = Y(inc["revenue"])

assert abs(inflow - outflow - net) < 0.02, "流入 - 流出 不等于净额"
assert abs(sales / rev - d["core_earnings"]["cash_to_revenue_2024"]) < 0.01

# 流入四段（销售收现 + 其他三段合并成「税费返还等」）
in_segs = [
    ("销售商品、提供劳务收到的现金", sales, C_BLUE),
    ("税费返还、利息与其他", other_in, "#6baed6"),
]
# 流出四段
out_segs = [
    ("购买商品、接受劳务支付的现金", goods, C_ORANGE),
    ("支付给职工", staff, "#fdae6b"),
    ("支付的各项税费", tax, "#fdd0a2"),
    ("支付其他", other_out, "#fee6ce"),
]

fig, ax = plt.subplots(figsize=(13.6, 7.0))
fig.subplots_adjust(left=0.045, right=0.975, top=0.855, bottom=0.235)

H = 0.46
xmax = 1560

# 流入条（y=2）
left = 0.0
for name, v, col in in_segs:
    ax.barh(2, v, left=left, height=H, color=col, edgecolor="white",
            linewidth=1.0, zorder=3)
    left += v

# 流出条（y=0.75）
left = 0.0
for name, v, col in out_segs:
    ax.barh(0.75, v, left=left, height=H, color=col, edgecolor="white",
            linewidth=1.0, zorder=3)
    left += v

ax.set_xlim(0, xmax)
ax.set_ylim(-0.95, 2.95)
ax.set_yticks([2, 0.75])
ax.set_yticklabels(["现金流入\n1,352.77", "现金流出\n1,135.37"], fontsize=12.5)
ax.set_xlabel("金额（亿元）", fontsize=12)
ax.set_title("217.40 亿元不是「一笔收入」，而是 1,352.77 亿减去 1,135.37 亿",
             fontsize=15, pad=14)
ax.tick_params(axis="y", pad=10)

# 大段内部标注
ax.text(sales / 2, 2, f"销售商品收现 {sales:,.2f}\n占流入 {sales / inflow * 100:.1f}%",
        ha="center", va="center", fontsize=12.2, color="white", weight="bold",
        linespacing=1.7, zorder=6)
ax.text(goods / 2, 0.75, f"购买商品付现 {goods:,.2f}\n占流出 {goods / outflow * 100:.1f}%",
        ha="center", va="center", fontsize=12.2, color="white", weight="bold",
        linespacing=1.7, zorder=6)

# 流入的小段：标注放在条上方
ax.annotate(f"税费返还、利息与其他 {other_in:,.2f}",
            xy=(inflow - other_in / 2, 2 + H / 2),
            xytext=(inflow - other_in / 2 - 40, 2.62),
            ha="right", va="bottom", fontsize=10.6, color=C_BLUE,
            weight="bold", zorder=7,
            bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=C_BLUE,
                      lw=0.9, alpha=0.96),
            arrowprops=dict(arrowstyle="-", color=C_BLUE, lw=0.9,
                            shrinkA=2, shrinkB=2))

# 流出的小段：三个标签排成一行，引线左右错开，互不交叉
small_out = [
    (goods + staff / 2, f"职工 {staff:,.2f}", goods + staff / 2 - 135),
    (goods + staff + tax / 2, f"税费 {tax:,.2f}", goods + staff + tax / 2 - 55),
    (goods + staff + tax + other_out / 2, f"其他 {other_out:,.2f}",
     goods + staff + tax + other_out / 2 + 50),
]
for x, txt, xt in small_out:
    ax.annotate(txt, xy=(x, 0.75 - H / 2), xytext=(xt, -0.30),
                ha="center", va="top", fontsize=10.6, color=C_ORANGE,
                weight="bold", zorder=7,
                bbox=dict(boxstyle="round,pad=0.26", fc="white", ec=C_ORANGE,
                          lw=0.9, alpha=0.96),
                arrowprops=dict(arrowstyle="-", color=C_ORANGE, lw=0.9,
                                shrinkA=2, shrinkB=2))

# 净额：两条之差
ax.annotate("", xy=(inflow, 1.42), xytext=(outflow, 1.42),
            arrowprops=dict(arrowstyle="<|-|>", color=C_GREEN, lw=2.0,
                            mutation_scale=18))
ax.plot([outflow, outflow], [0.52, 2.23], color=C_GRAY, lw=1.0,
        ls=(0, (4, 3)), zorder=2)
ax.text((inflow + outflow) / 2, 1.56,
        f"净额 {net:,.2f} 亿元",
        ha="center", va="bottom", fontsize=13, color=C_GREEN, weight="bold",
        bbox=dict(boxstyle="round,pad=0.34", fc="white", ec=C_GREEN,
                  lw=1.1, alpha=0.97), zorder=8)

clean_axes(ax)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)

fig.text(0.012, 0.100,
         f"收现比 = 销售商品收到的现金 {sales:,.2f} ÷ 营业收入 {rev:,.2f} = {sales / rev:.3f}："
         "每做 1 元收入，收回 1.13 元现金——多出来的部分来自收回旧应收和预收货款。",
         ha="left", va="bottom", fontsize=9.8, color="#333333")
fig.text(0.012, 0.048,
         "注意：流入 1,352.77 亿元里，96.6% 是卖货收到的钱，不是卖资产、不是借钱。"
         "这是判断「现金流是不是主业挣来的」最快的一眼。",
         ha="left", va="bottom", fontsize=9.4, color=C_GRAY)
fig.text(0.985, 0.002,
         "数据来源：伊利 2024 年报 page_091、page_094；单位：亿元",
         ha="right", va="bottom", fontsize=9.2, color=C_GRAY)

save(fig, "w08d40_ocf_anatomy.png")
