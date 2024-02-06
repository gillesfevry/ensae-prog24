# This will work if ran from the root folder ensae-prog24
# Ce test vise à vérifier sur un exemple que la technique du TD2 fonctionne bien

import sys 
sys.path.append("swap_puzzle/")

import random
import math

from grid import Grid
from graph import Graph
from solver import Solver

A=Grid(2,3)
States=A.other_states()
rand=random.randint(0,math.factorial(A.n * A.m)-1)

G=A.GridGraph()
Steps=G.bfs(States[rand],A)

print("On part de:", States[rand])
print("la méthode bfs donne:")

for i in range(len(Steps)):
    print (Steps[i])

print("elle le fait en :",len(Steps)-1, "étapes")
print("la méthode naive donne:")
C=Solver()
D=C.naif(States[rand])
print(D)
print("elle le fait en :",len(D), "étapes")