#!/usr/bin/sh
FILE_PATH='/root/tree/echoes'
rm "$FILE_PATH"
if [ $# -ne 0 ]; then
    for var in "$@"
    do
        echo "$var" >> "$FILE_PATH"
    done
fi
echo $QUTE_URL >> "$FILE_PATH"
echo $QUTE_TITLE >> "$FILE_PATH"
