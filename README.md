# Web Spider and Exploratory Data Anaylsis

Some web spiders including: Reddit and experience project.

There are two versions of Reddit spiders using Scrapy and Reddit API.

To run these spiders, some folders need to be created and the path name should be modified.

## 1. Web Spider
### 1.1 Reddit API
There are three scripts in the folder of redditapi.

[(1)](redditapi/crawl_reddit.py) crawl the posts (including titles and text bodies) of subreddit.

[(2)](redditapi/comments.py) crawl the posts and comments.

[(3)](redditapi/gen_seq.py) get the sequences of comments.

### 1.2 Reddit Scrapy
Scrapy is used to crawl the posts in this [script](redditscrapy/spiders/reddit.py) and comments in this [script](redditscrapy/spiders/comments.py).
XPATH and CSS are used to match specific information.
Run the code:
> python scrapy_reddit.py

### 1.3 Experience Project
Scrapy is used to crawl the posts from [Experience Project](http://www.experienceproject.com).
XPATH and CSS are used to match specific information.
Run the code: 
> python scrapy_ep.py


## 2. Exploratory Data Analysis
### 2.1 Text Analysis
- word cloud

positive and negative words

### 2.2 Statics 
age over 18 distribution
 
### 2.3 User activity
#### user activity by month
submissions per month

comments per month

users joined per month

#### user activity by week
across different days of the week

submissions, comments, average users joined

#### user activity by day
submissions, comments, average users joined


### 2.4 Most Active/Popular Users
top submissions, comments, score(submission, comments),

average time to response
number of response within a specified time


## Requirements
python 3.6

scrapy 1.3.3

requests 2.18.4

