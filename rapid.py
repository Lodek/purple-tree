#!/usr/bin/python
import os
import sys

path='/home/lodek/projects/purple-tree/'

if len(sys.argv) != 1:
    with open('{}echoes'.format(path), 'w') as echoes:
        echoes.write('{}'.format(sys.argv[1])) #expected to pass parent

else:
    with open('{}echoes'.format(path), 'r') as echoes:
        parent=echoes.read()#args expected: parent url

    fifo = open(os.getenv('QUTE_FIFO'), 'w')
    child = os.getenv('QUTE_URL')

    fifo.write('open -b {}\n'.format(child))

    with open('{}trunk'.format(path), 'a') as db:
        db.write('{} ;; {}\n'.format(parent,child))

    fifo.write('hint links userscript {}rapid.py'.format(path))
