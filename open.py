#!/usr/bin/python
import sys,os

path='/home/lodek/projects/purple-tree/'
if len(sys.argv) > 1:
    fifo = open(os.getenv('QUTE_FIFO'), 'w')
    parent = sys.argv[2]
    flag = sys.argv[1]

    query = ''
    for arg in sys.argv[3:]:
        query += '{} '.format(arg)
    query= query [:-1]


    fifo.write('open {} {}\n'.format(flag, query))

    with open('{}trunk'.format(path), 'a') as db:
        db.write('{} ;; '.format(parent))
    
    fifo.write('spawn -u {}open.py'.format(path))

else:
    child = os.getenv('QUTE_TITLE')
    with open('{}trunk'.format(path), 'a') as db:
        db.write('{}\n'.format(child))

    
