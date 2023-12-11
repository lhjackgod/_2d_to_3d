import numpy as np
import trimesh
import load_model
import RAndT
import isvisable
def getlowerindex(_3d,point_error,path_mesh,rtpath,kpath,RT_change):
    mesh = load_model.load_m(path_mesh)
    # 相机内外参
    R, t, K = RAndT.RAndT(rtpath, kpath, RT_change)
    r=-1
    r_error=float('inf')
    for idx in range(len(point_error[0])):
        if isvisable.isvisable(mesh,_3d[idx],R,t):
            if r_error > point_error[0,idx]:
                r_error=point_error[0,idx]
                r=idx
    return r
