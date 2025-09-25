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

    counter = -1
    total_nodes = 1

    # for each level, except the last one
    for k in range(0, level_node_number.size-1):
        # For each node in the level
        for i in range(0, int(level_node_number[k])):
            counter = counter + 1
            # Add a new node and connect it to the ones in the new level with the appropriate weight 
            for j in range(0, int(level_node_number[k+1])):
                graph.add_edge(counter, j+total_nodes, weight=int(weights.iloc[counter][j]))
        total_nodes = total_nodes + int(level_node_number[k+1])

    # Initialize the necessary variables to use the Dynamic Programming approach
    count = int(sum(level_node_number))-1
    best_cost = np.full(int(sum(level_node_number)), np.inf)
    best_choice = np.zeros(int(sum(level_node_number)))

    for i in range(0, num_of_levels):
        # Reverse the number of nodes for each level. Because we will go backwards
        for j in range(0, int(level_node_number[num_of_levels-i-1])):
            tmp = graph.node_adjaceny_list.get(count)
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