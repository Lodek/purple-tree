c.backend = 'webkit'
root_dir = '/root/tree'
c.content.geolocation = 'ask'
config.load_autoconfig()

config.bind('<', 'spawn -u /home/lodek/projects/purple-tree/hint.py -t {url} ;; hint links userscript /home/lodek/projects/purple-tree/hint.py', mode='normal')
config.bind('<', 'spawn -u /home/lodek/projects/purple-tree/rapid.py {url} ;; hint links userscript /home/lodek/projects/purple-tree/rapid.py', mode='normal')
config.bind('<', 'set-cmd-text -s :spawn --userscript /home/lodek/projects/purple-tree/open.py -t {url} ', mode='normal')  
