#!/usr/bin/python
import logging
import sys
from libs.cli_commands_parser import CommandsCli

root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s: %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


def main():
    try:
        CommandsCli()
    except Exception as err:
        logging.error("%s", err)


if __name__ == '__main__':
    main()
