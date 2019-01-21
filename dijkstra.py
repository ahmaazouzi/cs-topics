# Based on CLRS pseudocode

INFINITOID = 1000

def dijkstra(G, w, s):
	initialize_single_source(G, s)
	A = empty
	Q = G.V
	while Q not empty:
		u = extractMin(Q)
		S = S U {u}
		for v in G.V:
			relax(u, v ,w)

def initialize_single_source(G, s):
	for v in G.V:
		v.d = INFINITOID
		v.pi = None
	s.d = 0

def relax(u, v, weight):
	if v.d > u.d + w(u, v):
		v.d = ud + w(u, v)
		v.pi = ud

