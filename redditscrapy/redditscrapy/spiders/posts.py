#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import time
import scrapy
import pandas as pd
from sqlite_op import db_insert_post


class RedditPosts(scrapy.Spider):
    name = "posts"
    allowed_domains = ["reddit.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count = 0
        self.home = 'https://www.reddit.com'

    def start_requests(self):
        subs = pd.read_csv('../data/reddit_list/subreddits_top.csv')['subreddit'].as_matrix()
        for sub in subs:
            url = 'https://www.reddit.com/r/{}/'.format(sub)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for post, count in zip(response.css('div.entry'), response.css('div.midcol')):
            subreddit = post.css('span.domain a::text').extract_first()
            title = post.css('p.title a::text').extract_first()
            url = self.home + post.css('p.title a::attr(href)').extract_first()
            datetime = post.css('p.tagline time::attr(datetime)').extract_first()
            author = post.css('p.tagline a::text').extract_first()
            user_attr = post.css('span.userattrs a::attr(class)').extract_first()
            if user_attr is None:
                mod = 0
            else:
                mod = 1
            author_url = post.css('p.tagline a::attr(href)').extract_first()
            str_comments = post.css('li.first a::text').extract_first()
            if len(str_comments) > 9:
                ncomments = str_comments[:-9]
            else:
                ncomments = 0
            nscores = count.css('div.score.unvoted::text').extract_first()
            if nscores == '•':
                nscores = 0
            dict_post = {'subreddit': subreddit, 'title': title, 'url': url, 'datetime': datetime,
                         'author': author, 'ncomments': ncomments, 'nscores': nscores, 'mod': mod}
            db_insert_post(dict_data=dict_post)
            self.count += 1
        next_button = response.css('span.next-button a::attr(href)').extract_first()
        print(self.count, 'records crawled.')
        if next_button is not None:
            time.sleep(2)
            yield scrapy.Request(next_button, callback=self.parse)