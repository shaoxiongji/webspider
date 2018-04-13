# Web Spider

Some web spiders including: Reddit and experience project.

There are two versions of Reddit spiders using Scrapy and Reddit API.

To run these spiders, some folders need to be created and the path name should be modified.

## Reddit API
There are three scripts in the folder of redditapi.

[(1)](redditapi/crawl_posts.py) crawl the posts (including titles and text bodies) of subreddit.

[(2)](redditapi/comments.py) crawl the posts and comments.

[(3)](redditapi/gen_seq.py) get the sequences of comments.

## Reddit Scrapy
Scrapy is used to crawl the posts in this [script](redditscrapy/redditscrapy/spiders/reddit.py) and comments in this [script](redditscrapy/redditscrapy/spiders/comments.py).
XPATH and CSS are used to match specific information.
Run the code:
> python scrapy_reddit.py

## Experience Project
Scrapy is used to crawl the posts from [Experience Project](http://www.experienceproject.com).
XPATH and CSS are used to match specific information, implemented in this [script](scrapy_ep/scrapy_ep/spiders/experience.py).
Run the code: 
> python scrapy_ep.py

## Requirements
python 3.6

scrapy 1.3.3

requests 2.18.4
