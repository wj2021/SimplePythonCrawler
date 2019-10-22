from bs4 import BeautifulSoup
import requests
import os


# 获取下一页的链接地址
def get_next_page_url(soup1):
    next_page_ink = ''
    for s in soup1.find_all(name='a'):
        if str(s.string) == '下一页':
            next_page_ink = s.attrs.get('href')
    return next_page_ink


rootUrl = 'http://pic.netbian.com'
urlList = ['http://pic.netbian.com/4kfengjing/',
           'http://pic.netbian.com/4kmeinv/',
           'http://pic.netbian.com/4kyouxi/',
           'http://pic.netbian.com/4kdongman/',
           'http://pic.netbian.com/4kyingshi/',
           'http://pic.netbian.com/4kmingxing/',
           'http://pic.netbian.com/4kqiche/',
           'http://pic.netbian.com/4kdongwu/',
           'http://pic.netbian.com/4krenwu/',
           'http://pic.netbian.com/4kmeishi/',
           'http://pic.netbian.com/4kzongjiao/',
           'http://pic.netbian.com/4kbeijing/']

rootDir = 'E:\\壁纸2019.10.20\\'
if not os.path.exists(rootDir):
    os.mkdir(rootDir)

for url in urlList:
    savePath = rootDir + url.split('/')[-2]
    if not os.path.exists(savePath):
        os.mkdir(savePath)
    count = 0
    while True:
        try:
            r = requests.get(url)
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, 'html.parser')

            # 爬取图片并下载到本地
            imgList = soup.find_all(name='img', attrs={'title': ''})
            if len(imgList) > 0:
                picSavePath = savePath + '\\' + str(count)
                if not os.path.exists(picSavePath):
                    os.mkdir(picSavePath)

            for img in imgList:
                if str(img.attrs.get('alt')).find('发消息') < 0 and img.attrs.get('alt') is not None:
                    imgRealPath = rootUrl + img.attrs.get('src')
                    path = picSavePath + "\\" + imgRealPath.split('/')[-1]
                    if not os.path.exists(path):
                        img = requests.get(imgRealPath)
                        with open(path, 'wb') as f:
                            f.write(img.content)
                            f.close()
                    else:
                        pass
                        # print('文件已存在')

            nextPageLink = get_next_page_url(soup)
            if nextPageLink != '':
                url = rootUrl + nextPageLink
                count = count + 1
            else:
                break
        except:
            print('error')
    break
