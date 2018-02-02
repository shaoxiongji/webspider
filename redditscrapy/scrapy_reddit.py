#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

from datetime import date
from scrapy import cmdline

today = date.today().strftime("%Y%m%d")

subreddit = "popular"
cmdline.execute("scrapy crawl reddit -o ../crawl_neg/reddit_{}_{}.json".format(subreddit, today).split())
