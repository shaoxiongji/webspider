#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/09/17 1:50 PM
# @Author  : Shaoxiong Ji
# @Software: PyCharm
# @Version : 3.6.0

import json
import os
import pprint
import datetime
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


class RedditData(object):
    # def __init__(self):
    #     # self.path = source_path

    def clean_text(self, text):
        text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
        text = re.sub(r"what's", "what is ", text)
        # text = re.sub(r"\'s", " ", text)
        # text = re.sub(r"\'ve", " have ", text)
        text = re.sub(r"can't", "cannot ", text)
        text = re.sub(r"n't", " not ", text)
        # text = re.sub(r"i'm", "i am ", text)
        text = re.sub(r"\'re", " are ", text)
        text = re.sub(r"\'d", " would ", text)
        text = re.sub(r"\'ll", " will ", text)
        text = re.sub(r",", " ", text)
        text = re.sub(r"\.", " ", text)
        text = re.sub(r"!", " ! ", text)
        text = re.sub(r"\/", " ", text)
        text = re.sub(r"\^", " ^ ", text)
        text = re.sub(r"\+", " + ", text)
        text = re.sub(r"\-", " - ", text)
        text = re.sub(r"\=", " = ", text)
        text = re.sub(r"'", " ", text)
        text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
        text = re.sub(r":", " : ", text)
        text = re.sub(r" e g ", " eg ", text)
        text = re.sub(r" b g ", " bg ", text)
        text = re.sub(r" u s ", " american ", text)
        text = re.sub(r"\0s", "0", text)
        text = re.sub(r" 9 11 ", "911", text)
        text = re.sub(r"e - mail", "email", text)
        text = re.sub(r"j k", "jk", text)
        text = re.sub(r"\s{2,}", " ", text)
        return text

    def json2excel(self, file_path, files_list):
        # convert json file to csv
        for file_name in files_list:
            with open(file_path + file_name, 'r') as f:
                reddit_items = json.load(f)
            titles = reddit_items["title"]
            usertexts = reddit_items["usertext"]
            y = reddit_items["y"]
            data = {'title': titles,'usertext': usertexts, 'y': y}
            reddit = pd.DataFrame(data, columns=['title', 'usertext', 'y'])
            reddit.to_excel(file_path+'{}.xlsx'.format(file_name[:-5]), index=False)

    def gen_suicide(self, path_st):
        files_pos = os.listdir(path_st)
        files_json = []
        for file in files_pos:
            if file[-5:] == '.json':
                files_json.append(file)
        print('positive files')
        pprint.pprint(files_json)
        titles, usertexts, y, href =[], [], [], []
        for file_name in files_json:
            with open(path_st + file_name, 'rb') as f:
                reddit_items = json.load(f)
            reddit_items.pop(0)  # this one may be official guide or official post
            for items in reddit_items:
                if items['title_href'] not in href:
                    href.append(items['title_href'])
                    titles.append(items['title'])
                    temp = ' '
                    for t in items['texts']:
                        temp += t
                    usertexts.append(temp)
                    y.append(1)
        data = {'id': href, 'title': titles, 'usertext': usertexts, 'y': y }
        print("length of suicide: ", len(y))
        df_reddit = pd.DataFrame(data, columns=['id', 'title', 'usertext', 'y'], index=None)
        df_reddit.to_excel('./data_st/reddit_SW_{}.xlsx'.format(len(y)), index=False)
        # with open('./data_st/reddit_SW_{}.json'.format(len(y)), 'w') as fj:
        #     json.dump(data, fj)
        return df_reddit

    def gen_nonsuicide(self, subreddit):
        files = []
        path = './crawl_neg/'
        all_neg = os.listdir(path)
        for neg in all_neg:
            if subreddit == neg[7:-14]:
                files.append(neg)
        titles, usertexts, y, href = [], [], [], []
        for file_name in files:
            if subreddit == file_name[7:-14]:
                with open(path + file_name, 'rb') as f:
                    print(path+file_name)
                    reddit_items = json.load(f)
            reddit_items.pop(0) # this one may be official guide or official post
            for items in reddit_items:
                if items['title_href'] not in href:
                    href.append(items['title_href'])
                    titles.append(items['title'])
                    temp = ' '
                    for t in items['texts']:
                        temp += t
                    usertexts.append(temp)
                    y.append(0)
        data = {'id': href, 'title': titles, 'usertext': usertexts, 'y':y}
        print("length of {}: ".format(subreddit), len(y))
        reddit = pd.DataFrame(data, columns=['id', 'title', 'usertext', 'y'], index=None)
        reddit.to_excel('./data_nonst/reddit_{}_{}.xlsx'.format(subreddit, len(href)), index=False)
        # with open('./data_nonst/reddit_{}.json'.format(subreddit),'w') as fj:
            # json.dump(data, fj)
        return reddit

    def gen_href(self, data_path):
        files = os.listdir(data_path)
        posts_href = []
        count = 0
        for file_name in files:
            with open(data_path + file_name, 'rb') as f:
                sw = json.load(f)
            sw.pop(0)
            for content in sw:
                href = content['title_href']
                count += 1
                if href not in posts_href:
                    posts_href.append(href)
        print("number of duplicated posts: ", count - len(posts_href))
        print("number of SuicideWatch posts: ", len(posts_href))
        with open('posts_href_{}.json'.format(len(posts_href)), 'w') as wf:
            json.dump(posts_href, wf)

    def gen_balanced(self, df_pos, df_neg, subreddit):
        len_pos = len(df_pos['id'])
        len_neg = len(df_neg['id'])

        if len_neg <= len_pos:
            # sampling from suicide texts
            sample = df_pos.sample(len_neg)
            df = pd.concat([df_neg, sample])
            df = df.sample(frac=1)
        else:
            # sampling from non-suicide texts
            sample = df_neg.sample(len_pos)
            df = pd.concat([df_pos, sample])
            df = df.sample(frac=1)
        print('length of balanced data:', len(df['id']))
        print("Num of nonsuicidal:", len(df['y'])-sum(df['y']))
        print('Num of suicidal texts', sum(df['y']))
        df.to_excel('./data_balanced/{}.xlsx'.format(subreddit), sheet_name='default', index=False)

    def gen_imbalanced(self, file_path='./crawl_neg/'):
        files = os.listdir(file_path)
        id, titles, usertexts, y = [], [], [], []
        for file_name in files:
            print(file_name)
            with open(file_path+file_name, 'rb') as f:
                item_list = json.load(f)
                for items in item_list:
                    if items['title_href'] not in id:
                        titles.append(items['title'])
                        id.append(items['title_href'])
                        temp = ' '
                        for t in items['texts']:
                            temp += t
                        usertexts.append(temp)
                        y.append(0)
        files = os.listdir('./crawl_SuicideWatch/')
        for file_name in files:
            with open('./crawl_SuicideWatch/'+file_name, 'rb') as f:
                item_list = json.load(f)
                item_list.pop(0)
                for items in item_list:
                    if items['title_href'] not in id:
                        titles.append(items['title'])
                        id.append(items['title_href'])
                        usertexts.append(items['texts'])
                        y.append(1)
        data = {'id': id, 'title': titles, 'usertext': usertexts, 'y': y}
        reddit = pd.DataFrame(data, columns=['id', 'title', 'usertext', 'y'], index=None)
        reddit = reddit.sample(frac=1)
        reddit.to_excel('./data_imbalanced/reddit.xlsx', index=False)
        print('Length of imbalanced data: ', len(reddit['y']))
        print('Length of suicide data: ', sum(reddit['y']))
        print('Ratio of imbalanced data: ', sum(reddit['y'])/len(reddit['y']))


if __name__ == '__main__':
    reddit_data = RedditData()

    # collect all the hrefs of posts
    reddit_data.gen_href('./crawl_SuicideWatch/')
    print('\n')

    # collect all the suicidal posts
    df_suicide = reddit_data.gen_suicide('./crawl_SuicideWatch/')

    # collect all the non-suicidal posts
    for sub in ['Jokes', 'books', 'gaming', 'AskReddit', 'movies']:
        print("========={}=============".format(sub))
        df_nonsuicide = reddit_data.gen_nonsuicide(sub)

        # generate balanced dataset
        reddit_data.gen_balanced(df_suicide, df_nonsuicide, sub)

    # generate imbalanced dataset
    print("=========Imbalanced=============")
    reddit_data.gen_imbalanced('./crawl_neg/')

