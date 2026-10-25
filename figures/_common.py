# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""生图脚本公共设施：中文字体、输出目录、概念图常用的方框/箭头/标注函数。

每个 gen_*.py 脚本开头固定写：

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    from figures._common import OUT, save, fig_ax, fig_multi, box, arrow, label, ...

脚本可以独立运行（python3 figures/gen_w01d2_xxx.py），也可以被 gen_all.py 统一运行。

════════════════════════════════════════════════════════════════════════
图片质量硬要求（每次交付前必须自查，这是流程的一部分，不许跳过）
════════════════════════════════════════════════════════════════════════
1. 文字不遮挡文字、文字不遮挡线条、线条不遮挡文字、线条不遮挡线条；
2. 所有压在图形上的标注一律带白色衬底（本文件的 label() 已内置）；
3. 元素之间留足间距；放不下就加 figsize 或缩小字号，绝不许硬挤；
4. 生成后用 read_image 工具亲自看一遍，发现任何一类遮挡就改脚本重跑，
   直到干净为止；
5. 坐标、比例、排序这类「精确」信息一律用 PNG，禁止 ASCII 图。

几个经验数（本项目统一采用）：
- 单栏概念图：fig_ax(12, 7) 起；
- 数值条形图：figsize=(11, 6.5) 起，字号 title 14 / 轴标签 11.5 / 标注 11；
- 柱顶标注与柱顶留 1.5% 轴高的空隙；
- 图例用 loc="upper left" 且 bbox_to_anchor=(1.02, 1)，放图外，避免压柱子。
"""

import pathlib

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "figures" / "out"
DATA = ROOT / "data"

# 中文字体：按优先级回退。macOS 上 Arial Unicode MS / PingFang / Hiragino 都能用。
plt.rcParams["font.sans-serif"] = [
    "Arial Unicode MS",
    "PingFang SC",
    "PingFang HK",
    "Hiragino Sans GB",
    "STHeiti",
    "Songti SC",
]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["savefig.facecolor"] = "white"
plt.rcParams["font.size"] = 11.5

# 统一配色（全课程共用，同一含义用同一颜色）
C_BLUE = "#1f77b4"      # 主色：收入/资产
C_ORANGE = "#ff7f0e"    # 次色：成本/费用
C_GREEN = "#2ca02c"     # 正向：利润/现金流入
C_RED = "#d62728"       # 负向：减值/亏损/警示
C_GRAY = "#7f7f7f"      # 中性：辅助线/注释
C_PURPLE = "#9467bd"    # 结果：净利润/权益
C_BROWN = "#8c564b"
C_GOLD = "#b8860b"

# 浅色填充（和上面的主色配套）
F_BLUE = "#eef4fb"
F_ORANGE = "#fdf3e7"
F_GREEN = "#eef7ee"
F_RED = "#fbeaea"
F_GRAY = "#f2f2f2"
F_PURPLE = "#f2eef8"


def save(fig, name: str, dpi: int = 160):
    """保存图片到 figures/out/，并关闭画布。

    name 必须与脚本一一对应：gen_w{周}d{章}_{主题}.py → w{周}d{章}_{主题}.png。
    """
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved {path.relative_to(ROOT)}")


def fig_ax(width=10, height=6, xlim=(0, 10), ylim=(0, 10)):
    """新建一幅白底画布，返回 (fig, ax)；默认关闭坐标轴，坐标范围 0~10。"""
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def fig_multi(rows, cols, width=12, height=6):
    """新建多子图画布，返回 (fig, axes)；axes 为按行展平的列表。

    ⚠️ 本函数不会设置坐标范围。用每个子图前先手动 set_xlim/set_ylim。
    """
    fig, axes = plt.subplots(rows, cols, figsize=(width, height))
    flat = list(axes.flat) if hasattr(axes, "flat") else [axes]
    for ax in flat:
        ax.axis("off")
    return fig, flat


def box(ax, x, y, w, h, text, fc=F_BLUE, ec=C_BLUE, fontsize=12,
        tc="#222222", lw=1.6, style="round,pad=0.02,rounding_size=0.15",
        weight="normal", zorder=3):
    """画一个带文字的圆角方框（x, y 为左下角，w/h 为宽高）。

    文字居中；需要多行时在 text 里用 \\n（行距由 linespacing 控制）。
    """
    import matplotlib.patches as mpatches

    rect = mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle=style, fc=fc, ec=ec, lw=lw, zorder=zorder
    )
    ax.add_patch(rect)
    ax.text(
        x + w / 2, y + h / 2, text, ha="center", va="center",
        fontsize=fontsize, color=tc, weight=weight, zorder=zorder + 2,
        linespacing=1.5,
    )
    return rect


def arrow(ax, xy_from, xy_to, color=C_GRAY, lw=1.8, style="-|>",
          connectionstyle=None, ls="-", zorder=2, shrinkA=6, shrinkB=6):
    """画一支箭头（默认两端各留 6pt 空隙，避免箭头戳进方框或压住文字）。"""
    ax.annotate(
        "",
        xy=xy_to,
        xytext=xy_from,
        arrowprops=dict(
            arrowstyle=style,
            color=color,
            lw=lw,
            linestyle=ls,
            shrinkA=shrinkA,
            shrinkB=shrinkB,
            mutation_scale=16,
            connectionstyle=connectionstyle or "arc3,rad=0",
        ),
        zorder=zorder,
    )


def label(ax, x, y, text, color="#222222", fontsize=12, ha="center",
          va="center", weight="normal", zorder=6, alpha=0.92,
          pad=0.3, fc="white"):
    """放一段带白色衬底的文字（衬底把压在下面的线条垫掉，避免糊成一团）。"""
    ax.text(
        x, y, text, color=color, fontsize=fontsize, ha=ha, va=va,
        weight=weight, zorder=zorder, linespacing=1.5,
        bbox=dict(boxstyle=f"round,pad={pad}", fc=fc, ec="none", alpha=alpha),
    )


def bar_labels(ax, bars, values, fmt=lambda v: f"{v:,.0f}", dy_frac=0.015,
               fontsize=11.5, color="#333333", weight="bold", inside=False,
               inside_color="white"):
    """在柱子顶部（或柱内）统一标注数值，自动留出空隙，避免压住柱体。

    inside=True 时标在柱体内部靠上位置（适合柱子很矮、外部空间不足的情况）。
    """
    y0, y1 = ax.get_ylim()
    span = y1 - y0
    for b, v in zip(bars, values):
        x = b.get_x() + b.get_width() / 2
        top = b.get_y() + b.get_height()
        if inside:
            y = b.get_y() + b.get_height() * 0.82
            va = "top"
            col = inside_color
        else:
            y = top + span * dy_frac
            va = "bottom"
            col = color
        ax.text(x, y, fmt(v), ha="center", va=va, fontsize=fontsize,
                color=col, weight=weight, zorder=6)


def yi(v, digits=1):
    """把「元」快速换算成「亿元」字符串，方便图注与文案统一口径。"""
    return f"{v / 1e8:,.{digits}f} 亿"


def pct(x, digits=1):
    """小数转百分数字符串（0.3388 → '33.9%'）。"""
    return f"{x * 100:.{digits}f}%"


def legend_outside(ax, **kwargs):
    """把图例放到坐标区外面，避免压住柱子或折线。"""
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0),
              frameon=False, **kwargs)


def clean_axes(ax):
    """去掉上、右两条边框，保留左、下，让数值图更干净。"""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


# ══════════════════════════════════════════════════════════════════════
# 瀑布图：利润表逐行拆解、商誉「原值—减值—净额」桥、现金流桥都用它。
# 用法：
#     from figures._common import waterfall
#     waterfall(ax, [
#         ("营业收入", 1153.93, "total"),
#         ("营业成本", -762.99, "down"),
#         ("毛利",      390.94, "total"),
#     ], unit="亿元")
# ══════════════════════════════════════════════════════════════════════
def waterfall(ax, steps, unit="", fmt="{:,.2f}", fontsize=11,
              total_color=None, up_color=None, down_color=None,
              connector_color="#8c8c8c", connector_lw=1.0,
              label_gap_frac=0.022, ylim_head_frac=0.14, bar_width=0.56,
              rotate_labels=0, title=None):
    """画一张瀑布图。

    参数
    ----
    steps : list[tuple[str, float, str]]
        每一项是 (标签, 数值, 类型)：
        - 类型 "total"：一根从 0 画起的完整柱子（数值即高度）；
        - 类型 "up"   ：从当前累计位置向上长 value（value 应为正数）；
        - 类型 "down" ：从当前累计位置向下长 abs(value)（value 可正可负）。
    unit : 轴单位后缀，如 "亿元"，会写进 y 轴标签。
    fmt  : 数值标注格式。

    返回 (bars, values) —— bars 供进一步加工，values 是实际画出的高度。
    """
    mpl_colors = {
        "total": total_color or C_BLUE,
        "up": up_color or C_GREEN,
        "down": down_color or C_RED,
    }

    xs, bottoms, heights, values, kinds = [], [], [], [], []
    running = 0.0
    for i, (lab, val, kind) in enumerate(steps):
        if kind == "total":
            bottom, height = 0.0, float(val)
            running = float(val)
        elif kind == "up":
            bottom, height = running, abs(float(val))
            running += abs(float(val))
        elif kind == "down":
            bottom, height = running - abs(float(val)), abs(float(val))
            running -= abs(float(val))
        else:
            raise ValueError(f"未知类型 {kind!r}，只能是 total / up / down")
        xs.append(i)
        bottoms.append(bottom)
        heights.append(height)
        values.append(float(val))
        kinds.append(kind)

    bars = ax.bar(xs, heights, bottom=bottoms, width=bar_width,
                  color=[mpl_colors[k] for k in kinds],
                  edgecolor="white", linewidth=0.8, zorder=3)

    # 连接线：从前一根柱子的"落点"水平连到下一根柱子的起点
    for i in range(len(steps) - 1):
        cur_top = bottoms[i] + heights[i] if kinds[i] != "down" else bottoms[i]
        if kinds[i] == "total":
            cur_top = bottoms[i] + heights[i]
        nxt = bottoms[i + 1] + heights[i + 1] if kinds[i + 1] == "down" else bottoms[i + 1]
        if kinds[i + 1] == "total":
            nxt = 0.0
        ax.plot([xs[i] + bar_width / 2, xs[i + 1] - bar_width / 2],
                [cur_top, cur_top], color=connector_color,
                lw=connector_lw, ls=(0, (3, 3)), zorder=2)

    # 先定 y 轴范围，再标数值，保证留白比例一致
    top = max(b + h for b, h in zip(bottoms, heights))
    bot = min(bottoms)
    span = max(top - bot, 1e-9)
    ax.set_ylim(bot - span * 0.10, top + span * ylim_head_frac)

    for i, (b, h, v, k) in enumerate(zip(bottoms, heights, values, kinds)):
        y = b + h + (ax.get_ylim()[1] - ax.get_ylim()[0]) * label_gap_frac
        txt = fmt.format(v) if k == "total" else (
            "+" + fmt.format(abs(v)) if k == "up" else "−" + fmt.format(abs(v)))
        ax.text(i, y, txt, ha="center", va="bottom", fontsize=fontsize,
                color="#222222", weight="bold" if k == "total" else "normal",
                zorder=6)

    ax.set_xticks(xs)
    ax.set_xticklabels([s[0] for s in steps], fontsize=fontsize,
                       rotation=rotate_labels,
                       ha="right" if rotate_labels else "center")
    ax.axhline(0, color="#999999", lw=1.0, zorder=1)
    ax.set_ylabel(f"金额（{unit}）" if unit else "金额", fontsize=11.5)
    if title:
        ax.set_title(title, fontsize=14, pad=12)
    clean_axes(ax)
    return bars, values


# ══════════════════════════════════════════════════════════════════════
# 堆叠条：资产结构、负债结构、费用占比都用它。
# 窄分段（占比 < min_inside）自动改成「外置标签 + 引线」，绝不把字塞进挤不下的格子里。
# 用法：
#     from figures._common import stacked_bar
#     stacked_bar(ax, [("货币资金", 254.04, C_BLUE), ("存货", 107.45, C_GREEN)],
#                 total=1537.18, title="伊利 2024 年资产结构（亿元）")
# ══════════════════════════════════════════════════════════════════════
def stacked_bar(ax, segments, total=None, y=4.6, height=1.1, x0=0.6, width=8.8,
                unit="", min_inside=0.16, fontsize=10.5, pct_digits=1,
                upper_y=7.4, lower_y=2.6, title=None, subtitle=None,
                show_value=True, show_pct=True, char_scale=0.024):
    """画一根 100% 堆叠条；窄分段自动外置标注，避免文字压文字。

    segments : list[tuple[str, float, str]]
        (标签, 数值, 颜色)。数值单位随意，按 total 折算成占比。
    total : 归一化基准。为 None 时取各段之和。
    min_inside : 占比小于该值的段，标签移到条形外（上下交替放置 + 引线）。

    返回实际使用的 total。
    """
    import matplotlib.patches as mpatches

    if total is None:
        total = sum(s[1] for s in segments)
    widths = [s[1] / total for s in segments]
    xs = x0
    inside, outside = [], []
    for (name, val, color), wfrac in zip(segments, widths):
        w = width * wfrac
        ax.add_patch(mpatches.Rectangle((xs, y), w, height, facecolor=color,
                                        edgecolor="white", lw=1.2, zorder=3))
        cx = xs + w / 2
        # 两道门槛：占比够大，且色块物理宽度容得下最长那行字，才允许写在格子里
        label_w = _text_width(name, val, wfrac, unit, show_value, show_pct,
                              pct_digits, char_scale)
        if wfrac >= min_inside and label_w <= w * 0.92:
            txt = name if not (show_value or show_pct) else name + "\n" + _seg_num(
                val, wfrac, unit, show_value, show_pct, pct_digits)
            ax.text(cx, y + height / 2, txt, ha="center", va="center",
                    color="white", fontsize=fontsize, weight="bold",
                    linespacing=1.35, zorder=5)
        elif wfrac >= 0.055:
            # 中等分段：塞得下名字，数值挪到外面（只留名字，避免压边）
            ax.text(cx, y + height / 2, name, ha="center", va="center",
                    color="white", fontsize=fontsize - 0.5, weight="bold",
                    zorder=5)
            outside.append((name, val, wfrac, color, cx, True))
        else:
            outside.append((name, val, wfrac, color, cx, False))
        xs += w

    # 窄分段：上下交替外置，带引线
    for i, (name, val, wfrac, color, cx, name_inside) in enumerate(outside):
        up = (i % 2 == 0)
        ty = upper_y if up else lower_y
        num = _seg_num(val, wfrac, unit, show_value, show_pct, pct_digits)
        txt = num if name_inside else (name + " " + num)
        ax.annotate(
            txt, xy=(cx, y + height if up else y), xytext=(cx, ty),
            ha="center", va="bottom" if up else "top",
            fontsize=fontsize - 0.5, color=color, weight="bold",
            zorder=6,
            bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=color,
                      lw=0.9, alpha=0.95),
            arrowprops=dict(arrowstyle="-", color=color, lw=0.9,
                            shrinkA=2, shrinkB=2),
        )

    if title:
        ax.text(x0, upper_y + 1.05, title, fontsize=13.5, weight="bold",
                ha="left", va="bottom", zorder=6)
    if subtitle:
        ax.text(x0, y - 0.95, subtitle, fontsize=10.2, color="#555555",
                ha="left", va="top", zorder=6)
    return total


def _text_width(name, val, wfrac, unit, show_value, show_pct, pct_digits,
                char_scale):
    """粗估标签最宽那行的宽度（数据坐标单位）。

    中文按 1 个字宽、ASCII 按 0.55 个字宽估算；char_scale 是「一个字号 ≈ 多少数据单位」，
    由调用方按画布尺寸给，宁可高估一点（高估只会让标签外移，不会压边）。
    """
    num = _seg_num(val, wfrac, unit, show_value, show_pct, pct_digits)
    lines = [name, num] if (show_value or show_pct) else [name]
    widest = 0.0
    for ln in lines:
        w = 0.0
        for ch in ln:
            w += 1.0 if ord(ch) > 0x2E80 else 0.55
        widest = max(widest, w)
    return widest * char_scale


def _seg_num(val, wfrac, unit, show_value, show_pct, pct_digits):
    """拼一个分段的数值说明：'254 亿元 · 16.5%'。"""
    bits = []
    if show_value:
        bits.append(f"{val:,.1f}{unit}" if unit else f"{val:,.1f}")
    if show_pct:
        bits.append(f"{wfrac * 100:.{pct_digits}f}%")
    return " · ".join(bits)

