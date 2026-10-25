#!/usr/bin/env python3
# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""批量生成某一周（或全部）的配图。

用法：
    python3 scripts/gen_week.py 3      # 只跑 figures/gen_w03d*.py
    python3 scripts/gen_week.py        # 跑全部 gen_w*.py

每个脚本用独立子进程运行；任何一个失败都会列出并以非 0 退出。
"""

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    week = int(sys.argv[1]) if len(sys.argv) > 1 else None
    pattern = f"gen_w{week:02d}d*.py" if week else "gen_w*.py"
    scripts = sorted((ROOT / "figures").glob(pattern))
    if not scripts:
        print(f"没有匹配 {pattern} 的脚本")
        return 1

    failed = []
    for s in scripts:
        print(f"==> {s.name}")
        r = subprocess.run([sys.executable, str(s)], cwd=ROOT)
        if r.returncode != 0:
            failed.append(s.name)

    print()
    if failed:
        print("以下脚本失败：")
        for f in failed:
            print("  ", f)
        return 1
    print(f"✅ {len(scripts)} 个脚本全部完成，图片在 figures/out/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
