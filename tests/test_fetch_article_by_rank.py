import unittest
from unittest import mock
from utils.fetch_article_by_rank import fetch_article_by_rank, \
    ArticleRankException, \
    ArticleNotFound


class TestingFetchCommentsByRankArticle(unittest.TestCase):
    def test_throw_exception_on_wrong_user_input(self):
        # mock builtin input function
        with mock.patch('builtins.input', return_value=650):
            self.assertRaises(ArticleRankException, fetch_article_by_rank())

    def test_throw_article_not_found_exception(self):
        # mock builtin input function
        with mock.patch('builtins.input', return_value=500) :
            self.assertRaises(ArticleNotFound, fetch_article_by_rank())