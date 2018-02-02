#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import time
import scrapy
import json
from scrapy.selector import Selector


class RedditSpider(scrapy.Spider):
    name = "reddit"
    allowed_domains = ["reddit.com"]
    start_urls = ['http://reddit.com/r/popular']

    def __init__(self):
        self.count = 0

    def parse(self, response):
        for posts in response.css('div.top-matter'):
            title_href_relative = posts.css('p.title a::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(title_href_relative), callback=self.parse_posts)
                
        next_button = response.css('span.next-button a::attr(href)').extract_first()

        self.count = self.count + 25
        print('=========================')
        print(self.count)
        print('=========================')
        if next_button is not None:
            time.sleep(2)
            yield scrapy.Request(next_button, callback=self.parse)

    def parse_posts(self, response):
        posts = response.css('div.entry')[0]
        title = posts.css('p.title a::text').extract_first()
        title_href_relative = posts.css('p.title a::attr(href)').extract_first()
        timestamp = posts.css('p.tagline time::attr(title)').extract_first()
        datetime = posts.css('p.tagline time::attr(datetime)').extract_first()
        author = posts.css('p.tagline a::text').extract_first()
        author_href_absolute = posts.css('p.tagline a::attr(href)').extract_first()
        text_post = response.css('div.usertext-body')
        texts = text_post[1].css('div.md p::text').extract()

        yield {
            'title': title,
            'title_href': 'https://www.reddit.com' + title_href_relative,
            'timestamp': timestamp,
            'datetime': datetime,
            'author': author,
            'author_href_absolute': author_href_absolute,
            'texts': texts
        }