#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import collections
import requests
import sys
import os
import re

root_dir = '/home/lodek/projects/purple-tree/'
db_file = 'tree.db'
db_txt = 'trunk'
Base = declarative_base()
engine = create_engine('sqlite:///{}/{}'.format(root_dir,db_file), echo=True)
Session = sessionmaker(bind=engine)
session = Session()
relations_tb = Table('par_child_tb', Base.metadata, Column('par_id', Integer, ForeignKey('nodes.id'), primary_key = True), Column('child_id', Integer, ForeignKey('nodes.id'), primary_key = True))
Value = collections.namedtuple('Value', 'parent child')
forg = open('{}out.org'.format(root_dir), 'w')
fhtml = open('{}out.html'.format(root_dir), 'w')

class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key = True)
    url = Column(String)
    title = Column(String)
    childs = relationship("Node", secondary=relations_tb, primaryjoin=id==relations_tb.c.par_id, secondaryjoin=id==relations_tb.c.child_id, backref='parents')


def get_txt():
    with open('{}{}'.format(root_dir, db_txt), 'r') as ftrunk:
        hist = []
        for line in ftrunk.readlines():
            visit = line.strip('\n').split(' ;; ')
            hist.append(Value(parent = visit[0], child = visit [1]))
    return hist


def check_db():
    """ checks if db exists. If it does not, creates it  and adds root """
    if not os.path.isfile('{}/{}'.format(root_dir, db_file)):
        Base.metadata.create_all(engine)
        session.add(Node(title='root',url='root'))
        session.commit()
    return


def get_title(url):
    """ From URL returns title (if it exists, else it returns the url) """
    try:
        obj=requests.get(url)
        title=re.findall('<title>(.*?)<\/title>',obj.text)[0]
    except BaseException:
        title=url
    return title

    
def get_node(url):
    """ queries DB for Node with the given url if not existent creates it"""
    node = session.query(Node).filter(Node.url==url).first()
    if node is None:
        node = Node(url = url, title = get_title(url))
    return node


def add_node(visit):
    """ Expects an object of type visit (named tuple). Returns the node object for the matching child of the visit """
    node = get_node(visit.child)
    parent = get_node(visit.parent)
    node.parents.append(parent)
    if parent not in node.parents:
        node.parents.append(parent)
    session.add(node)
    return node


def gen_org():
    root = get_node('root')
    fhtml.write('<link rel="stylesheet" href="/home/lodek/projects/purple-tree/theme.css">\n')
    recursive(root,1)
    
          
def recursive(node,level):
    forg.write(('*'*level+' [[{}][{}]]\n'.format(node.url,node.title)))
    fhtml.write('<h{}> <a href="{}">{}*{}</a> </h{}>\n'.format(level,node.url,'-'*level,node.title,level))
    if node.childs == []:
        return
    else:
        for child in node.childs:
            recursive(child, level+1)


def main():
    check_db()
    hist = get_txt()
    for visit in hist:
        add_node(visit)
    session.commit()
    gen_org()

    
if __name__ == '__main__':
    main()
