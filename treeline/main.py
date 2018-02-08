import sys,os,datetime,re,requests
from model import Node, Note, Base
from config import *
import treeline

Base.metadata.create_all(engine)

def main():
    piped = ''
    while True:
        with open(fifo_fp, 'r') as fifo:
            while True:
                last_piped = fifo.read()
                if len(last_piped) == 0:
                    break
                
                piped += last_piped
                if ' ;; END' in piped:
                    packages=re.findall('([0-9]+.*? ;; END)', piped)
                    piped = ''
                    packages = [package.split(' ;; ') for package in packages]
                    for package in packages:
                        switch[package[0]](package)

######################################### End of main


class Pac_Node():
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child

def ex(package):
    """ Removes the treeline's entries from /tmp and breaks out of the while True loop. """
    return

    
def node_add(package):
    """ Adds a new node to the database and calls the update method
    Expected package: [1, parent, child, 'END'] """
    pac = Pac_Node(parent=package[1],child=package[2])
    pac.child = pac.child.replace('%20','+')
    node = get_node(pac.child)
    if node.date == '?':
        node.date = datetime.date.today()
    parent = get_node(pac.parent)
    if parent not in node.parents:
        node.parents.append(parent)
    db_session.add(node)
    update()
    return 


def fav_add(package):
    """ Marks a node as a favorite and update 
    expected package [2, URL, END]"""
    node = get_node(package[1])
    node.favorite = True
    update()
    return

def note_add(package):
    """ Adds a note entry to the Notes table
    expected package [3, URL, TEXT, END]"""
    node = get_note(package[1])
    body = package[2]
    note = Note(node=node, body=body)
    db_session.add(note)
    update()

def update(package=None):
    """ Saves the qute session, parses the file to identify the websites in session, updates the database and finally  updates the treeline.org and treeline.html """
    update_qt_session()
    db_session.commit()
    treeline.update()


def get_node(url):
    """ queries DB for Node with the given url if not existent creates it"""
    node = db_session.query(Node).filter(Node.url==url).first()
    if node is None:
        node = Node(url=url, title=get_title(url), date='?')
    return node

def get_title(url):
    """ From URL returns title (if it exists, else it returns the url) """
    try:
        obj=requests.get(url)
        title=re.findall('<title>(.*?)<\/title>',obj.text)[0]
    except BaseException:
        title=url
    return title

def update_qt_session():
    """ Updates the nodes with the current session info. Unmarks previous session and marks it with new one """

    old_session = db_session.query(Node).filter(Node.in_session==True).all()
    for node in old_session:
        node.in_session=False

    new_session = get_session()
    for node in new_session:
        node = get_node(node)
        node.in_session = True
    return

def get_session():
    """ Opens the session file, uses regex to find all open websites and returns the list of opened sites"""
    with open(session_fp, 'r') as session_f:
        session = [line.strip('\n') for line in session_f.readlines()]
        session = [line.group(1) for line in [re.match('.*url: (.*)',line) for line in session] if line is not None]
    return session

switch = {'0':ex, '1':node_add, '2':fav_add, '3':note_add, '4':update}

if __name__ == "__main__":
    main()
