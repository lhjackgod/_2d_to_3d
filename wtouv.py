import numpy as np
import trimesh
import load_model
import RAndT
import isvisable
import time
import usage
def _3d_to_uv(special,path_mesh,rtpath,kpath,RT_change,v_idx_path,f_idx_path):
    start_time = None
    if special==1:
        start_time = time.time()

    # 加载 OBJ 模型
    # mesh = load_model.load_m(path_mesh)
    mesh=usage.back_mesh(path_mesh,v_idx_path,f_idx_path)
    #存三维点
    _3d=[]
    # 相机内外参
    R, t, K = RAndT.RAndT(rtpath, kpath,RT_change)
    M = np.concatenate((R, t.T), axis=1)
    # 转换顶点坐标
    pixel_coords = []
    for vertex in mesh.vertices:
        if special == 1 and not isvisable.isvisable(mesh,vertex,R,t):
            continue
        _3d.append(vertex)
        p_word_homogeneous = np.append(vertex, 1).reshape(1, 4)
        P_camera = M.dot(p_word_homogeneous.T)
        p_image_homogeneous = K @ P_camera
        p_image = p_image_homogeneous / p_image_homogeneous[2, 0]
        pixel_coords.append(p_image.T.tolist()[0][:2])
    if special ==1 :
        end_time = time.time()
        execution_time = end_time - start_time
        print("程序执行时间为：", execution_time, "秒")
    return pixel_coords,_3d

# pixel_coords 包含所有顶点的像素坐标
