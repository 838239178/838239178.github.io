import re
import os
import logging
import requests

"""
百度站长平台
普通收录：向baidu推送页面以获得更高的曝光率
"""

# 推送目录
path = "./_posts"

# 获取目录的所有文件
fileList = os.listdir(path)

# 初始化日志
def initlogger():
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format='[%(levelname)s]: %(message)s')


# 解析文章名
def getPageName(fileName: str) -> str:
    return re.search(r'.*-.*-.*-(.*).md', fileName).group(1)


def main():
    content=[]
    url='https://blog.pressed.top/'
    for f in fileList:
        pageUrl = url + getPageName(f) + '.html '
        content.append(pageUrl)

    """"
    requests模块post类型使用text/plain的方法：
    1. 直接将字符串赋值到 parameter-data
    2. 换行使用 '\n'.join() 方法
    3. join内是字符串序列， 用迭代器获得
    4. 最终字符串用UTF-8进行编码->bytes
    """
    resp = requests.post(
        url='http://data.zz.baidu.com/urls?site=https://blog.pressed.top&token=by6mvvujkkDYRcdo', 
        data=('\n'.join(f'{k}' for k in content).encode('utf-8')))

    res: dict = resp.json()
    if resp.status_code == 200:
        info = '成功推送' + str(res['success']) + '条，' + '当日推送余量还剩' + str(res['remain']) + '条'
        if res.__contains__('not_valid'):
            # 返回的是raw_unicode编码的链接，直接输出会乱码，先用‘raw_unicode_escape’编码后再解码可以得到正确字符串
            # format of 'raw_unicode_escape' begin with '\x' then append 2 chars
            # format of 'unicode_escape' begin with '\u' then append 4 chars
            info += '\n 一些连接推送失败:\n' + '\n'.join((f'{k}'.encode('raw_unicode_escape').decode()) for k in res['not_valid'])
    else:
        info = '推送失败，' + res['message']

    logging.info(info)

if __name__ == '__main__':
    initlogger()
    main()