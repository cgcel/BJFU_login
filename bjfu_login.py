# -*- coding: utf-8 -*-
# author: Chan

import requests
from bs4 import BeautifulSoup as bs
import time

url = 'http://202.204.122.1/index.jsp'
url1 = 'http://202.204.122.1/checkLogin.jsp'
url2 = 'http://202.204.122.1/user/index.jsp?ip='
url3 = 'http://202.204.122.1/user/network/connect_action.jsp?userid='


class BJFULOGIN(object):
    def __init__(self, username, password):
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

        # get ip
        s = bs(self.session.get(url).content, 'html.parser')
        self.ip = s.find("input", {"name": "ip"})["value"]
        self.url2 = url2+self.ip+'&action=connect'

        self.username = username
        self.password = password

    def login(self):
        postdata = {
            'username': self.username,
            'password': self.password,
            'ip': self.ip,
            'action': 'admin'
        }
        try:
            self.session.post(url1, data=postdata)
        except:
            print("login failed.")

    def disconnect(self):
        self.session.get(url4+self.userid+'&ip='+self.ip+'&type=2')

    def connect(self):
        try:
            # get userid
            userid = ''
            r = self.session.get(self.url2)
            idinfo = r.text.find("userid=")
            for i in range(7, 13):
                userid = userid+r.text[int(idinfo)+i]
            self.userid = userid

            # build the url
            self.url3 = url3+self.userid+'&ip='+self.ip+'&type=2'
            self.session.get(self.url3)
        except:
            print("connect failed.")

    def info(self):
        try:
            soup = bs(self.session.get(
                self.url3).content, "html.parser")
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
    bjfu = BJFULOGIN('username', 'password')
    bjfu.login()
    bjfu.connect()
    time.sleep(1)
    bjfu.info()


if __name__ == "__main__":
    main()
