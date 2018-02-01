#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from subprocess import call
import collections
import requests
import sys
import os
import re

_dict = os.getenv('HOME')+'/.tlrc'
_data_dir = '/tmp/treeline'
_favoritef =  data_dir+'/favorite'
_trunkf = data_dir+'/trunk'
_dbf = ''

Base = declarative_base()
engine = create_engine('sqlite:///'+_dbf, echo=True)
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
    date = Column(String, default='')
    notes = Column(String)
    childs = relationship("Node", secondary=relations_tb, primaryjoin=id==relations_tb.c.par_id, secondaryjoin=id==relations_tb.c.child_id, backref='parents')
