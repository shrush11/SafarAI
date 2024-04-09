from queue import PriorityQueue
import random
result_array = {
    "source":{"H":22.1319024206127,"A":17.215863218382673},"A":{"F":15.253680165727571,"D":14.818664543151494,"C":15.142471021711533},"B":{"I":8.289554485554577,"A":12.068236878379405,"destination":16.605251913853277},"C":{"A":15.142471021711533,"D":0.3476409621761306},"D":{"source":4.783910320109943,"I":10.615455874064041},"E":{"B":12.081919437040984,"I":4.249029149330038,"A":0.017641429734543048},"F":{"D":0.4562008265849167,"B":4.769521418319367},"G":{"E":0.39765375146087817,"H":5.304973033675836},"H":{"B":16.983499850561287,"G":5.304973033675836,"I":9.233269950506596},"I":{"D":10.615455874064041,"F":11.05628400693568},"destination":{"E":4.879078993528801,"D":19.64688769514562,"B":16.605251913853277}}


def convert_dict_to_2d_array(data_dict):
    # Get all unique keys from the dictionary
    all_keys = list(data_dict.keys())
    # Initialize a 2D array with zeros
    num_rows = len(all_keys)
    num_cols = len(all_keys)
    result = [[0.0] * num_cols for _ in range(num_rows)]
    for i in range(1,num_rows-1):
        result[0][i]=all_keys[i]
        result[i][0]=all_keys[i]
    # Fill in the values from the dictionary
    for i, row_key in enumerate(all_keys):
        for j, col_key in enumerate(all_keys):
            if i == 0 and j == 0:
                # Leave the (0,0) position as zero
                continue
            elif i == 0:
                # Fill the first row with keys (excluding 0,0)
                result[i][j] = col_key
            elif j == 0:
                # Fill the first column with keys (excluding 0,0)
                result[i][j] = row_key
            else:
                # Fill other positions with corresponding values
                result[i][j] = data_dict.get(row_key, {}).get(col_key, 0.0)
    
    return result
k="Z"
v=0
data={k:v,**result_array}
# Convert the dictionary to a 2D array
result_arrays = convert_dict_to_2d_array(data)

# Print the result
for row in result_arrays:
    print(row)
print(type(result_arrays))
############################A*starts here###########################
class Node:
    def __init__(self, idx, pCost, h):
        self.index = idx
        self.pathCost = pCost  # Path cost from start node
        self.heuristicCost = h  # Heuristic cost for A* search

    def __lt__(self, other):
        # A* priority function, f(n) = g(n) + h(n)
        return (self.pathCost + self.heuristicCost) < (other.pathCost + other.heuristicCost)

class Graph:
    def __init__(self):
        self.adjacent = [[(-1, INF)] * MAX_NODES for _ in range(MAX_NODES)]  # Stores adjacent nodes and costs
        self.numNodes = 0
        self.nodeNames = [''] * MAX_NODES
        self.heuristicCosts = [0] * MAX_NODES

def aStar(graph, startNode, goalNode):
    parent = [-1] * MAX_NODES  # Store parent node of each node
    dist = [INF] * MAX_NODES  # Store distance from start node
    visited = [False] * MAX_NODES  # Visited array
    pq = PriorityQueue()

    startIndex = -1
    goalIndex = -1
    for i in range(graph.numNodes):
        if graph.nodeNames[i] == startNode:
            startIndex = i
        if graph.nodeNames[i] == goalNode:
            goalIndex = i
        if startIndex != -1 and goalIndex != -1:
            break

    if startIndex != -1 and goalIndex != -1:
        pq.put(Node(startIndex, 0, graph.heuristicCosts[startIndex]))
        dist[startIndex] = 0

        while not pq.empty():
            current = pq.get()
            currentNode = current.index

            if currentNode == goalIndex:
                # Path found, backtrack to get the shortest path
                print("\nA* Search Path from", startNode, "to", goalNode, ":")
                path = ""
                pathCost = dist[currentNode]
                while currentNode != startIndex:
                    path = " -> " + graph.nodeNames[currentNode] + path
                    currentNode = parent[currentNode]
                path = startNode + path
                print(path, "\nPath Cost:", pathCost)
                return

            if not visited[currentNode]:
                visited[currentNode] = True
                for j in range(graph.numNodes):
                    if graph.adjacent[currentNode][j][0] != -1:  # Check if adjacency exists
                        nextNode = graph.adjacent[currentNode][j][0]
                        edgeCost = graph.adjacent[currentNode][j][1]
                        if not visited[nextNode]:
                            parent[nextNode] = currentNode
                            dist[nextNode] = dist[currentNode] + edgeCost
                            pq.put(Node(nextNode, dist[nextNode], graph.heuristicCosts[nextNode]))
    print("Goal node cannot be reached from the start node.")
    return
MAX_NODES = 100
INF = 10**9  # Infinity value for initial distances
heuristicCosts=[random.randint(1, 10) for _ in range(11)]
print("Heuristic cost is",heuristicCosts)
start_node = "source"
goal_node = "destination"
aStar(result_arrays, start_node, goal_node)