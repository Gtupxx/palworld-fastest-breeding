import json
from collections import deque, defaultdict
import streamlit as st
import streamlit.components.v1 as components

# === 加载配种表 ===
with open('json/parents_en.json', 'r', encoding='utf-8') as f:
    breed_data = json.load(f)

# === 加载中英文对照表 ===
with open('json/zh_en_map.json', 'r', encoding='utf-8') as f:
    zh_en_map = json.load(f)

en_zh_map = {v: k for k, v in zh_en_map.items()}

# === 图床头像地址映射 ===
def get_image_url(name_en):
    return f"https://www.palworldbreed.com/images/{name_en}.webp"

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
def reverse_breeding_paths(start, target):
    queue = deque([(target, [])])
    visited = set()
    paths = defaultdict(list)
    shortest_path_length = float('inf')

    while queue:
        current, path = queue.popleft()
        if len(path) > shortest_path_length:
            continue
        if current == start:
            if len(path) < shortest_path_length:
                shortest_path_length = len(path)
                paths[current] = [path]
            elif len(path) == shortest_path_length:
                paths[current].append(path)
        for p1, p2 in child_to_parents.get(current, []):
            if (p1, p2) not in visited:
                visited.add((p1, p2))
                queue.append((p1, path + [(p1, p2, current)]))
                queue.append((p2, path + [(p1, p2, current)]))
    return paths[start]

# === 生成 Mermaid 图的函数（正圆头像+名字下方） ===
def create_mermaid_chart(path):
    mermaid_code = "graph LR\n"
    rendered_nodes = set()

    for p1, p2, child in path:
        for entity in [p1, p2, child]:
            if entity not in rendered_nodes:
                img_url = get_image_url(entity)
                name = to_zh(entity)
                mermaid_code += (
                    f'    {entity}(["<div style=\'text-align:center;\'><img src=\'{img_url}\' '
                    f'style=\'border-radius:50%;width:60px;height:60px;\'/><br>{name}</div>"])\n'
                )
                rendered_nodes.add(entity)

        mermaid_code += f"    {p1} --> {child}\n"
        mermaid_code += f"    {p2} --> {child}\n"

    return mermaid_code

# === Streamlit 页面 ===
st.title("配种路径查询系统")

all_biological_names = list(zh_en_map.keys())
col1, col2 = st.columns(2)

with col1:
    zh_start = st.selectbox("选择起始生物（中文名）：", all_biological_names)

with col2:
    zh_target = st.selectbox("选择目标生物（中文名）：", all_biological_names)

start = to_en(zh_start)
target = to_en(zh_target)
paths = reverse_breeding_paths(start, target)

if paths:
    st.write(f"从『{zh_start}』到『{zh_target}』的最短配种链路如下：")
    for idx, path in enumerate(paths):
        st.write(f"配种路径 {idx + 1}:")
        mermaid_code = create_mermaid_chart(path)
        components.html(f"""
            <div class="mermaid">
            {mermaid_code}
            </div>
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{startOnLoad:true}});
            </script>
        """, height=500, scrolling=True)
else:
    st.write(f"无法找到从『{zh_start}』配种到『{zh_target}』的路径")
