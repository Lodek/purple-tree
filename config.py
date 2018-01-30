c.backend = 'webkit'
c.content.geolocation = 'ask'
config.load_autoconfig()
c.aliases['sd'] = 'config-source -c'
c.aliases['f'] = 'spawn -u /home/lodek/projects/purple-tree/favorites.sh'
c.aliases['sr'] = 'config-source -c /home/lodek/projects/purple-tree/config.py'
c.aliases['w'] = 'spawn -u /home/lodek/projects/purple-tree/save-session.sh'
config.bind('f', 'spawn -u /home/lodek/projects/purple-tree/hint.py -t {url} ;; hint links userscript /home/lodek/projects/purple-tree/hint.py', mode='normal')
config.bind('F', 'spawn -u /home/lodek/projects/purple-tree/rapid.py {url} ;; hint links userscript /home/lodek/projects/purple-tree/rapid.py', mode='normal')
config.bind('<', 'set-cmd-text -s :spawn --userscript /home/lodek/projects/purple-tree/open.py -t root ', mode='normal')
config.bind('>', 'set-cmd-text -s :spawn --userscript /home/lodek/projects/purple-tree/open.py -t {url} ', mode='normal')  
