from collections import defaultdict
def GetCameraInfo(path):

    file_path = path
    Camera_sets = defaultdict(list)
    # 读取YAML文件
    with open(file_path, 'r') as file:
        lines = file.readlines()

    start_index = lines.index('cross_polarized:\n')
    end_index = lines.index('parallel_polarized:\n')
    Camera_data = []
    Camera_toal = ""
    for line in lines[start_index + 1:end_index]:  # 从下一行开始
        Camera_toal += line.rstrip('\n').rstrip(' ').rstrip('"').lstrip('- "')
        Camera_toal+=','
    Camera_toal=Camera_toal.rstrip(',')
    Camera_toal  = Camera_toal.split(',')
    cnt=0
    for item in Camera_toal:
        Camera_data.append(item)
        Camera_sets[item].append(str(cnt))
        Camera_sets[item].append('check_'+str(cnt))
        cnt+=1
    return Camera_sets
# for category, files in file_sets.items():
#     print(f"Category: {category}")
#     for file in files:
#         print(f"  - {file}")
