# This is a sample Python script.
import numpy as np
import pandas as pd
from collections import defaultdict


# Graph is represented using adjacency list. Every
# node of adjacency list contains vertex number of
# the vertex to which edge connects. It also contains
# weight of the edge
class Graph:
    def __init__(self, vertices):
        self.V = vertices  # No. of vertices

        # dictionary containing adjacency List
        self.graph = defaultdict(list)

    # function to add an edge to graph
    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))


# Using this function to import data from an excel sheet.
def import_data(vari):
    ws = pd.read_excel(vari)
    r = np.array(ws)
    return r


if __name__ == '__main__':
    filename = input("Enter the name of the excel you want to read from: ")
    data = import_data(filename)
    levelNum = int(data[0][0])  # Number of levels
    levelNodes = data[1][:]  # Number of nodes for each level
    weights = data[2:][:]

    # Initialize the Graph with the number of Vertices
    g = Graph(int(sum(levelNodes)))
    # Set the appropriate value of weight in each edge
    counter = 0

    for i in range(0, levelNum-1):
        for j in range(0, int(levelNodes[i])):
            print("Node", counter)
            for k in range(0, int(levelNodes[i+1])):
                g.add_edge(counter, int(sum(levelNodes[0:i+1])) + k, weights[counter][k])
                print(counter, "---",  weights[counter][k], "-->", int(sum(levelNodes[0:i+1])+k))
            counter = counter + 1
            print("------------------------")

    # Initialize the necessary variables to use the Dynamic Programming approach
    count = int(sum(levelNodes))-1
    best_cost = np.full(int(sum(levelNodes)), np.inf)
    best_choice = np.zeros(int(sum(levelNodes)))

    for i in range(0, levelNum):
        # Reverse the number of nodes for each level. Because we will go backwards
        for j in range(0, int(levelNodes[levelNum-i-1])):
            tmp = g.graph.get(count)
            if tmp is not None:
                # Initial value infinity because we need the smallest cost route
                node_best_cost = np.inf
                # Check the best value moving from this node
                for k in range(0, int(levelNodes[levelNum-i])):
                    # This removes the routes that are represented with -1, because there is no connection
                    if tmp[k][1] > 0:
                        node_best_cost = tmp[k][1] + best_cost[tmp[k][0]]
                        # Replace the best cost for this node if the new best cost is smaller than the general best cost
                        if node_best_cost < best_cost[count]:
                            best_choice[count] = tmp[k][0]
                            best_cost[count] = node_best_cost
            else:  # This means that the node has no children, using the examples, only the last node has it
                # Initialize the distance to 0, because the distance from the goal is 0
                best_cost[count] = 0
            count = count - 1

    # Calculate the best route using the best choice array we generated above, moving from the current node to its best.
    best_route = np.zeros(levelNum)
    current_node = 0
    for i in range(0, levelNum):
        next_node = int(best_choice[current_node])
        best_route[i] = current_node
        current_node = next_node

    print("These are the best choices for each node to follow in the graph \n", best_choice)
    print("This is the best route to follow from A to B \n", best_route, "\n and the cost of this route is ", best_cost[0])
