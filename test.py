import requests
import os
from bs4 import BeautifulSoup

url = 'https://baidu.com'
picUrl = 'http://img.mp.itc.cn/upload/20170707/f41afdf94bae4b7583b37dbef03e23b8_th.jpg'
videoPath = "https://jdvodrvfb210d.vod.126.net/mooc-video/nos/mp4/2014/10/07/768061_sd.mp4"

rootPath = 'E:\\picFromWeb\\'
path = rootPath + videoPath.split('/')[-1]

try:
    if not os.path.exists(rootPath):
        os.mkdir(rootPath)
    if not os.path.exists(path):
        r = requests.get(videoPath)
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()
        r.close()
    else:
        print('文件已存在')
except:
    print('error')


