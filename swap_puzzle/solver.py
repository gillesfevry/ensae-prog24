from grid import Grid

class Solver(): 
    """
    A solver class, to be implemented.
    """
    def trouve_pos_init(self, A,x):
        """
        Trouve le nombre dans la grille et renvoie sa position
        """
        i0, j0 =None,None
        for i in range(A.m):
            if x in A.state[i]:
                j0 = A.state[i].index(x)
                i0=i
                break
        return (i0,j0)
    
    def trouve_pos_finale(self, A,x):
        """
        Trouve la position finale du nombre dans la grille et renvoie les coordonnées de sa position finale
        """
        return ((x-1)//A.n, (x-1) % A.n)

    def naif(self, A):
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        v=[]
        for i in range(A.m * A.n):
            u=[]
            deb=self.trouve_pos_init(A,i+1)
            fin=self.trouve_pos_finale(A,i+1)
            if fin[1] > deb[1]:
                for k in range(fin[1]-deb[1]):
                    u=u+[((deb[0], deb[1]+k), (deb[0], deb[1]+k+1))]
            elif fin[1] < deb[1]:
                for k in range (deb[1]-fin[1]):
                    u=u+[((deb[0],deb[1]-k),(deb[0], deb[1]-k-1))]
            if fin[0] < deb [0]:
                for k in range (deb[0] - fin[0]):
                    u=u+[((deb[0] - k, fin[1]), (deb[0]-k-1, fin[1]))]
            A.swap_seq(u)
            v=v+u
        return(v)
