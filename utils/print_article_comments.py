import requests
import re
import textwrap
import json
import logging
from libs.common import HACKER_NEWS_API_ITEM_URL


def print_with_indent(t, indent):
    # repalce white space using regular expression
    t=re.sub('\s+', ' ', t)
    # match at beging of the string
    t=re.sub('^\s+','',t)
    # match at the end of the string immediately before the newline
    t=re.sub('\s+$','',t)
    # wrapping text with fixed size
    t=textwrap.wrap(t,width=150,
                    initial_indent='  '*indent,
                    subsequent_indent='  '*indent)
    s=""
    for i in t :
        # adding break line to our new line
        s=s+i+"\n"
    s=re.sub('\s+$','',s)
    return s


def print_comment(item, indent=0):
    """
     Recursively fetch and insert all nested comments into json object
     and then printing each comment with correct indentation
    :param item: comment id to fetch
    :param indent (int): comment indentation
    :return:
    """
    try :
        url = HACKER_NEWS_API_ITEM_URL % item
        data = requests.get(url).json()

        if 'text' in data :
            if indent >= 1 :
                print('  ' * indent + 'Posted by:' + data['by'])
                print(print_with_indent(data['text'], indent))
                print()
            else :
                print('Posted by: ' + data['by'])
                print(data['text'])
                print()
        if "kids" in data and len(data["kids"]) > 0 :
            for comment_id in data["kids"] :
                data[comment_id] = json.loads(print_comment(comment_id, indent+1))
        return json.dumps(data)
    except Exception as err :
        logging.error(err)
