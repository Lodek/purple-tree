#!/bin/sh
echo "open http://duckduckgo.com" >> "$QUTE_FIFO"
echo $QUTE_URL > ~/tree/out
echo "hint all tab-bg" 
echo $QUTE_URL >> ~/tree/out
