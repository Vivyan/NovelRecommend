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

# 抓取目录
def catalog(url):
    _list=[]
    req = requests.get(url,headers = header[random.randint(0,4)])
    _temp_result = req.content.decode('gbk')
    bs = BeautifulSoup(_temp_result, "html.parser")
    
    all_list = bs.find('div', id='list-chapterAll')
    if all_list==None:
        return _list

    list_tag = all_list.find('dl', 'panel-chapterlist')
    if list_tag==None:
        return _list

    a_tags = list_tag.findAll('a')
    for k in a_tags:
        _dict={}
        _dict['name'] = k.get_text()
        _dict['link'] = url + k.attrs['href']
        _list.append(_dict)
    
    return _list


if __name__=="__main__": 
    _temp = catalog('http://www.biqukan.cc/book/47583/')
    print(_temp)









































