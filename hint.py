#!/usr/bin/python
"""
Since qute doesn't allow arguments to be passed using 'hint links userscript /path/to/script arg1 arg2' we need to call the script twice 

1st call spawn -u ./hint.py -t {url} -> URL of parent + open flag
2nd call hint links userscript ./hint.py -> call the script to actually generate the hints

1st call echoes the arguments into a tmp file
2nd call receives the child url from qute, reads tmp file, opens the link and echoes parent + child to txt file

THis is how the script should be called on qute:
config.bind('f', 'spawn -u ./hint.py -t {url} ;; hint links userscript ./hint.py', mode='normal')
""" 

import os
import sys

path = os.path.dirname(__file__)

if len(sys.argv) > 1:  #does the echoing of the args received
    with open('{}/tmp/echoes'.format(path), 'w') as echoes:
        echoes.write('{} {}'.format(sys.argv[1],sys.argv[2]))

else:
    with open('{}/tmp/echoes'.format(path), 'r') as echoes:
        args=echoes.read().split(' ') #args expected: open flag(b,t,n) and parent url respectively

    fifo = open(os.getenv('QUTE_FIFO'), 'w')
    parent=args[1]
    child = os.getenv('QUTE_URL')

    fifo.write('open {} {}'.format(args[0], child))

    with open('{}/tmp/trunk'.format(path), 'a') as db:
        db.write('{} ;; {}\n'.format(parent,child))

