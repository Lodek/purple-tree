#!/usr/bin/zsh
SESSION="$2/.treeline/$1.yml"
ECHO="trees['"$1"']='"$2"'" #ideally $2 would automatically expand home but I havent managed to make that work yet
mkdir -p $2/.treeline/favorites
echo $ECHO >> ~/.config/treeline/trees.py
touch $SESSION
ln -sf $SESSION ~/.local/share/qutebrowser/sessions/

