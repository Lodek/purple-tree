c.backend = 'webkit'
root_dir = '/root/tree'
c.content.geolocation = 'ask'
config.load_autoconfig()
config.bind('[', 'set-cmd-text -s :spawn --userscript /root/tree/purple_tree.py open -t {url} ', mode='normal')
config.bind('|', 'set-cmd-text -s :spawn --userscript /root/tree/purple_tree.py open -t root ', mode='normal')  
config.bind('{', 'spawn -u /root/tree/echoer.sh hint -b ;; hint links userscript /root/tree/purple_tree.py', mode='normal')
config.bind('<', 'spawn -u /root/tree/echoer.sh rapid ;; hint links userscript /root/tree/purple_tree.py', mode='normal')

