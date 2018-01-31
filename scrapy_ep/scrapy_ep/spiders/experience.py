# -*- coding: utf-8 -*-
import re
import os
import time
import scrapy
import csv
from scrapy.selector import Selector


class RedditSpider(scrapy.Spider):
    name = "experience"
    allowed_domains = ["experienceproject.com"]

    def __init__(self):
        self.count = 0
        self.page = 1

    def start_requests(self):
        start_urls = ['http://www.experienceproject.com/groups/Think-About-Suicide/12159',
                      'http://www.experienceproject.com/groups/Am-Suicidal/9674'
                      ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def clean_text(self, text):
        """
        Clean text data
        :param df: raw DataFrame
        :return: DataFrame cleaned
        """
        text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
        text = re.sub(r"what's", "what is ", text)
        text = re.sub(r"\'s", " ", text)
        text = re.sub(r"\'ve", " have ", text)
        text = re.sub(r"can't", "cannot ", text)
        text = re.sub(r"n't", " not ", text)
        text = re.sub(r"i'm", "i am ", text)
        text = re.sub(r"i've", "i have ", text)
        text = re.sub(r"\'re", " are ", text)
        text = re.sub(r"\'d", " would ", text)
        text = re.sub(r"\'ll", " will ", text)
        text = re.sub(r" e g ", " eg ", text)
        text = re.sub(r" b g ", " bg ", text)
        text = re.sub(r" u s ", " american ", text)
        text = re.sub(r"\0s", "0", text)
        text = re.sub(r"e - mail", "email", text)
        text = re.sub(r"\&gt", ' ', text)
        text = re.sub(r"\&amp", ' ', text)
        text = re.sub(r"\^M", ' ', text)
        text = re.sub("\s", ' ', text)
        text = re.sub(r"  ", ' ', text)
        text = re.sub(r"   ", '', text)
        text = re.sub(r"^[ ]{3:10}", '', text)
        return text

    def parse(self, response):
        for posts in response.css('div.expression-content'):
            title_href_relative = posts.css('h2.legacy-title a::attr(href)').extract_first()
            yield scrapy.Request('http://www.experienceproject.com' + title_href_relative, callback=self.parse_posts)

        self.page += 1
        next_button = response.xpath('//*[@id="group-stories"]/a').extract_first()
        next_button = Selector(text=next_button, type='html').css('a::attr(href)').extract_first()

        print('=========================')
        print(self.page)
        print('=========================')
        if next_button is not None:
            time.sleep(2)
            yield scrapy.Request(next_button, callback=self.parse)

    def parse_posts(self, response):
        id = re.search(r'(\d{4,9})', response._url).group()
        id_story = "expression-story-{}".format(id)
        id_like = "like-count-Story-{}".format(id)
        head = response.xpath('//*[@id=$val]/div/div[2]/h1/text()', val=id_story).extract_first()
        if head is None:
            body = response.xpath('//*[@id=$val]/div/div[2]/text()', val=id_story).extract_first()
        else:
            body_list = response.xpath('//*[@id=$val]/div/div[2]/text()', val=id_story).extract()
            body = head
            for b in body_list:
                body += ' '
                body += b
        age = response.xpath('//*[@id=$val]/div/div[3]/span[1]/span[2]/span[1]/text()', val=id_story).extract_first()
        gender = response.xpath('//*[@id=$val]/div/div[3]/span[1]/span[2]/span[2]/text()', val=id_story).extract_first()
        if gender != None:
            gender = gender[-1]
        else:
            gender = 'X'
        date = response.xpath('//*[@id=$val]/div/div[3]/span[2]/span[3]/span/text()', val=id_story).extract_first()
        if date != None:
            date = date[2:-2]
        like_count = response.xpath('//*[@id=$val]/span[1]/text()', val=id_like).extract_first()
        time.sleep(1)
        body = self.clean_text(body)
        data_dict = {
            'id': id,
            'date': date,
            'age': age,
            'gender': gender,
            'likes': like_count,
            'body': body,
        }
        # yield data_dict
        file_result = '/data/shji/myprojects/redditscrapy/data_ep/ep.csv'
        with open(file_result, 'a') as f:
            field_names = ['id', 'date', 'age', 'gender', 'likes', 'body']
            writer = csv.DictWriter(f, fieldnames=field_names)
            if not os.path.isfile(file_result):
                writer.writeheader()
            writer.writerow(data_dict)