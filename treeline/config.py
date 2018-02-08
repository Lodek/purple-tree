from trees import *
import sys,datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

        
tmp_p = '/tmp/treeline'
fifo_fp = tmp_p+'/fifo'
session_fp = tmp_p+'/session.yml'
session_ln = home+'/.local/share/qutebrowser/sessions/tmp_treeline.yml'
make_dir(tmp_p)
#if os.path.islink(session_ln):
#    os.symlink(session_fp, session_ln)
if not os.path.exists(fifo_fp):
    os.mkfifo(fifo_fp)

if len(sys.argv) > 1:
    if sys.argv[1] in trees:
        target_p = trees[sys.argv[1]]
    else:
        target_p = home+'/.trees/'+sys.argv[1]
else:
    target_p = home+'/.trees/'+datetime.datetime.now().strftime("'%b %d, %y'")

treeline_p = target_p+'/.treeline'
db_fp = treeline_p+'/treeline.db'
make_dir(target_p)
make_dir(treeline_p)


engine = create_engine('sqlite:///{}'.format(db_fp), echo=True)
db_Session = sessionmaker(bind=engine)
db_session = db_Session()

