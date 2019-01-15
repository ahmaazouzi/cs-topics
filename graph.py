# Based heavily on Miller and Ranum's "Problem Solving with Algorithms and Data Structures"

# 1. Informally, a graphy is a set of nodes (vertices) connected by edges. Edges can have weights.
# 2. A graph can be represented by G = (V, E) where Graph V is a set of graph G's vertices,
# and E is a set of eges.
# 3. V={a, b, c} is a set of vertices of a graph. Each element in the set is a vertex (node).
# 4. Edges are tuples (v,w) that contain at least two vertices and in case of a weighted graph the tuple
# also contains the weight of the edge as in (v3,v5,3) where 3 is the weight. a set of vertices can be represented
# as E={(v0,v1,5),(v1,v2,4),(v2,v3,9)}.
# 5. A graph can be directed (also called a diagraph) whre edges are one way. Undirected graph edges are two way.
# 6. "A path in a graph is a sequence of vertices that are connected by edges." The path length between two vertices 
# is the number of edges separating them in an unwehighted graph. It's the sum of edge weights in a weighted graph. 
# 7. "A cycle in a directed graph is a path that starts and ends at the same vertex."
# 8. A graph is usually implemented as an adjacency matrix or adjacency list. When two vertices are connected by an 
# edge they are adjacent. 
# 9. An adjacency list is a list of vertices and lists of other vertices each vertex is connected to 
# (along with weights if applicable). A list is more space efficient that a matrix considering that most graphs are sparse.
# A sparse graph have few connections.

class Vertex:
	def __init__(self, key):
		self.id = key
		self.connectedTo = {}

	def addNeighbor(self, nbr, weight = 0):
		self.connectedTo[nbr] = weight

	def __str__(self):
		return str(self.id) + " connectedTo: " + str([x.id for x in self.connectedTo.keys()])

	def getConnections(self):
		return self.connectedTo.keys()

	def getId(self):
		return self.id

	def getWeight(self, nbr):
		return self.connectedTo[nbr]

class Graph:
	def __init__(self):
		self.vertList = {}
		self.numVertices = 0

	def addVertex(self, key):
		self.numVertices = self.numVertices + 1
		newVertex = Vertex(key)
		self.vertList[key] = newVertex
		return newVertex

	def getVertex(self, n):
		if n in self.vertList:
			return self.vertList[n]
		else:
			return None

	def __contains__(self, n):
		return n in self.vertList

	def addEdge(self, f, t, cost = 0):
		if f not in self.vertList:
			nv = self.addVertex(f) # You are not using nv anywhere.
		if t not in self.vertList:
			nv = self.addVertex(t)
		self.vertList[f].addNeighbor(self.vertList[t], cost)

	def getVertices(self):
		return self.vertList.keys()

	def __iter__(self):
		return iter(self.vertList.values())