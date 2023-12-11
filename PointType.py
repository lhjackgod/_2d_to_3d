import os
from collections import defaultdict
import re
# 文件夹路径
def PointType(path):
    folder_path = '../0000/features'

    # 创建一个默认字典来存储文件名集合
    file_sets = defaultdict(list)
    _set = []
    for filename in os.listdir(folder_path):
        match = re.search(r'IMG_[\w]+(?=\.txt)', filename)
        if match:
            extracted_part = match.group()
            _set.append(extracted_part)
    _set = list(set(_set))
    print(_set)
    # 遍历文件夹中的文件
    for filename in os.listdir(folder_path):
        match = re.search(r'IMG_[\w]+(?=\.txt)', filename)
        if match:
            extracted_part = match.group()
            for filetype in _set:
                if filetype == extracted_part:
                    file_sets[filetype].append(filename)


    # # # 打印结果或进行其他处理
    #     # for category, files in file_sets.items():
    #     #     print(f"Category: {category}")
    #     #     for file in files:
    #     #         print(f"  - {file}")
    return file_sets
