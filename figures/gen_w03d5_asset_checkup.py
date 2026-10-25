# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 3 周第 5 章配图：伊利 2024 年资产体检表——五个问题、五组答案、四种质量标签。

横向条形按「体检五问」分组：钱在哪 / 谁欠我 / 我囤了什么 / 我买了什么重东西 / 有没有虚的。
每根柱子后面标出占资产总计的比例，颜色代表质量标签。

口径：主表科目取自 data/yili2024.json 的 balance（page_087~088）；
大额存单取自 data/yili2024_supplement.json（page_166、page_188）；
零星科目取自同文件的 balance_minor。
脚本开头会现场验算「流动资产各科目之和 = 流动资产合计」，不平就直接报错，绝不带病出图。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_RED,
)
from figures._data import load  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as mpatches  # noqa: E402

d = load("yili2024")
sup = load("yili2024_supplement")
B = d["balance"]
E = 1e8
TOT = B["total_assets"] / E
minor = sup["balance_minor"]

# ── 先验算，不平就不画 ────────────────────────────────────────
cur_sum = (B["cash"] + B["trading_financial_assets"]
           + minor["current_2024"]["衍生金融资产"]
           + B["notes_receivable"] + B["accounts_receivable"]
           + B["prepayments"] + B["other_receivables"]
           + B["inventory"] + B["noncurrent_assets_due_1y"]
           + B["other_current_assets"])
non_sum = (B["long_term_equity_investment"]
           + minor["noncurrent_2024"]["其他权益工具投资"]
           + minor["noncurrent_2024"]["其他非流动金融资产"]
           + minor["noncurrent_2024"]["投资性房地产"]
           + B["fixed_assets"] + B["construction_in_progress"]
           + B["productive_biological_assets"] + B["right_of_use_assets"]
           + B["intangible_assets"] + B["goodwill"]
           + minor["noncurrent_2024"]["长期待摊费用"]
           + B["deferred_tax_assets"] + B["other_noncurrent_assets"])
assert abs(cur_sum - B["total_current_assets"]) < 1, "流动资产科目加总对不上"
assert abs(non_sum - B["total_noncurrent_assets"]) < 1, "非流动资产科目加总对不上"

# 质量标签 → 颜色
Q = {"好": C_GREEN, "一般": C_BLUE, "要追附注": C_ORANGE, "警惕": C_RED}

dep_cur = d["notes"]["time_deposits_in_other_current_assets"] / E
dep_non = d["notes"]["time_deposits_in_other_noncurrent_assets"] / E
other_cur = B["other_current_assets"] / E - dep_cur   # 其他流动资产里除存单外的部分

groups = [
    ("① 钱在哪：能马上动用的有多少", [
        ("货币资金", B["cash"] / E, "好"),
        ("其他流动资产里的存单及定存", dep_cur, "好"),
        ("其他非流动资产里的存单及定存", dep_non, "好"),
        ("一年内到期的非流动资产", B["noncurrent_assets_due_1y"] / E, "要追附注"),
        ("其他流动资产里的其余项目", other_cur, "要追附注"),
    ]),
    ("② 谁欠我：赊出去的账", [
        ("应收账款", B["accounts_receivable"] / E, "好"),
        ("应收票据", B["notes_receivable"] / E, "好"),
        ("预付款项", B["prepayments"] / E, "一般"),
        ("其他应收款", B["other_receivables"] / E, "一般"),
    ]),
    ("③ 我囤了什么：存货", [
        ("存货", B["inventory"] / E, "一般"),
    ]),
    ("④ 我买了什么重东西：长期经营资产", [
        ("固定资产", B["fixed_assets"] / E, "一般"),
        ("在建工程", B["construction_in_progress"] / E, "一般"),
        ("无形资产", B["intangible_assets"] / E, "要追附注"),
        ("长期股权投资", B["long_term_equity_investment"] / E, "一般"),
        ("生产性生物资产", B["productive_biological_assets"] / E, "要追附注"),
        ("使用权资产", B["right_of_use_assets"] / E, "一般"),
        ("投资性房地产等零星", (
            minor["noncurrent_2024"]["投资性房地产"]
            + minor["noncurrent_2024"]["其他权益工具投资"]
            + minor["noncurrent_2024"]["其他非流动金融资产"]) / E, "要追附注"),
    ]),
    ("⑤ 有没有虚的：说不清能变多少钱", [
        ("商誉", B["goodwill"] / E, "警惕"),
        ("递延所得税资产", B["deferred_tax_assets"] / E, "警惕"),
        ("长期待摊费用", minor["noncurrent_2024"]["长期待摊费用"] / E, "警惕"),
    ]),
]

rows = []
for gname, items in groups:
    rows.append(("__group__", gname, 0.0, "#ffffff"))
    for name, v, q in items:
        rows.append((name, v, q, gname))

fig, ax = plt.subplots(figsize=(13.6, 10.6))

ys, vals, cols, names, is_group = [], [], [], [], []
y = 0.0
for row in rows:
    if row[0] == "__group__":
        ys.append(y)
        vals.append(0.0)
        cols.append("#ffffff")
        names.append(row[1])
        is_group.append(True)
        y += 1.05
    else:
        name, v, q, _ = row
        ys.append(y)
        vals.append(v)
        cols.append(Q[q])
        names.append(name)
        is_group.append(False)
        y += 0.94

ax.barh(ys, vals, height=0.62, color=cols, edgecolor="white", lw=0.6, zorder=3)

ax.set_yticks(ys)
ax.set_yticklabels(["" if g else n for g, n in zip(is_group, names)], fontsize=11)
ax.invert_yaxis()
ax.set_xlim(0, 405)
ax.set_xlabel("金额（亿元）", fontsize=11.5)
ax.set_title(f"伊利 2024 年资产体检：{TOT:,.2f} 亿元分成五组，逐项贴质量标签",
             fontsize=14.5, pad=16, weight="bold")
ax.grid(axis="x", color="#ececec", lw=0.8, zorder=0)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

for yy, v, nm, g in zip(ys, vals, names, is_group):
    if g:
        ax.text(2.5, yy, nm, va="center", ha="left", fontsize=12, weight="bold",
                color="#1a1a1a", zorder=6)
        continue
    ax.text(v + 4.5, yy, f"{v:,.2f}　{v / TOT * 100:.1f}%",
            va="center", ha="left", fontsize=10.2, color="#333333", zorder=6)

handles = [mpatches.Patch(color=c, label=f"质量标签：{k}") for k, c in Q.items()]
ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.01, 1.0),
          frameon=False, fontsize=10.5, title="怎么读颜色", title_fontsize=11)

fig.text(0.99, 0.005,
         "数据来源：伊利 2024 年报 page_087、page_166、page_188；"
         "百分比 = 科目金额 ÷ 资产总计",
         ha="right", va="bottom", fontsize=9.5, color=C_GRAY)

save(fig, "w03d5_asset_checkup.png")
