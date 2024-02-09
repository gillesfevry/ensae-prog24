from grid import Grid
from graph import Graph 

g = Grid(2, 3)
print(g)

#data_path = "../input/"
#file_name = data_path + "grid0.in"

#print(file_name)

#g = Grid.grid_from_file(file_name)
#print(g)

print("debut test")

B=Grid(2,4,[[5,6,7,8],[1,2,3,4]])
for i in B.bfs_grid():
    print(i)