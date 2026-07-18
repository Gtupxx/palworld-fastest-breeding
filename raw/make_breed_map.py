import json
import re
from collections import defaultdict

INPUT_FILE = "constants.js"
OUTPUT_FILE = "breeding_map.json"


def js_array_to_json(text, variable):
    """
    从JS中提取 const xxx = [...]
    转换成Python对象
    """

    # 找数组
    pattern = rf"const\s+{variable}\s*=\s*(\[[\s\S]*?\])\s*;"

    match = re.search(pattern, text)

    if not match:
        raise Exception(f"{variable} not found")

    data = match.group(1)

    # 删除对象最后逗号
    data = re.sub(r",(\s*[}\]])", r"\1", data)

    # JS key -> JSON key
    # parent1: -> "parent1":
    data = re.sub(r"([{,]\s*)(\w+)\s*:", r'\1"\2":', data)

    # 如果有单引号
    data = data.replace("'", '"')

    return json.loads(data)


# ============================
# 读取JS
# ============================

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    js = f.read()


SPECIAL_RULES_DATA = js_array_to_json(js, "SPECIAL_BREEDING_RULES")

PAL_DATA = js_array_to_json(js, "PAL_DATA")


print("PAL:", len(PAL_DATA))

print("Special:", len(SPECIAL_RULES_DATA))


# ============================
# 特殊配种表
# ============================

SPECIAL_RULES = {}

for item in SPECIAL_RULES_DATA:

    key = frozenset([item["parent1"], item["parent2"]])

    SPECIAL_RULES[key] = item["child"]


# ============================
# CombiRank计算
# ============================


def build_special_child_set():
    """
    获取特殊配种产物集合
    """
    return {
        rule["child"]
        for rule in SPECIAL_RULES_DATA
    }


SPECIAL_CHILD_NAMES = build_special_child_set()



# 普通配种候选
NORMAL_PALS = [
    pal for pal in PAL_DATA
    if pal["name"] not in SPECIAL_CHILD_NAMES
]



def find_closest_pal(rank):

    candidates = NORMAL_PALS


    return min(
        candidates,
        key=lambda x: (
            abs(x["CombiRank"] - rank),

            # Priority越大越优先
            -x.get("Priority", 0),

            # Priority相同时
            # CombiRank小优先
            x["CombiRank"]
        )
    )

# ============================
# 穷举
# ============================

breed_map = defaultdict(list)


for i in range(len(PAL_DATA)):

    for j in range(i, len(PAL_DATA)):

        father = PAL_DATA[i]
        mother = PAL_DATA[j]

        # 同种
        if father["name"] == mother["name"]:

            child = father["name"]

        else:

            key = frozenset([father["name"], mother["name"]])

            # 特殊规则
            if key in SPECIAL_RULES:

                child = SPECIAL_RULES[key]

            else:

                # 普通公式
                rank = (father["CombiRank"] + mother["CombiRank"] + 1) // 2

                child = find_closest_pal(rank)["name"]

        breed_map[child].append({"A": father["name"], "B": mother["name"]})


# ============================
# 输出
# ============================

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    json.dump(breed_map, f, ensure_ascii=False, indent=4)


print(f"Done: {len(breed_map)} children")
