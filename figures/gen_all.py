# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""一键重新生成所有配图。

用法（仓库根目录）：
    python3 figures/gen_all.py

脚本按文件名排序依次运行；任何一张图失败都会在最后汇总并返回非 0。
"""
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
scripts = sorted(HERE.glob("gen_w*.py"))

if not scripts:
    print("还没有任何 gen_w*.py 脚本。")
    sys.exit(0)

failed = []
for s in scripts:
    print(f"==> {s.name}")
    r = subprocess.run([sys.executable, str(s)], cwd=HERE.parent)
    if r.returncode != 0:
        failed.append(s.name)

print()
if failed:
    print("以下脚本失败：")
    for f in failed:
        print("  ", f)
    sys.exit(1)
print(f"全部 {len(scripts)} 个脚本完成。图片在 figures/out/")
