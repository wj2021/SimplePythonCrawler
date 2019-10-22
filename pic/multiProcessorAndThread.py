from bs4 import BeautifulSoup
import requests
import os
from multiprocessing import Pool as ProcessorPool
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import time


# 创建本地保存爬取数据的根目录
localSaveRootDir = 'F:\\壁纸2019.10.20\\multiProcessAndThread002\\'
if not os.path.exists(localSaveRootDir[0:localSaveRootDir.index(localSaveRootDir.split('\\')[-2])]):
    os.mkdir(localSaveRootDir[0:localSaveRootDir.index(localSaveRootDir.split('\\')[-2])])
if not os.path.exists(localSaveRootDir):
    os.mkdir(localSaveRootDir)

# 需要爬取数据的网页url地址
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


# # 根据当前页面的soup获取下一页的链接地址
# def get_next_page_url(soup1):
#     next_page_ink = ''
#     for s in soup1.find_all(name='a'):
#         if str(s.string) == '下一页':
#             next_page_ink = s.attrs.get('href')
#     return next_page_ink


# 获取需要爬取的网页列表
def get_page_url_list(soup1, url_prefix):
    list_a = soup1.find_all(name='a')
    url_list = []
    for _i in range(len(list_a)-1, -1, -1):
        try:
            max_page_num = int(str(list_a[_i].string))
            # 如果没有发生异常，说明获取到了最大的页数
            for _j in range(max_page_num+1):
                if _j == 1:
                    url_list.append(url_prefix+'/index.html')
                if _j > 1:
                    url_list.append(url_prefix+'/index_'+str(_j)+'.html')
            return url_list
        except ValueError:
            pass


# 根据一个网页获取该网页下所有的图片网页集合，如根据 http://pic.netbian.com/4kfengjing/ 获取该链接下所有存在图片页面的集合：
# [index.html, index_2.html, index_2.html, ..., index_187.html]，并为不同页面的图片创建不同的存储目录
def get_page_url_list_from_url(_url):
    save_dir = localSaveRootDir + _url.split('/')[-2]
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    try:
        _r = requests.get(_url)
        _r.encoding = _r.apparent_encoding
        soup = BeautifulSoup(_r.text, 'html.parser')
        _page_url_list = get_page_url_list(soup, _url)
        return _page_url_list
    except:
        print('error occur in method: get_pic_from_url')


# 爬取网页中一页的图片，如爬取 http://pic.netbian.com/4kfengjing/index_2.html 这一页的所有图片
def download_pic(_url, save_dir):
    try:
        r = requests.get(_url)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')

        # 爬取图片并下载到本地
        img_list = soup.find_all(name='img', attrs={'title': ''})
        if len(img_list) > 0:
            pic_save_path = save_dir + '\\' + _url.split('/')[-1]
            if not os.path.exists(pic_save_path):
                os.mkdir(pic_save_path)
        for img in img_list:
            if str(img.attrs.get('alt')).find('发消息') < 0 and img.attrs.get('alt') is not None:
                img_real_path = rootUrl + img.attrs.get('src')
                path = pic_save_path + "\\" + img_real_path.split('/')[-1]
                if not os.path.exists(path):
                    img = requests.get(img_real_path)
                    with open(path, 'wb') as f:
                        f.write(img.content)
                        f.close()
                        print('保存图片' + path + '成功')
                else:
                    print('文件' + path + '已存在')
    except:
        print('error occur in method: download_pic')


# # 自定义线程
# class MyThread(threading.Thread):
#     def __init__(self, thread_id, process_id, url1, _save_dir):
#         threading.Thread.__init__(self)
#         self.threadID = process_id * 1000 + thread_id
#         self.processID = process_id
#         self.url = url1
#         self.saveDir = _save_dir
#
#     def run(self):
#         print("start thread:" + str(self.threadID) + ' (processID:', self.processID, ') ' + self.url + ' ' + time.ctime(time.time()))
#         download_pic(self.url, self.saveDir)
#         print("end thread:" + str(self.threadID) + ' (processID:', self.processID, ') ' + self.url + ' ' + time.ctime(time.time()))
#
#
# # 自定义进程
# class MyProcess(multiprocessing.Process):
#     def __init__(self, process_id, url1):
#         multiprocessing.Process.__init__(self)
#         self.processID = process_id
#         self.url = url1
#
#     def run(self):
#         print("start process: " + str(self.processID) + ' ' + self.url + ' ' + time.ctime(time.time()))
#         get_pic_from_url(self.url, self.processID)
#         print("end process: " + str(self.processID) + ' ', self.url + ' ' + time.ctime(time.time()))


#for url in urlList:
    # 单独使用线程爬取数据
    # MyThread(1, url).start()
    # 单独使用多进程并发爬取数据
    # multiprocessing.Process(target=get_pic_from_url, args=(url,)).start()


if __name__ == '__main__':
    # i = 0
    # for url in urlList:
    #     MyProcess(i, url).start()
    #     i = i + 1

    print('start time: ', time.ctime(time.time()))
    start = time.time()

    pool = ProcessorPool(processes=len(urlList) if len(urlList)<64 else 64)
    page_url_list = []
    for url in urlList:
        pool.apply_async(get_page_url_list_from_url, (url,), callback=lambda _page_url_list: page_url_list.extend(_page_url_list))
    pool.close()
    pool.join()

    # 使用进程池 multiprocessing.Pool，此线程池中的线程数目只受内存大小的限制
    pool = ProcessorPool(processes=128)
    for page_url in page_url_list:
        pool.apply_async(download_pic, (page_url, localSaveRootDir+page_url.split('/')[-3], ))
    pool.close()  # 关闭进程池，表示不能在往进程池中添加进程
    pool.join()  # 等待进程池中的所有进程执行完毕，必须在close()之后调用

    # # 使用进程池 concurrent.futures.ProcessPoolExecutor, 此线程池的程序本身会限制线程的最大数目
    # processor_executor = ProcessPoolExecutor(60)
    # for page_url in page_url_list:
    #     processor_executor.submit(download_pic, page_url, localSaveRootDir+page_url.split('/')[-3])
    # processor_executor.shutdown(wait=True)

    # # 使用线程池 concurrent.futures.ThreadPoolExecutor
    # thread_executor = ThreadPoolExecutor(128)
    # for page_url in page_url_list:
    #     thread_executor.submit(download_pic, page_url, localSaveRootDir+page_url.split('/')[-3])
    # thread_executor.shutdown(wait=True)

    print('end time: ', time.ctime(time.time()))
    end = time.time()
    print('total time：%s s' % round(end - start))
