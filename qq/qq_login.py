# -*- coding: utf-8 -*-
# author: Chan

import requests
from bs4 import BeautifulSoup as bs

url_login = 'http://qq.bjfu.edu.cn/XueSheng/Login.aspx'
url_main = 'http://qq.bjfu.edu.cn/XueSheng/All_Activities.aspx'


class qqLogin():
    def __init__(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            # "Cookie": "",#"ASP.NET_SessionId=z0k4duhhl1a2e0ezg3qga55f",
            "Host": "qq.bjfu.edu.cn",
            "Referer": "http://qq.bjfu.edu.cn/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
        }
        self.session = requests.Session()
        r = self.session.get(url_login)
        cookie_value = 'ASP.NET_SessionId=' + \
            dict(r.cookies)['ASP.NET_SessionId']
        soup = bs(r.content, 'html.parser')
        self.v1 = soup.find("input", {"id": "__VIEWSTATE"})['value']
        self.v2 = soup.find("input", {"id": "__VIEWSTATEGENERATOR"})['value']
        self.session.headers.update(headers)
        self.session.headers.update({"Cookie": cookie_value})

    def login(self):
        postdata = {
            "__VIEWSTATE": self.v1,
            "__VIEWSTATEGENERATOR": self.v2,
            "txtZhangHao": "username",
            "txtMiMa": "password",
            "imgbtnDengLu.x": "66",
            "imgbtnDengLu.y": "26"
        }
        self.session.post(url_login, data=postdata)
        self.r = self.session.get(url_main)

    def get_info(self):
        soup = bs(self.r.content, 'html.parser')
        # print(soup.prettify())
        result = soup.find_all("a", {"class": "btnChaKan"})
        for part in result:
            act = part.get_text().strip()
            print(act)


def main():
    qq = qqLogin()
    qq.login()
    qq.get_info()


if __name__ == '__main__':
    main()
