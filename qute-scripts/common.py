#!/usr/bin/python
import datetime,sys,os

_fifo = open(os.getenv('QUTE_FIFO'), 'w')
_pdata = '/tmp/treeline'
_pfavoritef = _pdata+'/favorite'
_ptrunkf = _pdata+'/trunk'
_pechof =  _pdata+'/echo'

path = os.path.dirname(os.path.realpath(__file__))
date = datetime.datetime.today().replace(microsecond=0).isoformat(' ')
qute_url = os.getenv('QUTE_URL') 

#makes /tmp/treeline dir if it doesn't exist
if not os.path.exists(_pdata):
    os.makedirs(_pdata)
    
def echo_fifo(voice):
    """ writes to qute fifo """
    _fifo.write('{}\n'.format(voice))
    
def echo_echo(voice):
    """ writes voice to echof"""
    with open(_pechof, 'w') as echo:
        echo.write(voice)
        
def echo_trunk(voice):
    """ writes voice to trunkf"""
    with open(_ptrunkf, 'a') as trunk:
        trunk.write(voice)

def echo_favorite(voice):
    """ writes voice to favoritef"""
    with open(_pfavoritef, 'a') as favorite:
        favorite.write(voice+'\n')

def hear_echo():
    """ read echof"""
    with open(_pechof, 'r') as echo:
        return echo.read()
