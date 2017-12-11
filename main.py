#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Version : 3.6.0
# @scrapy  : 1.3.3

from scrapy import cmdline
import datetime
from RedditData import *

date = datetime.date.today().strftime("%Y%m%d")

cmdline.execute("scrapy crawl reddit -o ./crawl_neg/reddit_books_{}.json".format(date).split())

# cmdline.execute("scrapy crawl comments -o ./crawl_sw_coms/SW_{}.json".format(date).split())

# cmdline.execute("scrapy crawl experience -o ./crawl_ep/ep_{}.json".format(date).split())
