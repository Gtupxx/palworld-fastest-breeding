import json
import base64
import os
from collections import deque, defaultdict
import streamlit as st
import streamlit.components.v1 as components
from BFS import to_en, to_zh, reverse_breeding_paths, en_zh_map, zh_en_map

# === 本地图片路径 ===
IMAGE_DIR = "images/imgv1.0"


def get_image_base64(name_en):
    """
    读取本地图片并转换为base64
    """

    img_path = os.path.join(IMAGE_DIR, f"{name_en}.png")

    if not os.path.exists(img_path):
        return ""

    with open(img_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()

    return f"data:image/png;base64,{img_data}"


def get_image_base64(name_en):
    """
    读取本地图片并转换为base64
    """

    img_path = os.path.join(IMAGE_DIR, f"{name_en}.png")

    if not os.path.exists(img_path):
        print(f"图片不存在: {img_path}")
        return ""

    with open(img_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()

    return f"data:image/png;base64,{img_data}"


# === 图床头像地址映射 ===
def get_image_url(name_en):
    return f"https://www.palworldbreed.com/images/{name_en}.webp"


def render_breeding_graph(path):

    import streamlit.components.v1 as components

    def to_zh(name):
        return en_zh_map.get(name, name)

    def add_generation(name, index):

        unique_id = f"node_{index}"

        img = get_image_base64(name)

        return (
            f"""
        <div class="node" id="{unique_id}">
            <img src="{img}" />
            <div class="label" style="color:#DC143C;">
                {to_zh(name)}
            </div>
        </div>
        """,
            unique_id,
        )

    html_generations = []
    edges = []

    node_index = 0

    for i, (father, mother, child) in enumerate(path):

        generation_html = """
        <div class="generation">
        """

        # 父亲节点
        father_html, father_id = add_generation(father, node_index)

        node_index += 1

        # 母亲节点
        mother_html, mother_id = add_generation(mother, node_index)

        node_index += 1

        generation_html += father_html
        generation_html += mother_html

        generation_html += "</div>"

        # 子代单独作为下一代节点

        child_html, child_id = add_generation(child, node_index)

        node_index += 1

        html_generations.append(generation_html)

        html_generations.append(f"""
            <div class='generation child'>
                {child_html}
            </div>
            """)

        edges.append((father_id, child_id))

        edges.append((mother_id, child_id))

    components.html(
        f"""
            <html>
                <head>
                    <style>
                    .container {{
                        display:flex;
                        flex-direction:row;
                        align-items:center;
                        gap:60px;
                        padding:20px;
                        overflow-x:auto;
                    }}

                    .generation {{
                        display:flex;
                        flex-direction:column;
                        align-items:center;
                        gap:30px;
                    }}

                    .node {{
                        width:100px;
                        text-align:center;
                    }}

                    .node img {{
                        width:80px;
                        height:80px;
                        border-radius:50%;
                        border:2px solid #888;
                    }}

                    .label {{
                        margin-top:6px;
                        font-size:14px;
                    }}

                    </style>
                </head>
            <body>
            <div class="container">
                {''.join(html_generations)}
            </div>

            <script src="https://cdn.jsdelivr.net/npm/leader-line"></script>
            <script>

            const lines=[];

            window.onload=()=>{{
                {''.join(
                f"""
                    lines.push(
                        new LeaderLine(
                            document.getElementById('{p}'),
                            document.getElementById('{c}'),
                            {{
                            color:'#444',
                            size:2,
                            path:'fluid',
                            startSocket:'right',
                            endSocket:'left',
                            endPlug:'arrow3'
                            }}
                        )
                    );
               """
                for p,c in edges
                )}
            }};

            window.onresize=()=>{{
                lines.forEach(
                    l=>l.position()
                );
            }};

            </script>


            </body>

            </html>
            """,
        height=350,
        scrolling=True,
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

if zh_start == zh_target:
    st.write("起始生物和目标生物相同，无需配种。")

else:
    if paths:
        st.write(f"从『{zh_start}』到『{zh_target}』的最短配种链路如下：")
        for idx, path in enumerate(paths):
            st.write(f"配种路径 {idx + 1}:")

            # 渲染图表
            render_breeding_graph(path[::-1])

    else:
        st.write(f"无法找到从『{zh_start}』配种到『{zh_target}』的路径")
