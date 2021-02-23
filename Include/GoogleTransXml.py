#!/usr/bin/python

# -*- coding: UTF-8 -*-
import time
from time import sleep
from tqdm import tqdm
from typing import List
from xml.dom.minidom import Document
from xml.dom.minidom import parse
import http.client
import hashlib
import urllib
import random
import json
import xml.dom.minidom

from Include.GoogleTran import Yuguii


# 把需要翻译的语言全部写在languageList里，批量翻译
# languageList = ['auto', 'cht', 'zh', 'jp', 'kor', 'fra', 'spa', 'th', 'ara', 'ru', 'pt', 'de', 'it',
#                 'el', 'nl', 'pl', 'bul',
#                 'dan', 'fin', 'cs', 'rom', 'slo', 'swe', 'hu', 'cht', 'vie']
# languageList = ['heb', 'sec', 'mot', 'mac', 'bos', 'alb', 'moc', 'hrv', 'slo', 'bul', 'geo']

# 希伯来语heb,塞尔维亚-克罗地亚语sec,黑山语mot,马其顿语mac,波斯尼亚语	bos,阿尔巴尼亚语alb,
# 蒙古语（西里尔）	moc ,	克罗地亚语	hrv,斯洛文尼亚语	slo,保加利亚语bul,格鲁吉亚语	geo

languageList = ['bn']
# 保加利亚语bul，斯洛文尼亚语	slo

# 具体语言对照详见README.md

fromLang = 'en'  # 默认原文语种
# toLang = languageList[5]  # 译文语种
salt = random.randint(32768, 65536)
speed = 0.1  # 高级版本 每秒10个字符翻译
# 使用minidom解析器打开 XML 文档
fromFileName = xml.dom.minidom.parse("test0.xml")
collection = fromFileName.documentElement


# 最后保存的文档
# toFileName = 'strings_' + toLanguage + '.xml'

def open_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read().decode('utf-8')
    return data


def translate(content, tk, toLang):
    if len(content) > 4891:
        print("翻译文本超过限制！")
        return

    content = urllib.parse.quote(content)

    url = "http://translate.google.cn/translate_a/single?client=t" \
          "&sl=en&tl=%s&hl=%s&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
          "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
          "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (toLan, toLan, tk, content)

    result = open_url(url)

    end = result.find("\",")
    if end > 4:
        return result[4:end]


def autoTranslate(toLanguage):
    strings = collection.getElementsByTagName("string")
    nameList = []
    keyList = []
    print('文件翻译进度：')
    for myString in tqdm(strings):
        # print("name: %s" % myString.getAttribute("name"))
        keys = myString.childNodes[0].data
        # print("key== %s" % keys)
        # print("translate== %s" % baiduTranslate(keys, toLanguage))
        # print("=========================================")
        nameList.append(myString.getAttribute('name'))
        keyList.append(GoogleTranslate(keys, toLanguage))
    saveXML(nameList, keyList, toLanguage)


def GoogleTranslate(q, toLanguage):
    js = Yuguii()
    tk = js.getTk(q)
    return translate(q, tk, toLanguage)


def saveXML(nameList, keyList, toLanguage):
    doc = Document()  # 创建DOM文档对象
    resources = doc.createElement('resources')  # 创建根元素
    doc.appendChild(resources)
    # 最后保存的文档
    toFileName = 'strings_' + toLanguage + '.xml'
    try:
        if len(nameList) == len(keyList):
            for (name, key) in zip(nameList, keyList):
                stringItem = doc.createElement('string')  # 创建string
                stringItem.setAttribute('name', name)  # 把name加入
                content = doc.createTextNode(key)  # 创建key
                stringItem.appendChild(content)  # 把两个>...< 中的key 加入
                resources.appendChild(stringItem)  # 最后把string加到resources中
        f = open(toFileName, 'w', encoding='utf-8')
        # f.write(doc.toprettyxml(indent = ' ', newl = '\n', encoding = 'utf-8'))
        doc.writexml(f, indent=' ', newl='\n', addindent='\t', encoding='utf-8')
        f.close()
        print('保存文件%s成功！' % toFileName)
    except TypeError as err:
        print('所有值都为空！翻译失败', err)


if __name__ == '__main__':
    for toLan in languageList:
        autoTranslate(toLan)
