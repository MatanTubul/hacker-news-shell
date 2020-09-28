import logging
import requests
from utils.validators import validate_input_number
from libs.common import HACKER_NEWS_API_BASE_URL, \
    HACKER_NEWS_API_ITEM_URL
from alive_progress import alive_bar
from .print_article_comments import print_comment


class ArticleRankException(Exception):
    pass

class ArticleNotFound(Exception):
    pass

def fetch_article_by_rank():
    """
        Fetching article by given rank from user input
        and printing all article comments, rank should be limit
        according to HN api's docs there is a limit of
        Up to 500 top articles returning from the api.
    """
    try :

        rank = input("Enter a rank number between 1 - 500: ")
        # input return string so converting to int
        rank = int(rank)

        if not validate_input_number(1, rank, 500):
            raise ArticleRankException("Rank out of range")
        # query top articles by filtering data using startAt and endAt filters
        # range of articles will be by the rank which the user provided
        query = "topstories.json?orderBy=%22$key%22&startAt=%22{0}%22&endAt=%22{1}%22".format(str(rank), str(rank))
        url_to_fetch = ''.join([HACKER_NEWS_API_BASE_URL,
                                query])

        # fetching top stories limit by rank value
        article = {}
        with alive_bar(None,"Fetching article") as bar:
            response = requests.get(url_to_fetch)
            bar()
            # decoding data to json format
            articles_id = response.json()
            if not str(rank) in articles_id:
                raise ArticleNotFound("Not found article with rank %s" % rank)

            # extract last article in list which gives us the article for the provided rank.
            article = requests.get(HACKER_NEWS_API_ITEM_URL
                                   % (articles_id[str(rank)])).json()
            bar()
        if 'kids' in article:
            logging.info("Fetching and printing comments, please wait...")

            for comment_id in article['kids']:
                print()
                print_comment(comment_id)
        else:
            logging.info("No comments found for article with rank %d", rank)

    except ValueError:
        logging.error('Invalid input')
    except Exception as err:
        logging.error(err)
