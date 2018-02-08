#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

relations_tb = Table('par_child_tb', Base.metadata, Column('par_id', Integer, ForeignKey('nodes.id'), primary_key = True), Column('child_id', Integer, ForeignKey('nodes.id'), primary_key = True))

class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key = True)
    url = Column(String)
    title = Column(String)
    favorite = Column(Boolean, default=False)
    in_session = Column(Boolean, default=False)
    date = Column(String, default='?')
    notes = relationship('Note', back_populates='node')
    childs = relationship("Node", secondary=relations_tb, primaryjoin=id==relations_tb.c.par_id, secondaryjoin=id==relations_tb.c.child_id, backref='parents')


class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key = True)
    node_id = Column(Integer, ForeignKey('nodes.id'))
    node = relationship('Node', back_populates='notes')
    date_added = Column(Date, default=datetime.date.today())
    body = Column(String)

