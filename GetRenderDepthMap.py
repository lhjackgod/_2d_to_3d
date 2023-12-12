import cv2
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import ViewProjectionMatrix
import pywavefront


def init_gl(width, height):
    # 初始化 GLUT
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH)
    glut.glutInitWindowSize(width, height)
    glut.glutCreateWindow("OpenGL Window")

    # 设置背景颜色和深度测试
    gl.glClearColor(0.0, 0.0, 0.0, 1.0)
    gl.glClearDepth(1.0)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glDepthFunc(gl.GL_LEQUAL)


def load_model(file_path):
    model = pywavefront.Wavefront(file_path, collect_faces=True)
    return model


def setup_fbo(width, height):
    # 创建帧缓冲对象
    fbo = gl.glGenFramebuffers(1)
    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, fbo)

    # 创建深度纹理
    depth_tex = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, depth_tex)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_DEPTH_COMPONENT,
                    width, height, 0, gl.GL_DEPTH_COMPONENT, gl.GL_FLOAT, None)

    # 将深度纹理附加到 FBO
    gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, gl.GL_TEXTURE_2D, depth_tex, 0)

    # 检查 FBO 状态
    if gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) != gl.GL_FRAMEBUFFER_COMPLETE:
        raise RuntimeError("Unable to create FBO for depth rendering.")

    # 解绑 FBO 和纹理
    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    return fbo, depth_tex

def render_model(model):
    for mesh in model.mesh_list:
        gl.glBegin(gl.GL_TRIANGLES)

        for face in mesh.faces:
            for vertex_i in face:
                # 获取顶点坐标
                # 注意: 这里的索引方式和具体的pywavefront版本有关
                vertex = model.vertices[vertex_i]
                gl.glVertex3f(*vertex)

        gl.glEnd()



def render_depth(model, fbo, view_matrix, proj_matrix):
    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, fbo)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    # 加载视图和投影矩阵
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadMatrixf(view_matrix.T)

    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadMatrixf(proj_matrix.T)

    # 渲染模型
    render_model(model)

    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)


def save_depth_image(depth_tex, width, height, filename):
    # 绑定深度纹理
    gl.glBindTexture(gl.GL_TEXTURE_2D, depth_tex)

    # 读取深度数据
    depth_data = gl.glGetTexImage(gl.GL_TEXTURE_2D, 0, gl.GL_DEPTH_COMPONENT, gl.GL_FLOAT)

    # 将深度数据转换为灰度图像
    depth_image = np.frombuffer(depth_data, dtype=np.float32)
    depth_image = depth_image.reshape((height, width))
    depth_image = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX)
    depth_image = np.uint8(depth_image)

    # 保存图像
    cv2.imwrite(filename, depth_image)

    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)


def render_depth_map(model, view_matrix, proj_matrix, width, height,path):
    fbo, depth_tex = setup_fbo(width, height)

    # 渲染深度图
    render_depth(model, fbo, view_matrix, proj_matrix)

    # 保存深度图像
    save_depth_image(depth_tex, width, height, f'{path}depth_image.png')

    # 释放资源
    gl.glDeleteTextures(1, [depth_tex])
    gl.glDeleteFramebuffers(1, [fbo])


def getRenderDepthMap(R,t,K,model_path,width,height,near,far,path):
    # 初始化 OpenGL 窗口
    init_gl(width, height)
    #加载模型
    model=load_model(model_path)
    print(model)
    # 设置视图和投影矩阵
    view_matrix, proj_matrix = ViewProjectionMatrix.ViewProjection(R, t, K, width, height, near, far)

    # 渲染深度图
    render_depth_map(model, view_matrix, proj_matrix, width, height,path)


