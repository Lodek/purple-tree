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

Base = declarative_base()
engine = create_engine('sqlite:///{}/tree.db'.format(root_dir), echo=True)
Session = sessionmaker(bind=engine)
session = Session()
relations_tb = Table('par_child_tb', Base.metadata, Column('par_id', Integer, ForeignKey('nodes.id'), primary_key = True), Column('child_id', Integer, ForeignKey('nodes.id'), primary_key = True))


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


def main():
    check_db()
    
if __name__ == '__main__':
    main()

