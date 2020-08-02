#!/usr/bin/python
#coding:utf-8

import random
import requests
import re
from bs4 import BeautifulSoup
#from BeautifulSoup import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from config import source
from config import header

##
# 抓取小说正文
#
def detail(url):
    per_artitle_limit_page = 3;
    title=''
    content=''
    for i in range(1, per_artitle_limit_page):
        if i==1:
            part_url = ''
        else:
            part_url = '_%s'%i

        req = requests.get(url.replace('.html',part_url + '.html'),headers = header[random.randint(0,4)])
        _temp_result = req.content.decode('gbk')
        bs = BeautifulSoup(_temp_result, "html.parser")

        # title
        if len(title)<=0:
            title = bs.find('li','active').get_text()#re.findall(title_re, _temp_result)[0]

        
        content_tag = bs.find('div', id='htmlContent')
        if content_tag==None:
            break
        
        next_tag = content_tag.find('p', 'text-danger')
        if next_tag!=None:
            next_tag.clear()
        _ = content_tag.get_text().replace('-->>', '').replace('一秒记住【笔趣阁 www.biqukan.cc】，更新快，无弹窗，免费读！','')
        content += _
    return content


def filter(content):
    _temp = content.split('\r\n')
    for index in range(len(_temp)):
        _temp[index] = _temp[index].replace(' ','')
    _temp = [elem for elem in _temp if elem != None and len(elem) != 0]
    return ''.join(_temp)


if __name__=="__main__": 
    _temp = detail('http://www.biqukan.cc/book/20461/12592815.html')
    print(filter(_temp))


























































