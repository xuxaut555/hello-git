#多进程爬虫
"""
多进程的使用方法
1 from multiprocessing import Pool
2 pool = Pool(processes=4)
3 pool.map(func,iterable)
"""

import re
import time
from multiprocessing import Pool

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
}

def re_scraper(url):
    res = requests.get(url,headers=headers)
    names = re.findall('<h2>(.*?)</h2>', res.text, re.S)
    contents = re.findall('<div class="content">.*?<span>(.*?)</span>', res.text, re.S)
    laughs = re.findall('<i class="number">(\d+)</i>',res.text,re.S)
    comments = re.findall('<i class="number">(\d+)</i>', res.text, re.S)
    infos = list()
    for name,content,laugh,comment in zip(names,contents,laughs,comments):
        info = {
            'name':name,
            'content':content,
            'laugh':laugh,
            'comment':comment
        }
        infos.append(info)
    return infos

if __name__ == "__main__":
    urls = ['https://www.qiushibaike.com/8hr/page/{}/'.format(str(i)) for i in range(1, 36)]
    start_1 = time.time()
    for url in urls:
        re_scraper(url)
    end_1 = time.time()
    print('串行爬虫耗时:',end_1 - start_1)

    start_2 = time.time()
    pool = Pool(processes=2)
    pool.map(re_scraper,urls)
    end_2 = time.time()
    print('2进程爬虫耗时:',end_2 - start_2)

    start_3 = time.time()
    pool = Pool(processes=4)
    pool.map(re_scraper,urls)
    end_3 = time.time()
    print('4进程爬虫耗时:',end_3 - start_3)