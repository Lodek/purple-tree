#!/usr/bin/python
""" this script simply takes the url of the current tab and sends a command to treeline's fifo in order to bookmark it """
from common import *
with open(tree_fifo, 'w') as treeline:
    treeline.write('2 ;; {} ;; END'.format(voice))


