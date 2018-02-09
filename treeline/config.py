import sys,datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
ptrees = os.getenv('HOME')+'/.config/treeline'
sys.path.insert(0,ptrees)
from trees import trees

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

#default treeline paths
dftrees_p = home+'/.trees/'
tmp_p = '/tmp/treeline'
fifo_fp = tmp_p+'/fifo'
session_fp = tmp_p+'/session.yml'
session_ln = home+'/.local/share/qutebrowser/sessions/tmp_treeline.yml'
make_dir(tmp_p)

#sym link on qutes sessions directory
os.remove(session_ln)
os.symlink(session_fp, session_ln)

#make fifo
if not os.path.exists(fifo_fp):
    os.mkfifo(fifo_fp)

#defines treeline path, if an arg was passed checks the dictionary, if dictionary has entry use that else make a folder under ~/.trees
#if no arg was passed, makes folder with todays date
if len(sys.argv) > 1:
    if sys.argv[1] in trees:
        target_p = trees[sys.argv[1]]
    else:
        target_p = dftrees_p+sys.argv[1]
else:
    target_p = dftrees_p+datetime.datetime.now().strftime("%b-%d-%y")

#relative treeline path
treeline_p = target_p+'/.treeline'
db_fp = treeline_p+'/treeline.db'
make_dir(target_p)
make_dir(treeline_p)

#sqlalchemy inits
engine = create_engine('sqlite:///{}'.format(db_fp), echo=True)
db_Session = sessionmaker(bind=engine)
db_session = db_Session()

