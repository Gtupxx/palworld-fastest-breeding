import sys
import json
from collections import deque, defaultdict

# # === 加载配种表 ===
# with open('json/parents_en.json', 'r', encoding='utf-8') as f:
#     breed_data = json.load(f)

# # === 加载中英文对照表 ===
# with open('json/zh_en_map.json', 'r', encoding='utf-8') as f:
#     zh_en_map = json.load(f)
# === 加载配种表 ===
with open("json\\v1.0\\breeding_map.json", "r", encoding="utf-8") as f:
    breed_data = json.load(f)

# === 加载中英文对照表 ===
with open("json\\v1.0\\pal_name_map.json", "r", encoding="utf-8") as f:
    zh_en_map = json.load(f)

en_zh_map = {v: k for k, v in zh_en_map.items()}


def to_en(name):
    return zh_en_map.get(name, name)


def to_zh(name):
    return en_zh_map.get(name, name)


# === 构建 子代 -> 父母组合 的反向图 ===
child_to_parents = defaultdict(list)

for child, combos in breed_data.items():
    for combo in combos:
        p1 = combo.get("A")
        p2 = combo.get("B")
        if p1 and p2:
            child_to_parents[child].append((p1, p2))

# === BFS 逆向追踪路径 ===
from collections import deque, defaultdict

from collections import deque, defaultdict


def reverse_breeding_paths(start, target):

    queue = deque([(target, [])])

    visited = set()

    shortest_length = float("inf")

    results = []

    while queue:

        current, path = queue.popleft()

        # 超过最短路径不用搜索
        if len(path) > shortest_length:
            continue

        # 找到目标
        if current == start:

            if len(path) < shortest_length:

                shortest_length = len(path)
                results = [path]

            elif len(path) == shortest_length:

                results.append(path)

            continue

        # 当前生物的所有父母组合
        for p1, p2 in child_to_parents.get(current, []):

            # 排序只是为了显示稳定
            # 不影响 A+B 和 B+A
            parents = tuple(sorted([p1, p2]))

            state = (current, parents)

            if state in visited:
                continue

            visited.add(state)

            new_path = path + [(p1, p2, current)]

            # 继续寻找两个父母来源

            queue.append((p1, new_path))

            queue.append((p2, new_path))

    return results


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: BFS.py 起始生物 目标生物")
        sys.exit(1)

    # === 中文输入来自命令行参数 ===
    zh_start = sys.argv[1].strip()
    zh_target = sys.argv[2].strip()

    start = to_en(zh_start)
    target = to_en(zh_target)

    paths = reverse_breeding_paths(start, target)

    # === 输出结果 ===
    if paths:
        print(f"从『{zh_start}』到『{zh_target}』的最短配种链路如下：\n")
        for path in paths:
            for p1, p2, child in path[::-1]:
                print(f"{to_zh(p1)} + {to_zh(p2)} → {to_zh(child)}")
            print("-----------")
    else:
        print(f"无法找到从『{zh_start}』配种到『{zh_target}』的路径")
