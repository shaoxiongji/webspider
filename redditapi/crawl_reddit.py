#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time
import os
import datetime
from tqdm import tqdm


def crawl_json(list_subreddit, hdr):
    """
    Crawl each pages of a list of subreddit in specific day.
    :param list_subreddit: list of subreddits
    :param hdr: request header
    :return:
    """
    today = datetime.date.today().strftime("%Y%m%d")
    for sub in tqdm(list_subreddit):
        if not os.path.isfile('/data/shji/myprojects/redditscrapy/api_json/sub_{}_{}.json'.format(sub, today)):
            print("===================================")
            print('Crawling subreddit {}'.format(sub))
            url = 'https://www.reddit.com/r/{}/.json'.format(sub)
            req = requests.get(url, headers=hdr)
            json_data = json.loads(req.text)
            # posts = json.dumps(json_data['data']['children'], indent=4, sort_keys=True)
            # print(posts)
            # print(len(json_data['data']['children']))
            # print(type(json_data['data']['children']))
            data_all = []
            entries = json_data['data']['children']
            for entry in entries:
                if entry['data']['domain'] == 'self.{}'.format(sub):
                    data_all.append(entry)
            num_of_posts = 0
            while len(data_all) <= 10000:
                time.sleep(2)
                last = data_all[-1]['data']['name']
                url = 'https://www.reddit.com/r/{}/.json?after={}'.format(sub, last)
                req = requests.get(url, headers=hdr)
                data = json.loads(req.text)
                entries = data['data']['children']
                for entry in entries:
                    if entry['data']['domain'] == 'self.{}'.format(sub):
                        data_all.append(entry)
                if num_of_posts == len(data_all):
                    break
                else:
                    num_of_posts = len(data_all)
            with open('/data/shji/myprojects/redditscrapy/api_json/sub_{}_{}.json'.format(sub, today), 'w') as f:
                json.dump(data_all, f)
            print('Crawling posts ...')
            print('{} posts crawled. '.format(len(data_all)))


if __name__ == '__main__':
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5' +
                      '(by /u/sheldonhow)'}

    subreddits = ['SuicideWatch', 'depression', 'StopSelfHarm', 'MMFB', 'offmychest',
                      'BipolarReddit', 'ADHD', 'Anxiety', 'CPTSD', 'socialanxiety',
                      'HealthAnxiety', 'Agoraphobia', 'OCD', 'PanicParty', 'bipolar',
                      'disability', 'mentalhealth', 'Anger', 'anxietysupporters', 'TwoXADHD',
                      'emetophobia', 'GFD'
                      ]
    # MMFB: Make Me Feel Better
    # ADHD: "Attention Deficit Hyperactivity Disorder" is a developmental disorder found in both children and adults.
    # CPTSD: Complex Post Traumatic Stress Disorder
    # Obsessive-Compulsive Disorder (OCD) is a disorder characterized by two components: obsessions and compulsions.
    # Gamers Fighting Depression's mission is to provide a safe and supportive environment for those who suffer from mental ill health.
    crawl_json(subreddits, header)

