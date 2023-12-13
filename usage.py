import trimesh
import numpy as np
import os
import igl
def back_mesh(mesh_path,v_idx_path,f_idx_path):
	v_idx = np.loadtxt(v_idx_path, dtype=np.int32)
	f_idx = np.loadtxt(f_idx_path, dtype=np.int32)
	v_all, f_all = igl.read_triangle_mesh(mesh_path)
	v_focus = v_all[v_idx]
	mesh_focus = trimesh.Trimesh(v_focus, f_idx)
	return mesh_focus
# if __name__ == "__main__":
# 	base_path = "D:/自动step/feature_data/example"
# 	v_idx_path = f'{base_path}/v_idx.txt'
# 	f_idx_path = f'{base_path}/f_idx.txt'
# 	mesh_path = 'D:/second_try_test/example/face_0000_pr.obj'
# 	mesh_save_path = os.path.join("face_mesh.obj")
#
# 	v_idx = np.loadtxt(v_idx_path, dtype=np.int32)
# 	f_idx = np.loadtxt(f_idx_path, dtype=np.int32)
# 	v_all, f_all = igl.read_triangle_mesh(mesh_path)
#
# 	v_focus = v_all[v_idx]
#
# 	mesh_focus = trimesh.Trimesh(v_focus, f_idx)
# 	mesh_focus.export(mesh_save_path, file_type="obj")

