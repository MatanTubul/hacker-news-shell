import logging
import argparse
import asyncio
import requests
from prettytable import PrettyTable
from alive_progress import alive_bar
from utils.validators import validate_input_number
from libs.async_fetch_articles import fetch_all
from libs.common import build_items_url, HACKER_NEWS_API_BASE_URL, \
    TOP_ARTICLES_WITH_LIMIT_PATH

class TypeMismatchError(Exception):
    pass

def print_top_articles(args):
    """
     Printing predefined top articles whit their rank
    :param args: contain num of articles to select
    :return:
    """
    try :
        num_articles_to_fetch  = args.num
        if not validate_input_number(10, num_articles_to_fetch, 500) :
            raise argparse.ArgumentError(None,
                                         "Articles number is out of range")
        # table to store all articles for pretty print
        articles_table = PrettyTable()
        # columns to show
        columns = ["rank", "title"]
        # init columns
        articles_table.field_names = columns

        for article in fetch_top_articles(str(num_articles_to_fetch)) :
            try:
                # store rank in article object for article_table use
                articles_table.add_row([article[k] for k in columns])
            except Exception as err :
                logging.error('Failed to print article id %s with error: %s',
                              article['id'], err)
        print(articles_table)
    except Exception as err :
        logging.error('Failed to fetch articles  with error: %s',
                      err)


def fetch_top_articles(num_articles) :
    """
    Fetching Hacker News API <num_articles> top articles with limit from first
    :param num_articles: number articles to fetch
    :return: generator
    """
    try:
        if not type(num_articles) == str:
            raise TypeMismatchError("number is not from str type")
        url_to_fetch = ''.join([HACKER_NEWS_API_BASE_URL,
                                TOP_ARTICLES_WITH_LIMIT_PATH,
                                "&limitToFirst=",
                                num_articles])


        logging.info("Fetching top %s Hacker News articles, please wait...",
                     num_articles)

        # fetching top stories
        with alive_bar(None, "Fetching top articles id's") as bar:
            bar()
            # Fetching articles id's
            response = requests.get(url_to_fetch)
            bar()
        # async fetching for all
        loop = asyncio.get_event_loop()  # event loop
        future = asyncio.ensure_future(
            fetch_all(build_items_url(response.json())))  # tasks to do
        articles = loop.run_until_complete(future)  # loop until done
        loop.close()
        articles = sorted(articles, key=lambda k :k['rank'])
        return articles

    except Exception as err:
        logging.error('Failed to fetch articles with error: %s', err)
