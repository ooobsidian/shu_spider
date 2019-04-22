# coding=utf-8
from bs4 import BeautifulSoup
import re
import requests
import datetime
import json
import hashlib
import random

base_url = 'http://www.bio.shu.edu.cn/'
user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",

]


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
            "Content-Type": "application/json",
            "User-Agent": random.choice(user_agent)
        }
        # 若跳转链接不属于信息办网站，则不爬取内容
        # print i['target']
        # 这里判断一下是不是在站内页面 如果跳转到新页面例如shu.edu.cn就将content置为标题
        if str(i['target']) != '_new':
            news_content = get_news_content(base_url + i['href'])
        else:
            news_content = i['title']
            news_url = i['href']
            print news_url
        # 在此将新闻插入数据库
        # TODO 1
        para = {"userId": "a65a06a6-8e44-4b4c-8207-6f3f0a32635c", "mediaTitle": i['title'],
                "newsUrl": news_url, "newsLabelId": "5c90e520-56c4-432e-a33c-04608f500e13",
                "contentFromScrapy": news_content, "md5": md5, "createTime": str(date)}
        para = json.dumps(para)
        res = requests.post(url=url, data=para, headers=header)
        print i['title']
        if res.status_code == 200:
            print res.text
            print "插入新闻成功"
        else:
            print res.status_code


# 获取新闻内容
def get_news_content(url):
    news_res = requests.get(url)
    news_res.encoding = news_res.apparent_encoding
    news_soup = BeautifulSoup(news_res.text, 'html.parser')
    news_content = news_soup.find('span', attrs={'class': 'ArticleContent'})
    if news_content is not None:
        # fuck搞了一晚上，直接.get_text()获取一个标签下的所有文字，包括子标签
        news_content_stripe = news_content.get_text()
        news_content_stripe = news_content_stripe.encode('utf-8')
        return news_content_stripe


# 获取新闻页数
def get_page_num(url):
    soup = get_html(url)
    # TODO 改页码id
    page = soup.find('span', attrs={'id': 'dnn_ctr60049_ArticleList__ctl0_plTotalPage'})
    # # 将正则匹配到的页码转成数字
    tmp = re.findall(r'[0-9]+', page.string.encode('utf-8'))
    page_num = int(tmp[0])
    return page_num


# TODO 2
def get_next_page(current_view_state):
    raw = r'''------WebKitFormBoundarySCw7dznpMFYKyT0X
Content-Disposition: form-data; name="__EVENTTARGET"

dnn:ctr60049:ArticleList:_ctl0:lbtnNext
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
    # TODO 3
    Url = base_url + '/Default.aspx?tabid=31647&mid=60049&ShowAll=true'
    header = {'content-type': 'multipart/form-data;boundary=----WebKitFormBoundarySCw7dznpMFYKyT0X'}
    # 模拟提交multipart/form-data表单数据
    params = raw + current_view_state + '\n' + end
    # 改data为files
    r = requests.post(url=Url, data=params, headers=header)
    # print r.request.body
    if r.status_code == 200:
        print '翻页成功'
        # print r.text
        return r.text
    else:
        print '翻页失败'


def get_all_news():
    # TODO 4
    url = base_url + '/Default.aspx?tabid=31647&mid=60049&ShowAll=true'
    current_html = get_html(url)
    page = get_page_num(url)
    get_first_page(url)
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
