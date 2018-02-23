#!/usr/bin/env python
"""
this script is responsable for generating the treeline html and org files as well as the graph
it also uses wget to download any favorites that aren't in the .treeline/favorites directory yet
"""

from model import Node, Note
from config import *
import os



def gen_org_tree():
    org_fp = target_p+'/treeline.org'
    org_f = open(org_fp, 'w')
    nodes = db_session.query(Node).order_by(Node.id).all()
    elisp_link = lambda url,title: '*** [[elisp:(treeline-goto-node "{}" "{}")][{}]]\n'.format(url,title,title)
    for node in nodes:
        org_f.write('* [[{}][{}]]    '.format(node.url, node.title))
        if node.mark is True:
            org_f.write('[M]')
        if node.in_session is True:
            org_f.write('[O]')
        org_f.write('\n')
        org_f.write('** notes\n')
        for note in node.notes:
            org_f.write(note.body+'\n')
        org_f.write('** parents\n')
        for parent in node.parents:
            org_f.write(elisp_link(parent.url, parent.title))
        org_f.write('** children\n')
        for child in node.childs:
            org_f.write(elisp_link(child.url, child.title))
        

def dl_marks():
    marks_p = target_p+'/.treeline/marks'
    marks = db_session.query(Node).filter(Node.mark==True).all()
    for mark in marks:
        folder=marks_p+'/'+str(mark.id)
        if not os.path.exists(folder):
            os.makedirs(folder)
            os.system("wget -k -E -p -P {} '{}'".format(folder,mark.url))

def gen_notes():
    notes_fp = target_p+'/treeline-notes.org'
    with open(notes_fp,'w') as notes_f:
        notes = db_session.query(Note).all()
        if notes is None:
            return
        for note in notes:
            notes_f.write('* {}\n{}'.format(note.node.url,note.body))
        


        
def update():
    gen_org_tree()
    gen_notes()
    dl_marks()
    return
