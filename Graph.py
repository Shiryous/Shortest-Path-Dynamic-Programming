from collections import defaultdict

# Graph is represented using adjacency list. Every
# node of adjacency list contains vertex number of
# the vertex to which edge connects. It also contains
# weight of the edge

class Graph:

    def __init__(self, vertices):
        self.vertice_number = vertices 
        self.graph_adjaceny_list = defaultdict(list)

    # Adds new edge with weight on top of this node
    def add_edge(self, u, v, weight):
        self.graph_adjaceny_list[u].append((v, weight))
