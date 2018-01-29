#!/usr/bin/zsh
SCRIPT_DIR=$0:a:h
echo "w $1\n" >> $QUTE_FIFO
cd "$SCRIPT_DIR"
source "${0:a:h}/dict.sh" 
TARGET_DIR=${TREES[$1]}
cat trunk >> "$TARGET_DIR/trunk"
cat favorites >> "$TARGET_DIR/favorites"
rm trunk favorites
./purple-tree.sh $TARGET_DIR
