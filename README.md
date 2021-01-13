# 调用baidu翻译的接口，实现转换android stuido 中的values/strings.xml 解放生产力，自动翻译生成文件
## 因为使用的是合法免费的接口，每秒只能请求一次，测试结果翻译330个字段需要8分钟左右
### 更多文档请参考[百度翻译api文档](https://api.fanyi.baidu.com/doc/21)
### 常见语种列表

名称      |代码	|名称	|代码	|名称	|代码
------|-------|-------|--------|--------|----
自动检测	|auto	|中文	|zh	    |英语	|en
粤语	    |yue	|文言文  |wyw	|日语|jp
韩语	    |kor	|法语	|fra	|西班牙语	|spa
泰语	    |th	    |阿拉伯语 |ara	|俄语	|ru
葡萄牙语	|pt	    |德语	|de	    |意大利语 |it
希腊语	|el	    |荷兰语	|nl	    |波兰语	|pl
保加利亚语|bul	|爱沙尼亚语|est	|丹麦语	|dan
芬兰语	|fin	|捷克语	|cs	    |罗马尼亚语	|rom
斯洛文尼亚语|slo	|瑞典语	|swe	|匈牙利语	|hu
繁体中文	|cht	|越南语	|vie	 

## 运行结果：
### 文件翻译进度：
100%|██████████| 330/330 [08:02<00:00,  1.46s/it]
保存文件strings_cht.xml成功！

### [核心代码](https://github.com/liuyingliuxia/stringTranlate/blob/master/Include/stringXML.py)