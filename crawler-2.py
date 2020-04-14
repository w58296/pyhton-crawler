import requests
from bs4 import BeautifulSoup
import csv
import os
import time

#网页的爬取
def get_html(offset):
    url = 'https://maoyan.com/board/4'
    params = {'offset': offset}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
    except:
        return None

    return response.text

#网页解析
def parse_html(html, list):
    soup = BeautifulSoup(html, 'lxml')
    dds = soup.dl.find_all('dd')
    for dd in dds:
        index = dd.i.text.strip()
        title = dd.a['title'].strip()
        star = dd.find('p', class_='star').text.strip()
        realeasetime = dd.find('p', class_='releasetime').text.strip()
        image = dd.a.find('img', class_='board-img')['data-src']
        p = dd.find('p', class_='score')
        score = p.find('i', class_='integer').text+p.find('i', class_='fraction').text.strip()
        item = {'排名': index, '电影名称': title, '图片地址': image, '主演': star[3:], '上映时间': realeasetime[5:], '评分': score}
        list.append(item)

#保存文件
def save_file(list):
    os.chdir('/Users/chenchunrong/Desktop')
    with open('top100.csv', 'w',  encoding='utf-8-sig') as f:
        header = ['排名', '电影名称', '图片地址', '主演', '上映时间', '评分']
        f_csv = csv.DictWriter(f, header)
        f_csv.writeheader()
        f_csv.writerows(list)

if __name__ == '__main__':
    L = []
    for i in range(10):
        html = get_html(i*10)
        parse_html(html, L)
        time.sleep(1)
    save_file(L)
    print('保存成功！')