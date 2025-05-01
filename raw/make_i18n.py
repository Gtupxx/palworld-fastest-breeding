import json

# 读取原始 JSON 文件
with open('parents.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 存放中英文对照的结果
en_zh_map = {}

# 遍历顶层每个 key 的 list
for value_list in data.values():
    if isinstance(value_list, list):
        for item in value_list:
            # 获取英文名和中文名的组合
            if isinstance(item, dict):
                en1 = item.get("A")
                zh1 = item.get("AN")
                en2 = item.get("B")
                zh2 = item.get("BN")

                if en1 and zh1:
                    en_zh_map[en1] = zh1
                if en2 and zh2:
                    en_zh_map[en2] = zh2

# 去重后写入文件
with open('en_zh_map.json', 'w', encoding='utf-8') as f:
    json.dump(en_zh_map, f, indent=4, ensure_ascii=False)

print(f"提取完成，共提取 {len(en_zh_map)} 对中英文名。结果保存在 en_zh_map.json")
