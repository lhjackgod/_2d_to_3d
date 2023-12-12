import numpy as np
import OpenGL.GL as gl

def build_projection_matrix(K, width, height, near, far):
    fx, fy = K[0, 0], K[1, 1]
    cx, cy = K[0, 2], K[1, 2]

    # 创建投影矩阵
    proj_matrix = np.zeros((4, 4))
    proj_matrix[0, 0] = 2 * fx / width
    proj_matrix[1, 1] = 2 * fy / height
    proj_matrix[0, 2] = 1 - 2 * cx / width
    proj_matrix[1, 2] = 2 * cy / height - 1
    proj_matrix[2, 2] = -(far + near) / (far - near)
    proj_matrix[3, 2] = -1
    proj_matrix[2, 3] = -2 * far * near / (far - near)

    return proj_matrix
def build_view_matrix(R, t):
    # 创建视图矩阵
    view_matrix = np.eye(4)
    view_matrix[:3, :3] = R
    view_matrix[:3, 3] = t

    # OpenGL 需要右手坐标系
    flip_yz = np.eye(4)
    flip_yz[1, 1], flip_yz[2, 2] = -1, -1
    view_matrix = view_matrix @ flip_yz

    return view_matrix
def ViewProjection(R,t,K,width, height, near, far):
    view_matrix = build_view_matrix(R, t)
    proj_matrix = build_projection_matrix(K, width, height, near, far)
    return view_matrix,proj_matrix
