#!/usr/bin/python
"""
Since qute doesn't allow arguments to be passed using 'hint links userscript /path/to/script arg1 arg2' we need to call the script twice 

1st call spawn -u ./hint.py -t {url} -> URL of parent + open flag
2nd call hint links userscript ./hint.py -> call the script to actually generate the hints

1st call:  echoes the open flag into tmp file and parent to tree line fifo
2nd call reads open flag from tmp file, opens link in qute and echo child url to treeline fifo

sample config: config.bind('f', 'spawn -u ./hint.py -h {url} ;; hint links userscript ./hint.py', mode='normal')
""" 

from common import *

if len(sys.argv) > 1:
    echo_echo(sys.argv[1]) #echo open flag to echo file
    echo_treeline('1 ;; {} ;; '.format(sys.argv[2])) #echo parent to treeline fifo

else:
    #args expected: open flag(b,t,n)
    flag = listen_echo()
    flag = flag_parser(flag)
    child = qute_url
    echo_qt('open {} {}'.format(flag, child))
    session_save()
    echo_treeline('{} ;; END'.format(child))

