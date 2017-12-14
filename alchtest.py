from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:////root/tree/tree.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

relations_tb = Table('par_child_tb', Base.metadata, Column('par_id', Integer, ForeignKey('nodes.id'), primary_key = True), Column('child_id', Integer, ForeignKey('nodes.id'), primary_key = True))
                                                                                         
class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key = True)
    url = Column(String)
    title = Column(String)
    parents = relationship("Node", secondary=relations_tb, back_populates = 'childs')
    childs = relationship("Node", secondary=relations_tb, back_populates = 'parents')
