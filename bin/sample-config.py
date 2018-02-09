config.load_autoconfig()

c.aliases['sd'] = 'config-source -c'
c.aliases['sr'] = 'config-source -c ~/.config/treeline/treeline-config.py'
c.aliases['f'] = 'spawn -u {}/mark.py'.format(scripts_p)
c.aliases['n'] = 'spawn -u {}/notes.py'.format(scripts_p)

config.bind('f', 'spawn -u {}/hint.py -h {{url}} ;; hint links userscript {}/hint.py'.format(scripts_p,scripts_p), mode='normal')
config.bind('F', 'spawn -u {}/hint.py -b {{url}} ;; hint links userscript {}/hint.py'.format(scripts_p,scripts_p), mode='normal')
config.bind('<', 'set-cmd-text -s :spawn --userscript {}/open.py -t root '.format(scripts_p), mode='normal')
config.bind('>', 'set-cmd-text -s :spawn --userscript {}/open.py -t {{url}} '.format(scripts_p), mode='normal')

config.bind('u', 'undo ;; spawn -u {}/update.py'.format(scripts_p), mode='normal')
config.bind('d', 'tab-close  ;; spawn -u {}/update.py'.format(scripts_p), mode='normal')
config.bind('H', 'back ;; spawn -u {}/update.py'.format(scripts_p), mode='normal')
config.bind('L', ' forward ;; spawn -u {}/update.py'.format(scripts_p), mode='normal')

