#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/09/17 2:27 PM
# @Author  : Shaoxiong Ji
# @Software: PyCharm
# @Version : 3.6.0
# @scrapy  : 1.3.3

from datetime import date
from scrapy import cmdline

today = date.today().strftime("%Y%m%d")

subreddit = "popular"
cmdline.execute("scrapy crawl reddit -o ../crawl_neg/reddit_{}_{}.json".format(subreddit, today).split())


