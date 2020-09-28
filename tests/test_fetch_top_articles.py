import unittest
import sys
from argparse import ArgumentParser, ArgumentError
from utils.fetch_top_articles import print_top_articles, \
    fetch_top_articles, TypeMismatchError


class TestingFetchTopArticles(unittest.TestCase):

    def test_throw_exception_on_num_out_of_range(self):
        parser = ArgumentParser()
        parser.add_argument("--num", type=int, default=900)
        # ignoring test module name
        args = parser.parse_args(sys.argv[2:])
        self.assertRaises(ArgumentError, print_top_articles(args))

    def test_throw_exception_on_wrong_num_type(self):
        self.assertRaises(TypeMismatchError, fetch_top_articles(40))

    def test_expected_correct_size_fetched_articles(self):
        expected_top_articles = "20"
        top_articles = fetch_top_articles(expected_top_articles)
        self.assertEqual(len(top_articles),int(expected_top_articles))
