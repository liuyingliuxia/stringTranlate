#!/usr/bin/python

# -*- coding: UTF-8 -*-


from xml.dom.minidom import parse
import http.client
import hashlib
import urllib
import random
import json
import xml.dom.minidom

# 使用minidom解析器打开 XML 文档
fileName = xml.dom.minidom.parse("strings.xml")
DOMTree = xml.dom.minidom.parse("movies.xml")

# collection = DOMTree.documentElement
collection = fileName.documentElement

appid = '20210110000668359'  # 填写你的appid
secretKey = 'rX_4tltNBEZMl5PsxW79'  # 填写你的密钥

httpClient = None
myurl = '/api/trans/vip/translate'

fromLang = 'en'  # 原文语种
toLang = 'jp'  # 译文语种
salt = random.randint(32768, 65536)


def printxml():
    if collection.hasAttribute("shelf"):
        print
        "Root element : %s" % collection.getAttribute("shelf")

    # 在集合中获取所有电影

    movies = collection.getElementsByTagName("movie")

    # 打印每部电影的详细信息

    for movie in movies:

        print("*****Movie*****")

        if movie.hasAttribute("title"):
            print("Title: %s" % movie.getAttribute("title"))

        type = movie.getElementsByTagName('type')[0]

        print("Type: %s" % type.childNodes[0].data)

        format = movie.getElementsByTagName('format')[0]

        print("Format: %s" % format.childNodes[0].data)

        rating = movie.getElementsByTagName('rating')[0]

        print("Rating: %s" % rating.childNodes[0].data)

        description = movie.getElementsByTagName('description')[0]

        print("Description: %s" % description.childNodes[0].data)


def printString():
    strings = collection.getElementsByTagName("string")
    for myString in strings:
        print("name: %s" % myString.getAttribute("name"))
        # key = collection.getElementsByTagName("string")[0]
        keys = myString.childNodes[0].data
        print("key== %s" % keys)
        print("translate== %s" % baiduTranslate(keys))
        print("=========================================")


def baiduTranslate(q):
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurls = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurls)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        # print(result)
        return jsonToString(result)

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


def jsonToString(data):
    # Python 字典类型转换为 JSON 对象
    # data1 = {
    #     'no': 1,
    #     'name': 'Runoob',
    #     'url': 'http://www.runoob.com'
    # }

    json_str = json.dumps(data)
    # print("Python 原始数据：", repr(data))
    print("JSON 请求结果：", json_str)

    # 将 JSON 对象转换为 Python 字典
    data2 = json.loads(json_str)
    # print("%s to %s " % (data2['from'], data2["to"]))
    print("data['trans_result']: ", data2['trans_result'])
    result = data2['trans_result']
    # print("======",result[0]['dst'])
    return result[0]['dst']


if __name__ == '__main__':
    # printxml();
    printString()
    datas = baiduTranslate('hello world')
    jsonToString(datas)
