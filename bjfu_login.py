# -*- coding: utf-8 -*-
# Author: ElvinChan<ElvinChan0644@outlook.com>

import requests
from bs4 import BeautifulSoup
from neu6_login import neu6
import time
url1 = 'http://202.204.122.1/checkLogin.jsp'
#check your own ip and ueser id on your computer, and fill into url2 and url3 above
url2 = 'http://202.204.122.1/user/index.jsp?ip=118.228.167.204&action=connect'
url3 = 'http://202.204.122.1/user/network/connect_action.jsp?userid=104374&ip=118.228.167.204&type=2'


class BJFULOGIN(object):
    def __init__(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '87',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': '202.204.122.1',
            'Origin': 'http://202.204.122.1',
            'Referer': 'http://202.204.122.1/index.jsp',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(headers)

    def login(self):
        postdata = {
            'username': '',
            'password': '',
            'ip': '',
            'action': 'admin'
        }
        try:
            self.session.post(url1, data=postdata)
            #print(response1.text)
        except:
            print("login failed.")

    def connect(self):
        try:
            self.session.get(url3)
            #print(response3.text)
            #print(response3.status_code)
        except:
            print("connect failed.")

    def info(self):
        try:
            soup = BeautifulSoup(self.session.get(url3).content, "html.parser")
            information = soup.find_all("td", {"class": "left_bt2"})
            info_m = soup.find_all("td", {"class": "form_td_middle"})
            print(information[0].text.strip())
            print("用户类型：", info_m[0].text.strip())
            print("账户余额：", info_m[2].text.strip())
            print("剩余免费流量：", info_m[6].text.strip())
            print("剩余基础流量：", info_m[10].text.strip())
        except:
            print("获取信息失败")


def main():
    bjfu = BJFULOGIN()
    bjfu.login()
    bjfu.connect()
    time.sleep(1)
    bjfu.info()
    print("六维空间:")
    neu = neu6()  # 初始化
    neu.login()


if __name__ == "__main__":
    main()
