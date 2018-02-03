#!/usr/bin/env python
"""
this script is responsible for reading the txt db file and parsing it and transforming it into a sqlite3 file, it uses sqlalchemy to do so.
it also reads the favorites files (which signalizes that the souce code of that page should also be saved

finally is generates tree.html and tree.org. 
this script should be called by the save-session,sh script
"""
import collections
from model import *

Value = collections.namedtuple('Value', 'parent child date')

#tmp files to generate database
pdata = '/tmp/treeline'
pfavoritef = pdata+'/favorite'
ptrunkf = pdata+'/trunk'
pechof =  pdata+'/echo'



def read_trunkf():
    """ reads the txt db file and parses it """
    with open(ptrunkf, 'r') as trunkf:
        trunk = []
        for line in trunkf.readlines():
            visit = line.strip('\n').split(' ;; ')
            trunk.append(Value(parent=visit[0], child=visit[1], date=visit[2]))
    return trunk


def add_node(visit):
    """ Expects an object of type visit (named tuple). Returns the node object for the matching child of the visit """
    node = get_node(visit.child)
    if node.date == '?':
        node.date = visit.date
    parent = get_node(visit.parent)
    if parent not in node.parents:
        node.parents.append(parent)
    session.add(node)
    return node


def mark_favorites():
    with open(pfavoritef, 'r') as favoritesf:
        favorites = [fav.strip('\n') for fav in favoritesf.readlines()]
    for favorite in favorites:
        node = get_node(favorite)
        node.favorite = True
    return


def mark_session():
    with open(psessionf, 'r') as sessionf:
        session = [line.strip('\n') for line in sessionf.readlines()]
        session = [line.group(1) for line in [re.match('.*url: (.*)',line) for line in session] if line is not None]
        for line in session:
            node = get_node(line)
            node.in_session = True
    return


def main():
    hist = read_trunkf()
    for visit in hist:
        add_node(visit)
    mark_favorites()
    mark_session()
    session.commit()
    path = os.path.dirname(os.path.realpath(__file__))
    call([path+'/treeline.py', session_name])
if __name__ == '__main__':
    main()
