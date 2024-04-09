from flask import Flask, request, render_template
from queue import PriorityQueue
import random
import json

import heapq
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Safar.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    print("connected")
    data = request.form['graphs']
    print(data)
    print(type(data))
    result=main(data)
    print(result)
    return render_template('result.html',result=result)
MAX_NODES = 100
INF = 10**9  # Infinity value for initial distances
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
        self.adjacent = [[] for _ in range(MAX_NODES)]  # Stores adjacent nodes and costs
        self.numNodes = 0
        self.nodeNames = [''] * MAX_NODES
        self.heuristicCosts = [0] * MAX_NODES

    def inputGraph(self):
        self.numNodes = int(input("Enter the number of nodes: "))
        print("Enter the names and heuristic costs of nodes:")
        for i in range(self.numNodes):
            self.nodeNames[i], self.heuristicCosts[i] = input().split()

        for i in range(self.numNodes):
            numAdjacent = int(input(f"Enter the number of adjacent nodes for {self.nodeNames[i]}: "))
            print(f"Enter the names and costs of adjacent nodes for {self.nodeNames[i]}:")
            for _ in range(numAdjacent):
                adjNode, cost = input().split()
                adjNodeIndex = self.nodeNames.index(adjNode)
                self.adjacent[i].append((adjNodeIndex, int(cost)))


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
        pq.put(Node(startIndex, 0, int(graph.heuristicCosts[startIndex])))
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
                print(path, "Distance Between Source and Destination is:", pathCost,"Kms")
                mymodeoftransport=mode_of_transport(path,pathCost)
                return mymodeoftransport
            if not visited[currentNode]:
             visited[currentNode] = True
             for j in range(len(graph.adjacent[currentNode])):  
              if graph.adjacent[currentNode][j][0] != -1: 
                nextNode = graph.adjacent[currentNode][j][0]
                edgeCost = graph.adjacent[currentNode][j][1]
                if not visited[nextNode]:
                  parent[nextNode] = currentNode
                  dist[nextNode] = dist[currentNode] + edgeCost
                  pq.put(Node(nextNode, dist[nextNode], int(graph.heuristicCosts[nextNode])))

    print("Goal node cannot be reached from the start node.")
    return
def mode_of_transport(path, distance):
    transport_options = {
        "Rental/Private Car": {
            "Sedan": 13 * distance,
            "SUV": 35 * distance
        },
        "Auto": 23 + (15.33 * distance),
        "Bus": {
            "Non Ac": 8 * distance,
            "Ac": 12 * distance
        }
    }
    
    mymode = {
        "path": path,
        "distance": distance,
        "transport_options": transport_options
    }
    return mymode

def main(data):
    graph = Graph()

    # Manually define the graph structure
    graph.numNodes =  11 # Example: Assuming there are 5 nodes in the graph

    # Manually set node names and heuristic costs
    graph.nodeNames = ["source","A", "B", "C", "D", "E","F","G","H","I","destination"]
    graph.heuristicCosts = [8,5,4,3,7,12,5, 3, 2, 4, 1]  # Example heuristic costs

    ## Convert input code 
    # The input string

    # Convert the string to a dictionary
    input_dict = json.loads(data)
    # Create a list of node names
    node_names = list(input_dict.keys())
    # Initialize the adjacency list
    adjacent = [[] for _ in range(len(node_names))]
    # Fill the adjacency list
    for node, neighbors in input_dict.items():
        node_index = node_names.index(node)
        for neighbor, cost in neighbors.items():
            neighbor_index = node_names.index(neighbor)
            adjacent[node_index].append((neighbor_index, cost))
    graph.adjacent = adjacent
    for i in range(len(node_names)):
        print(f"Node {node_names[i]}:")
        for j in range(len(adjacent[i])):
            print(f"Adjacent node: node {node_names[adjacent[i][j][0]]} with cost {adjacent[i][j][1]}")
    startNode = "source"  # Example: Starting node
    goalNode = "destination"   # Example: Goal node
    result=aStar(graph, startNode, goalNode)
    return result


if __name__ == "__main__":
    app.run(debug=True)


