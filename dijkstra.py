# Based on CLRS pseudocode

from graph import Graph, Vertex
import minheap

INFINITOID = 10000

def dijkstra(G, s):
	initialize_single_source(G, s)
	Q = [(G.getVertex(key).getDistance(), G.getVertex(key)) for key in G.getVertices()]
	minheap.build_max_heap(Q)

	while Q != []:
		lis = [i[1].getDistance() for i in Q]
		l = minheap.heap_extract_max(Q)
		minheap.build_max_heap(Q)
		minheap.build_max_heap(Q)
		
		
		u = l[1]
		print u.getDistance(), lis

		for key in u.getConnections():
			v = G.getVertex(key)
			relax(u, v)


		

def initialize_single_source(G, s):
	for key in G.getVertices():
		v = G.getVertex(key)
		v.setDistance(INFINITOID)
		v.setPred(None)
	s.setDistance(0)

def relax(u, v):
	w = u.getWeight(v.getId())
	if v.getDistance() > u.getDistance() + w:
		v.setPred(u)
		v.setDistance(u.getDistance() + w)
	
		

g = Graph()

s = g.addVertex("s")
t = g.addVertex("t")

y = g.addVertex("y")
z = g.addVertex("z")
x = g.addVertex("x")

s.addNeighbor(t.getId(), 10)
s.addNeighbor(y.getId(), 5)

t.addNeighbor(x.getId(), 1)
t.addNeighbor(y.getId(), 2)

x.addNeighbor(z.getId(), 4)

y.addNeighbor(t.getId(), 3)
y.addNeighbor(x.getId(), 9)
y.addNeighbor(z.getId(), 2)




dijkstra(g,s)

def path(s):
	l = []
	while s != None:
		if s != None:
			l.append((s.getId(), s.getDistance()))
		s = s.getPred()

	return l


for i in g.getVertices():
	v = g.getVertex(i)
	print v.getId(), ": ", v.getDistance(), path(v)

