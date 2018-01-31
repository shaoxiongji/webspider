import requests
import json
import time
import os
from tqdm import tqdm
import pandas as pd
from crawl_reddit import crawl_json
from gen_seq import gen_sequences


def read_urls_sw():
    json_path = '/data/shji/myprojects/redditscrapy/posts_href_7085.json'
    with open(json_path, 'r') as f:
        start_urls = json.load(f)
    return start_urls


def crawl_comments_sw(start_urls, hdr, sub, base_path):
    # num = []
    data_all = []
    for u in tqdm(start_urls):
        url = u + '.json'
        req = requests.get(url, headers=hdr)
        json_data = json.loads(req.text)
        data_all.append(json_data)
        # num_comments = json_data[0]['data']['children'][0]['data']['num_comments']
        # num.append(num_comments)
        # print(num_comments)
        time.sleep(2)
    with open(os.path.join(base_path, 'api_coms/sub_{}.json'.format(sub)), 'w') as f:
        json.dump(data_all, f)
    print('{} of posts and comments crawled.'.format(len(data_all)))


def read_urls_sub(path_json, subreddit):
    """
    Collect URLs of crawled posts from JSON file without duplication
    :param path_json: the path of crawled JSON files
    :param subreddit: a list of subreddits
    :return: a list of URLs of crawled posts.
    """
    list_json = os.listdir(path_json)
    start_urls = []
    for json_name in list_json:
        if subreddit == json_name[4:-14]:
            with open(os.path.join(path_json, json_name), 'r') as f:
                data_all = json.load(f)
            for i in range(0, len(data_all)):
                if data_all[i]['data']['url'] not in start_urls:  # the URL is a unique ID
                    start_urls.append(data_all[i]['data']['url'])
    return start_urls


def crawl_comments_sub(start_urls, hdr, sub, base_path):
    """
    Crawl the comments of subreddit into JSON files with appending
    :param start_urls: lists of URLs of posts
    :param hdr: request header
    :param sub: name of subreddit
    :param base_path: path of the project
    :return: none, write JSON file
    """
    print("===================================")
    print('Crawling comments of {} ...'.format(sub))
    path_com = os.path.join(base_path, 'api_coms/sub_{}.json'.format(sub))
    if not os.path.isfile(path_com):
        data_all, urls_crawled = [], []
    else:
        with open(path_com, mode='r', encoding='utf-8') as fr:
            data_all = json.load(fr)
            urls_crawled = []  # load all urls crawled
            for data in data_all:
                url = data[0]['data']['children'][0]['data']['url']
                urls_crawled.append(url)
    for u in tqdm(start_urls):
        if u not in urls_crawled and 'https://www.reddit.com/r/' in u:
            url = u + '.json'
            req = requests.get(url, headers=hdr)
            json_data = json.loads(req.text)
            data_all.append(json_data)
            time.sleep(2)
    with open(path_com, mode='w', encoding='utf-8') as fw:
        json.dump(data_all, fw)
    print('{} of posts and comments crawled.'.format(len(data_all)))


if __name__ == '__main__':
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5' +
                      '(by /u/sheldonhow)'}

    path_project = "/data/shji/myprojects/redditscrapy/"

    df_sub = pd.read_csv(os.path.join(path_project, 'subreddits.csv'))
    subreddits = df_sub['subreddit'].values

    crawl_json(list_subreddit=subreddits, hdr=header)

    stat_info = []
    for sub in subreddits:
        p = os.path.join(path_project, 'api_json/')
        urls = read_urls_sub(path_json=p, subreddit=sub)
        crawl_comments_sub(start_urls=urls, hdr=header, sub=sub, base_path=path_project)
        stat_subreddit = gen_sequences(path_project, sub)
        stat_info.append(stat_subreddit)

    from pprint import pprint
    pprint(stat_info)
