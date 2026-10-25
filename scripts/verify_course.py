# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""课程一致性检查：目录、图片、数据出处、章节结构、ASCII 图禁令。

用法（仓库根目录）：
    python3 scripts/verify_course.py            # 全量检查
    python3 scripts/verify_course.py --week 3   # 只查第 3 周（SUMMARY 链接仍全量查）
    python3 scripts/verify_course.py --figures  # 只查图

年报原文目录（可选）：
    本仓库不包含年报原文（第三方版权材料），只包含从原文核实过的数据与页码引用。
    如果你想校验 `<!-- src: 目录/page_NNN.md -->` 是否指向真实存在的页面，
    把年报文本按同样结构放好，然后设置环境变量：

        export RAW_DIR=/path/to/your/annual-reports
        python3 scripts/verify_course.py

    未设置 RAW_DIR 时，该项检查会自动跳过（其余检查照常进行）。

检查项：
  1. SUMMARY.md 里的链接都存在；learning-guide/ 下的每个 .md 都被 SUMMARY 收录；
  2. 每章标题编号与文件名前缀一致（12-xxx.md → 第 12 章）；
  3. 每章必备结构：本章你将 / ✍️ 想一想 / 📎 数据出处 / 下一章；
  4. 正文引用的图都存在、alt 不为空；每张图都有对应的 gen_*.py 生成脚本；
  5. `<!-- src: 目录/page_NNN.md -->` 指向的年报页面真实存在（需 RAW_DIR）；
  6. 代码围栏之外禁止 ASCII 制表符画图（┌┐└┘├┤┬┴┼）；
  7. 每周 README 必备结构。
"""

import argparse
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
# 年报原文不在本仓库里（版权原因）。设置 RAW_DIR 才会校验 src 路径。
RAW = pathlib.Path(os.environ["RAW_DIR"]) if os.environ.get("RAW_DIR") else None

CHAPTER_RE = re.compile(r"^# 第 (\d+) 章：[^\n]+", re.M)
SRC_RE = re.compile(r"<!--\s*src:\s*([^>\n]+?)\s*-->")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
ASCII_BOX = set("┌┐└┘├┤┬┴┼")

REQUIRED_CHAPTER = ["> 本章你将：", "## ✍️ 想一想", "## 📎 数据出处", "下一章："]
REQUIRED_README = ["## 目录", "## 学完你会得到什么", "## 本周术语表", "下一站："]


def md_files(week=None):
    files = sorted(ROOT.glob("learning-guide/**/*.md"))
    if week is not None:
        tag = f"week{week:02d}"
        files = [f for f in files if tag in f.parts]
    return files


def is_appendix(path: pathlib.Path) -> bool:
    return path.name.startswith("appendix")


def summary_links():
    text = (ROOT / "SUMMARY.md").read_text(encoding="utf-8")
    return re.findall(r"\[[^\]]*\]\(([^)]+\.md)\)", text)


def check_summary(problems, week=None):
    """校验 SUMMARY.md 与实际文件是否一致。

    week 不为空时，只校验该周范围内的链接与文件（便于逐周交付）。
    """
    links = summary_links()
    listed = set()
    tag = f"week{week:02d}" if week else None
    for link in links:
        p = (ROOT / link).resolve()
        listed.add(p)
        if tag and tag not in p.parts:
            continue
        if not p.exists():
            problems.append(f"SUMMARY.md 链接指向不存在的文件：{link}")
    for f in md_files(week):
        if f.resolve() not in listed:
            problems.append(f"文件没有被 SUMMARY.md 收录：{f.relative_to(ROOT)}")
    return links


def check_chapter(path, problems):
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)

    m = CHAPTER_RE.search(text)
    if not m:
        problems.append(f"{rel}: 标题不是「# 第 N 章：标题」格式")
    else:
        num = int(m.group(1))
        prefix = path.name.split("-")[0]
        if not prefix.isdigit() or int(prefix) != num:
            problems.append(f"{rel}: 文件名前缀 {prefix} 与标题第 {num} 章不一致")

    for must in REQUIRED_CHAPTER:
        if must not in text:
            problems.append(f"{rel}: 缺少必备结构 {must!r}")

    if not re.search(r"^## 📎 数据出处\s*$", text, re.M):
        problems.append(f"{rel}: 「## 📎 数据出处」必须是二级标题独占一行")

    if not re.search(r"下一章：\[[^\]]+\]\([^)]+\.md\)", text):
        problems.append(f"{rel}: 结尾的「下一章：」必须是 markdown 链接")


def check_images(path, problems, png_refs):
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)
    for alt, target in IMG_RE.findall(text):
        if target.startswith("http"):
            continue
        if len(alt.strip()) < 10:
            problems.append(f"{rel}: 图片 alt 太短（{alt!r}），必须写清图在讲什么")
        p = (path.parent / target).resolve()
        if not p.exists():
            problems.append(f"{rel}: 图片不存在：{target}")
        png_refs.add(p)


def check_src(path, problems):
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)
    refs = []
    for block in SRC_RE.findall(text):
        refs.extend(block.split())
    if not refs:
        problems.append(f"{rel}: 没有任何 <!-- src: ... --> 数据出处注释")
    if RAW is None:
        # 没设置 RAW_DIR：本仓库不含年报原文，只做格式检查
        return
    for r in refs:
        if not (RAW / r).exists():
            problems.append(f"{rel}: 数据出处指向的年报页面不存在：{r}")


def check_ascii(path, problems):
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if any(ch in ASCII_BOX for ch in line):
            problems.append(
                f"{rel}:{lineno}: 代码围栏外出现 ASCII 制表符画图，坐标图请用 PNG"
            )
            break


def check_figures(problems, png_refs, week=None):
    figs = sorted((ROOT / "figures" / "out").glob("*.png"))
    if week is not None:
        figs = [f for f in figs if f.name.startswith(f"w{week:02d}d")]
    scripts = list((ROOT / "figures").glob("gen_*.py"))
    script_text = "\n".join(s.read_text(encoding="utf-8") for s in scripts)
    out_dir = (ROOT / "figures" / "out").resolve()
    for png in figs:
        if png.stem not in script_text:
            problems.append(f"图片没有对应的生图脚本：{png.name}")
        if png.resolve() not in png_refs:
            problems.append(f"图片已生成但正文没有引用：{png.name}")
    for png in png_refs:
        if not png.exists():
            continue
        if png.parent != out_dir:
            problems.append(f"图片不在 figures/out/ 下：{png}")


def check_readme_week(path, problems):
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)
    for must in REQUIRED_README:
        if must not in text:
            problems.append(f"{rel}: 缺少必备结构 {must!r}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int, default=None, help="只检查某一周")
    ap.add_argument("--figures", action="store_true", help="只检查图")
    args = ap.parse_args()

    problems = []
    png_refs = set()

    if not args.figures:
        check_summary(problems, args.week)

    files = md_files(args.week)
    chapters = [
        f for f in files if f.name != "README.md" and not is_appendix(f)
    ]
    for f in chapters:
        if not args.figures:
            check_chapter(f, problems)
            check_src(f, problems)
            check_ascii(f, problems)
        check_images(f, problems, png_refs)

    if not args.figures:
        for f in files:
            if f.name == "README.md":
                check_readme_week(f, problems)

    check_figures(problems, png_refs, args.week)

    scope = f"第 {args.week} 周" if args.week else "全部"
    if problems:
        print(f"❌ {scope}：共 {len(problems)} 个问题：\n")
        for p in problems:
            print("  -", p)
        return 1
    print(
        f"✅ {scope}检查通过：{len(chapters)} 章、"
        f"{len(list((ROOT / 'figures' / 'out').glob('*.png')))} 张图、"
        f"{len(summary_links())} 条目录链接"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
