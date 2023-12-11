import math

import numpy as np
def isvisable(mesh,vertex,R_matrix,t_matrix):
    t_matrix = t_matrix.reshape(-1)
    camera_location = np.dot(np.linalg.inv(R_matrix), -t_matrix)
    locations, index_ray, index_tri = mesh.ray.intersects_location(
        ray_origins=[vertex],
        ray_directions=[camera_location - vertex]
    )
    if len(locations)>1:
        return False
    else :
        if len(locations)==1:
            tp_t = np.linalg.norm(locations[0] - vertex)
            if tp_t  > 0.00001:
                return False
        return True