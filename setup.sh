#!/usr/bin/zsh
DIR=$0:a:h
mkdir -p ~/.local/share/qutebrowser/userscripts
ln -sf $DIR/hint.py ~/.local/share/qutebrowser/userscripts/
ln -sf $DIR/open.py ~/.local/share/qutebrowser/userscripts/
ln -sf $DIR/rapid.py ~/.local/share/qutebrowser/userscripts/
ln -sf $DIR/favorite.sh ~/.local/share/qutebrowser/userscripts/
ln -sf $DIR/save-session.sh ~/.local/share/qutebrowser/userscripts/
