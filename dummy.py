from graph import Graph, Vertex
from queue import Queue

def bfs(s):
	s.setColor("white")
	s.setPred(0)
	vertQ = Queue()
	vertQ.enqueue(s)


d = Graph()
v = d.addVertex(44)
print v.getColor()
bfs(v)
print v.getColor()