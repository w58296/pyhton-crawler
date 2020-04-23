from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import TimeoutException
import re
from pyquery import PyQuery as pq

#防止新浪微博登录输入验证码
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(options=option)

def login():
    try:
        browser.get('https://www.taobao.com/')

        loginBtn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.screen-outer.clearfix > div.col-right > div.tbh-member.J_Module > div > div.member-ft > div.member-logout.J_MemberLogout > a.btn-login.ml1.tb-bg.weight'))
        )

        loginBtn.click()

        windows = browser.window_handles
        browser.switch_to.window(windows[-1])

        weiboLogin = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#login-form > div.login-blocks.sns-login-links > a.weibo-login'))
        )

        weiboLogin.click()

        account = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#pl_login_logged > div > div:nth-child(2) > div > input'))
        )

        password = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#pl_login_logged > div > div:nth-child(3) > div > input'))
        )

        button = browser.find_element_by_css_selector('#pl_login_logged > div > div:nth-child(7) > div:nth-child(1) > a > span')
        #已绑定淘宝的新浪微博账号
        account.send_keys('**************')
        #密码
        password.send_keys('*************')
        button.click()
        #搜索商品
        search()
    except TimeoutException:
        login()

#搜索关键词
def search():
    try:
        search_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )

        search_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
        )
        #搜索关键字
        search_input.send_keys('美食')
        search_button.click()

    except TimeoutException:
        search()



#读取页码数量
def get_page_num():
    page_num = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
    )
    return int(re.search(r'(\d+)', page_num.text, re.S).group(1))



#跳转至下一页
def next_page(page_num):
    print(page_num)
    try:
        page_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )

        page_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )

        page_input.clear()
        page_input.send_keys(str(page_num))

        page_button.click()

        page = WebDriverWait(browser, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_num))
        )

        get_product()
    except TimeoutException:
        print('第%d页跳转异常' %page_num)
        next_page(page_num)


#解析商品信息
def get_product():
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist > div > div > div:nth-child(1)'))
    )
    html = browser.page_source
    doc = pq(html)

    items = doc.find('#mainsrp-itemlist > div > div > div:nth-child(1) > div.item.J_MouserOnverReq').items()

    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }

        print(product)



def main():
    login()
    page_num = get_page_num()
    get_product()
    for i in range(2, page_num+1):
        next_page(i)



if __name__ == '__main__':
    main()