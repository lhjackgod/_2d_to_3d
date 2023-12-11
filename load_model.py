import trimesh

# 读取OBJ文件
def load_m(path):

    mesh = trimesh.load_mesh(path)

    # 输出模型信息
    return mesh