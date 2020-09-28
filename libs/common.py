

# base Hackers news api url
HACKER_NEWS_API_BASE_URL = 'https://hacker-news.firebaseio.com/v0/'
# suffix path for fetching top articles with limit from the first item
TOP_ARTICLES_WITH_LIMIT_PATH = 'topstories.json?orderBy=%22$key%22'

HACKER_NEWS_API_ITEM_URL = HACKER_NEWS_API_BASE_URL + "item/%s.json"


MIN_ARTICLE_RANK = 1
"""
According to API documintation at https://github.com/HackerNews/API, we will
Get up to 500 articles
"""
MAXIMUM_ARTICLE_RANK = 500

def build_items_url(items):
    return [HACKER_NEWS_API_ITEM_URL % url for url in items]