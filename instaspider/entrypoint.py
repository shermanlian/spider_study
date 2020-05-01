#!/usr/bin/env python
# -*- coding:utf-8 -*-
#代替cmd执行爬虫
from scrapy.cmdline import execute
#爬虫运行命令：scrapy crawl instasipder[爬虫名字]
# execute("scrapy crawl instasipder -s LOG_FILE=log/log1.txt".split())
execute("scrapy crawl instasipderj".split())