import logging
import os
import re
import sys
import time

"""
读取文件内‘YAML Front Matter’中的‘date’标签，获取日期
然后自动按‘year-month-day-xxx.md’重名命名文件
如果文件名中的日期与文字内‘date’的日期不同，则会更改为date内的日期
"""

# 格式化目录
path = "." + os.sep + "_posts"

# 获取目录的所有文件
fileList = os.listdir(path)

# 忽略特殊文件列表
ignoreList = [
    r'.*.txt',
    r'.*.bat'
]


# 获取文件中定义的日期
def getDateStr(filePath: str) -> str:
    with open(filePath, 'r', encoding='utf-8') as file:
        content = file.read()
    try:
        return re.search(r'(date:)\s+(.*-.*-.*)', content).group(2)
    except:
        logging.error(filePath + " has not date text")
        sys.exit(-1)


# 检测是否在排除列表中
def ignored(name: str) -> bool:
    for i in ignoreList:
        if re.match(i, name) is not None:
            return True

    return False


# 初始化logger
def initLogger():
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format='[%(levelname)s]: %(message)s')


def main():
    for i in fileList:
        if not ignored(i):
            oldname = path + os.sep + i
            timeStr = getDateStr(oldname)
            newname = path + os.sep + timeStr + '-' + i
            match = re.match(r'(.*-.*-.*)-(.*.md)', i)
            if match is not None:
                titleTime, name = match.groups()
                if not timeStr.__eq__(titleTime):
                    newname = path + os.sep + timeStr + '-' + name
                else:
                    newname = oldname
            os.rename(oldname, newname)
    logging.info('rename success')


if __name__ == '__main__':
    initLogger()
    main()
