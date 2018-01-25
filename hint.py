#!/usr/bin/python
import os
import sys

path='/home/lodek/projects/purple-tree/'

if len(sys.argv) != 1:
    with open('{}echoes'.format(path), 'w') as echoes:
        echoes.write('{} {}'.format(sys.argv[1],sys.argv[2]))

else:
    with open('{}echoes'.format(path), 'r') as echoes:
        args=echoes.read().split(' ') #args expected: open flag(b,t,n) and parent url respectively

    fifo = open(os.getenv('QUTE_FIFO'), 'w')
    parent=args[1]
    child = os.getenv('QUTE_URL')

    fifo.write('open {} {}'.format(args[0], child))

    with open('{}trunk'.format(path), 'a') as db:
        db.write('{} ;; {}\n'.format(parent,child))

