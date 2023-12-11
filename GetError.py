import math

import numpy as np


def GetError(camerauv,point,ll):
    # 给定的点列表
    points = camerauv
    # 假设的给定点 [x, y]
    given_point = point
    # 使用距离公式计算给定点到列表中所有点的距离
    distances = [math.sqrt((x - given_point[0]) ** 2 + (y - given_point[1]) ** 2) for x, y in points]
    return np.array(distances).reshape(1,ll)