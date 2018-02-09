#!/usr/bin/zsh
CWD="$0:a:h"
CFD="$HOME/.config/treeline"
mkdir -p "$CFD"
touch "$CFD"/trees.py
cd $CWD/../qute-scripts/
SCRIPT_DIR=$(pwd)
cd $CWD
echo "scripts_p = '"$SCRIPT_DIR"'" > "$CFD/treeline-config.py"
cat ./sample-config.py >> "$CFD/treeline-config.py"
echo "add the following line to your qutebrowser config file.
c.aliases['sr'] = 'config-source -c ~/.config/treeline/treeline-config.py'"


