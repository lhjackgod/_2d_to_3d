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
import shutil
import os
import GetIdx
import getlowerindex
def sort_feature_point(path, facial):
    target_dir = os.path.join(path, "feature_point")
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    source_file_name = os.path.join(path, facial, "{}.json".format(facial))
    target_file_name = os.path.join(target_dir, "{}.json". format(facial))
    shutil.copy(source_file_name, target_file_name)
def approach(path,facial,RT_change,v_idx_path,f_idx_path):
    CameraInfo = GetCameraInfo.GetCameraInfo(f'{path}/cam_info.yml')
    camerainfouv = defaultdict(list)
    _3d_left=GetIdx.getidx(f'{path}/{facial}/364056001175.txt')
    _3d_right=GetIdx.getidx(f'{path}/{facial}/064051002443.txt')
    _3d = []
    _3d_left_ear=GetIdx.getidx(f'{path}/{facial}/064051002446.txt')
    _3d_right_ear=GetIdx.getidx(f'{path}/{facial}/364056001172.txt')
    # 三维点数量
    ll = 0
    for cameratype, data in CameraInfo.items():
        pixel_coords, _3d = wtouv._3d_to_uv(0,f'{path}/{facial}/obj/face_0000_pr.obj', f'{path}/cam_res/{data[0]}.yml',
                                        f'{path}/calib_res/{data[1]}.yml',RT_change,v_idx_path,f_idx_path)
        camerainfouv[cameratype].append(pixel_coords)
    PointT = PointType.PointType(f'{path}/{facial}/features')
    dic={}#存储所有的点
    for category, files in PointT.items():
        _3d_pass=[]
        _3d_idx=[]
        # 计算误差
        if (category == 'IMG_ear'):
            typ=0
            for file in files:
                if file == '064051002446_IMG_ear.txt':
                    _3d_pass=[_3d[i] for i in _3d_left_ear]
                    typ=0
                    _3d_idx=_3d_left_ear
                elif file == '364056001172_IMG_ear.txt':
                    _3d_pass = [_3d[i] for i in _3d_right_ear]
                    typ=1
                    _3d_idx = _3d_right_ear
                oriuv = get_uv_location.get_uv_location(f'{path}/{facial}/features/{file}')
                ll = len(_3d_idx)
                lk=len(oriuv)
                error_total = np.zeros((lk, ll))
                # error_end = np.zeros((lk, ll))
                # startpoint = oriuv[4]
                # endpoint = oriuv[18]
                # midpoint = oriuv[math.floor(len(oriuv) / 2)]
                match = re.match(r'\d+', file)
                if match:
                    number_part = match.group()
                    # 当前文件参数对应的摄像机
                    camerauv = camerainfouv[number_part][0]
                    camerauv = [camerauv[i] for i in _3d_idx]
                    # 计算当前点的当前视角的error
                    j=0
                    for i in oriuv:
                        error=error_total[j,:].reshape(1,-1)
                        error+=GetError.GetError(camerauv, i, ll)
                        error_total[j,:]=error
                        j+=1
                    # error_total += GetError.GetError(camerauv, startpoint, ll)
                    # error_end += GetError.GetError(camerauv, endpoint, ll)
                min_index_total=[]
                for i in range(j):
                    min_index_total.append(np.argmin(error_total[i]))
                # min_index_start = np.argmin(error_start)
                # min_index_end = np.argmin(error_end)
                strr='leftear'
                if typ==1:
                    strr='rightear'
                if f'{strr}{category}' not in dic:
                    dic[f'{strr}{category}'] = {}  # 创建一个新的字典条目
                ppp=[_3d_pass[i] for i in min_index_total]
                dic[f'{strr}{category}']['earpoint'] = []
                for point in ppp:
                    dic[f'{strr}{category}']['earpoint'].append(point.tolist())
            continue
        if 'left' in category:
            _3d_pass=[_3d[i] for i in _3d_left]
            _3d_idx=_3d_left
        elif 'right' in category:
            _3d_pass = [_3d[i] for i in _3d_right]
            _3d_idx=_3d_right
        else:
            _3d_pass = [_3d[i] for i in _3d_left]
            _3d_idx = _3d_left
        ll=len(_3d_pass)
        error_start = np.zeros((1, ll))
        error_end = np.zeros((1, ll))
        error_mid=np.zeros((1,ll))
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
                camerauv = [camerauv[i] for i in _3d_idx]
                error_start+=GetError.GetError(camerauv, startpoint,ll)
                error_end+=GetError.GetError(camerauv,endpoint,ll)
                error_mid+=GetError.GetError(camerauv,midpoint,ll)
        # 找出最小数的位置
        min_index_start = np.argmin(error_start)
        min_index_end=np.argmin(error_end)
        mid_index_mid=np.argmin(error_mid)
        if category not in dic:
            dic[category] = {}  # 创建一个新的字典条目
        dic[category]['startpoint']=_3d_pass[min_index_start].tolist()
        dic[category]['endpoint']=_3d_pass[min_index_end].tolist()
        dic[category]['midpoint']=_3d_pass[mid_index_mid].tolist()
    # 打印结果或进行其他处理
    print(dic)
    # 将字典转换为格式化的字符串
    formatted_data = json.dumps(dic, indent=4)
    # 写入文件
    with open(f'{path}/{facial}/{facial}.json', 'w') as file:
        file.write(formatted_data)
    sort_feature_point(path,facial)
if __name__=='__main__':
    path='D:/second_try_test/feature_data'
    facial=None
    v_idx_path = './v_idx.txt'
    f_idx_path = './f_idx.txt'
    # facial='0000'
    # RT_change=True
    # approach(path, facial, RT_change, v_idx_path, f_idx_path)
    for i in range(18):
        if i < 10 :
            facial=f'000{i}'
        else:
            facial=f'00{i}'
        RT_change = True  # 是否为transformer转化为R ,T外参数矩阵
        approach(path, facial, RT_change,v_idx_path,f_idx_path)



# for uv in oriuv:
#     idx = 0
#     MinNum = float('inf')
