from grid import Grid
from graph import Graph 
from solver import Solver

data_path = "input/"
file_name = data_path + "grid2.in"

print(file_name)

g = Grid.grid_from_file(file_name)
print(g)

print("debut")

S = Solver()
for i in S.bfs_heuristique(g, S.Heuristique_simple):
    print(i)
print("autre")
for i in S.bfs_heuristique(g, S.Heuristique_euclidienne):
    print(i)
print("autre")
for i in S.bfs_heuristique(g, S.Heuristique_naif):
    print(i)