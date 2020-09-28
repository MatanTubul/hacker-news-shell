#!/usr/bin/python
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.INFO)
from libs import CommandsCli
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s: %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


# usefull for indentation level https://stackoverflow.com/a/43232415/2393280

def main() :
    try :
        CommandsCli()
    except Exception as err :
        logging.error("%s", err)


if __name__ == '__main__' :
    main()
