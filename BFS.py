import sys
import json
from collections import deque, defaultdict

# === 加载配种表 ===
with open('json/parents_en.json', 'r', encoding='utf-8') as f:
    breed_data = json.load(f)

# === 加载中英文对照表 ===
with open('json/zh_en_map.json', 'r', encoding='utf-8') as f:
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

def reverse_breeding_paths(start, target):
    queue = deque([(target, [])])  # 初始队列包含目标生物与空路径
    visited = set()  # 记录已经访问过的节点
    paths = defaultdict(list)  # 存储每个节点的最短路径
    
    # 路径追踪的深度
    shortest_path_length = float('inf')
    
    # 已经作为父本出现的节点
    fathers = set()

    while queue:
        current, path = queue.popleft()

        # 如果当前路径长度大于已知的最短路径长度，则不继续扩展
        if len(path) > shortest_path_length:
            continue

        # 如果找到了目标，更新最短路径长度
        if current == start:
            if len(path) < shortest_path_length:
                shortest_path_length = len(path)
                paths[current] = [path]  # 如果找到新的最短路径，清空旧路径
            elif len(path) == shortest_path_length:
                paths[current].append(path)

        # 扩展当前节点
        for p1, p2 in child_to_parents.get(current, []):
            # 避免 target 自己作为父母参与后续路径
            if target in (p1, p2):
                continue 

            # 如果父本还没出现过，将 p1 设为父本
            if p1 not in fathers and p2 not in fathers:
                # 选择父本和母本，父本放到 p1，母本放到 p2
                p1, p2 = (p1, p2) if p1 < p2 else (p2, p1)
                fathers.add(p1)
                fathers.add(p2)
            elif p1 in fathers:  # 如果 p1 是父本，p2 就是母本
                p1, p2 = p1, p2
            else:  # 如果 p2 是父本，p1 就是母本
                p1, p2 = p2, p1

            # 避免重复访问
            if (p1, p2) not in visited:
                visited.add((p1, p2))
                queue.append((p1, path + [(p1, p2, current)]))
                queue.append((p2, path + [(p1, p2, current)]))

    return paths[start]


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
