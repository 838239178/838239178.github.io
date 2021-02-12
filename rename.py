import os
import time
import re
import logging

"""
自动按’year-month-day-xxx.md‘重名命名文件
使用正则表达式排除已经已格式化的文件
"""

# 格式化目录
path = "./_posts"

# 获取目录的所有文件
fileList = os.listdir(path)

# 忽略特殊文件列表
ignoreList=[]

for i in fileList:
    if re.match(r'.*-.*-.*-.*.md', i) is None and not ignoreList.__contains__(i):
        timeStr = time.strftime("%Y-%m-%d", time.localtime())
        oldname = path + os.sep + i
        newname = path + os.sep + timeStr + '-' + i
        os.rename(oldname, newname)

logging.getLogger().setLevel(logging.INFO)
logging.info(' rename success')

