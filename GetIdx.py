def getidx(path):
    res=[]
    with open(path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        res.append(int(line))
    return res