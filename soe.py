# coding=utf-8
from bs4 import BeautifulSoup
import re
import requests
import datetime
import json
import hashlib
import random


class MyInfo(object):
    def __init__(self, base_url, append_url, news_label, event_target, page_num_id, ):
        self.base_url = base_url
        self.append_url = append_url
        self.news_label = news_label
        self.event_target = event_target
        self.page_num_id = page_num_id


cnt = 1
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
def get_news_info(soup, base_url, news_label):
    news_list = soup.find_all(name='a', attrs={'class': 'linkfont1'})
    date_list = soup.find_all(name='span', attrs={'class': 'linkfont1'})
    for (i, j) in zip(news_list, date_list):
        # 构造datetime
        time = j.string.split('-')
        date = datetime.datetime(int(time[0]), int(time[1]), int(time[2]))
        # md5 = re.findall(r'Id=([0-9]+)', i['href'])[0]
        if i['href']:
            md5 = get_md5(base_url + i['href'])
        else:
            md5 = get_md5(i)
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
                "newsUrl": news_url, "newsLabelId": news_label,
                "contentFromScrapy": news_content, "md5": md5, "createTime": str(date)}
        para = json.dumps(para)
        res = requests.post(url=url, data=para, headers=header)
        global cnt
        if res.status_code == 200:
            code = json.JSONDecoder().decode(res.text.replace('/', ''))['code']
            message = json.JSONDecoder().decode(res.text.replace('/', ''))['message']
            if code == 200:
                print ('\033[1;32;0m' + str(cnt) + '\033[0m'), ': ',
                print i['title'],
                print('\033[1;32;0m' + str(code) + '\033[0m')
                cnt += 1
            else:
                print ('\033[1;31;0m' + '✘' + '\033[0m'), ": ",
                print i['title'],
                print('\033[1;31;0m' + str(code) + '\033[0m')
                # print message
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
        news_content_stripe = news_content.get_text().strip().replace(' ', '').replace('\r\n', ' ')
        news_content_stripe = news_content_stripe.encode('utf-8')
        # print news_content_stripe
        return news_content_stripe


# 获取新闻页数
def get_page_num(url, page_num_id):
    soup = get_html(url)
    # TODO 改页码id
    page = soup.find('span', attrs={'id': page_num_id})
    # # 将正则匹配到的页码转成数字
    tmp = re.findall(r'[0-9]+', page.string.encode('utf-8'))
    page_num = int(tmp[0])
    return page_num


# TODO 2
def get_next_page(base_url, append_url, current_view_state, event_target):
    raw = r'''------WebKitFormBoundarySCw7dznpMFYKyT0X
Content-Disposition: form-data; name="__EVENTTARGET"

''' + event_target + '''
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
    url = base_url + append_url
    header = {'content-type': 'multipart/form-data;boundary=----WebKitFormBoundarySCw7dznpMFYKyT0X'}
    # 模拟提交multipart/form-data表单数据
    params = raw + current_view_state + '\n' + end
    # print params
    # 改data为files
    r = requests.post(url=url, data=params, headers=header)
    # print r.request.body
    if r.status_code == 200:
        # print r.text
        return r.text
    else:
        print '翻页失败'


def get_all_news(base_url, append_url, news_label, event_target, page_num_id):
    # TODO 4
    url = base_url + append_url
    current_html = get_html(url)
    page = get_page_num(url, page_num_id)
    get_first_page(base_url, append_url, news_label)
    for i in range(page - 1):
        current_view_state = get_view_state(current_html)
        next_html = get_next_page(base_url, append_url, current_view_state, event_target)
        current_html = BeautifulSoup(next_html, 'html.parser')
        get_news_info(current_html, base_url, news_label)


def get_first_page(base_url, append_url, news_label):
    url = base_url + append_url
    first_html = get_html(url)
    get_news_info(first_html, base_url, news_label)


def get_md5(url):
    # print type(url)
    url = url.encode('utf-8')
    # if isinstance(url, str):
    #     pass
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == '__main__':
    base = 'http://www.soe.shu.edu.cn'
    table_id = '/Default.aspx?tabid='

    i1 = MyInfo(base, table_id + '35739', "0121e3ee-b138-4cf9-b5a8-02c9997cd736",
                "dnn:ctr66333:ArticleList:_ctl0:lbtnNext", "dnn_ctr66333_ArticleList__ctl0_plTotalPage")
    i2 = MyInfo(base, table_id + '35741', "255c2ace-d8ea-48dd-acdb-deceb4aef3fd",
                "dnn:ctr66335:ArticleList:_ctl0:lbtnNext", "dnn_ctr66335_ArticleList__ctl0_plTotalPage")
    i3 = MyInfo(base, table_id + '35742', "b78c35cb-44d9-431c-9e52-f9136c829d4c",
                "dnn:ctr66336:ArticleList:_ctl0:lbtnNext", "dnn_ctr66336_ArticleList__ctl0_plTotalPage")

repeat_list = [i1, i2, i3]
for i in range((len(repeat_list))):
    get_all_news(repeat_list[i].base_url, repeat_list[i].append_url, repeat_list[i].news_label,
                 repeat_list[i].event_target, repeat_list[i].page_num_id)
    print('\033[1;33;0m')
    print "☆" * 61
    print "☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆章节爬取完毕☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆"
    print "☆" * 61
    print('\033[0m')
print('\033[1;34;0m'),
print "本次爬取结束，共新增", cnt - 1, '条新闻资讯'
print('\033[0m')
