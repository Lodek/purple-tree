#!/bin/sh
export QUTE_PAR_URL=$QUTE_URL
export QUTE_PAR_TITLE=$QUTE_TITLE
echo 'hint links userscript ~/tree/hinttest.sh' >> "$QUTE_FIFO"
