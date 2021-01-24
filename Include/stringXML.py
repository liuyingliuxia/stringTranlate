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

appid = '20210110000668359'  # 填写你的appid
secretKey = 'rX_4tltNBEZMl5PsxW79'  # 填写你的密钥

httpClient = None
myurl = '/api/trans/vip/translate'

# 把需要翻译的语言全部写在languageList里，批量翻译
# languageList = ['auto', 'cht', 'zh', 'jp', 'kor', 'fra', 'spa', 'th', 'ara', 'ru', 'pt', 'de', 'it',
#                 'el', 'nl', 'pl', 'bul',
#                 'dan', 'fin', 'cs', 'rom', 'slo', 'swe', 'hu', 'cht', 'vie']
# languageList = ['heb', 'sec', 'mot', 'mac', 'bos', 'alb', 'moc', 'hrv', 'slo', 'bul', 'geo']

# 希伯来语heb,塞尔维亚-克罗地亚语sec,黑山语mot,马其顿语mac,波斯尼亚语	bos,阿尔巴尼亚语alb,
# 蒙古语（西里尔）	moc ,	克罗地亚语	hrv,斯洛文尼亚语	slo,保加利亚语bul,格鲁吉亚语	geo

languageList = ['bul', 'slo']
# 保加利亚语bul，斯洛文尼亚语	slo

# 具体语言对照详见README.md

fromLang = 'en'  # 原文语种
# toLang = languageList[5]  # 译文语种
salt = random.randint(32768, 65536)
speed = 0.1  # 默认值为1 请求接口的频率 最快0.8了，再快就要充钱了
# 使用minidom解析器打开 XML 文档
fromFileName = xml.dom.minidom.parse("strings.xml")
collection = fromFileName.documentElement


# 最后保存的文档
# toFileName = 'strings_' + toLanguage + '.xml'


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
        keyList.append(baiduTranslate(keys, toLanguage))
    saveXML(nameList, keyList, toLanguage)


def baiduTranslate(q, toLanguage):
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurls = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLanguage + '&salt=' + str(
        salt) + '&sign=' + sign
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurls)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        time.sleep(speed)  # 免费的api接口，只能1秒请求一次
        # print(result)
        return jsonToString(result)

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


def jsonToString(data):
    # Python 字典类型转换为 JSON 对象
    json_str = json.dumps(data)
    # print("JSON 请求结果：", json_str)

    # 将 JSON 对象转换为 Python 字典
    data2 = json.loads(json_str, encoding='utf-8')
    # print("%s to %s " % (data2['from'], data2["to"]))
    # print("data['trans_result']: ", data2['trans_result'])
    result = data2['trans_result']
    return result[0]['dst']


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
    except TypeError as err:
        print('所有值都为空！翻译失败', err)
    finally:
        f = open(toFileName, 'w', encoding='utf-8')
        # f.write(doc.toprettyxml(indent = ' ', newl = '\n', encoding = 'utf-8'))
        doc.writexml(f, indent=' ', newl='\n', addindent='\t', encoding='utf-8')
        f.close()
        print('保存文件%s成功！' % toFileName)


if __name__ == '__main__':
    for toLan in languageList:
        autoTranslate(toLan)
    # autoTranslate('jp')
