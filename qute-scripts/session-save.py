#!/usr/bin/python
from subprocess import call
from common import *
pgendbf = os.path.abspath(os.path.join(path, '../treeline/gen-db.py')) 
session = sys.argv[1]
echo_fifo('session-save {}'.format(session))
call([pgendbf,session])
