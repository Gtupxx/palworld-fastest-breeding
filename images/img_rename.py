import os
import re
import json
import shutil
import time

# =========================
# 配置
# =========================

JS_FILE = r"C:\Users\11523\Desktop\palworld-fastest-breeding\raw\constants.js"

IMAGE_DIR = "imgv1.0/"

# True: 复制
# False: 移动
COPY_MODE = True

# 是否把空格替换成 _
# True:
# Jormuntide Ignis.png
# ->
# Jormuntide_Ignis.png
#
# False:
# 保持原名字
#
REPLACE_SPACE = False


# =========================
# JS数组解析
# =========================


def extract_pal_data(js):

    pattern = r"const\s+PAL_DATA\s*=\s*(\[.*?\]);"

    match = re.search(pattern, js, re.S)

    if not match:
        raise Exception("没有找到 PAL_DATA")

    data = match.group(1)

    # 删除尾逗号
    data = re.sub(r",(\s*[}\]])", r"\1", data)

    # JS key 转 JSON key
    #
    # name:
    # ->
    # "name":
    #
    data = re.sub(r"([{,]\s*)(\w+)\s*:", r'\1"\2":', data)

    # 单引号
    data = data.replace("'", '"')

    return json.loads(data)


# =========================
# 安全复制
# =========================


def safe_copy(src, dst, retry=5):

    for i in range(retry):

        try:

            shutil.copy2(src, dst)

            return True

        except PermissionError:

            print(f"文件被占用，等待 {i+1}/{retry}: {src}")

            time.sleep(1)

    return False


# =========================
# 主程序
# =========================


with open(JS_FILE, "r", encoding="utf-8") as f:

    js = f.read()


PAL_DATA = extract_pal_data(js)


print(f"读取 PAL 数量: {len(PAL_DATA)}")


success = 0
missing = []
failed = []


for pal in PAL_DATA:

    name = pal["name"]

    image_name = pal["image_name"]

    # 原图片
    src = os.path.join(IMAGE_DIR, image_name + ".png")

    # 输出名字

    new_name = name

    if REPLACE_SPACE:

        new_name = new_name.replace(" ", "_")

    dst = os.path.join(IMAGE_DIR, new_name + ".png")

    # 检查源文件

    if not os.path.exists(src):

        missing.append(image_name + ".png")

        continue

    # 已存在

    if os.path.exists(dst):

        print(f"跳过: {dst}")

        continue

    # 复制/移动

    if COPY_MODE:

        ok = safe_copy(src, dst)

    else:

        try:

            os.rename(src, dst)

            ok = True

        except PermissionError:

            ok = False

    if ok:

        success += 1

        print(f"{image_name}.png -> {new_name}.png")

    else:

        failed.append(dst)


# =========================
# 输出结果
# =========================

print("\n==========完成==========")

print(f"成功: {success}")


if missing:

    print("\n缺失图片:")

    for x in missing:
        print(x)


if failed:

    print("\n失败图片:")

    for x in failed:
        print(x)
