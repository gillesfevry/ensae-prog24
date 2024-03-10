from solver import Solver 
from grid import Grid  

import matplotlib.pyplot as plt
import numpy as np

S=Solver()
A=Grid(3,3)
x=[]
y=[]
z=[]
t=[]

for i in range(100):
    print(i,"%")
    A.Shuffle()
    t = t + [len(S.A_star(A, S.Heuristique_Manhattan))]
    y = y + [len(S.naif(A))+1]
    z = z + [len(S.compromis(A, S.Heuristique_Manhattan))]
    x = x + [S.Heuristique_Manhattan(A)]

pente, intercept = np.polyfit(x, y, 1)
plt.plot(x, pente*np.array(x) + intercept, color='blue')
plt.scatter(x, y, color='blue')
plt.text(min(x), min(y)+1, 'naif', verticalalignment='bottom', horizontalalignment='right', color='blue')
plt.text(max(x), int(pente*100)/100 * max(x) + int(intercept*100)/100, f'y={int(pente*100)/100} x + {int(intercept*100)/100}', verticalalignment='bottom', horizontalalignment='right', color='blue')

pente, intercept = np.polyfit(x, z, 1)
plt.plot(x, pente*np.array(x) + intercept, color='red')
plt.scatter(x, z, color='red')
plt.text(min(x), min(z), 'compromis', verticalalignment='bottom', horizontalalignment='right', color='red')
plt.text(max(x), int(pente*100)/100 * max(x) + int(intercept*100)/100 , f'y={int(pente*100)/100} x + {int(intercept*100)/100}', verticalalignment='bottom', horizontalalignment='right', color='red')

pente, intercept = np.polyfit(x, t, 1)
plt.plot(x, pente*np.array(x) + intercept, color='green')
plt.scatter(x, t, color='green')
plt.text(min(x), min(t)-1, 'A_star', verticalalignment='bottom', horizontalalignment='right', color='green')
plt.text(max(x), int(pente*100)/100 * max(x) + int(intercept*100)/100 , f'y={int(pente*100)/100} x + {int(intercept*100)/100}', verticalalignment='bottom', horizontalalignment='right', color='green')

plt.plot(x, x, color='black')
plt.text(min(x)+1, min(x), 'A*', verticalalignment='bottom', horizontalalignment='right', color='black')
plt.text(max(x), max(x)-1, f'y=x', verticalalignment='bottom', horizontalalignment='right', color='black')

plt.title("Comparaison de différents algorithmes pour 100 grilles 3x3:")
plt.xlabel('Heuristique de Manhattan')
plt.ylabel('Cout des algorithmes')

plt.show()