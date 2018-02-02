#!/usr/bin/zsh
PTARGET="$HOME/.local/share/qutebrowser/userscripts/"
PSCRIPTS=$0:a:h/qute-scripts
mkdir -p  $PTARGET
ln -sf $PSCRIPTS/favorite.py $PTARGET 
ln -sf $PSCRIPTS/hint.py $PTARGET 
ln -sf $PSCRIPTS/open.py $PTARGET 
ln -sf $PSCRIPTS/rapid.py $PTARGET 
ln -sf $PSCRIPTS/session-save.py $PTARGET
ln -sf $PSCRIPTS/research-add.sh $PTARGET 
