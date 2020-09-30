import asyncio
from aiohttp import ClientSession
from alive_progress import alive_bar


async def fetch_all(urls):
    """
    Given a list of urls, scheduling tasks using event loop and
    run them asynchronously.
    :param urls: [] of urls
    :return: [] list of dict not sorted
    """
    tasks = []
    async with ClientSession() as session :
        with alive_bar(len(urls)) as bar :
            for index, url in enumerate(urls, start=1) :
                task = asyncio.ensure_future(fetch(url, session, index,
                                                   bar))
                tasks.append(task)  # create list of tasks
            responses = await asyncio.gather(*tasks)  # gather task responses
            return responses


async def fetch(url, session, rank, progress_bar):
    """
    :param url: item to fetch from Hacker news api
    :param session: client session
    :param rank: article rank derived from fetching topstories
    :param progress_bar: progress_bar callback for updating console
    :return:
    """
    """Fetch a url, using specified ClientSession."""
    async with session.get(url) as response:
        # done fetching item updating progress bar
        progress_bar()
        resp = await response.json()
        return {'title' :resp['title'], 'rank' :rank}
