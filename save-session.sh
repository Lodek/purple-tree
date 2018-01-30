#!/usr/bin/zsh
SCRIPT_DIR=$0:a:h
echo "session-save $1\n" >> $QUTE_FIFO
cd "$SCRIPT_DIR"
source "${0:a:h}/dict.sh" 
TARGET_DIR=${TREES[$1]}
cat tmp/trunk >> "$TARGET_DIR/trunk"
cat tmp/favorites >> "$TARGET_DIR/favorites"
rm tmp/trunk tmp/favorites
$SCRIPT_DIR/purple-tree.py $TARGET_DIR
