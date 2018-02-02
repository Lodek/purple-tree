#!/usr/bin/python
"""
the logic of this script is very similar to 'hints.py', again since qute cannot handle arguments while called through hint links userscript... this script needs to be called twice

first time, to get parent url and echo it to tmp file
second time it does the hinting receives the child url and opens the link, writes it to the db and calls itself once again for the rapid hint behavior

example of config file
config.bind('F', 'spawn -u ./rapid.py {url} ;; hint links userscript ./rapid.py', mode='normal')

"""
from common import *

if len(sys.argv) > 1:
    echo_echo(sys.argv[1]) #expected to pass parent

else:
    parent = hear_echo() #args expected: parent url
    child = qute_url
    echo_fifo('open -b {}'.format(child))
    echo_trunk('{} ;; {} ;; {}\n'.format(parent,child,date))
    echo_fifo('hint links userscript {}/rapid.py'.format(path))
