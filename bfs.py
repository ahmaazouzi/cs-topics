# Can be used for udacity  cs101 path problem

from graph import Graph, Vertex
from queue import Queue

def bfs(start):
	start.setDistance(0)
	start.setPred(None)
	vertQueue = Queue()
	vertQueue.enqueue(start)
	while (vertQueue.size() > 0):
		currentVert = vertQueue.dequeue()
		for nbr in currentVert.getConnections():
			if (nbr.getColor() == 'white'):
				nbr.setColor('gray')
				nbr.setDistance(currentVert.getDistance() + 1)
				nbr.setPred(currentVert)
				vertQueue.enqueue(nbr)
		currentVert.setColor('black')

d = Graph()
v = d.addVertex(44)
print v.getColor()
bfs(v)
print v.getColor()

