import numpy as np
import yaml
import cv2
def RAndT(pathrrt,pathk,RT_change):
    file_pathk=pathk
    file_path = pathrrt

    # 读取YAML文件
    with open(file_pathk,'r') as file:
        linesk=file.readlines()
    with open(file_path, 'r') as file:
        lines = file.readlines()
    R_data = []
    R_toal = ''
    t_data = []
    t_toal = ''
    k_data = []
    k_toal = ''
    # 处理R矩阵数据
    if RT_change :
        transform_total=''
        transform_data=[]
        start_index = lines.index('Transform: !!opencv-matrix\n')
        for line in lines[start_index + 4:]:  # 从下一行开始
            transform_total += line.rstrip('\n').rstrip(' ').replace(' ', '')
        transform_total = transform_total.split(':')[1].lstrip('[').rstrip(']').split(',')
        for item in transform_total:
            transform_data.append(float(item))
        transform_data=np.array(transform_data)
        t_data=transform_data[:3].reshape(1,3)
        R_data,_=cv2.Rodrigues(transform_data[3:])
    else :
        start_index = lines.index('R: !!opencv-matrix\n')
        end_index = lines.index('t: !!opencv-matrix\n')

        for line in lines[start_index + 4:end_index]:  # 从下一行开始
            R_toal += line.rstrip('\n').rstrip(' ').replace(' ', '')
        R_toal = R_toal.split(':')[1].lstrip('[').rstrip(']').split(',')
        for item in R_toal:
            R_data.append(float(item))
        # 处理t矩阵数据
        for line in lines[end_index + 4:]:
            t_toal += line.rstrip('\n').rstrip(' ').replace(' ', '')
        t_toal = t_toal.split(':')[1].lstrip('[').rstrip(']').split(',')
        for item in t_toal:
            t_data.append(float(item))
    # 处理k矩阵数据
    start_index = linesk.index('K: !!opencv-matrix\n')
    end_index = linesk.index('D: !!opencv-matrix\n')
    for line in linesk[start_index + 4:end_index]:
        k_toal+=line.rstrip('\n').rstrip(' ').replace(' ','')
    k_toal = k_toal.split(':')[1].lstrip('[').rstrip(']').split(',')
    for item in k_toal:
        k_data.append(float(item))
    # 转换为NumPy数组
    R_matrix = np.array(R_data).reshape((3, 3))
    t_matrix = np.array(t_data).reshape((1, 3))
    k_matrix=np.array(k_data).reshape((3,3))
    return R_matrix,t_matrix,k_matrix
    # Transf=np.concatenate((R_matrix,t_matrix.T),axis=1)

# import yaml
#
# # 读取YAML文件
# file_path = 'cam_res_mat/0.yml'  # 替换为你的YAML文件路径
# with open(file_path, 'r') as file:
#     yaml_data = yaml.load(file,Loader=yaml.FullLoader)
#
# # 获取R和t数据
# R_data = yaml_data['R']['data']
# t_data = yaml_data['t']['data']
#
# # 将数据转换为NumPy数组
# import numpy as np
#
# R_matrix = np.array(R_data).reshape((yaml_data['R']['rows'], yaml_data['R']['cols']))
# t_matrix = np.array(t_data).reshape((yaml_data['t']['rows'], yaml_data['t']['cols']))
#
# print("R矩阵：")
# print(R_matrix)
# print("t矩阵：")
# print(t_matrix)
