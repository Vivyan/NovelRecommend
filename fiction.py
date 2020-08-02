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
import hashlib
import time

hash_md5 = hashlib.md5()

## 
# 通过分类获取文章名和对应的链接
# 
def fiction():
    url = source['biquge']['category_url']
    cur_category_name = ''
    _list = {}
    for i in range(source['biquge']['category_min'], source['biquge']['category_max']):
        req = requests.get(url.replace('{id}', '%s'%i), headers = header[random.randint(0,4)])
        _temp_result = req.content.decode('gbk')
        bs = BeautifulSoup(_temp_result, "html.parser")

        next_page = bs.find('ul', id='pagelink')
        while next_page!=None:
            next_page = next_page.find('a', 'next')
            if next_page==None:
                break

            # 更新小说
            _page = _cur_page(bs)
            print('page.length = %d'%len(_page))
            _list.update(_page)

            # 获取下一页数据
            req = requests.get(next_page.attrs['href'], headers = header[random.randint(0,4)])
            _temp_result = req.content.decode('gbk')
            bs = BeautifulSoup(_temp_result, "html.parser")
            next_page = bs.find('ul', id='pagelink')

            # 短暂休息一下
            time.sleep(random.random())

    return _list

## 
# 当前页面的所有小说信息
# 
def _cur_page(bs):
    _list = {}
    # top列表
    li_tags = bs.findAll('li', 'list-group-item')
    if li_tags==None or len(li_tags)<=0:
        return _list

    for item in li_tags:
        a_tag = item.find('a')
        _item = {'name':a_tag.get_text(), 'link': a_tag.attrs['href']}

        # 作者
        author = item.find('small').get_text().replace('/ ', '')
        _item['author'] = author

        # 阅读数
        readers = item.find('span').get_text()
        _item['readers'] = readers

        hash_md5.update(_item['link'])
        _list[hash_md5.hexdigest()] = _item

    # 最近更新列表
    tr_tags = bs.findAll('tr')
    if tr_tags==None or len(tr_tags)<=1:
        return _list

    for item in tr_tags:
        a_tag = item.find('a')
        if a_tag==None:
            continue

        _item = {'name':a_tag.get_text(), 'link': a_tag.attrs['href']}

        # 作者
        author = item.find('td', 'text-muted').get_text()
        _item['author'] = author

        # 状态
        status = item.findAll('td')
        _item['status'] = status[len(status)-1].get_text()

        hash_md5.update(_item['link'])
        if _list.has_key(hash_md5.hexdigest())!=True:
            _list[hash_md5.hexdigest()] = _item
        else:
            _list[hash_md5.hexdigest()]['status'] = _item['status']

    return _list


if __name__=="__main__": 
    _temp = fiction()
    print('done')












































































































