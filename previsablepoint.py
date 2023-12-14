import GetCameraInfo
import wtouv
def approach(path,facial, RT_change, v_idx_path, f_idx_path):
    CameraInfo = GetCameraInfo.GetCameraInfo(f'{path}/cam_info.yml')
    for cameratype, data in CameraInfo.items():
        idx=[]
        if cameratype == '064051002446':
            idx=wtouv._3d_to_uv(2,f'{path}/{facial}/obj/face_0000_pr.obj', f'{path}/cam_res/{data[0]}.yml',
                                            f'{path}/calib_res/{data[1]}.yml',RT_change,v_idx_path,f_idx_path)
        elif cameratype =='364056001172':
            idx=wtouv._3d_to_uv(2,f'{path}/{facial}/obj/face_0000_pr.obj', f'{path}/cam_res/{data[0]}.yml',
                                            f'{path}/calib_res/{data[1]}.yml',RT_change,v_idx_path,f_idx_path)
        elif cameratype=='364056001175':
            idx=wtouv._3d_to_uv(2,f'{path}/{facial}/obj/face_0000_pr.obj', f'{path}/cam_res/{data[0]}.yml',
                                            f'{path}/calib_res/{data[1]}.yml',RT_change,v_idx_path,f_idx_path)
        elif cameratype=='064051002443':
            idx=wtouv._3d_to_uv(2,f'{path}/{facial}/obj/face_0000_pr.obj', f'{path}/cam_res/{data[0]}.yml',
                                            f'{path}/calib_res/{data[1]}.yml',RT_change,v_idx_path,f_idx_path)
        else:
            continue
        with open(f'{path}/{facial}/{cameratype}.txt','w') as file:
            for i in idx:
                file.write(i+"\n")

if __name__=='__main__':
    path='D:/second_try_test/feature_data'
    facial=None
    v_idx_path = './v_idx.txt'
    f_idx_path = './f_idx.txt'
    for i in range(18):
        if i < 10 :
            facial=f'000{i}'
        else:
            facial=f'00{i}'
        RT_change = True  # 是否为transformer转化为R ,T外参数矩阵
        approach(path, facial, RT_change,v_idx_path,f_idx_path)
    # facial='0000'
    # RT_change=True
    # approach(path, facial, RT_change, v_idx_path, f_idx_path)