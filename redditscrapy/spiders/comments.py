#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/10/17 4:15 PM
# @Author  : Shaoxiong Ji
# @Software: PyCharm
# @Version : 3.6.1

import time
import scrapy
import json


class RedditCommentsSpider(scrapy.Spider):
    name = "reddit-comments"
    allowed_domains = ["reddit.com"]

    def __init__(self):
        self.count = 0
        self.subreddit = 'SuicideWatch'

    def start_requests(self):
        with open("./posts_href.json",'r') as f:
            start_urls = json.load(f)
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_comments)

    def parse_comments(self, response):
        # TODO parse comments
        posts = response.css('div.entry')[0]
        title = posts.css('p.title a::text').extract_first()
        id = hash(title)

        title_href_relative = posts.css('p.title a::attr(href)').extract_first()
        timestamp = posts.css('p.tagline time::attr(title)').extract_first()
        datetime = posts.css('p.tagline time::attr(datetime)').extract_first()
        author = posts.css('p.tagline a::text').extract_first()
        author_href_absolute = posts.css('p.tagline a::attr(href)').extract_first()

        # n_comments = response.xpath('/html/body/div[4]/div[2]/div[1]/span/text()').extract_first()[4:-9]

        text_post = response.css('div.usertext-body')
        base = 1
        if posts.css('div.expando p::text').extract() == []:
            texts = [None]
        else:
            texts = text_post[base].css('div.md p::text').extract()
            base += 1

        comment = []
        for com_ in text_post[base:]:
            com_text = com_.css('div.md p::text').extract_first()
            if com_text != []:
                comment.append(com_text)
            else:
                comment.append(None)

        timestamp_com, datetime_com, commenter, upvote = [], [], [], []
        for ind, comments in enumerate(response.css('div.entry')[1:]):
            timestamp_com.append(comments.css('p.tagline time::attr(title)').extract_first())
            datetime_com.append(comments.css('p.tagline time::attr(datetime)').extract_first())
            user = comments.css('p.tagline a::text').extract()
            if len(user) >= 2:
                commenter.append(user[1])
            else:
                commenter.append('deleted')
            vote = comments.css('p.tagline span::attr(title)').extract()
            if len(vote) == 3:
                upvote.append(vote[2])
            else:
                upvote.append(0)

        com = {
            'com_timestamp': timestamp_com,
            'com_datetime': datetime_com,
            'com_username': commenter,
            'com_upvote': upvote,
            'com_text': comment
        }

        yield {
            'id': id,
            'text_title': title,
            'title_href': 'https://www.reddit.com' + title_href_relative,
            'timestamp': timestamp,
            'datetime': datetime,
            'author': author,
            'author_href': author_href_absolute,
            'text_body': texts,
            'dict_comments': com
        }

        if len(title) == 0:
            with open('log.txt', 'a') as fa:
                fa.write(response.url)
        self.count += 1
        print("============\n", self.count, "\n===========")
        time.sleep(2)