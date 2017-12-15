#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import collections
import requests
import logging
import os
import re

#LOG_FILENAME = '/root/tree/log'
#FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
#logging.basicConfig(format=FORMAT, filename=LOG_FILENAME, level=logging.ERROR)


Base = declarative_base()
engine = create_engine('sqlite:////root/tree/tree.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
relations_tb = Table('par_child_tb', Base.metadata, Column('par_id', Integer, ForeignKey('nodes.id'), primary_key = True), Column('child_id', Integer, ForeignKey('nodes.id'), primary_key = True))

class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key = True)
    url = Column(String)
    title = Column(String)
    childs = relationship("Node", secondary=relations_tb, primaryjoin=id==relations_tb.c.par_id, secondaryjoin=id==relations_tb.c.child_id, backref='parents')

    
Base.metadata.create_all(engine)


def get_title(url):
    """ Returns title from URL """
    obj = requests.get(url)
    title = re.findall('<title>(.*)<\/title>', obj.text)[0]
    return title


def get_param():
    with open('/root/tree/param', 'r') as params_f:
        return params.readlines()[0]

    

def get_parent():
    url=''
    with open('/root/tree/parent', 'r') as par_f:
        url = par_f.readlines()[0]
    return url
#    return session.query(Node).filter(Node.url==url).first()


def main():
    parent = Node(url='http://google.com', title=get_title('http://google.com'))
    session.add(parent)
 #   logging.info('main - ROOT created')
    
    child =  Node(url=os.getenv('QUTE_URL'), title=get_title(os.getenv('QUTE_URL')))
#    logging.info('main - child node created with {} url'.format(os.getenv('QUTE_URL')))

#    child_q = session.query(Node).filter(Node.url==child.url).first()
#    if child_q is not None:
#        child = child_q
    child.parents.append(parent)
    session.add(child)
    session.commit()
#    logging.info('main - both objects created and added to DB')
#    logging.info('main - qute  fifo = {}'.format(os.getenv('QUTE_FIFO')))

    with open(os.getenv('QUTE_FIFO'), 'w') as fifo:
        logging.info('main - opened FIFO')
#        fifo.write('open {} {}'.format(get_param(),child.url))
        fifo.write('open -b {}'.format(child.url))                  
 #       logging.info('main - written to fifo')

                  
if __name__ == '__main__':
#    logging.info('__name__')
    main()

