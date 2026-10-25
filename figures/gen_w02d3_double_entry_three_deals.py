# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 2 周第 8 章配图：伊利 2024 年三件真事，每一件都同时动两个格子。

不教借贷方向，只教「一笔交易至少要落在两个格子里，而且两边同时变」。
三件事的数字全部来自 data/yili2024.json 与 raw 年报 page_045 / page_088 / page_095 / page_217。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.patches as mpatches  # noqa: E402

from figures._common import (  # noqa: E402
    save, fig_ax,
    C_BLUE, C_ORANGE, C_GREEN, C_PURPLE, C_GRAY, C_RED,
    F_BLUE, F_ORANGE, F_GREEN, F_PURPLE, F_GRAY,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
b = d["balance"]
cf = d["cashflow"]

# 余额直接读 JSON
stb_begin = d["compare_2023"]["balance"]["short_term_borrowings"] / 1e8  # 397.55
stb_end = b["short_term_borrowings"] / 1e8                              # 363.55
contract_end = b["contract_liabilities"] / 1e8                           # 120.73
contract_begin = d["compare_2023"]["balance"]["contract_liabilities"] / 1e8  # 86.96
div_cash_line = cf["dividends_and_interest_paid"] / 1e8                  # 90.92

# 以下四个数只出现在附注里、data/*.json 未收录，逐字取自 raw 年报对应页：
stb_in = 81255984329.65 / 1e8       # page_217 短期借款「本期增加·现金变动」
stb_out = 85446869984.31 / 1e8      # page_217 短期借款「本期减少·现金变动」
div_paid = 7639318446.00 / 1e8      # page_045 2023 年度现金红利
minority_div = 60172342.82 / 1e8    # page_095 子公司支付给少数股东的股利、利润

fig, ax = fig_ax(14.2, 9.6, xlim=(0, 100), ylim=(0, 100))

ax.text(50, 96.4, "三件真事，六个格子：钱一动，至少两个地方同时变",
        ha="center", va="center", fontsize=15.5, weight="bold", color="#1a1a1a")
ax.text(50, 92.2, "伊利 2024 年报里的三笔交易 · 单位：亿元 · 「＋」增加「－」减少",
        ha="center", va="center", fontsize=11, color=C_GRAY)

COLS = [
    (2.0, 21.0, "事件"),
    (24.4, 23.2, "动的第一个格子"),
    (49.0, 23.2, "动的第二个格子"),
    (73.6, 24.4, "恒等式怎么变"),
]
HEAD_Y, HEAD_H = 84.2, 6.0
for x, w, txt in COLS:
    ax.add_patch(mpatches.Rectangle((x, HEAD_Y), w, HEAD_H, facecolor="#3f3f3f",
                                    edgecolor="white", lw=1.2, zorder=3))
    ax.text(x + w / 2, HEAD_Y + HEAD_H / 2, txt, ha="center", va="center",
            fontsize=11.6, weight="bold", color="white", zorder=5)

ROWS = [
    (dict(
        head="① 借新还旧\n短期借款滚动",
        a="短期借款\n＋812.56（新借）\n－854.47（还旧）",
        b="货币资金\n＋812.56\n－854.47",
        c=f"负债内部一增一减、\n资产内部一增一减；\n两边总额都不变。\n余额 {stb_begin:,.2f} → {stb_end:,.2f}",
        fc=F_ORANGE, ec=C_ORANGE,
    ), 66.0),
    (dict(
        head="② 先收钱后发货\n合同负债",
        a=f"货币资金\n＋预收的货款",
        b=f"合同负债\n期末 {contract_end:,.2f}\n（年初 {contract_begin:,.2f}）",
        c=f"资产 ＋\n负债 ＋\n两边同时变厚；\n发货后转为收入",
        fc=F_BLUE, ec=C_BLUE,
    ), 47.2),
    (dict(
        head="③ 分红\n2023 年度现金红利",
        a=f"未分配利润\n－{div_paid:,.2f}",
        b=f"货币资金\n－{div_paid:,.2f}\n（经「应付股利」过渡）",
        c=f"资产 －{div_paid:,.2f}\n权益 －{div_paid:,.2f}\n两边同时变薄",
        fc=F_PURPLE, ec=C_PURPLE,
    ), 28.4),
]

ROW_H = 17.0
for r, y in ROWS:
    for (x, w, _), key in zip(COLS, ("head", "a", "b", "c")):
        strong = key == "head"
        ax.add_patch(mpatches.Rectangle(
            (x, y), w, ROW_H,
            facecolor=r["fc"] if strong else "white",
            edgecolor=r["ec"] if strong else "#d5d5d5",
            lw=1.8 if strong else 1.0, zorder=3,
        ))
        ax.text(x + w / 2, y + ROW_H / 2, r[key], ha="center", va="center",
                fontsize=11.4 if strong else 10.6,
                weight="bold" if strong else "normal",
                color=r["ec"] if strong else "#222222",
                linespacing=1.7, zorder=5)
    # 事件列左侧的编号色条
    ax.add_patch(mpatches.Rectangle((2.0, y), 0.55, ROW_H, facecolor=r["ec"],
                                    edgecolor="none", zorder=4))

# ── 底部说明 ────────────────────────────────────────────────────────
ax.text(50, 20.4,
        f"分红这一行：现金流量表「分配股利、利润或偿付利息支付的现金」合计 {div_cash_line:,.2f} 亿元，"
        f"其中含少数股东股利 {minority_div:,.2f} 亿元与利息。",
        ha="center", va="center", fontsize=10.6, color="#333333")
ax.text(50, 14.6,
        "分红分两步：宣告时未分配利润转成应付股利（总额不变），付款时应付股利与货币资金同时减少。",
        ha="center", va="center", fontsize=10.6, color="#333333")

ax.text(2.0, 7.4,
        "记住这一条就够用：没有任何一笔交易只动一个格子。只动一个格子，等式立刻破。",
        ha="left", va="center", fontsize=11.4, weight="bold", color=C_RED)
ax.text(98.0, 2.4,
        "数据来源：伊利 2024 年报 page_045、page_088、page_095、page_217；单位：亿元",
        ha="right", va="center", fontsize=9.5, color=C_GRAY)

save(fig, "w02d3_double_entry_three_deals.png")
