# -*- coding: utf-8 -*-
# author: Chan

import requests
from bs4 import BeautifulSoup as bs
import codecs

url_start = 'http://newjwxt.bjfu.edu.cn/jsxsd/xsxk/xklc_list?Ves632DSdyV=NEW_XSD_PYGL'  # GET
url_main = 'http://newjwxt.bjfu.edu.cn/jsxsd/framework/xsMain.jsp'  # GET
url_login = 'http://newjwxt.bjfu.edu.cn/jsxsd/xk/LoginToXk'  # POST
url_classes = 'http://newjwxt.bjfu.edu.cn/jsxsd/xskb/xskb_list.do'
url_cet = 'http://newjwxt.bjfu.edu.cn/jsxsd/kscj/djkscj_list'


class newjwxt(object):
    def __init__(self, username, password):

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'newjwxt.bjfu.edu.cn',
            'Referer': 'http://newjwxt.bjfu.edu.cn/Logon.do?method=logon',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.get(url_start)
        self.username = username
        self.password = password

    def login(self):
        postdata = {
            'USERNAME': self.username,
            'PASSWORD': self.password
        }
        self.session.post(url_login, data=postdata)
        if(self.session.get(url_main).status_code == 200):
            print("登录成功")

    def info(self):
        r = self.session.get(url_main)
        # print(r.text)
        soup = bs(r.content, "html.parser")
        basic_info = soup.find_all("div", {"class": "Nsb_top_menu_nc"})
        info = basic_info[0].text.strip()
        print(info)

    def saveclasses(self):
        Myclasses = []
        name = 'D:/Download/Myclasses.txt'
        r = self.session.get(url_classes)
        soup = bs(r.content, "html.parser")
        classes = soup.find_all("div", {"class": "kbcontent"})
        classes_1 = soup.find_all("div", {"class": "kbcontent1"})
        print("Saving your classes...")
        for i in range(0, len(classes)):
            Myclasses.append(classes[i].text.strip())
            for i in range(0, len(classes_1)):
                Myclasses.append(classes_1[i].text.strip())
        f = codecs.open(name, 'w')
        for i in Myclasses:
            f.write(str(i)+'\n')
        f.close()
        print("Classes saved.")

    def get_cetscore(self):
        r = self.session.get(url_cet)
        soup = bs(r.content, 'html.parser')
        tr = soup.find_all("tr")
        for i in range(3, len(tr)-1):
            s = tr[i].text.replace('\n\n\n', '\n').replace(
                '\n', ',').split(',')
            print("等级:", s[2], "总分:", s[5], "日期:", s[7], "准考证号:", s[8])


def main():
    new = newjwxt('username', 'password')
    new.login()
    new.info()
    print("请选择执行功能:\na.保存课表\nb.查询四六级成绩\n")
    while True:
        key = input()
        if(key == "a"):
            new.saveclasses()
        elif (key == "b"):
            new.get_cetscore()


if __name__ == '__main__':
    main()
