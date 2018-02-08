#!/usr/bin/python
""" 
This file contain a series of functions and variable definitions that are common to the qutebrowser scripts, every script under this directory imports this module
"""
import datetime,sys,os

path = os.path.dirname(os.path.realpath(__file__))

tmp_p = '/tmp/treeline'
tree_fifo = tmp_p+'/fifo'
echo_fp = tmp_p+'/echo'

qute_fifo = open(os.getenv('QUTE_FIFO'), 'w')
qute_url = os.getenv('QUTE_URL') 
    
def echo_qt(voice):
    """ writes to qute fifo """
    qute_fifo.write('{}\n'.format(voice))

def echo_treeline(voice):
    """ writes to treeline's fifo """
    with open(tree_fifo, 'w') as tree:
        tree.write('{}'.format(voice))

def echo_echo(voice):
    """ echoes whatever to tmp file """
    with open(echo_fp, 'w') as echo:
        echo.write(voice)

def listen_echo():
    """ reads tmp file """
    with open(echo_fp, 'r') as echo:
        return echo.read()

def session_save():
    """ echoes a command to save the tmp treeline session into qute's fifo """
    echo_qt('session-save tmp_treeline')
    
def flag_parser(flag):
    """ removes the -h flag from the flags string. (since the other scripts always expect a flag argument, this was the easiest way to handle an open here requests """
    if '-h' in flag:
        flag = flag.strip('-h')
    return flag
