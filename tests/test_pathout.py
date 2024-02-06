# This will work if ran from the root folder ensae-prog24

import sys
sys.path.append("swap_puzzle/")

import unittest

from grid import Grid
from graph import Graph

A = Graph.graph_from_file("input/graph1.in")
file = open("input/graph1.path.out", "r")

for i in range(20):
    for j in range(i+1, 20):
        var = (str(i+1) + " " + str(j+1) + " " + str(len(A.bfs(i+1, j+1))-1) + " " + str(A.bfs(i+1, j+1))).split()
        Y = file.readline().split()
        assert (Y == var)

print("pathout works for graph1!")

A = Graph.graph_from_file("input/graph2.in")
file = open("input/graph2.path.out", "r")

for i in range(20):
    for j in range(i+1, 20):
        if A.bfs(i+1, j+1) is None:
            var = (str(i+1) + " " + str(j+1) + " " + "None").split()
            Y = file.readline().split()
        else:
            var = (str(i+1) + " " + str(j+1) + " " + str(len(A.bfs(i+1, j+1))-1) + " " + str(A.bfs(i+1, j+1))).split()
            Y = file.readline().split()
        assert (Y == var)

print("pathout works for graph2!")
