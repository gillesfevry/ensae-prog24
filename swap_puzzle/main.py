from grid import Grid
from graph import Graph 
from solver import Solver
import matplotlib.pyplot as plt

#data_path = "input/"
#file_name = data_path + "grid2.in"

#print(file_name)

#g = Grid.grid_from_file(file_name)
#print(g)

#print("debut")

S=Solver()
A=Grid(3,3)
A.Shuffle()

print(len(S.bfs_heuristique(A, S.Heuristique_euclidienne)))
print(len(S.A_star(A,S.Heuristique_euclidienne)))
