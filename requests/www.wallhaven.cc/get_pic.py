from bs4 import BeautifulSoup
import requests
import os
import time
from multiprocessing import Pool
import traceback

totalPage = 174
rootUrl = 'https://wallhaven.cc/search?categories=111&purity=100&resolutions=3840x2160&ratios=16x9&topRange=1y&sorting=toplist&order=desc&page='
rootDir = 'C:/Users/Jun/Desktop/test/'
header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.69 Safari/537.36 Edg/81.0.416.34"}


# 获取当前时间并格式化
def curTime():
    return '['+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'] '


def urlGet(url, sleepTime=0, timeout1=10):
    # 不停的进行get请求直到成功，并返回结果
    while True:
        try:
            r = requests.get(url, headers=header, timeout=timeout1)
            time.sleep(sleepTime)
            r.close()
            if r.ok: # 检查网页是否返回成功
                return r
            print(curTime() + "429 Too Many Requests, reGet " + url + " again!!!")
            sleepTime = sleepTime + 1
            if sleepTime > 10:
                sleepTime = 10
        except:
            sleepTime = sleepTime + 1
            if sleepTime > 10:
                sleepTime = 10
            print(curTime() + "Exception occured, reGet " + url + " again!!!")


def down_pic(_page_num):
    # 创建保存图片的目录
    save_path = rootDir + str(_page_num)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    img_real_url = "NULL"

    try:
        # 获取图片网站主页
        r = urlGet(rootUrl + str(_page_num), sleepTime=2)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        # 获取所有壁纸的img标签
        img_list = soup.find_all(name='img', attrs={'alt': 'loading', 'class': 'lazyload'})
        picCount = len(img_list)
        print('page: ' + str(_page_num) + '/' + str(totalPage) + ', ' + 'pic_count: ' + str(picCount))

        count = 1
        for img in img_list:
            # 获取图片真实url地址
            r = urlGet(img.next_sibling.attrs.get('href'), sleepTime=5)
            img_real_url = BeautifulSoup(r.text, 'html.parser').find(name='img', attrs={'id': 'wallpaper'}).attrs.get('src')
            path = save_path + "/" + str(img_real_url).split('/')[-1]
            if not os.path.exists(path):
                # 获取图片并保存到本地
                img = urlGet(img_real_url, 1)
                with open(path, 'wb') as file:
                    file.write(img.content)
                print(curTime() + 'page ' + str(_page_num) + ', pic ' + str(count) + '/' + str(picCount) + ', url: ' + str(img_real_url) + ' saved success!')
            else:
                print(curTime() + 'page ' + str(_page_num) + ', pic ' + str(count) + '/' + str(picCount) + ',  ' + path + ' 文件已存在')
            count = count + 1
    except Exception as e:
        print(curTime() + 'page ' + str(_page_num) + ', url: ' + str(img_real_url) + ' exception!!!')
        print(e.args)
        print('============================================================')
        print(traceback.format_exc())


if __name__ == '__main__':
    if not os.path.exists(rootDir):
        os.mkdir(rootDir)

    start_time = time.time()
    processNum = 16
    pool = Pool(processNum)
    for page_num in range(1, totalPage+1):
        pool.apply_async(down_pic, (page_num,))
    pool.close()
    pool.join()
    end_time = time.time()
    print('total time：%s s ' % (end_time - start_time))
