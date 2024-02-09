from grid import Grid

class Solver(): 
    """
    A solver class, to be implemented.
    """
    def trouve_pos_init(self, A, x):
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
    
    def trouve_pos_finale(self, A, x):
        """
        Trouve la position finale du nombre dans la grille et renvoie les coordonnées de sa position finale
        """
        return ((x-1)//A.n, (x-1) % A.n)

    def convertisseur(self,X):
        """
        Transforme une liste de swap puzlles (swappables de proche en proche) en liste des swaps à effectuer
        """
        v=[]
        for i in range(len(X)-1):
            for w in range(X[0].m*X[0].n):
                a, b = self.trouve_pos_init(X[i], w+1), self.trouve_pos_init(X[i+1], w+1)
                if a != b:
                    v=v+[(a,b)]
                    break
        return(v)

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
        A.swap_seq(list(reversed(v)))
        return(v)

    def bfs_graph(self,A):
        G=A.GridGraph()
        dst=Grid(A.m,A.n)
        return(G.bfs(A,dst))

    def bfs_grid(self,A):
        dst=Grid(A.m,A.n)
        # Initialisation de la file avec le nœud source et le chemin initial contenant uniquement le nœud source
        queue = [(A, [A])]
        # Boucle principale
        while queue:
            # Retire le premier élément de la file (nœud actuel et chemin associé)
            current_node, path = queue.pop(0)
            # Vérifie si le nœud actuel est la destination:
            if current_node == dst:            
                return path # Retourne le premier chemin trouvé (le plus court)                       
                # Explore les voisins du nœud actuel:            
            for neighbor in current_node.Reachable_states():            
            # Vérifie si le voisin n'est pas déjà présent dans le chemin           
                if neighbor not in path:           
                    # Ajoute le voisin à la file avec le chemin mis à jour          
                    queue.append((neighbor, path + [neighbor]))
