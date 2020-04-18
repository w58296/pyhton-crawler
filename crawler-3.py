import json
import re
import requests
import html
import os
from hashlib import md5
from multiprocessing.pool import Pool


#列表页面对单页链接的获取
def get_page_index(offset, keyword):
    #查看Chrome对应的query string parameter
    params = {
    'aid': 24,
    'app_name': 'web_search',
    'offset': offset,
    'format': 'json',
    'keyword': keyword,
    'autoload': 'true',
    'count': 20,
    'en_qc': 1,
    'cur_tab': 1,
    'from': 'search_tab',
    'pd': 'synthesis',
    '_signature': '6JkUpAAgEBDRZ8Yf6j7WrOiYVbAALYMK1oqx8RGxwo9EfOP3P4h2l.4dWrtlx4AxePcpp16HIaQwm40FzFziTLUZlLJOUVUIm.LZPFVpEAAajXsk - QzqFHrniYZ8P.8qqOc'
    }

    #没有cookie爬取不到
    headers = {
    'x-requested-with': 'XMLHttpRequest',
    'user - agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'cookie': '__tasessionId=ma7hh1k0i1564919983167; csrftoken=a2318e2879cb7daac5e3169ac6731316; tt_webid=6721280117165032963; UM_distinctid=16c5c7fee055e9-09bb3e770de9ee-7a1437-144000-16c5c7fee0685f; CNZZDATA1259612802=745403741-1564916538-%7C1564916538; s_v_web_id=7a3ff2239d94842e143caf217478bc62'
    }

    url = 'https://www.toutiao.com/api/search/content/?'

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.text
    except:
        print('访问失败！')
        return None

#解析列表页，提取网址
def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            if 'cell_type' in item.keys() or 'ala_src' in item.keys():
                yield None
            else:
                 yield item.get('article_url')


#获取单页的网页内容
def get_page(url):
    if url:
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            'cookie': 'tt_webid=6816147933877700103; s_v_web_id=verify_k927nskn_hMeoJpoA_o5hR_4NbG_8TLz_LBsa32K6ErEE; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6816147933877700103; ttcid=9bec03390f394de48a4b78b71a72dae519; csrftoken=f778b695c5457d2d20e3c29d11f45efa; SLARDAR_WEB_ID=6878ab60-2f00-4f4f-bf16-0cc516030a14; __tasessionId=des62luta1587116858610; tt_scid=gMbRERg08rd-4poCTwAab2HoWxhFhSZhLOI6SV0YGdqaJlSlGDIozjoTddBkiFb1717a'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except:
            print('爬取页面失败！',url)
        return None
    return None


#图集形式解析
def get_images(content):
    #有两种不同的页面，要分开解析
    #图集页面的正则
    pattern1 = re.compile('.*?<title>(.*?)</title>.*?gallery:\sJSON\.parse\((.*?)\).*?', re.S)
    #文章界面的解析
    pattern2 = re.compile('.*?articleInfo:.*?title:\s(.*?),.*?content:\s(.*?),.*?', re.S)

    result1 = re.search(pattern1, content)

    if result1:
        title = result1.group(1)
        sub_images = json.loads(json.loads(result1.group(2)))
        if sub_images and 'sub_images' in sub_images.keys():
           print(sub_images.get('sub_images'))
           return {
                    'title': title,
                    'urls': [url.get('url') for url in sub_images.get('sub_images')]
                   }

    else:
        result2 = re.search(pattern2, content)

        if result2:
            title = result2.group(1)
            pattern3 = re.compile('<img.*?"(.*?)\"', re.S)
            urls = html.unescape(result2.group(2).encode('utf-8').decode('unicode-escape'));
            result3 = re.findall(pattern3, urls)
            return {
                'title': title[7:-15],
                'urls': [url[0:-1] for url in result3]
            }

    return None


#保存图片
def save_images(page):
    if page:
        title = page.get('title')
        urls = page.get('urls')

        img_path = 'img' + os.path.sep + title

        if not os.path.exists(img_path):
            os.makedirs(img_path)

        try:
            for url in urls:
                response = requests.get(url)
                response.raise_for_status()
                file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                    file_name=md5(response.content).hexdigest(),
                    file_suffix='jpg')  # 单一文件的路径
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print('Downloaded image path is %s' % file_path)
                else:
                    print('Already Downloaded', file_path)
        except Exception as e:
            print(e)



def main(offset):
    html = get_page_index(offset, '街拍')
    if html:
        for url in parse_page_index(html):
            page = get_page(url)
            if page:
                images = get_images(page)
                save_images(images)


if __name__ == '__main__':

    pool = Pool()
    groups = ([x * 20 for x in range(0, 3)])
    pool.map(main, groups)


