from aiohttp import ClientSession
from .common import HACKER_NEWS_API_ITEM_URL
from alive_progress import alive_bar


async def fetch_comments(article):
    """
     Open session for fetching multiple comments in
     Asynchronous way.
    :param article: article to fetch comments from him
    :return: dict of comments.
    """
    async with ClientSession() as session:
        # init progress bar
        with alive_bar(article['descendants'], "Collecting comments") as bar:
            data = (await fetch_comment(session, article['id'], bar))
            return data


async def fetch_comment(session, item, progress_bar):
    """
    Recursively fetching comments excluding (deleted & dead) in asynchronous
    approach, the logic is keeping the original "kids" entry due to that
    they already sorted according to HN API's docs,
    than adding for each comment a new entry for each child
    as follows:
    comment = {
        "kids": [1, 2, 3, ...] (comments_id's),
        ...rest
    }

    will transform to:
    comment = {
    1: {child comment data},
    2: {child comment data},
    3: {child comment data},
    "kids": [1, 2, 3, ...] (comments_id's),
    ...rest
    }
    :param session: client session
    :param item: item id
    :param progress_bar:progress_bar callback for updating console
    :return:
    """
    url = HACKER_NEWS_API_ITEM_URL % item
    async with session.get(url) as response:
        data = await response.json()
        is_dead = data.get('dead', None)
        is_deleted = data.get('deleted', None)

        # ignoring dead or deleted comments
        if is_dead or is_deleted:
            return None

        # increasing progress bar only on comment fetch
        if data['type'] == 'comment':
            progress_bar()

        # Recursively fetch and insert all nested comments
        if "kids" in data:
            for rank, comment_id in enumerate(data["kids"]):
                data[comment_id] = await fetch_comment(session,
                                                       comment_id,
                                                        progress_bar)

        return data
