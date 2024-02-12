# This will work if ran from the root folder ensae-prog24
# Ce test vise à vérifier sur un exemple que la technique du TD2 fonctionne bien

import sys 
sys.path.append("swap_puzzle/")

import random
import math

from grid import Grid
from graph import Graph
from solver import Solver

S=Solver()

A=Grid(2,3,[[2,5,4],[1,3,6]])
print(A)

print("La méthode naive donne:")
print(S.naif(A))
A.swap_seq(S.naif(A))
assert(A.is_sorted())

A=Grid(2,3,[[2,5,4],[1,3,6]])
print("La méthode bfs en construisant entièrement le graphe donne")
print(S.convertisseur(S.bfs_graph(A)))
A.swap_seq(S.convertisseur(S.bfs_graph(A)))
assert(A.is_sorted())

A=Grid(2,3,[[2,5,4],[1,3,6]])
print("La méthode bfs en construisant progressivement le graphe donne:")
print(S.convertisseur(S.bfs_grid(A)))
A.swap_seq(S.convertisseur(S.bfs_grid(A)))
assert(A.is_sorted())
