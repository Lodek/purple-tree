#!/usr/bin/sh
echo $(cat ~/tree/temp) > ~/tree/out
rm ~/tree/temp
echo $QUTE_URL >> ~/tree/out
echo 'open -b '$QUTE_URL >> "$QUTE_FIFO"
