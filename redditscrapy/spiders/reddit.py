# -*- coding: utf-8 -*-
import time
import scrapy
import json
from scrapy.selector import Selector


class RedditSpider(scrapy.Spider):
    name = "reddit"
    allowed_domains = ["reddit.com"]
    start_urls = ['http://reddit.com/r/movies']

    def __init__(self):
        self.count = 0

    def parse(self, response):
        for posts in response.css('div.top-matter'):
            title_href_relative = posts.css('p.title a::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(title_href_relative), callback=self.parse_posts)
            #
            # yield {
            #     'title': posts.css('a.title::text').extract_first(),
            #     'title_href': 'https://www.reddit.com' + posts.css('p.title a::attr(href)').extract_first(),
            #     'timestamp': posts.css('p.tagline time::attr(title)').extract_first(),
            #     'datetime': posts.css('p.tagline time::attr(datetime)').extract_first(),
            #     'author': posts.css('a.author::text').extract_first(),
            #     'author_href_absolute': posts.css('p.tagline a::attr(href)').extract_first()
            # }

            # num_comments = posts.css('li.first a::text').extract_first()[0]
            # num_upvotes = posts.css()
                
        next_button = response.css('span.next-button a::attr(href)').extract_first()

        self.count = self.count + 25
        print('=========================')
        print(self.count)
        print('=========================')
        if next_button is not None:
            time.sleep(2)
            yield scrapy.Request(next_button, callback=self.parse)
        # self.log("Saved file %s" % filename)

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


    def parse_posts_comments(self, response):
        #TODO parse comments
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


        file_path = './data_coms/'
        id = hash(title)
        timestamp, datetime, username, upvote, comment = [], [], [], [], []
        for ind, comments in enumerate(response.css('div.entry')[1:]):
            timestamp.append(comments.css('p.tagline time::attr(title)').extract_first())
            datetime.append(comments.css('p.tagline time::attr(datetime)').extract_first())
            user = comments.css('p.tagline a::text').extract()
            if len(user) >= 2:
                username.append(user[1])
            else:
                username.append('deleted')
            vote = comments.css('p.tagline span::attr(title)').extract()
            if len(vote) >= 3:
                upvote.append(vote[2])
            else:
                upvote.append(0)
            if len(text_post) >= 3:
                comment.append(text_post[ind+2].css('div.md p::text').extract())
            else:
                comment.append("no comments")
        com = {
            'id': id,
            'title': title,
            'timestamp': timestamp,
            'datetime': datetime,
            'username': username,
            'upvote': upvote,
            'comment': comment
        }
        with open(file_path + '{}.json'.format(id), 'w') as f:
            json.dump(com, f)


    def parse_author(self, response):
        #TODO parse user profile
        pass