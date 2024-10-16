# Uncomment if encounter problems with openpyxl
# import pip
# pip.main(["install", "openpyxl"])

import numpy as np
import pandas as pd

from Graph import Graph

def main(filename, sheet_name):

    data = pd.read_excel(filename, sheet_name=sheet_name, header=None)
    num_of_levels = int(data.iloc[0][0])
    assert num_of_levels > 2    # Less than 2 levels cannot exist

    level_node_number = data.iloc[1]
    weights = data.iloc[2:]

    # Initialize the Graph with the number of Vertices
    graph = Graph(int(level_node_number.values.sum()))

    # Set the appropriate value of weight in each edge
    counter = 0
    
    graph.add_edge(counter, 1, weight=int(weights.iloc[counter][0]))
    graph.add_edge(counter, 2, weight=int(weights.iloc[counter][1]))
    
    for i in range(0, 2):
        counter = counter + 1

        graph.add_edge(counter, 3, weight=int(weights.iloc[counter][0]))
        graph.add_edge(counter, 4, weight=int(weights.iloc[counter][1]))
        graph.add_edge(counter, 5, weight=int(weights.iloc[counter][2]))

    for i in range(0, 3):
        counter = counter + 1
        graph.add_edge(counter, 6, weight=int(weights.iloc[counter][0]))
        graph.add_edge(counter, 7, weight=int(weights.iloc[counter][1]))
        graph.add_edge(counter, 8, weight=int(weights.iloc[counter][2]))
        graph.add_edge(counter, 9, weight=int(weights.iloc[counter][3]))

    for i in range(0, 4):
        counter = counter + 1

        graph.add_edge(counter, 10, weight=int(weights.iloc[counter][0]))
        graph.add_edge(counter, 11, weight=int(weights.iloc[counter][1]))
        graph.add_edge(counter, 12, weight=int(weights.iloc[counter][2]))

    for i in range(0, 3):
        counter = counter + 1

        graph.add_edge(counter, 13, weight=int(weights.iloc[counter][0]))
        graph.add_edge(counter, 14, weight=int(weights.iloc[counter][1]))

    for i in range(0, 2):
        counter = counter + 1

        graph.add_edge(counter, 15, weight=int(weights.iloc[counter][0]))
        
    # Initialize the necessary variables to use the Dynamic Programming approach
    count = int(sum(level_node_number))-1
    best_cost = np.full(int(sum(level_node_number)), np.inf)
    best_choice = np.zeros(int(sum(level_node_number)))

    for i in range(0, num_of_levels):
        # Reverse the number of nodes for each level. Because we will go backwards
        for j in range(0, int(level_node_number[num_of_levels-i-1])):
            tmp = g.graph.get(count)
            if tmp is not None:
                # Initial value infinity because we need the smallest cost route
                node_best_cost = np.inf
                # Check the best value moving from this node
                for k in range(0, int(level_node_number[num_of_levels-i])):
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
    best_route = np.zeros(num_of_levels)
    current_node = 0
    for i in range(0, num_of_levels):
        next_node = int(best_choice[current_node])
        best_route[i] = current_node
        current_node = next_node

    print("These are the best choices for each node to follow in the graph \n", best_choice)
    print("This is the best route to follow from A to B \n", best_route, "\n and the cost of this route is ", best_cost[0])


if __name__ == '__main__':
    main(filename="data.xlsx", sheet_name="Sheet1")