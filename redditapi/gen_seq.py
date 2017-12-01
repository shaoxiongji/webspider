#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import time
import os
import csv
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def gen_sequences(path_base, subreddit):
    """
    Generate posts and comments sequences of each subreddit
    :param path_base: the path of the project
    :param subreddit: the name of subreddit
    :return: None
    """

    def recursive_replies(comment_list):
        for c in comment_list:
            list_posts.append()
        return

    print("===================================")
    print('Generating sequences of {} ...'.format(subreddit))
    with open(os.path.join(path_base, 'api_coms/sub_{}.json'.format(subreddit)), 'r') as fr:
        list_data = json.load(fr)
    path_seq = '../api_seq/sub_{}.json'.format(subreddit)
    # if not os.path.isfile(path_seq):
    #     seq_all, seq_crawled = [], []
    # else:
    #     with open(path_seq, mode='r', encoding='utf-8') as fr:
    #         seq_all = json.load(fr)
    seq_all = []
    list_com_count = []
    for item in tqdm(list_data):
        # print(ix)
        if len(item) >= 2:
            list_posts = []
            post_0 = item[0]
            child_0 = post_0['data']['children'][0]['data']
            author = child_0['author']
            list_posts.append((child_0['created_utc'], child_0['author'], child_0['title']+child_0['selftext']))
            coms = item[1]
            for item_child in coms['data']['children']:
                if item_child['kind'] != 'more':
                    comment = item_child['data']
                    list_posts.append((comment['created_utc'], comment['author'], comment['body'], comment['ups']))
                    # print(comment.keys())
                    # print(comment['depth'])
                    if not comment['replies'] == '':
                        replies = comment['replies']['data']['children']
                        for re in replies:
                            comment_child = re['data']
                            if not 'body' in comment_child.keys():
                                continue
                            list_posts.append((comment_child['created_utc'], comment_child['author'],
                                               comment_child['body'], comment_child['ups']))
                            print((comment_child['created_utc'], comment_child['author'], comment_child['body'], comment_child['ups']))
                            if not comment_child['replies'] == '':
                                replies_child = comment_child['replies']['data']['children']
                                for re_child in replies_child:
                                    comment_grandchild = re_child['data']
                                    if not 'body' in comment_grandchild.keys():
                                        continue
                                    list_posts.append((comment_grandchild['created_utc'], comment_grandchild['author'],
                                                       comment_grandchild['body'], comment_grandchild['ups']))
                else:
                    with open(os.path.join(path_base, 'more_urls.txt'), 'a') as fw:
                        fw.write(child_0['url'])
            # post_length = len(list_posts)
            seq_data = {'subreddit': subreddit,
                        'author': author,
                        'list_posts': list_posts}
            seq_all.append(seq_data)
        list_com_count.append(len(list_posts))
    with open(os.path.join(path_base, 'api_seq/sub_{}.json'.format(subreddit)), 'w') as fw:
        json.dump(seq_all, fw)
    print('{} of sequences generated.'.format(len(seq_all)))

    data_dict = {'date': datetime.date.today().strftime("%Y%m%d"), 'subreddit': subreddit,
                 'com_num': len(list_com_count), 'com_mean': np.mean(list_com_count),
                 'com_median': np.median(list_com_count), 'com_max': max(list_com_count)}
    with open('../res_eda/stat.csv', 'a') as f:
        field_names = ['date', 'subreddit', 'com_num', 'com_mean', 'com_median', 'com_max']
        writer = csv.DictWriter(f, fieldnames=field_names)
        if not os.path.isfile('../res_eda/stat.csv'):
            writer.writeheader()
        writer.writerow(data_dict)
    return data_dict


if __name__ == '__main__':
    subreddits = ['depression', 'StopSelfHarm', 'MMFB', 'offmychest','addiction',
                  'BipolarReddit', 'ADHD', 'Anxiety', 'CPTSD', 'socialanxiety',
                  'HealthAnxiety', 'Agoraphobia', 'OCD', 'PanicParty', 'bipolar',
                  'disability', 'mentalhealth', 'Anger', 'TwoXADHD','alcoholism',
                  'BipolarSOs', 'BPD', 'dpdr', 'EatingDisorders', 'MaladaptiveDreaming',
                  'psychoticreddit', 'schizophrenia', 'traumatoolbox', 'getting_over_it', 'hardshipmates',
                  'emetophobia', 'GFD', 'mentalillness', 'SuicideWatch'
                  ]
    path_project = "your_path_here"
    # MMFB: Make Me Feel Better
    # ADHD: "Attention Deficit Hyperactivity Disorder" is a developmental disorder found in both children and adults.
    # CPTSD: Complex Post Traumatic Stress Disorder
    # Obsessive-Compulsive Disorder (OCD) is a disorder characterized by two components: obsessions and compulsions.
    # Gamers Fighting Depression's mission is to provide a safe and supportive environment for those who suffer from mental ill health.

    for sub in subreddits:
        p = '../api_coms/'
        gen_sequences(path_project, sub)
