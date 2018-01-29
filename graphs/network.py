#!/home/lodek/.virtualenvs/graph/bin/python
import mpld3
import matplotlib.pyplot as plt
from mpld3 import plugins
import sqlalchemy


class Node():
    def __init__(x,y,title,url,depth,children,date,note):
        hello = ok
tree = read_db()

#tree = {0: root, 1:[], 2:[]...}



    
        

fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')

y = [10 for x in range(10)]
x = [x*(2*3.14/10) for x in range(10)]

points = ax.scatter(x,y)
labels = ["Point {0}".format(i) for i in range(40)]
tooltip = plugins.PointLabelTooltip(points, labels)
plugins.connect(fig, tooltip)

