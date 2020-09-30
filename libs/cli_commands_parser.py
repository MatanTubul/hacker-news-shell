import argparse
import sys
import logging
from utils.fetch_top_articles import print_top_articles
from utils.fetch_article_by_rank import fetch_article_by_rank


class CommandsCli(object):
    """
    Get user input args, if validated executed the correct attribute function
    Cli has position arg, first <command> arg should be one of the functions
    declared below.
    """

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='shellHN interactive cli for Hacker News API',
            usage='''<command> [<args>]
            top  <--num>     list top Hacker news articles title and rank       
            comments         list specific article comments by given rank
            ''')
        # make sure command is provided and avoiding printing error message
        if len(sys.argv) < 2:
            parser.print_help()
            exit(1)

        parser.add_argument('command',
                            help='Subcommand to run from list above',
                            choices=['top', 'comments'])
        # command validation, excluding only command name
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def top(self):
        """
        Handling top command including optional num number
        On success executing command
        :return:
        """
        parser = argparse.ArgumentParser(
            description='Num of articles to fetch, default 40')
        # prefixing the argument with -- means it's optional
        parser.add_argument('--num', type=int, default=40)
        # ignore first arg which is our command to execute
        args = parser.parse_args(sys.argv[2:])
        print_top_articles(args)

    def comments(self):
        """
        Handling comments commands, no extra paramters need at
        This level.
        :return:
        """
        try:
            fetch_article_by_rank()
        except Exception as err:
            logging.error("%s", err)
