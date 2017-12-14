#!/usr/bin/env python
import collections
import os
import re
import requests


def get_title(url):
    """ Returns title from URL """
    obj = requests.get(url)
    title = re.findall('<title>(.*)<\/title>', obj.text)[0]
    return title


def main():

    Node = collections.namedtuple('Node', 'url title')

    parent_list = []
    with open('/root/tree/temp', 'r') as out_file:
        parent_list = out_file.readlines()
    
    parent = Node(url=parent_list[0], title=parent_list[1])
    child =  Node(url=os.getenv('QUTE_URL'), title=get_title(os.getenv('QUTE_URL'))

if __name__ == '__main__':
    main()
