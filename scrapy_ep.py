#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/09/17 2:27 PM
# @Author  : Shaoxiong Ji
# @Software: PyCharm
# @Version : 3.6.0
# @scrapy  : 1.3.3

from scrapy import cmdline
import datetime
from RedditDataScrapy import *

date = datetime.date.today().strftime("%Y%m%d")

cmdline.execute("scrapy crawl experience".split())

