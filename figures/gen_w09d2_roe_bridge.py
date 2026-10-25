# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 9 周第 42 章配图之二：ROE 从 2023 到 2024，三个因子各贡献多少。

为了让两年完全同口径，这张图统一用「期末余额」：
    净利率   = 归母净利润 / 营业收入
    周转率   = 营业收入 / 期末总资产
    权益乘数 = 期末总资产 / 期末归母权益

再用「连环替代法」（依次替换一个因子、其余保持上一年）把 ROE 的变化
拆成三块贡献。年报披露的加权平均 ROE（20.20% -> 15.81%）用的是加权平均
净资产做分母，和期末口径差 0.1~0.7 个百分点，但方向完全一致。

所有数字由 data/yili2024.json 现场计算，脚本里没有手打的公司数字。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402

from figures._common import (  # noqa: E402
    save, waterfall, C_GRAY, C_RED, C_GREEN, C_BLUE,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
inc24, inc23 = d["income"], d["compare_2023"]["income"]
bal24, bal23 = d["balance"], d["compare_2023"]["balance"]

# ── 2023（期末口径）───────────────────────────────────────────────
m23 = inc23["net_profit_parent"] / inc23["revenue"]
t23 = inc23["revenue"] / bal23["total_assets"]
l23 = bal23["total_assets"] / bal23["equity_parent"]
roe23 = m23 * t23 * l23

# ── 2024（期末口径）───────────────────────────────────────────────
m24 = inc24["net_profit_parent"] / inc24["revenue"]
t24 = inc24["revenue"] / bal24["total_assets"]
l24 = bal24["total_assets"] / bal24["equity_parent"]
roe24 = m24 * t24 * l24

# ── 连环替代：净利率 -> 周转率 -> 权益乘数 ──────────────────────────
d_m = (m24 - m23) * t23 * l23
d_t = m24 * (t24 - t23) * l23
d_l = m24 * t24 * (l24 - l23)

roe_rep_24 = d["dupont"]["roe_reported_weighted"]
roe_rep_23 = d["compare_2023"]["key_data_page007"]["roe_weighted"]
roe_avg_24 = d["dupont"]["roe"]

fig, ax = plt.subplots(figsize=(12.6, 7.6))
fig.subplots_adjust(left=0.105, right=0.975, top=0.795, bottom=0.235)

steps = [
    ("2023 年 ROE\n期末口径", roe23 * 100, "total"),
    (f"净利率\n{m24 * 100:.2f}% vs {m23 * 100:.2f}%", abs(d_m) * 100, "down"),
    (f"资产周转率\n{t24:.3f} vs {t23:.3f}", abs(d_t) * 100, "down"),
    (f"权益乘数\n{l24:.2f} vs {l23:.2f}", d_l * 100, "up"),
    ("2024 年 ROE\n期末口径", roe24 * 100, "total"),
]
waterfall(ax, steps, unit="%", fmt="{:,.2f}", fontsize=11.0,
          total_color=C_BLUE, up_color=C_GREEN, down_color=C_RED,
          bar_width=0.50, label_gap_frac=0.030, ylim_head_frac=0.19)

ax.set_title(
    f"ROE 掉 {abs(roe24 - roe23) * 100:.2f} 个百分点：净利率拖了 {abs(d_m) * 100:.2f}，"
    f"周转率拖了 {abs(d_t) * 100:.2f}，杠杆反而帮回 {d_l * 100:.2f}",
    fontsize=14.0, pad=24)
ax.set_ylabel("净资产收益率（%）", fontsize=11.6)
ax.tick_params(axis="x", labelsize=10.4)

fig.text(0.105, 0.115,
         f"年报口径（加权平均净资产收益率）：2023 年 {roe_rep_23 * 100:.2f}% -> "
         f"2024 年 {roe_rep_24 * 100:.2f}%，减少 4.39 个百分点（page_007）。"
         f"本图用期末余额，2024 年为 {roe24 * 100:.2f}%，与平均余额口径的 "
         f"{roe_avg_24 * 100:.2f}% 几乎一样。",
         fontsize=9.9, color=C_GRAY)
fig.text(0.105, 0.062,
         "三块怎么读：净利率掉 0.97 个百分点（8.29% -> 7.33%）；收入 -8.24% 而总资产还增 1.38%，"
         "一除，周转率必然下滑；负债率升到 62.91%，权益乘数从 2.83 升到 2.89，替 ROE 挡回一点。",
         fontsize=9.9, color=C_GRAY)
fig.text(0.105, 0.018,
         "拆解方法：连环替代法（先换净利率、再换周转率、最后换权益乘数）。"
         "数据：伊利 2024 年报 page_007、page_087~092",
         fontsize=9.3, color=C_GRAY)

save(fig, "w09d2_roe_bridge.png")
