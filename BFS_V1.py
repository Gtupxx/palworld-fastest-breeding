import json
from collections import deque, defaultdict
import streamlit as st
import streamlit.components.v1 as components
from BFS import to_en, to_zh, reverse_breeding_paths, en_zh_map, zh_en_map


# === 图床头像地址映射 ===
def get_image_url(name_en):
    return f"https://www.palworldbreed.com/images/{name_en}.webp"

# === 渲染图表的函数（带头像+中文名） ===
def render_breeding_graph(path):
    import streamlit.components.v1 as components

    def to_zh(id):
        return en_zh_map[id]  # 可替换为中文名映射字典

    def add_generation(name, index):
        unique_id = f"{name}_id{index}"  # 为每个节点生成一个独一无二的 ID
        return f"""
            <div class="node" id="{unique_id}">
                <img src="https://www.palworldbreed.com/images/{name}.webp" />
                <div class="label" style="color: #DC143C;">{to_zh(name)}</div>
            </div>
            """

    html_generations = []
    edges = []
    seen_nodes = set()
    pre_child = None
    node_index = 0  # 用来为每个节点分配唯一 ID 的索引

    for i, (father, mother, child) in enumerate(path):
        generation_html = "<div class='generation'>"

        # 处理父本
        if pre_child != father:
            (mother, father) = (father, mother)
            pre_child = child

        # 父本节点
        father_id = f"{father}_id{node_index}"
        generation_html += add_generation(father, node_index)
        seen_nodes.add(father)
        node_index += 1

        # 母本节点
        mother_id = f"{mother}_id{node_index}"
        generation_html += add_generation(mother, node_index)
        seen_nodes.add(mother)
        node_index += 1

        # 最后一步时才渲染 child（target）
        child_id = f"{child}_id{node_index}"
        if i == len(path) - 1 and child not in seen_nodes:
            generation_html += "</div><div class='generation'>"
            
            generation_html += add_generation(child, node_index)
            seen_nodes.add(child)
            node_index += 1

        generation_html += "</div>"
        html_generations.append(generation_html)

        # 连接边：使用唯一的节点 ID 来构建边
        edges.append((father_id, child_id))
        edges.append((mother_id, child_id))

    # 渲染 HTML 页面
    components.html(
        f"""
    <html>
    <head>
        <style>
            .container {{
                display: flex;
                flex-direction: row;
                align-items: center;
                gap: 60px;
                padding: 20px;
                overflow-x: auto;
                white-space: nowrap;
            }}
            .generation {{
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 30px;
                min-width: 100px;
            }}
            .node {{
                text-align: center;
                width: 100px;
            }}
            .node img {{
                width: 80px;
                height: 80px;
                border-radius: 50%;
                border: 2px solid #888;
                background-color: #fff;
            }}
            .label {{
                margin-top: 6px;
                font-size: 14px;
                word-wrap: break-word;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {''.join(html_generations)}
        </div>

        <script src="https://cdn.jsdelivr.net/npm/leader-line"></script>
        <script>
            const lines = [];
            window.addEventListener('load', () => {{
                {''.join(
                    f"""lines.push(new LeaderLine(
                        document.getElementById('{p}'),
                        document.getElementById('{c}'),
                        {{
                            color: '#444',
                            size: 2,
                            path: 'fluid',
                            startSocket: 'right',
                            endSocket: 'left',
                            startPlug: 'behind',
                            endPlug: 'arrow3'
                        }}
                    ));""" for p, c in edges
                )}
            }});
            window.addEventListener('resize', () => {{
                lines.forEach(line => line.position());
            }});
        </script>
    </body>

    </html>
    """,
        height=300,
        scrolling=False,
    )


# === Streamlit 页面 ===
st.set_page_config(layout="wide")
st.title("配种路径查询系统")
# 获取所有生物的中文名列表
all_biological_names = list(zh_en_map.keys())

# 使用 Streamlit 的列布局来并排显示两个选择框
col1, col2 = st.columns(2)

with col1:
    zh_start = st.selectbox("选择起始生物（中文名）：", all_biological_names)

with col2:
    zh_target = st.selectbox("选择目标生物（中文名）：", all_biological_names)

start = to_en(zh_start)
target = to_en(zh_target)

# 获取最短路径
paths = reverse_breeding_paths(start, target)

if paths:
    st.write(f"从『{zh_start}』到『{zh_target}』的最短配种链路如下：")
    for idx, path in enumerate(paths):
        st.write(f"配种路径 {idx + 1}:")

        # 渲染图表
        render_breeding_graph(path[::-1])

else:
    st.write(f"无法找到从『{zh_start}』配种到『{zh_target}』的路径")
