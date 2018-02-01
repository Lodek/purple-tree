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

from common import *

if len(sys.argv) > 1:
    #echoes of the args received
    echo_echo('{} {}'.format(sys.argv[1],sys.argv[2]))

else:
    #args expected: open flag(b,t,n) and parent url respectively
    args = hear_echo().split(' ')
    flags = args[0]
    parent = args[1]
    child = qute_url
    #date defined in common
    echo_fifo('open {} {}'.format(flags, child))
    echo_trunk('{} ;; {} ;; {}\n'.format(parent,child,date))
