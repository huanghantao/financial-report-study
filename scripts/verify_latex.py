# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""LaTeX 转换规范性检查（全仓库正文）。

检查 learning-guide/ 与根 README.md：
  1. 剥离代码围栏 / 行内代码 / 图片 / 链接文字之后，剩余正文中的 $ 必须成对
     （行内 $...$ 同行闭合；$$ 成对）；
  2. 正文不得残留 Unicode 数学字符；
  3. 正文不得残留制表符矩阵边框；
  4. 公式内换行必须写四个反斜杠 \\\\；
  5. 不得出现会被 Markdown 吃掉的 \\; \\, \\: \\| \\{ \\} \\! \\~ 写法。

用法：python3 scripts/verify_latex.py
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

# 正文不允许残留的 Unicode 数学字符（代码块/行内代码/图片 alt 中豁免）
# 注意：间隔号 "·" 不在此列 —— 它单独检查：夹在两个 CJK 字符之间视为中文人名
# 标点（如"沃伦·巴菲特"）放行；其余位置（数学语境）一律要求改写为 \cdot。
BANNED = set("×≈≠≤≥√∑∏λθαβγεΣΠΔ¹²³⁰ᵀ⁻½⅓⅔¼₁₂⇔−")


def is_cjk(ch: str) -> bool:
    return "\u4e00" <= ch <= "\u9fff"


def strip_protected(text: str) -> str:
    """去掉代码围栏、行内代码、图片、链接显示文字，返回「纯正文」。"""
    text = re.sub(r"```[^\n]*\n.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    text = re.sub(r"`[^`]*`", "", text)
    return text


def check_file(path: pathlib.Path) -> list:
    problems = []
    text = path.read_text(encoding="utf-8")
    prose = strip_protected(text)

    # 换行反斜杠检查：公式换行在 md 源里必须写 \\\\（四个反斜杠），
    # 否则 Markdown 吃掉一层后 MathJax 收不到换行，多行公式挤成一行。
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.search(r"(\\+)\s*$", line)
        if m and len(m.group(1)) % 4 != 0:
            problems.append(
                f"  第 {lineno} 行行尾反斜杠数 {len(m.group(1))} 会被 Markdown 吃掉一层："
                f"{line.strip()[:60]}"
            )

    # $ 成对（$$ 也满足偶数个 $）；行内必须同行闭合
    for lineno, line in enumerate(prose.splitlines(), 1):
        n = line.count("$")
        if n % 2 == 1:
            problems.append(f"  第 {lineno} 行 $ 数量为奇数：{line.strip()[:60]}")
    if prose.count("$$") % 2 == 1:
        problems.append("  $$ 不配对")

    # 制表符矩阵残留
    if re.search(r"[┌┐└┘│]", prose):
        problems.append("  残留制表符矩阵边框（┌┐└┘│）")

    # 单反斜杠 + ASCII 标点：mdBook 的 Markdown 解析器会吃掉反斜杠
    eaten = sorted(set(re.findall(r"(?<!\\)\\[;,:|{}!~]", prose)))
    if eaten:
        problems.append(
            f"  会被 Markdown 吃掉反斜杠的写法：{' '.join(eaten)}"
            "（间距请用 \\ ，范数请用 \\Vert，集合括号请用 \\lbrace \\rbrace）"
        )

    # }_{ ：下划线紧跟在标点 } 后面会被 Markdown 当成强调。
    # 但 \underbrace{...}_{...} 这类在数学环境里合法，只在数学定界符之外告警。
    outside_math = re.sub(r"\$\$.*?\$\$", "", prose, flags=re.DOTALL)
    outside_math = re.sub(r"\$[^$]*\$", "", outside_math)
    if "}_{" in outside_math:
        problems.append("  出现 }_{：会被 Markdown 当成下划线强调，请写 }\\_{")

    # Unicode 数学字符残留
    leftover = sorted({c for c in prose if c in BANNED})

    # 间隔号 "·"：两侧都是 CJK 才算人名标点放行
    for i, ch in enumerate(prose):
        if ch == "·":
            prev_ok = i > 0 and is_cjk(prose[i - 1])
            next_ok = i + 1 < len(prose) and is_cjk(prose[i + 1])
            if not (prev_ok and next_ok):
                # 允许「中文 · 中文」这类列表分隔符（前后可能带空格）
                left = prose[max(0, i - 2):i].strip()
                right = prose[i + 1:i + 3].strip()
                if not (left and right and is_cjk(left[-1]) and is_cjk(right[0])):
                    leftover.append("·")
                    break

    if leftover:
        problems.append(f"  残留 Unicode 数学字符：{''.join(sorted(set(leftover)))}")

    return problems


def main():
    files = sorted(ROOT.glob("learning-guide/**/*.md")) + [ROOT / "README.md"]
    files = [f for f in files if f.exists()]
    total = 0
    for f in files:
        problems = check_file(f)
        if problems:
            total += len(problems)
            print(f"✗ {f.relative_to(ROOT)}")
            for p in problems:
                print(p)
    if total == 0:
        print(f"✅ 全部 {len(files)} 个文件 LaTeX 规范检查通过")
        return 0
    print(f"❌ 共 {total} 个问题")
    return 1


if __name__ == "__main__":
    sys.exit(main())
