#!/usr/bin/env python
"""
this script is responsable for generating the treeline html and org files as well as the graph
it also uses wget to download any favorites that aren't in the .treeline/favorites directory yet
"""

from model import Node, Note
from config import *
from subprocess import call
marks_p = target_p+'/.treeline/marks'


def gen_files(files):
    root = db_session.query(Node).filter(Node.url=='root').first()
    recursive(root,1,files)

def recursive(node,level,files):
    """ some recursive action to generate html and org tree files
        essentially it calls this function for each child in a node until there is no child """
    files[1].write(('*'*level+' [[{}][{}]]    '.format(node.url,node.title)))
    files[1].write('[M]') if node.mark is True else ''
    files[1].write('[O]') if node.in_session is True else ''
    files[1].write('\n')
    for note in node.notes:
        files[1].write('{}\n'.format(note.body))
    if node.childs == []:
        return
    else:
        for child in node.childs:
            recursive(child, level+1,files)


def dl_marks():
    marks = db_session.query(Node).filter(Node.mark==True).all()
    for mark in marks:
        folder=marks_p+'/'+mark.id
        if not os.path.exists(folder):
            os.makedirs(folder)
            call(['wget', '-k', '-E', '-p', '-P', url, mark.url])


def gen_notes(files):
    notes = db_session.query(Note).all()
    if notes is None:
        return
    for note in notes:
        files[2].write('* {}\n{}'.format(note.node.url,note.body))
        

def open_files():
    html_fp = target_p+'/treeline.html'
    org_fp = target_p+'/treeline.org'
    notes_fp = target_p+'/treeline-notes.org'

    html_f = open(html_fp,'w')
    org_f = open(org_fp,'w')
    notes_f = open(notes_fp,'w')
    return (html_f, org_f, notes_f)

def close_files(files):
    for f in files:
        f.close()
        
def update():
    files=open_files()
    gen_files(files)
    gen_notes(files)
    dl_marks()
    close_files(files)
    return
