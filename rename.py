import os
import time
import re
import logging

"""
读取文件内‘YAML Front Matter’中的‘date’标签，获取日期
然后自动按‘year-month-day-xxx.md’重名命名文件
使用正则表达式排除已经已格式化的文件
"""

# 格式化目录
path = "./_posts"

# 获取目录的所有文件
fileList = os.listdir(path)

# 忽略特殊文件列表
ignoreList=[]

# 获取文件中定义的日期
def getDateStr(filePath: str) -> str:
    with open(filePath, 'r') as file:
        content = file.read()
    return re.search(r'(date: )(.*-.*-.*)', content).group(2)

# 初始化logger
def initlogger():
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format='[%(levelname)s]: %(message)s')

def main():
    initlogger()
    for i in fileList:
        if re.match(r'.*-.*-.*-.*.md', i) is None and not ignoreList.__contains__(i):
            # timeStr = time.strftime("%Y-%m-%d", time.localtime())
            oldname = path + os.sep + i
            timeStr = getDateStr(oldname)
            newname = path + os.sep + timeStr + '-' + i
            os.rename(oldname, newname)
    logging.info('rename success')


if __name__ == '__main__':
    main()




