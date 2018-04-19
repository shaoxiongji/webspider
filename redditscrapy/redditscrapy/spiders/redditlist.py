#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import time
import scrapy
import pandas as pd


class RedditList(scrapy.Spider):
    name = "redditlist"
    allowed_domains = ["redditlist.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count = 0
        self.list_sub = []

    def start_requests(self):
        url = 'http://redditlist.com/sfw'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for sub in response.css('div.listing-item'):
            sub_url = sub.css('span.subreddit-url a::attr(href)').extract_first()
            self.count += 1
            if sub_url not in self.list_sub:
                self.list_sub.append(sub_url)
        next_button = response.css('li.next-button a::attr(href)').extract_first()
        print(self.count, 'records crawled.')
        if next_button is not None:
            time.sleep(2)
            yield scrapy.Request(next_button, callback=self.parse)
        df = pd.DataFrame({'subreddit': self.list_sub}, index=None)
        df.to_csv('../data/reddit_list/subreddits_list.csv', columns=['subreddit'], index=False)