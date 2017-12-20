#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import collections
import requests
import logging
import time
import sys
import os
import re


root_dir = '/root/tree'
script_file = root_dir + '/purple_tree.py'
echoes_file = root_dir + '/echoes'
echoer_file = root_dir + '/echoer.sh'
LOG_FILENAME = '/root/tree/log'
FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, filename=LOG_FILENAME, level=logging.INFO)

Base = declarative_base()
engine = create_engine('sqlite:///{}/tree.db'.format(root_dir), echo=True)
Session = sessionmaker(bind=engine)
session = Session()
relations_tb = Table('par_child_tb', Base.metadata, Column('par_id', Integer, ForeignKey('nodes.id'), primary_key = True), Column('child_id', Integer, ForeignKey('nodes.id'), primary_key = True))

fifo = open(os.getenv('QUTE_FIFO'), 'w')


class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key = True)
    url = Column(String)
    title = Column(String)
    childs = relationship("Node", secondary=relations_tb, primaryjoin=id==relations_tb.c.par_id, secondaryjoin=id==relations_tb.c.child_id, backref='parents')


def check_db():
    """ checks if db exists. If it does not, creates it  and adds root """
    if not os.path.isfile('{}/tree.db'.format(root_dir)):
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


def get_root():
    """ Simple query, returns root node """
    return session.query(Node).first()

    
def get_node(url):
    """ queries DB for Node with the given url """
    node = session.query(Node).filter(Node.url==url).first()
    return node


def get_parent(url, title):
    """ queries db for parent. if it doesn't exist, creates it and returns the object"""
    parent = get_node(url)
    if parent is None:
        parent = Node(url=url, title=title)
        parent.parents.append(get_root())
        session.add(parent)
    return parent


def create_child(impostor):
    """ returns child node. queries the db, if that node exists that is return else creates the node with title"""
    child = get_node(impostor.url)
    if child is None:
        impostor.title = get_title(impostor.url)
        child = impostor
        session.add(child)
    return child


def qute_open(arguments):
    if arguments[2] == 'root':
        parent = get_root()
    else:
        parent = get_parent(arguments[2], os.getenv('QUTE_TITLE'))
    search = ''
    for word in arguments[3:]:
        search += '{} '.format(word)
    search = search[:-1]

    fifo.write('open {} {}\n'.format(arguments[1],search))
    time.sleep(.2)
    fifo.write('spawn -u {}'.format(echoer_file))
    time.sleep(1)
    echoes = listen_echoes()
    child = Node(url=echoes[1], title=get_title(echoes[1]))
    child.parents.append(parent)
    session.add(child)
    session.commit()
    return 


def qute_hint(arguments):
    child = Node(url=os.getenv('QUTE_URL'))
    fifo.write('open {} {}'.format(arguments[1], child.url))
    parent = get_parent(arguments[2], arguments[3])
    child = create_child(child)
    child.parents.append(parent)
    session.commit()
    return


def qute_rapid(arguments):
    child = Node(url=os.getenv('QUTE_URL'))
    fifo.write('open -b {}\n'.format(child.url))
    fifo.write('hint links userscript {}\n'.format(script_file))
    parent = get_parent(arguments[1], arguments[2])
    child = create_child(child)
    child.parents.append(parent)
    session.commit()
    return


def listen_echoes():
    with open('/root/tree/echoes', 'r') as echoes:
        return [echo.strip('\n') for echo in echoes.readlines()]


def main():
    check_db()
    if len(sys.argv) != 1:
        arguments = [argument for argument in sys.argv[1:]]
    else:
        arguments = listen_echoes()
    if arguments[0] == 'rapid':
        qute_rapid(arguments)
    elif arguments[0] == 'hint':
        qute_hint(arguments)
    elif arguments[0] == 'open':
        qute_open(arguments)
    
if __name__ == '__main__':
    main()

