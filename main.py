import numpy as np

import wtouv
import get_uv_location
import GetCameraInfo
import PointType
from collections import defaultdict
import re
import GetError
import time
import json
import math
import getlowerindex
def approach(path,facial,RT_change):
    CameraInfo = GetCameraInfo.GetCameraInfo(f'{path}/cam_info.yml')
    camerainfouv = defaultdict(list)
    _3d = []
    _3d_left_ear=[]
    _3d_right_ear=[]
    # 三维点数量
    ll = 0
    for cameratype, data in CameraInfo.items():
        if cameratype == '064051002446':
            pixel_coords, _3d_left_ear=wtouv._3d_to_uv(1,f'{path}/{facial}/obj/face_0000_pr.obj', f'{path}/cam_res/{data[0]}.yml',
                                            f'{path}/calib_res/{data[1]}.yml',RT_change)

        elif cameratype =='364056001172':
            pixel_coords, _3d_right_ear=wtouv._3d_to_uv(1,f'{path}/{facial}/obj/face_0000_pr.obj', f'{path}/cam_res/{data[0]}.yml',
                                            f'{path}/calib_res/{data[1]}.yml',RT_change)

        else :
            pixel_coords, _3d = wtouv._3d_to_uv(0,f'{path}/{facial}/obj/face_0000_pr.obj', f'{path}/cam_res/{data[0]}.yml',
                                            f'{path}/calib_res/{data[1]}.yml',RT_change)

        camerainfouv[cameratype].append(pixel_coords)
        if ll == 0:
            ll = len(_3d)

    PointT = PointType.PointType(f'{path}/{facial}/features')
    dic={}#存储所有的点
    for category, files in PointT.items():
        # 计算误差
        error_start = np.zeros((1, ll))
        error_end = np.zeros((1, ll))
        # error_mid=np.zeros((1,ll))
        if (category == 'IMG_ear'):
            typ=0
            for file in files:
                if file == '064051002446_IMG_ear.txt':
                    typ=0
                elif file == '364056001172_IMG_ear.txt':
                    typ=1
                lk = len(_3d_left_ear)
                if typ == 1:
                    lk = len(_3d_right_ear)
                error_start = np.zeros((1, lk))
                error_end = np.zeros((1, lk))
                oriuv = get_uv_location.get_uv_location(f'{path}/{facial}/features/{file}')
                startpoint = oriuv[4]
                endpoint = oriuv[18]
                match = re.match(r'\d+', file)
                if match:
                    number_part = match.group()
                    # 当前文件参数对应的摄像机
                    camerauv = camerainfouv[number_part][0]
                    # 计算当前点的当前视角的error
                    error_start += GetError.GetError(camerauv, startpoint, lk)
                    error_end += GetError.GetError(camerauv, endpoint, lk)
                min_index_start = np.argmin(error_start)
                min_index_end = np.argmin(error_end)
                strr='leftear'
                if typ==1:
                    strr='rightear'
                if f'{strr}{category}' not in dic:
                    dic[f'{strr}{category}'] = {}  # 创建一个新的字典条目
                if typ==0:
                    dic[f'{strr}{category}']['startpoint'] = _3d_left_ear[min_index_start].tolist()
                    dic[f'{strr}{category}']['endpoint'] = _3d_left_ear[min_index_end].tolist()
                elif typ==1:
                    dic[f'{strr}{category}']['startpoint'] = _3d_right_ear[min_index_start].tolist()
                    dic[f'{strr}{category}']['endpoint'] = _3d_right_ear[min_index_end].tolist()
            continue
        for file in files:
            oriuv = get_uv_location.get_uv_location(f'{path}/{facial}/features/{file}')
            startpoint = oriuv[0]
            endpoint = oriuv[len(oriuv) - 1]
            midpoint=oriuv[math.floor(len(oriuv)/2)]
            match = re.match(r'\d+', file)
            if match:
                number_part = match.group()
                # 当前文件参数对应的摄像机
                camerauv = camerainfouv[number_part][0]
                # 计算当前点的当前视角的error
                error_start+=GetError.GetError(camerauv, startpoint,ll)
                error_end+=GetError.GetError(camerauv,endpoint,ll)
                # error_mid+=GetError.GetError(camerauv,midpoint,ll)
        # 找出最小数的位置
        min_index_start = np.argmin(error_start)
        min_index_end=np.argmin(error_end)
        # mid_index_mid=np.argmin(error_mid)
        if category not in dic:
            dic[category] = {}  # 创建一个新的字典条目
        dic[category]['startpoint']=_3d[min_index_start].tolist()
        dic[category]['endpoint']=_3d[min_index_end].tolist()
        # dic[category]['midpoint']=_3d[mid_index_mid].tolist()
    # 打印结果或进行其他处理
    print(dic)
    # 将字典转换为格式化的字符串
    formatted_data = json.dumps(dic, indent=4)
    # 写入文件
    with open(f'{path}/{facial}/{facial}.json', 'w') as file:
        file.write(formatted_data)
if __name__=='__main__':
    path='D:/自动step/feature_data'
    facial = f'0000'
    RT_change = True  # 是否为transformer转化为R ,T外参数矩阵
    approach(path, facial, RT_change)



# for uv in oriuv:
#     idx = 0
#     MinNum = float('inf')
