import re
import json

# 输入文件
INPUT_FILE = "constants.js"

# 输出文件
OUTPUT_FILE = "pal_name_map.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# 匹配每一个对象
object_pattern = re.compile(r'\{(.*?)\}', re.DOTALL)

# 匹配字段
name_pattern = re.compile(r'name\s*:\s*"([^"]*)"')
chinese_pattern = re.compile(r'chinese_name\s*:\s*"([^"]*)"')

result = {}

for obj in object_pattern.findall(text):
    name_match = name_pattern.search(obj)
    chinese_match = chinese_pattern.search(obj)

    if name_match and chinese_match:
        english = name_match.group(1)
        chinese = chinese_match.group(1)
        result[chinese] = english

# 写入JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print(f"共提取 {len(result)} 条数据")
print(f"已保存到 {OUTPUT_FILE}")