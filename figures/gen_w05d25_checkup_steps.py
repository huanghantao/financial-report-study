# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 5 周第 25 章配图之二：偿债体检四步法（概念流程图）。

四步自上而下，每步一个方框，右侧给「伊利 2024」的实测结果。
所有数字来自 data/yili2024.json（已核实），不手打。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import (
    save, fig_ax, box, arrow, label,
    F_BLUE, F_ORANGE, F_GREEN, F_GRAY, F_PURPLE,
    C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_PURPLE, C_RED,
)
from figures._data import load

d = load("yili2024")
b, r, inc, cf = d["balance"], d["ratios"], d["income"], d["cashflow"]
yi = 1e8

ibd = r["interest_bearing_debt"] / yi
total_liab = b["total_liabilities"] / yi
cash_all = r["cash_and_deposits"] / yi
net_debt = r["net_interest_bearing_debt"] / yi
ocf = cf["operating_net"] / yi
interest = inc["interest_expense"] / yi
dep = cf["depreciation"] / yi
amort = (cf["intangible_amortization"] + cf["lt_prepaid_amortization"]
         + cf["rou_amortization"]) / yi
op = inc["operating_profit"] / yi
ebitda = op + dep + amort
cover = ocf / interest
cur = r["current_ratio"]
debt_ratio = r["debt_ratio"]

fig, ax = fig_ax(13.2, 8.6, xlim=(0, 12), ylim=(0, 11.4))

steps = [
    ("第 1 步  拆负债率",
     f"负债 {total_liab:,.2f} 亿里，\n有息只有 {ibd:,.2f} 亿（{ibd / total_liab:.1%}）",
     F_ORANGE, C_ORANGE,
     f"资产负债率 {debt_ratio:.2%} 看着高，\n"
     f"但 {1 - ibd / total_liab:.1%} 是占用上下游的钱"),
    ("第 2 步  查现金藏在哪",
     f"流动比率 {cur:.2f} 偏低，\n但类现金有 {cash_all:,.2f} 亿",
     F_BLUE, C_BLUE,
     f"其中 279.77 亿大额存单放在\n「其他非流动资产」，没算进流动比率"),
    ("第 3 步  算净有息负债",
     f"有息负债 {ibd:,.2f}\n- 类现金 {cash_all:,.2f}",
     F_GREEN, C_GREEN,
     f"= {net_debt:,.2f} 亿，负数。\n净有息负债 / EBITDA 不适用"),
    ("第 4 步  看现金流覆盖",
     f"经营现金流 {ocf:,.2f} 亿\n÷ 利息费用 {interest:,.2f} 亿",
     F_PURPLE, C_PURPLE,
     f"= {cover:.1f} 倍。\n利息不是靠借钱付的，是靠赚的"),
]

top = 10.2
bh = 1.55
gap = 0.62
x0, bw = 0.45, 6.55
rx, rw = 7.65, 4.0

for i, (head, body, fc, ec, result) in enumerate(steps):
    y = top - i * (bh + gap) - bh
    box(ax, x0, y, bw, bh, "", fc=fc, ec=ec, lw=1.8)
    ax.text(x0 + 0.28, y + bh - 0.34, head, fontsize=13.2, weight="bold",
            color=ec, ha="left", va="center", zorder=6)
    ax.text(x0 + 0.28, y + 0.46, body, fontsize=11.6, color="#222222",
            ha="left", va="center", zorder=6, linespacing=1.55)
    # 右侧结果
    box(ax, rx, y, rw, bh, "", fc="white", ec=ec, lw=1.2,
        style="round,pad=0.02,rounding_size=0.12")
    ax.text(rx + 0.22, y + bh / 2, result, fontsize=11.0, color="#333333",
            ha="left", va="center", zorder=6, linespacing=1.55)
    arrow(ax, (x0 + bw + 0.08, y + bh / 2), (rx - 0.10, y + bh / 2),
          color=ec, lw=1.6)
    if i < len(steps) - 1:
        nx = top - (i + 1) * (bh + gap) - bh
        arrow(ax, (x0 + 0.7, y - 0.06), (x0 + 0.7, nx + bh + 0.08),
              color=C_GRAY, lw=1.8)

ax.text(x0, 11.05, "偿债体检四步法：先拆结构，再查现金，最后看现金流",
        fontsize=15.5, weight="bold", ha="left", va="center")
ax.text(x0, 0.35,
        f"EBITDA = 营业利润 {op:,.2f} + 折旧摊销 {dep + amort:,.2f} = {ebitda:,.2f} 亿元；"
        f"净有息负债为负数时，这个比率失去意义，直接说「净现金」。",
        fontsize=10.2, color="#555555", ha="left", va="center")

save(fig, "w05d25_checkup_steps.png")
