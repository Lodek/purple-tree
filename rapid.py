#!/usr/bin/python
"""
the logic of this script is very similar to 'hints.py', again since qute cannot handle arguments while called through hint links userscript... this script needs to be called twice

first time, to get parent url and echo it to tmp file
second time it does the hinting receives the child url and opens the link, writes it to the db and calls itself once again for the rapid hint behavior

example of config file
config.bind('F', 'spawn -u ./rapid.py {url} ;; hint links userscript ./rapid.py', mode='normal')

"""

import os
import sys
path = os.path.dirname(__file__)

if len(sys.argv) > 1:
    with open('{}/tmp/echoes'.format(path), 'w') as echoes:
        echoes.write('{}'.format(sys.argv[1])) #expected to pass parent

else:
    with open('{}/tmp/echoes'.format(path), 'r') as echoes:
        parent=echoes.read()#args expected: parent url

    fifo = open(os.getenv('QUTE_FIFO'), 'w')
    child = os.getenv('QUTE_URL')

    fifo.write('open -b {}\n'.format(child))

    with open('{}/tmp/trunk'.format(path), 'a') as db:
        db.write('{} ;; {}\n'.format(parent,child))

    fifo.write('hint links userscript {}/rapid.py'.format(path))
