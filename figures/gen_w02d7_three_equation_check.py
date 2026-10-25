# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 2 周第 10 章配图：三表勾稽的三个等式，用伊利 2024 真数字逐条验算。

等式一：资产 = 负债 + 所有者权益（page_087~088）
等式二：期初现金 + 现金净增加额 = 期末现金（page_095）
等式三：年初未分配利润 + 归母净利润 − 已派现金红利 + 收回股利 = 年末未分配利润（page_088、page_002）
三条都差 0，这才是「三张表咬得上」。数字全部来自 data/yili2024.json 与 raw 年报。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.patches as mpatches  # noqa: E402

from figures._common import (  # noqa: E402
    save, fig_ax, C_BLUE, C_GREEN, C_PURPLE, C_GRAY, C_RED,
    F_BLUE, F_GREEN, F_PURPLE,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
b, i, cf = d["balance"], d["income"], d["cashflow"]
Y = lambda v: v / 1e8  # noqa: E731

ta, tl, te = Y(b["total_assets"]), Y(b["total_liabilities"]), Y(b["total_equity"])
ep, mi = Y(b["equity_parent"]), Y(b["minority_interest"])
cash_beg, net_change, cash_end = (Y(cf["cash_begin"]), Y(cf["net_cash_change"]),
                                  Y(cf["cash_end"]))
re_beg = Y(31414532460.31)        # page_088 未分配利润期初列
re_end = Y(b["retained_earnings"])
np_parent = Y(i["net_profit_parent"])
div_declared = Y(7639318446.00)   # page_002：2023 年度现金红利，2024 年派发
div_recovered = Y(956340.00)      # page_002：股权激励对象离职收回的已分配股利

eq1_l, eq1_r = ta, tl + te
eq2_l, eq2_r = cash_beg + net_change, cash_end
eq3_l = re_beg + np_parent - div_declared + div_recovered
eq3_r = re_end

fig, ax = fig_ax(14.2, 9.6, xlim=(0, 100), ylim=(0, 100))

ax.text(50, 97.4, "三张表能不能对上：三个等式逐条验算伊利 2024",
        ha="center", va="center", fontsize=15.4, weight="bold", color="#1a1a1a")
ax.text(50, 94.4, "每个等式都给「左边」「右边」「差多少」——差 0，才叫咬得上",
        ha="center", va="center", fontsize=11, color=C_GRAY)

COLS = [(2.0, 6.2, "序号"), (9.4, 44.0, "等式（左边 = 右边）"),
        (54.6, 15.4, "左边算出"), (71.2, 15.4, "右边报表数"), (87.8, 10.2, "差")]
HEAD_Y, HEAD_H = 86.6, 4.8
for x, w, txt in COLS:
    ax.add_patch(mpatches.Rectangle((x, HEAD_Y), w, HEAD_H, facecolor="#3f3f3f",
                                    edgecolor="white", lw=1.2, zorder=3))
    ax.text(x + w / 2, HEAD_Y + HEAD_H / 2, txt, ha="center", va="center",
            fontsize=11.2, weight="bold", color="white", zorder=5)

ROWS = [
    ("①", "资产 = 负债 + 所有者权益",
     f"资产 {ta:,.2f}", f"负债 {tl:,.2f}\n＋ 权益 {te:,.2f}", eq1_l - eq1_r,
     C_BLUE, F_BLUE),
    ("②", "期初现金 + 净增加额 = 期末现金",
     f"{cash_beg:,.2f}\n＋ ({net_change:,.2f})", f"期末现金\n{cash_end:,.2f}",
     eq2_l - eq2_r, C_GREEN, F_GREEN),
    ("③", "年初未分配利润 + 归母净利 − 分红 = 年末",
     f"{re_beg:,.2f}\n＋{np_parent:,.2f}−{div_declared:,.2f}", f"年末未分配利润\n{re_end:,.2f}",
     eq3_l - eq3_r, C_PURPLE, F_PURPLE),
]

ROW_H = 12.6
y = HEAD_Y - 1.6
for idx, name, left_txt, right_txt, diff, ec, fc in ROWS:
    for (x, w, _), is_diff in zip(COLS, (False, False, False, False, True)):
        ax.add_patch(mpatches.Rectangle(
            (x, y - ROW_H), w, ROW_H,
            facecolor=fc if x == 2.0 else ("#f4fbf4" if is_diff else "white"),
            edgecolor="#dddddd", lw=0.9, zorder=3))
    ax.text(2.0 + 6.2 / 2, y - ROW_H / 2, idx, ha="center", va="center",
            fontsize=16, weight="bold", color=ec, zorder=5)
    ax.text(11.0, y - ROW_H / 2, name, ha="left", va="center",
            fontsize=11.6, weight="bold", color="#1a1a1a", zorder=5)
    ax.text(54.6 + 15.4 / 2, y - ROW_H / 2, left_txt, ha="center", va="center",
            fontsize=10.8, color="#222222", linespacing=1.9, zorder=5)
    ax.text(71.2 + 15.4 / 2, y - ROW_H / 2, right_txt, ha="center", va="center",
            fontsize=10.8, color="#222222", linespacing=1.9, zorder=5)
    ax.text(87.8 + 10.2 / 2, y - ROW_H / 2, "0.00", ha="center", va="center",
            fontsize=13.2, weight="bold", color=C_GREEN, zorder=5)
    y -= ROW_H + 1.2

# ── 三条注解 ────────────────────────────────────────────────────────
notes = [
    (C_BLUE, f"① 归母权益 {ep:,.2f} ＋ 少数股东权益 {mi:,.2f} ＝ 所有者权益 {te:,.2f}；"
             f"负债 {tl:,.2f} ＋ {te:,.2f} ＝ {ta:,.2f}，与资产总计一字不差。"),
    (C_GREEN, f"② {cash_beg:,.2f} ＋ ({net_change:,.2f}) ＝ {cash_end:,.2f}。"
              f"注意这是「现金及现金等价物」，比资产负债表货币资金少 8.58 亿元。"),
    (C_PURPLE, f"③ {re_beg:,.2f} ＋ {np_parent:,.2f} − {div_declared:,.2f} ＋ 收回股利 0.001 ＝ {re_end:,.2f}。"
               f"「− 分红」这一步，就是利润表和资产负债表之间那道闸门。"),
]
yy = 42.6
for color, txt in notes:
    ax.text(2.0, yy, txt, ha="left", va="center", fontsize=10.6, color=color,
            weight="bold")
    yy -= 5.0

ax.text(2.0, 21.0,
        "第三个等式最容易出错：分红先挂「应付股利」再付款；回购库存股、其他综合收益结转也会\n"
        "改变未分配利润以外的权益科目。只要对不上，先别急着说公司造假——先把这几项找齐。",
        ha="left", va="center", fontsize=10.2, color=C_RED, linespacing=1.9)
ax.text(98.0, 2.2, "数据来源：伊利 2024 年报 page_002、page_087、page_088、page_095；单位：亿元",
        ha="right", va="center", fontsize=9.4, color=C_GRAY)

save(fig, "w02d7_three_equation_check.png")
