import json
import re

def replace_keys_with_values(json_file, txt_file, output_file):
    # 加载中->英映射
    with open(json_file, 'r', encoding='utf-8') as f:
        zh_en_map = json.load(f)

    # 读取文本内容
    with open(txt_file, 'r', encoding='utf-8') as f:
        text_data = f.read()

    # 替换：只替换被双引号包裹的中文
    def replace_quoted(match):
        zh_key = match.group(1)
        en_val = zh_en_map.get(zh_key, zh_key)
        return f'"{en_val}"'

    # 使用正则匹配双引号包裹的内容
    result = re.sub(r'"(.*?)"', replace_quoted, text_data)

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"✅ 中文替换完成，结果已保存为 {output_file}")

# 示例调用
replace_keys_with_values(
    json_file='zh_en_map.json',
    txt_file='parents_zh.json',
    output_file='parents_en.json'
)
