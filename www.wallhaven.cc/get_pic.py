from bs4 import BeautifulSoup
import requests
import os
import time
from multiprocessing import Pool
import traceback


rootUrl = 'https://wallhaven.cc/toplist?page='
rootDir = 'E:\\壁纸\\wallhaven.cc\\'
if not os.path.exists(rootDir):
    os.mkdir(rootDir)


def down_pic(_page_num):
    save_path = rootDir + str(_page_num)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    try:
        r = requests.get(rootUrl + str(_page_num))
        r.close()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        # 爬取图片并下载到本地
        img_list = soup.find_all(name='img', attrs={'alt': 'loading', 'class': 'lazyload'})
        print('page num: ' + str(_page_num) + ' :: ' + 'pic_count: ' + str(len(img_list)))

        count = 1
        for img in img_list:
            # 获取图片真实url地址
            r = requests.get(img.next_sibling.attrs.get('href'), timeout=5)
            r.close()
            soup1 = BeautifulSoup(r.text, 'html.parser')

            img_real_url = soup1.find(name='img', attrs={'id': 'wallpaper'}).attrs.get('src')

            path = save_path + "\\" + str(img_real_url).split('/')[-1]
            if not os.path.exists(path):
                img = requests.get(img_real_url)
                img.close()
                with open(path, 'wb') as file:
                    file.write(img.content)
                    file.close()
                    print(str(time.ctime())+' '+str(_page_num)+' page\'s pic url: '+str(img_real_url)+' saved success!')
            else:
                print(str(time.ctime()) + ' ' + path + ' 文件已存在')
                # 避免被检测到请求过快而终止
                time.sleep(2)
            time.sleep(2)
            count = count + 1
    except Exception as e:
        print(str(time.ctime()) + ' ' + str(_page_num) + ' ' + img_real_url + ' exception')
        print(e.args)
        print('==============================')
        print(traceback.format_exc())


if __name__ == '__main__':
    start_time = time.time()
    pool = Pool(10)
    for page_num in range(1, 201):
        pool.apply_async(down_pic, (page_num,))
    pool.close()
    pool.join()
    end_time = time.time()
    print('total time：%s s ' % (end_time - start_time))
