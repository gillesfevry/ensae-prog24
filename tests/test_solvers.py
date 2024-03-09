# This will work if ran from the root folder ensae-prog24
# Ce test vise à vérifier sur un exemple que la technique du TD2 fonctionne bien

import sys 
import time
sys.path.append("swap_puzzle/")

import random
import math

from grid import Grid
from graph import Graph
from solver import Solver

S=Solver()

A=Grid(2,3,[[2,5,4],[1,3,6]])
print(A)

start = time.time()

print("The naive method gives:")
print(S.naif(A))
A.swap_seq(S.naif(A))
assert(A.is_sorted())

end=time.time()

print("it took", 100*(end - start),"milliseconds")
print(" ")

A=Grid(2,3,[[2,5,4],[1,3,6]])

start = time.time()

print("The bfs method creating the entire graph gives:")
print(S.convertisseur(S.bfs_graph(A)))
A.swap_seq(S.convertisseur(S.bfs_graph(A)))
assert(A.is_sorted())

end=time.time()

print("it took", 100*(end - start),"milliseconds")
print(" ")

A=Grid(2,3,[[2,5,4],[1,3,6]])

start = time.time()

print("The bfs method building progressively the graph gives:")
print(S.convertisseur(S.bfs_grid(A)))
A.swap_seq(S.convertisseur(S.bfs_grid(A)))
assert(A.is_sorted())
end=time.time()

print("it took", 100*(end - start),"milliseconds")
print(" ")

A=Grid(2,3,[[2,5,4],[1,3,6]])

start = time.time()

print("The A* method using the euclidian heuristic gives")
print(S.convertisseur(S.bfs_heuristique(A, S.Heuristique_euclidienne)))
A.swap_seq(S.convertisseur(S.bfs_heuristique(A, S.Heuristique_euclidienne)))
assert(A.is_sorted())
end=time.time()

print("it took", 100*(end - start),"milliseconds")
print(" ")

A=Grid(2,3,[[2,5,4],[1,3,6]])

start = time.time()

print("The A* method using the naif heuristic gives")
print(S.convertisseur(S.bfs_heuristique(A, S.Heuristique_naif)))
A.swap_seq(S.convertisseur(S.bfs_heuristique(A, S.Heuristique_naif)))
assert(A.is_sorted())
end=time.time()

print("it took", 100*(end - start),"milliseconds")
print(" ")

A=Grid(2,3,[[2,5,4],[1,3,6]])

start = time.time()

print("The A* method using the simple heuristic gives")
print(S.convertisseur(S.bfs_heuristique(A, S.Heuristique_simple)))
A.swap_seq(S.convertisseur(S.bfs_heuristique(A, S.Heuristique_simple)))
assert(A.is_sorted())
end=time.time()

print("it took", 100*(end - start),"milliseconds")
print(" ")