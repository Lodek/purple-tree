#!/usr/bin/python
from subprocess import call
from common import *
ptreesf = os.getenv('HOME')+'/.config/treeline/trees.py'
sys.path.insert(0,ptreesf)
from trees import trees
pgendbf = os.path.exists(os.path.join(path, '../treeline/gen-db.py')) 
session = sys.argv[1]
echo_fifo('session-save {}'.format(session))
call([gendbf, trees[session]])
