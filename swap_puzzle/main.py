from grid import Grid
from graph import Graph 
from solver import Solver
import matplotlib.pyplot as plt
import time

#data_path = "input/"
#file_name = data_path + "grid2.in"

#print(file_name)

#g = Grid.grid_from_file(file_name)
#print(g)

#print("debut")

S=Solver()

A=Grid(3,3,[[9, 4, 3],[1, 8, 5],[2, 7, 6]])
print(len(S.naif(A))+1)
print(len(S.A_star(A, S.Heuristique_Manhattan)))
