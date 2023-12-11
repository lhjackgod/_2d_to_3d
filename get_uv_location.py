import numpy as np


def get_uv_location(path):

    file_path = path

    data = []  # 存储读取的数据

    # 逐行读取文件并处理数据
    with open(file_path, 'r') as file:
        for line in file:
            # 去除行尾的换行符，并按空格分割字符串为列表
            line_data = line.strip().split('\t')

            # 将每一行的数据转换为浮点数列表
            float_line_data = [float(value) for value in line_data]

            # 添加到数据列表中
            data.append(float_line_data)

    return data
    # 输出读取的数据
