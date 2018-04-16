#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import sqlite3
import time
import scrapy
from sqlite_op import db_insert_userposts

def load_db_users(path_db):
    with sqlite3.connect(path_db) as conn:
        print('Open database sucessfully.')
        c = conn.cursor()
        c.execute('SELECT AUTHOR FROM POSTS')
        users = c.fetchall()
        users = [row[0] for row in users]
    return users


class RedditUsers(scrapy.Spider):
    name = "users"
    allowed_domains = ["reddit.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count = 0
        self.uname = ''
        self.home = 'https://www.reddit.com'

    def start_requests(self):
        users = load_db_users('../data/reddit_db/reddit.sqlite3')
        # urls = ['https://www.reddit.com/user/{}/posts/'.format(uname) for uname in users]
        for uname in users:
            self.uname = uname
            url = 'https://www.reddit.com/user/{}/posts/'.format(uname)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.count = 0
        for post in response.css('div.PostList__post'):
            subreddit = post.css('span.Post__source a::text').extract_first()
            title = post.css('div.Post__header a::text').extract_first()
            url = self.home + post.css('div.Post__header a::attr(href)').extract_first()
            datetime = post.css('div.Post__tagline time::attr(datetime)').extract_first()
            str_comments = post.css('div.Post__flatList a::text').extract_first()
            if str_comments == 'comment':
                ncomments = 0
            elif str_comments == '1 comment':
                ncomments = 1
            else:
                ncomments = str_comments[:-9]
            nscores = post.css('div.Post__score::text').extract_first()

            dict_post = {'author': self.uname, 'subreddit': subreddit, 'url': url, 'title': title,
                         'datetime': datetime, 'ncomments': ncomments, 'nscores': nscores}

            db_insert_userposts(dict_post)

            self.count += 1
        next_button = response.css('div.ListingPagination a::attr(href)').extract_first()

        if next_button is not None:
            next_button = self.home + next_button
            time.sleep(2)
            yield scrapy.Request(next_button, callback=self.parse)

        print(self.uname, '\t', self.count, 'records crawled.')
