#!/usr/bin/python
"""
the command to use the open script is as follows:
set-cmd-text -s :spawn --userscript ./open.py -t {root/{url}}

the set-cmd-text -s simply writes whatever follows into the qute command line

the user script is called and as arguments it receives the flag on how to open 
parent url which might be root or {url} which gets the url of the current page

the script still calls itself since it needs to retreive the child URL and since I thought it was wiser to let qute handle the search engine dictionary stuff this ugly solution is nescessary.

first the script runs with the arguments
it opens the new tab, echoes the parent url to the txt db and calls this script once again with no args

the second call simply reads the child URL with os,getenv and echoes it to the txt db file

Example of config to be added on config.py

config.bind('<', 'set-cmd-text -s :spawn --userscript ./open.py -t root ', mode='normal')
"""

from common import *

if len(sys.argv) > 1:
    parent = sys.argv[2]
    flags = sys.argv[1]

    query = ''
    for arg in sys.argv[3:]:
        query += '{} '.format(arg)
    query= query [:-1]

    echo_fifo('open {} {}'.format(flags, query))
    echo_trunk('{} ;; '.format(parent))
    echo_fifo('spawn -u {}/open.py'.format(path))

else:
    child = qute_url
    #date defined in common
    echo_trunk('{} ;; {}\n'.format(child,date))

    
