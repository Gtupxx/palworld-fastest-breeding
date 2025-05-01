import json

# 读取原始 JSON 文件
with open('parents.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 创建新数据结构，只保留 A 和 B
filtered_data = {}

for key, value_list in data.items():
    if isinstance(value_list, list):
        new_list = []
        for item in value_list:
            if isinstance(item, dict):
                filtered_item = {}
                if "A" in item:
                    filtered_item["A"] = item["A"]
                if "B" in item:
                    filtered_item["B"] = item["B"]
                new_list.append(filtered_item)
        filtered_data[key] = new_list
    else:
        filtered_data[key] = value_list

# 写入新 JSON 文件
with open('parents_no_zh.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, indent=4, ensure_ascii=False)

print("中文字段已移除，结果保存在 parents_no_zh.json")
