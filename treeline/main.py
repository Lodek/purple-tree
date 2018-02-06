#!/usr/bin/python
import sys,os,time

fifo_p = '/tmp/treeline'
fifo_fp = fifo_p+'/fifo'
if not os.path.exists(fifo_p):
    os.makedirs(fifo_p)
if not os.path.exists(fifo_fp):
    os.mkfifo(fifo_fp)

piped = ''

def ex(package):
    """ Removes the treeline's entries from /tmp and breaks out of the while True loop. """
    

def node_add(package):
    """ Adds a new node to the database and calls the update method """
    
def fav_add(package):
    """ Marks a node as a favorite, wgets the page to the directory and updates 
    """
def update(package):
    """ Saves the qute session to a session file in the /tmp/treeline, parses the file to identify the websites in session, updates the database and finally  updates the treeline.org and treeline.html """


switch = {'0':ex, '1':node_add, '2':fav_add, '3':update}

while True:
    with open(fifo_fp, 'r') as fifo:
        while True:
            last_piped = fifo.read()
            if len(last_piped) == 0:
                break

            piped += last_piped
            print(piped)
            if ' ;; END' in piped:
                package = piped.split(' ;; ')
                piped = ''
                switch[package[0]](package)
