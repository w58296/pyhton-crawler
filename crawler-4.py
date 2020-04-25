import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from wordcloud import WordCloud

def get_html():
    url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=179242916'


    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
    }


    response = requests.get(url, headers=headers)

    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, 'lxml')

    return [item.text for item in soup.find_all('d')]


def generate_word_cloud(data):
    wc = WordCloud(
        font_path=r'simhei.ttf',
        background_color='white',
        width=500,
        height=350,
        max_font_size=50,
        min_font_size=10,
        mode='RGBA'
    )

    wc.generate(" ".join(data))
    wc.to_file('wordcloud.png')


def get_html_by_chrome():
    browser = webdriver.Chrome()
    browser.get('https://www.bilibili.com/video/BV1ZT4y1G75S')

    try:
        button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#bilibiliPlayer > div.bilibili-player-area.video-state-pause.video-control-show.video-state-blackside > div.bilibili-player-video-wrap > div.bilibili-player-video-control-wrap > div.bilibili-player-video-control > div.bilibili-player-video-control-bottom > div.bilibili-player-video-control-bottom-left > div.bilibili-player-video-btn.bilibili-player-video-btn-start.video-state-pause > button.bilibili-player-iconfont.bilibili-player-iconfont-start > span > svg'))
        )
        button.click()

        return browser.page_source

    except EC:
        return get_html_by_chrome()


if __name__ == '__main__':
    data = get_html()
    generate_word_cloud(data)