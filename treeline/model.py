#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from subprocess import call
import requests
import sys
import os
import re
ptrees = os.getenv('HOME')+'/.config/treeline'
sys.path.insert(0,ptrees)
from trees import trees

session_name = sys.argv[1]
ptarget = trees[session_name]
ptl = ptarget+'/.treeline'
pdbf = ptl+'/treeline.db'
psessionf ='{}/{}.yml'.format(ptl,session_name)

#sql socery
Base = declarative_base()
engine = create_engine('sqlite:///{}'.format(pdbf), echo=True)
Session = sessionmaker(bind=engine)
session = Session()
relations_tb = Table('par_child_tb', Base.metadata, Column('par_id', Integer, ForeignKey('nodes.id'), primary_key = True), Column('child_id', Integer, ForeignKey('nodes.id'), primary_key = True))

class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key = True)
    url = Column(String)
    title = Column(String)
    favorite = Column(Boolean, default=False)
    in_session = Column(Boolean, default=False)
    date = Column(String, default='?')
    notes = Column(String, default='None')
    childs = relationship("Node", secondary=relations_tb, primaryjoin=id==relations_tb.c.par_id, secondaryjoin=id==relations_tb.c.child_id, backref='parents')

Base.metadata.create_all(engine)

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
        node = Node(url=url, title=get_title(url), date='?')
    return node

