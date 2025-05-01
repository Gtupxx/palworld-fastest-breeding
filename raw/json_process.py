import json

# 加载映射表（昵称 -> 字符），然后构造反向映射（字符 -> 昵称）
with open('name_map.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)
reverse_mapping = {v: k for k, v in mapping.items()}

# 读取原始输入文件
with open('breed_map.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 统计目标总数和实际替换数量
total_target_keys = 0
replaced_count = 0

# 构建一个新的字典，把需要替换的键替换掉
new_data = {}

for key, value in data.items():
    if isinstance(value, list):
        total_target_keys += 1
        if key in reverse_mapping:
            new_key = reverse_mapping[key]
            new_data[new_key] = value
            replaced_count += 1
        else:
            new_data[key] = value
    else:
        new_data[key] = value

# 保存为新文件
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=4, ensure_ascii=False)

# 打印统计信息
print(f"替换完成，共找到 {total_target_keys} 个目标键，成功替换了 {replaced_count} 个。")
print("结果保存在 output.json")
