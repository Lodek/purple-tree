"""
 This file is the treeline service that reads the fifo and dynamically generates the database
"""
import sys,os,datetime,re,requests
from model import Node, Note, Base
from config import *
import treeline

Base.metadata.create_all(engine) 

def main():
    """ Loop that opens the fifo, reads from it and executes the commands when specified """
    piped = ''
    #this while continuously opens the fifo file. Unix only opens a fifo when both ends of it are open (write end, listen end), so this efficiently waits for a write request before opening it, otherwise it hangs and waits for an open
    while True: 
        with open(fifo_fp, 'r') as fifo:
            while True:
                last_piped = fifo.read()
                if len(last_piped) == 0: #len 0 implies that the write end has been closed
                    break
                
                piped += last_piped
                 #only executes the command when the END part of the package is received
                if ' ;; END' in piped:
                    #since requests is slow, it might happen that there are more than one command on the fifo at a time
                    #this uses regex to create a list with all the commands
                    packages=re.findall('([0-9]+.*? ;; END)', piped) 
                    piped = ''
                    packages = [package.split(' ;; ') for package in packages]
                    for package in packages:
                        switch[package[0]](package)

######################################### End of main


class Pac_Node():
    """ simple class definition to make note_add more readable"""
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
    #qute generates URL's with %20 instead of +, duck redirects to an url using +, this is needed otherwise it would create orphans
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


def mark_add(package):
    """ marks a node and update 
    expected package: [2, URL, END]"""
    node = get_node(package[1])
    node.mark = True
    update()
    return

def note_add(package):
    """ Adds a note entry to the Notes table
    expected package [3, URL, TEXT, END]"""
    node = get_node(package[1])
    body = package[2]
    note = Note(node=node, body=body)
    db_session.add(note)
    update()

def update(package=None):
    """ Parses the session file to identify the opened pages, updates the database and finally  updates the treeline.org and treeline.html """
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
    """  Updates the nodes with the current session info. Unmarks previous session and marks it with new one """

    old_session = db_session.query(Node).filter(Node.in_session==True).all()
    for node in old_session:
        node.in_session=False

    new_session = get_session()
    for node in new_session:
        node = get_node(node)
        node.in_session = True
    return

def get_session():
    """ Opens the session file, uses regex to find all open websites and returns the list of open sites"""
    with open(session_fp, 'r') as session_f:
        session = [line.strip('\n') for line in session_f.readlines()]
        session = [line.group(1) for line in [re.match('.*url: (.*)',line) for line in session] if line is not None]
    return session

#dictionary containing function objects so main is cleaner
switch = {'0':ex, '1':node_add, '2':mark_add, '3':note_add, '4':update}

if __name__ == "__main__":
    main()
