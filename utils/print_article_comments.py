import re
import textwrap
import logging
from bs4 import BeautifulSoup as BS


def print_with_indent(text, indent):
    """
    Manipulate comment text to keep indentation
    :param text: text input
    :param indent: (int) to indent
    :return:
    """
    # replace white space using regular expression
    text=re.sub('\s+', ' ', text)
    # match at beging of the string
    text=re.sub('^\s+', '', text)
    # match at the end of the string immediately before the newline
    text=re.sub('\s+$', '', text)
    # wrapping text with fixed size
    text=textwrap.wrap(text, width=150,
                       initial_indent='  '*indent,
                       subsequent_indent='  '*indent)
    s=""
    for i in text :
        # adding break line to our new line
        s=s+i+"\n"
    s=re.sub('\s+$','',s)
    return s


def print_comment(comment, indent=0):
    """
     Recursively print nested comments keeping correct indentation
    :param comment: comment dict
    :param item: comment to print
    :param indent (int): comment indentation default is 0
    :return:
    """
    try:
        if not comment:
            return
        if 'text' in comment:
            # parsing text from html format
            parsed_text = BS(comment['text'], "html.parser").get_text()

            if indent >= 1:
                print('  ' * indent + 'Posted by: ' + comment['by'])
                print(print_with_indent(parsed_text, indent))
                print()
            else:
                print('Posted by: ' + comment['by'])
                print(parsed_text)
                print()
        # printing children comments
        if "kids" in comment:
            for comment_id in comment["kids"]:
                print_comment(comment[comment_id], indent + 1)
        return None
    except Exception as err:
        logging.error(err)
