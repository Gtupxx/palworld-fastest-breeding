import json
import os
import requests

# 读取 JSON 文件
with open("zh_en_map.json", "r", encoding="utf-8") as f:
    zh_en_map = json.load(f)

# 图片基础 URL
base_url = "https://www.palworldbreed.com/images/"

# 创建保存文件夹
save_dir = "palworld_images"
os.makedirs(save_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0"
}

# 下载每一张图片
for zh_name, en_name in zh_en_map.items():
    img_url = f"{base_url}{en_name}.webp"
    save_path = os.path.join(save_dir, f"{en_name}.webp")
    try:
        response = requests.get(img_url, headers=headers, timeout=10)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"下载成功：{en_name} -> {img_url}")
    except Exception as e:
        print(f"下载失败：{en_name} -> {img_url}，原因：{e}")
