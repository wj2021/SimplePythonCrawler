import requests
import os

url = 'https://baidu.com'
picUrl = 'http://img.mp.itc.cn/upload/20170707/f41afdf94bae4b7583b37dbef03e23b8_th.jpg'
rootPath = 'E:\\picFromWeb\\'
path = rootPath + picUrl.split('/')[-1]

try:
    if not os.path.exists(rootPath):
        os.mkdir(rootPath)
    if not os.path.exists(path):
        r = requests.get(picUrl)
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()
        r.close()
    else:
        print('文件已存在')
except:
    print('error')