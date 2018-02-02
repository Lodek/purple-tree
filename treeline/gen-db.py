#!/usr/bin/env python
"""
this script is responsible for reading the txt db file and parsing it and transforming it into a sqlite3 file, it uses sqlalchemy to do so.
it also reads the favorites files (which signalizes that the souce code of that page should also be saved

finally is generates tree.html and tree.org. 
this script should be called by the save-session,sh script
"""

Value = collections.namedtuple('Value', 'parent child date')


def check_db():
    """ checks if db exists. If it does not, creates it  and adds root """
    #make db dir
    if not os.path.exists(sys.argv[1]+'/treeline/'):
    os.makedirs(sys.argv[1]+'/treeline/')
    if not os.path.isfile(_dbf)):
        Base.metadata.create_all(engine)
        session.add(Node(title='root',url='root'))
        session.commit()
    return


def read_trunkf():
    """ reads the txt db file and parses it """
    with open(_trunkf, 'r') as tf:
        trunk = []
        for line in tf.readlines():
            visit = line.strip('\n').split(' ;; ')
            trunk.append(Value(parent=visit[0], child=visit[1]), date=visit[2])
    return trunk


def add_node(visit):
    """ Expects an object of type visit (named tuple). Returns the node object for the matching child of the visit """
    node = get_node(visit.child)
    if node.date == '':
        node.date = visit.date
    parent = get_node(visit.parent)
    if parent not in node.parents:
        node.parents.append(parent)
    session.add(node)
    return node


def mark_favorites():
    with open(favoritef, 'r') as ff:
        favorites = [fav.strip('\n') for fav in ff.readlines()]
    for favorite in favorites:
        node = get_node(favorite)
        node.favorite = True

        
def mark_session():
    return

    
def get_node(url):
    """ queries DB for Node with the given url if not existent creates it"""
    node = session.query(Node).filter(Node.url==url).first()
    if node is None:
        node = Node(url=url, title=get_title(url))
    return node


def get_title(url):
    """ From URL returns title (if it exists, else it returns the url) """
    try:
        obj=requests.get(url)
        title=re.findall('<title>(.*?)<\/title>',obj.text)[0]
    except BaseException:
        title=url
    return title

def main():
    
    check_db()
    
    hist = read_trunkf()
    for visit in hist:
        add_node(visit)
    mark_favorites()
    mark_session()
    session.commit()
    
if __name__ == '__main__':
    main()
