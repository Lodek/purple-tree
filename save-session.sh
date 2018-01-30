#!/usr/bin/zsh
SCRIPT_DIR=$0:a:h
TARGET_DIR=${TREES[$1]}
TMP_DIR="/tmp/treeline-$1/"

echo "session-save $1\n" >> $QUTE_FIFO
source "$SCRIPT_DIR/dict.sh"
cd "$SCRIPT_DIR"
mkdir $TMP_DIR
cp tmp/trunk tmp/favorites $TMP_DIR
rm -f tmp/trunk tmp/favorites
touch tmp/trunk tmp/favorites
$SCRIPT_DIR/treeline.py $TARGET_DIR $TMP_DIR
