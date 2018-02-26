#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import requests
import json
import time
import os
import datetime
import sqlite3
from tqdm import tqdm
import pandas as pd
from pprint import pprint


def db_insert(data):
    """
    Inserting data into database
    :param data: a list of data dict
    :return: 0
    """
    conn = sqlite3.connect('../database/reddit_posts_api.sqlite')
    c = conn.cursor()
    print('Opened database successfully. ')
    for item in data:
        try:
            c.execute("insert into POSTS values (?, ?, ?, ?, ?, ?, ?)",
                      (item['subreddit'], item['url'], item['title'], item['selftext'],
                       item['created'], item['created_utc'], item['author']))
        except sqlite3.Error as e:
            print('Error:', e.args[0])
    conn.commit()
    print('Records created.')
    conn.close()
    return 0


def crawl_json(list_subreddit, hdr):
    """
    Crawl each pages of a list of subreddit in specific day.
    :param list_subreddit: list of subreddits
    :param hdr: request header
    :return:
    """
    for sub in tqdm(list_subreddit):
        print('Crawling subreddit {}'.format(sub))
        url = 'https://www.reddit.com/r/{}/.json'.format(sub)
        req = requests.get(url, headers=hdr)
        try:
            json_data = json.loads(req.text)
            data_all = []
            entries = json_data['data']['children']
            for entry in entries:
                if entry['data']['domain'] == 'self.{}'.format(entry['data']['subreddit']):
                    data_all.append(entry['data'])
                    pprint(entry['data']['url'])
        except json.JSONDecodeError as e:
            print('Error:', e)
        num_of_posts = 0
        while len(data_all) <= 10000:
            time.sleep(2)
            last = json_data['data']['children'][-1]['data']['name']
            url = 'https://www.reddit.com/r/{}/.json?after={}'.format(sub, last)
            req = requests.get(url, headers=hdr)
            try:
                data = json.loads(req.text)
                entries = data['data']['children']
                for entry in entries:
                    if entry['data']['domain'] == 'self.{}'.format(entry['data']['subreddit']):
                        data_all.append(entry['data'])
                        pprint(entry['data']['url'])
                if num_of_posts == len(data_all):
                    break
                else:
                    num_of_posts = len(data_all)
            except json.JSONDecodeError as e:
                print('Error:', e)
        if len(data_all) == 0:
            continue
        db_insert(data=data_all)
        # with open('../api_json/sub_{}_{}.json'.format(sub, today), 'w') as f:
        #     json.dump(data_all, f)
        #     print('json saved.')
        print('{} posts crawled. '.format(len(data_all)))


if __name__ == '__main__':
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5' +
                      '(by /u/sheldonhow)'}

    path_project = "../"

    # crawl icd subreddits
    df_icd = pd.read_csv(os.path.join(path_project, 'subreddits_icd.csv'))
    subreddits = df_icd['subreddit'].values
    crawl_json(subreddits, header)

    # crawl top subreddits
    df_top = pd.read_csv(os.path.join(path_project, 'subreddits_top.csv'))
    tops = df_top['subreddit'].values
    crawl_json(tops, header)
