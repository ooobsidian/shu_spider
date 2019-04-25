# coding=utf-8
from bs4 import BeautifulSoup
import re
import requests
import datetime
import json
import hashlib

base_url = 'http://www.its.shu.edu.cn'


def get_html(url):
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


# 获取viewState,用于翻页请求
def get_view_state(soup):
    view_state = soup.find(name='input', attrs={'name': '__VIEWSTATE'})
    return view_state['value']


# 获取新闻信息（标题,链接,发布时间,内容）
def get_news_info(soup):
    news_list = soup.find_all(name='a', attrs={'class': 'linkfont1'})
    date_list = soup.find_all(name='span', attrs={'class': 'linkfont1'})
    for (i, j) in zip(news_list, date_list):
        # 构造datetime
        time = j.string.split('-')
        date = datetime.datetime(int(time[0]), int(time[1]), int(time[2]))
        # md5 = re.findall(r'Id=([0-9]+)', i['href'])[0]
        md5 = get_md5(base_url + i['href'])
        news_url = base_url + i['href']
        url = "http://129.204.71.113:9999/api/v2/spider/news"
        header = {
            "Authorization": "",
            "Content-Type": "application/json"
        }
        # 若跳转链接不属于信息办网站，则不爬取内容
        # 这里判断一下是不是在站内页面 如果跳转到新页面例如shu.edu.cn就将content置为标题
        if str(i['target']) != '_new':
            news_content = get_news_content(base_url + i['href'])
        else:
            news_content = i['title']
            news_url = i['href']
            print(news_url)
        # 在此将新闻插入数据库
        para = {"userId": "a65a06a6-8e44-4b4c-8207-6f3f0a32635c", "mediaTitle": i['title'],
                "newsUrl": news_url, "newsLabelId": "255c2ace-d8ea-48dd-acdb-deceb4aef3fd",
                "contentFromScrapy": news_content, "md5": md5, "createTime": str(date)}
        para = json.dumps(para)
        res = requests.post(url=url, data=para, headers=header)
        print(i['title'])
        if res.status_code == 200:
            print(res.text)
            print("插入新闻成功")
        else:
            print(res.status_code)


# 获取新闻内容
def get_news_content(url):
    news_res = requests.get(url)
    news_res.encoding = news_res.apparent_encoding
    news_soup = BeautifulSoup(news_res.text, 'html.parser')
    news_content = news_soup.find('span', attrs={'class': 'ArticleContent'})
    # fuck搞了一晚上，直接.get_text()获取一个标签下的所有文字，包括子标签
    news_content_stripe = news_content.get_text().strip().replace(' ', '').replace('\r\n', ' ')
    news_content_stripe = news_content_stripe.encode('utf-8')
    return news_content_stripe


# 获取新闻页数
def get_page_num(url):
    soup = get_html(url)
    page_info = soup.findChild(attrs={'class': 'pgctl'})
    for i, val in enumerate(page_info):
        if i == 0:
            page = val.string
            break
    # 将正则匹配到的页码转成数字
    tmp = re.findall(r'[0-9]+', page)
    page_num = int(tmp[0])
    return page_num


def get_next_page(current_view_state):
    raw = r'''------WebKitFormBoundarySCw7dznpMFYKyT0X
Content-Disposition: form-data; name="__EVENTTARGET"

dnn:ctr57430:ArticleList:_ctl0:lbtnNext
------WebKitFormBoundarySCw7dznpMFYKyT0X
Content-Disposition: form-data; name="__EVENTARGUMENT"


------WebKitFormBoundarySCw7dznpMFYKyT0X
Content-Disposition: form-data; name="ScrollTop"


------WebKitFormBoundarySCw7dznpMFYKyT0X
Content-Disposition: form-data; name="__dnnVariable"


------WebKitFormBoundarySCw7dznpMFYKyT0X
Content-Disposition: form-data; name="__VIEWSTATE"


'''
    end = r'------WebKitFormBoundarySCw7dznpMFYKyT0X--'
    Url = 'http://www.its.shu.edu.cn/Default.aspx?tabid=30346'
    header = {'content-type': 'multipart/form-data;boundary=----WebKitFormBoundarySCw7dznpMFYKyT0X'}
    # 模拟提交multipart/form-data表单数据
    params = raw + current_view_state + '\n' + end
    # 改data为files
    r = requests.post(url=Url, data=params, headers=header)
    # print r.request.body
    if r.status_code == 200:
        print('翻页成功')
        # print r.text
        return r.text
    else:
        print('翻页失败')


def get_all_news():
    url = 'http://www.its.shu.edu.cn/Default.aspx?tabid=30346'
    current_html = get_html(url)
    get_first_page(url)
    page = get_page_num(url)
    for i in range(page - 1):
        current_view_state = get_view_state(current_html)
        next_html = get_next_page(current_view_state)
        current_html = BeautifulSoup(next_html, 'html.parser')
        get_news_info(current_html)


def get_first_page(url):
    first_html = get_html(url)
    get_news_info(first_html)


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == '__main__':
    get_all_news()
