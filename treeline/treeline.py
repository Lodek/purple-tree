#!/usr/bin/env python
"""
this script is responsible for reading the txt db file and parsing it and transforming it into a sqlite3 file, it uses sqlalchemy to do so.
it also reads the favorites files (which signalizes that the souce code of that page should also be saved

finally is generates tree.html and tree.org. 
this script should be called by the save-session,sh script
"""

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from subprocess import call
import collections
import requests
import sys
import os
import re

css = "<style media='screen' type='text/css'> body{    background: #000;    font-family: Georgia, Palatino, serif;    color: #EEE;    line-height: 1;    padding: 30px;    margin:auto;    max-width:42em;}h1, h2, h3, h4 {    font-weight: 400;}h1, h2, h3, h4, h5, p {    margin-bottom: 24px;    padding: 0;}h1 {    font-size: 48px;}h2 {    font-size: 36px;    margin: 24px 0 6px;}h3 {    font-size: 24px;}h4 {    font-size: 21px;}h5 {    font-size: 18px;}a {    color: #61BFC1;    margin: 0;    padding: 0;    text-decoration: none;    vertical-align: baseline;}a:hover {    text-decoration: underline;}a:visited {    color: #466B6C;}ul, ol {    padding: 0;    margin: 0;}li {    line-height: 24px;}li ul, li ul {    margin-left: 24px;}p, ul, ol {    font-size: 16px;    line-height: 24px;    max-width: 540px;}pre {    padding: 0px 24px;    max-width: 800px;    white-space: pre-wrap;}code {    font-family: Consolas, Monaco, Andale Mono, monospace;    line-height: 1.5;    font-size: 13px;}aside {    display: block;    float: right;    width: 390px;}blockquote {    border-left:.5em solid #eee;    padding: 0 2em;    margin-left:0;    max-width: 476px;}blockquote  cite {    font-size:14px;    line-height:20px;    color:#bfbfbf;}blockquote cite:before {    content: '\2014 \00A0';}blockquote p {      color: #666;    max-width: 460px;}hr {    width: 540px;    text-align: left;    margin: 0 auto 0 0;    color: #999;}/* Code below this line is copyright Twitter Inc. */button,input,select,textarea {  font-size: 100%;  margin: 0;  vertical-align: baseline;  *vertical-align: middle;}button, input {  line-height: normal;  *overflow: visible;}button::-moz-focus-inner, input::-moz-focus-inner {  border: 0;  padding: 0;}button,input[type='button'],input[type='reset'],input[type='submit'] {  cursor: pointer;  -webkit-appearance: button;}input[type=checkbox], input[type=radio] {  cursor: pointer;}/* override default chrome & firefox settings */input:not([type='image']), textarea {  -webkit-box-sizing: content-box;  -moz-box-sizing: content-box;  box-sizing: content-box;}input[type='search'] {  -webkit-appearance: textfield;  -webkit-box-sizing: content-box;  -moz-box-sizing: content-box;  box-sizing: content-box;}input[type='search']::-webkit-search-decoration {  -webkit-appearance: none;}label,input,select,textarea {  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;  font-size: 13px;  font-weight: normal;  line-height: normal;  margin-bottom: 18px;}input[type=checkbox], input[type=radio] {  cursor: pointer;  margin-bottom: 0;}input[type=text],input[type=password],textarea,select {  display: inline-block;  width: 210px;  padding: 4px;  font-size: 13px;  font-weight: normal;  line-height: 18px;  height: 18px;  color: #808080;  border: 1px solid #ccc;  -webkit-border-radius: 3px;  -moz-border-radius: 3px;  border-radius: 3px;}select, input[type=file] {  height: 27px;  line-height: 27px;}textarea {  height: auto;}/* grey out placeholders */:-moz-placeholder {  color: #bfbfbf;}::-webkit-input-placeholder {  color: #bfbfbf;}input[type=text],input[type=password],select,textarea {  -webkit-transition: border linear 0.2s, box-shadow linear 0.2s;  -moz-transition: border linear 0.2s, box-shadow linear 0.2s;  transition: border linear 0.2s, box-shadow linear 0.2s;  -webkit-box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);  -moz-box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);}input[type=text]:focus, input[type=password]:focus, textarea:focus {  outline: none;  border-color: rgba(82, 168, 236, 0.8);  -webkit-box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1), 0 0 8px rgba(82, 168, 236, 0.6);  -moz-box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1), 0 0 8px rgba(82, 168, 236, 0.6);  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1), 0 0 8px rgba(82, 168, 236, 0.6);}/* buttons */button {  display: inline-block;  padding: 4px 14px;  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;  font-size: 13px;  line-height: 18px;  -webkit-border-radius: 4px;  -moz-border-radius: 4px;  border-radius: 4px;  -webkit-box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2), 0 1px 2px rgba(0, 0, 0, 0.05);  -moz-box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2), 0 1px 2px rgba(0, 0, 0, 0.05);  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2), 0 1px 2px rgba(0, 0, 0, 0.05);  background-color: #0064cd;  background-repeat: repeat-x;  background-image: -khtml-gradient(linear, left top, left bottom, from(#049cdb), to(#0064cd));  background-image: -moz-linear-gradient(top, #049cdb, #0064cd);  background-image: -ms-linear-gradient(top, #049cdb, #0064cd);  background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0%, #049cdb), color-stop(100%, #0064cd));  background-image: -webkit-linear-gradient(top, #049cdb, #0064cd);  background-image: -o-linear-gradient(top, #049cdb, #0064cd);  background-image: linear-gradient(top, #049cdb, #0064cd);  color: #fff;  text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.25);  border: 1px solid #004b9a;  border-bottom-color: #003f81;  -webkit-transition: 0.1s linear all;  -moz-transition: 0.1s linear all;  transition: 0.1s linear all;  border-color: #0064cd #0064cd #003f81;  border-color: rgba(0, 0, 0, 0.1) rgba(0, 0, 0, 0.1) rgba(0, 0, 0, 0.25);}button:hover {  color: #fff;  background-position: 0 -15px;  text-decoration: none;}button:active {  -webkit-box-shadow: inset 0 3px 7px rgba(0, 0, 0, 0.15), 0 1px 2px rgba(0, 0, 0, 0.05);  -moz-box-shadow: inset 0 3px 7px rgba(0, 0, 0, 0.15), 0 1px 2px rgba(0, 0, 0, 0.05);  box-shadow: inset 0 3px 7px rgba(0, 0, 0, 0.15), 0 1px 2px rgba(0, 0, 0, 0.05);}button::-moz-focus-inner {  padding: 0;  border: 0;} </style>"

#filenames stuff
root_dir = os.path.dirname(os.path.realpath(__file__))
target_dir = sys.argv[1]
tmp_dir = sys.argv[2]
    
db_file = '{}/treeline/treeline.db'.format(target_dir)
db_txt = '{}/trunk'.format(tmp_dir)

forg = open('{}/treeline.org'.format(target_dir), 'w')
fhtml = open('{}/treeline.html'.format(target_dir), 'w')


#sqlalchemy sorcery
Base = declarative_base()
engine = create_engine('sqlite:///{}/{}'.format(target_dir,db_file), echo=True)
Session = sessionmaker(bind=engine)
session = Session()
relations_tb = Table('par_child_tb', Base.metadata, Column('par_id', Integer, ForeignKey('nodes.id'), primary_key = True), Column('child_id', Integer, ForeignKey('nodes.id'), primary_key = True))
Value = collections.namedtuple('Value', 'parent child')

class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key = True)
    url = Column(String)
    title = Column(String)
    favorite = Column(Boolean, default=False)
    in_session = Column(Boolean, default=False)
    date = Column(String)
    childs = relationship("Node", secondary=relations_tb, primaryjoin=id==relations_tb.c.par_id, secondaryjoin=id==relations_tb.c.child_id, backref='parents')


def get_txt():
    """ reads the txt db file and parses it """
    with open('{}/{}'.format(souce_dir, db_txt), 'r') as ftrunk:
        hist = []
        for line in ftrunk.readlines():
            visit = line.strip('\n').split(' ;; ')
            hist.append(Value(parent = visit[0], child = visit [1]))
    return hist


def check_db():
    """ checks if db exists. If it does not, creates it  and adds root """
    if not os.path.isfile('{}/{}'.format(target_dir, db_file)):
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


def gen_files():
    root = get_node('root')
    fhtml.write('{}\n'.format(css))
    recursive(root,1)
    

def recursive(node,level):
    """ some recursive action to generate html and org tree files
        essentially it calls this function for each child in a node until there is no child """
    forg.write(('*'*level+' [[{}][{}]]\n'.format(node.url,node.title)))
    fhtml.write('<h{}> <a href="{}">{}*{}</a> </h{}>\n'.format(level,node.url,'-'*level,node.title,level))
    if node.childs == []:
        return
    else:
        for child in node.childs:
            recursive(child, level+1)

def handle_favorites():
    with open(favorites_file, 'r') as ff:
        favorites = [fav.strip('\n') for fav in ff.readlines()]
    for favorite in favorites:
        node = get_node(favorite)
        node.favorite = True
        
def dl_favorite(url):
    call(['wget', '-k', '-E', '-p', '-P', target_dir, url])

def main():
    check_db()
    hist = get_txt()
    for visit in hist:
        add_node(visit)
    mark_favorites()
    dl_favorites()
    mark_session()
    session.commit()
    gen_files()

    
if __name__ == '__main__':
    main()