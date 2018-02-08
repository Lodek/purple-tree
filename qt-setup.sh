#!/usr/bin/zsh
PTARGET="$HOME/.local/share/qutebrowser/userscripts/"
PSCRIPTS=$0:a:h/qute-scripts
mkdir -p  $PTARGET
ln -sf $PSCRIPTS/bookmark.py $PTARGET/treeline_bookmark.py
ln -sf $PSCRIPTS/hint.py $PTARGET/treeline_hint.py
ln -sf $PSCRIPTS/open.py $PTARGET/treeline_open.py
ln -sf $PSCRIPTS/rapid.py $PTARGET/treeline_rapid.py
ln -sf $PSCRIPTS/update.py $PTARGET/treeline_update.py
ln -sf $PSCRIPTS/notes.py $PTARGET/treeline_notes.py
