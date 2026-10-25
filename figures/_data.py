# 许可：本文件适用 MIT License（见仓库根目录 LICENSE）。
"""读取 data/ 下已核实的真实财报数据。

用法：
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    from figures._data import load, yi, pct

    d = load("yili2024")
    rev = d["income"]["revenue"]

约定：
- 所有金额单位统一为「元」（港股年报里的「千元」已在 JSON 中换算成元）；
- 每个小节的 key 都是英文，中文名写在 data/*.md 的对照表里；
- **图中出现的真实数字必须来自这里**，不许图省事手打。
"""

import json
import pathlib

DATA = pathlib.Path(__file__).resolve().parents[1] / "data"


def load(name: str) -> dict:
    """加载 data/<name>.json。name 不带 .json 后缀。"""
    path = DATA / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"找不到数据文件 {path}；先在 data/ 下补齐并核实")
    return json.loads(path.read_text(encoding="utf-8"))


def get(d: dict, *keys, default=None):
    """安全地按路径取值：get(d, "income", "revenue")。"""
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur
