# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""第 1 周第 2 章配图：一份年报的披露链条——谁写、谁查、谁接收、谁看。

四道环节 + 三道闸门，底部给出伊利 2024 年报里可核对的真实落点。
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from figures._common import (  # noqa: E402
    save, fig_ax, box, arrow, label,
    C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_PURPLE, C_RED,
    F_BLUE, F_ORANGE, F_GREEN, F_GRAY, F_PURPLE, F_RED,
)
from figures._data import load  # noqa: E402

d = load("yili2024")
rev = d["income"]["revenue"] / 1e8  # 1,153.93

fig, ax = fig_ax(13.6, 9.2, xlim=(0, 100), ylim=(0, 100))

ax.text(50, 96.5, "管理层写 → 审计师查 → 交易所挂网 → 你翻开",
        ha="center", va="center", fontsize=15, weight="bold", color="#1a1a1a")
ax.text(50, 92.0, "四步里任何一步出问题，年报都不可信；三道闸门就是为这一步一步设的",
        ha="center", va="center", fontsize=11.2, color=C_GRAY)

# ── 四个环节 ────────────────────────────────────────────────
w, h = 21.0, 18
xs = [2.5, 26.5, 50.5, 74.5]
ys = 67
stages = [
    ("① 董事会 / 管理层", "编报表、写 MD&A\n签字背书：真实、准确、完整", F_BLUE, C_BLUE),
    ("② 会计师事务所", "信永中和\n出具「标准无保留意见」", F_GREEN, C_GREEN),
    ("③ 交易所", "上交所\n格式审查、挂网披露", F_ORANGE, C_ORANGE),
    ("④ 投资者", "你\n免费下载，逐页读", F_PURPLE, C_PURPLE),
]
for x, (title, body, fc, ec) in zip(xs, stages):
    box(ax, x, ys, w, h, "", fc=fc, ec=ec, lw=1.8)
    ax.text(x + w / 2, ys + h - 3.6, title, ha="center", va="center",
            fontsize=12.2, weight="bold", color="#1a1a1a")
    ax.text(x + w / 2, ys + h / 2 - 4.2, body, ha="center", va="center",
            fontsize=10.8, color="#333333", linespacing=1.6)

for i in range(3):
    arrow(ax, (xs[i] + w + 0.6, ys + h / 2), (xs[i + 1] - 0.6, ys + h / 2),
          color=C_GRAY, lw=2.0)

# ── 三道闸门 ────────────────────────────────────────────────
gates = [
    (12.7, "闸门一：董事会声明",
     "page_002 重要提示：\n「保证……不存在虚假记载」"),
    (40.0, "闸门二：审计意见",
     "page_083：标准无保留意见\n关键审计事项＝收入确认"),
    (67.5, "闸门三：监管格式",
     "章节顺序、财务指标口径、\n非经常性损益专表都有规定"),
]
for x, title, body in gates:
    box(ax, x - 11.0, 33.0, 22.0, 15.0, "", fc=F_RED, ec=C_RED, lw=1.5)
    ax.text(x, 44.8, title, ha="center", va="center",
            fontsize=11.2, weight="bold", color=C_RED)
    ax.text(x, 37.8, body, ha="center", va="center",
            fontsize=10.2, color="#333333", linespacing=1.6)
    arrow(ax, (x, ys - 0.6), (x, 48.6), color=C_RED, lw=1.5, ls=(0, (4, 3)))

ax.text(50, 53.0, "三道闸门，各管一段", ha="center", va="center",
        fontsize=12.0, weight="bold", color="#1a1a1a")

# ── 说明与落点 ──────────────────────────────────────────────
label(ax, 50, 28.0,
      "「标准无保留意见」不是夸公司好，只是说：以审计师看到的证据，报表没有重大错报。",
      fontsize=10.6, color=C_RED, ha="center")

ax.text(50, 20.5, "伊利 2024 年报里，这条链留下了三个可核对的痕迹：",
        ha="center", va="center", fontsize=11.0, color="#333333")

box(ax, 4, 4.5, 27, 11.5,
    "签字页（page_092 末尾）\n潘刚 · 赵成霞 · 邹赢", fc=F_GRAY, ec=C_GRAY, fontsize=10.5)
box(ax, 36.5, 4.5, 27, 11.5,
    "审计报告（page_083）\nXYZH/2025XAAA4B0186", fc=F_GRAY, ec=C_GRAY, fontsize=10.5)
box(ax, 69, 4.5, 27, 11.5,
    f"关键审计事项（page_083）\n营业收入 {rev:,.2f} 亿元", fc=F_GRAY, ec=C_GRAY, fontsize=10.5)

ax.text(99, 0.8, "数据来源：伊利 2024 年报 page_002、page_083、page_092",
        ha="right", va="center", fontsize=9.3, color=C_GRAY)

save(fig, "w01d2_disclosure_chain.png")
