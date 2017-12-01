import requests
import json
import time
import os
from tqdm import tqdm

from crawl_reddit import crawl_reddit
from gen_seq import gen_sequences


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


def crawl_comments_sub(start_urls, hdr, sub):
    """
    Crawl the comments of subreddit into JSON files with appending
    :param start_urls: lists of URLs of posts
    :param hdr: request header
    :param sub: name of subreddit
    :return: none, write JSON file
    """
    print("===================================")
    print('Crawling comments of {} ...'.format(sub))
    path_com = '../api_coms/sub_{}.json'.format(sub)
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
        'User-Agent': 'your_agent' +
                      '(by /u/your_user_name)'} # please change this to your own info

    path_project = "your_path_here"

    subreddits = ['depression', 'StopSelfHarm', 'MMFB', 'offmychest','addiction',
                  'BipolarReddit', 'ADHD', 'Anxiety', 'CPTSD', 'socialanxiety',
                  'HealthAnxiety', 'Agoraphobia', 'OCD', 'PanicParty', 'bipolar',
                  'disability', 'mentalhealth', 'Anger', 'TwoXADHD','alcoholism',
                  'BipolarSOs', 'BPD', 'dpdr', 'EatingDisorders', 'MaladaptiveDreaming',
                  'psychoticreddit', 'schizophrenia', 'traumatoolbox', 'getting_over_it', 'hardshipmates',
                  'emetophobia', 'GFD', 'mentalillness', 'NonZeroDay', 'fuckeatingdisorders', 'SuicideWatch'
                  ]
    # MMFB: Make Me Feel Better
    # ADHD: "Attention Deficit Hyperactivity Disorder" is a developmental disorder found in both children and adults.
    # CPTSD: Complex Post Traumatic Stress Disorder
    # Obsessive-Compulsive Disorder (OCD) is a disorder characterized by two components: obsessions and compulsions.
    # Gamers Fighting Depression's mission is to provide a safe and supportive environment for those who suffer from mental ill health.

    crawl_reddit(list_subreddit=subreddits, hdr=header)

    stat_info = []
    for sub in subreddits:
        p = '../api_json/'
        urls = read_urls_sub(path_json=p, subreddit=sub)
        crawl_comments_sub(start_urls=urls, hdr=header, sub=sub)
        stat_subreddit = gen_sequences(path_project, sub)
        stat_info.append(stat_subreddit)

    from pprint import pprint
    pprint(stat_info)
