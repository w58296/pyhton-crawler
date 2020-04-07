import requests
import re

#豆瓣读书的爬取

def book_crawler():
    url = "https://book.douban.com/"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        html = r.text


        #----------正则表达式太长匹配很慢-----------
        #pattern = re.compile('<li.*?cover.*?src="(.*?)".*?title="(.*?)".*?author">(.*?)</div>.*?more-meta.*?year">(.*?)</span>.*?publisher">(.*?)</span>.*?abstract">(.*?)</p>.*?</li>', re.S)
        # results = re.findall('<li.*?cover.*?src="(.*?)".*?title="(.*?)".*?author">(.*?)</div>.*?more-meta.*?year">(.*?)</span>.*?publisher">(.*?)</span>.*?abstract">(.*?)</p>.*?</li>', html, re.S)
        # print(len(results))

        results = re.findall("<ul.*?list-col list-col5 list-express slide-item\">(.*?)</ul>", html, re.S)
        for result in results:
            img_urls = re.findall("<li.*?<img\ssrc=\"(.*?)\".*?</li>", result, re.S)
            titles = re.findall("<li.*?<a\sclass.*?href.*?>(.*?)</a>.*?</li>", result, re.S)
            authors = re.findall("<li.*?author\">(.*?)</div>.*?</span>", result, re.S)
            years = re.findall("<li.*?year\">(.*?)</span>.*?</li>", result, re.S)
            publisher = re.findall("<li.*?publisher\">(.*?)</span>.*?</li>", result, re.S)
            abstracts = re.findall("<li.*?abstract\">(.*?)</p>.*?</li>", result, re.S)

            for i in range(len(img_urls)):
                print("图片地址："+img_urls[i])
                print("书名："+titles[i].strip())
                print("作者："+authors[i].strip())
                print("出版年份："+years[i].strip())
                print("出版社："+publisher[i].strip())
                print("简介："+abstracts[i].strip())
                print("------------------------------")

    except requests.HTTPError:
        print("爬取失败")


if __name__ == "__main__":
    book_crawler()