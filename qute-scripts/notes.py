#!/usr/bin/python
""" Formats a new_note command request for treeline's fifo.
A new note can be issue by either typing the note in qute's command line and sending it as argument or by selecting some text in the webpage
If there is a selected text, any arguments will be ignored. If there is no selected text, the arguments will used as the none. And if there are no arguments it returns
"""
from common import *
selected = os.getenv('QUTE_SELECTED_TEXT')

if selected is None and len(sys.argv) == 1:
    pass
else:
    if selected is None:
        for arg in sys.argv[2:]:
            note += '{} '.format(arg)
            note = note[:-1]
    else:
        note = selected
    echo_treeline('3 ;; {} ;; {} ;; END'.format(qute_url,note))

