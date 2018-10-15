# -*- coding:utf-8 -*-
# author: Chan

import requests
from bs4 import BeautifulSoup as bs
import re
from newjwxt import newjwxt

url_base = 'http://newjwxt.bjfu.edu.cn'
url_main = 'http://newjwxt.bjfu.edu.cn/jsxsd/xspj/xspj_find.do?Ves632DSdyV=NEW_XSD_JXPJ'
url_post = 'http://newjwxt.bjfu.edu.cn/jsxsd/xspj/xspj_save.do'

pattern = re.compile(r'javascript:JsMod1\(\'(.+)\">评教')


class JXPJ(object):
    def __init__(self, username, password):
        self.session = newjwxt(username, password).login()

    def get_url(self):
        r = self.session.get(url_main)
        soup = bs(r.content, 'html.parser')
        # print(soup)
        s = soup.find_all("a", {"title": "点击进入评价"})
        url = url_base + s[0]['href']
        return url

    def get_courses(self):
        url_target = self.get_url()
        r = self.session.get(url_target)
        result = pattern.findall(r.text)
        target_urls = []
        for part in result:
            target_urls.append(url_base + part.split('\'')[0])
        return target_urls

    def evaluate(self):
        target_urls = self.get_courses()
        for url in target_urls:
            formdata = {}
            r = self.session.get(url)
            soup = bs(r.content, 'html.parser')
            result = soup.find_all("input", {"type": "hidden"})
            part1 = result[1:11]
            formdata['issubmit'] = 1  # part1[0]['value']
            for part in part1:
                formdata[part['name']] = part['value']
            for part in result[11:]:
                formdata[part['name']] = part['value']
            part2 = soup.find_all("input", {"name": "pj06xh"})
            for part in part2:
                num = part['value']
                s = "pj0601id_"
                data = soup.find_all("input", {"name": s+num})[1]['value']
                formdata[s+num] = data
            part3 = soup.find_all("input", {"name": "xszwpjxh"})
            for part in part3:
                num = part['value']
                s = "pj0601id_"
                data = soup.find_all("input", {"name": s+num})[1]['value']
                formdata[s+num] = data
            self.session.post(url_post, formdata)
        print("Completed.")


def main():
    username = input("请输入学号: ")
    password = input("请输入教务系统密码: ")
    print("评教中...")
    JXPJ(username, password).evaluate()


if __name__ == '__main__':
    main()