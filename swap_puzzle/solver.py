from grid import Grid
import heapq

class Solver():
    """
    A class that helps solving puzzles.
    """
    def trouve_pos_init(self, A, x):
        """
        Finds one number in the grid and return its position

        Parameters:
        -----------
        (A,x) where A is a grid from the Grid class and x is the number to look for.

        Output:
        -----------
        (i0,j0), the position of the number in the grid
        """
        i0, j0 = None, None
        for i in range(A.m):
            for j in range(A.n):
                if x == A.state[i][j]:
                    i0,j0=i,j
                    break
        return (i0, j0)

    def trouve_pos_finale(self, A, x):
        """
        Finds the final position of a number in the grid

        Parameters:
        -----------
        (A,x) where A is a grid from the Grid class and x is the number to look for.

        Output:
        -----------
        (i0,j0), the final position of the number in the grid
        """
        assert (0 < x <= A.n * A.m)
        return ((x-1)//A.n, (x-1) % A.n)

    def convertisseur(self, X):
        """
        Transforms a list of swap puzzles in a lists of swaps.

        Parameter:
        -----------
        X = [X1, X2...], a list of grids of the same size
        where Xi can be swapped with Xi+1 in one single swap

        Output:
        -----------
        returns the sequence of swaps at the format
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """
        v = []
        for i in range(len(X)-1):
            for w in range(X[0].m*X[0].n):
                a, b = self.trouve_pos_init(X[i], w+1), self.trouve_pos_init(X[i+1], w+1)
                if a != b:
                    v = v + [(a, b)]
                    break
        return (v)

    def naif(self, A):
        """
        Solves a grid and returns a sequence of swaps. Grid is then set back to it's original state.

        Parameter:
        -----------
        A, a Grid.

        Output:
        -----------
        returns the sequence of swaps at the format
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """
        v = []
        # for every number in the grid...
        for i in range(A.m * A.n):
            u = []
            # we find it's  current and final position
            deb = self.trouve_pos_init(A, i + 1)
            fin = self.trouve_pos_finale(A, i + 1)
            # we find the sequence of horizontal swaps, not disrupting what has already been done
            if fin[1] > deb[1]:
                for k in range(fin[1]-deb[1]):
                    u = u + [((deb[0], deb[1] + k), (deb[0], deb[1] + k + 1))]
            elif fin[1] < deb[1]:
                for k in range(deb[1]-fin[1]):
                    u = u + [((deb[0], deb[1]-k), (deb[0], deb[1] - k - 1))]
            # then the sequence of horizontal swaps
            if fin[0] < deb[0]:
                for k in range(deb[0] - fin[0]):
                    u = u+[((deb[0] - k, fin[1]), (deb[0] - k - 1, fin[1]))]
            # we apply the sequence of horizontal and vertical swaps
            A.swap_seq(u)
            # we register those swaps
            v = v + u
            # we return the grid to its original state
        A.swap_seq(list(reversed(v)))
        return (v)

    def bfs_graph(self, A):
        """
        Solves a grid, by creating the graph of all it's possible sates and applying bfs to it

        Parameter:
        -----------
        A, a Grid.

        Output:
        -----------
        path: list[Grid] | None
            The shortest path from src to dst. Returns None if dst is not reachable from src
        """
        G = A.GridGraph()
        dst = Grid(A.m, A.n)
        return (G.bfs(A, dst))

    def bfs_grid(self, A):
        """
        Solves a grid, by applying bfs to a graph that is progressively built.

        Parameter:
        -----------
        A, a Grid.

        Output:
        -----------
        path: list[Grid] | None
            The shortest path from src to dst. Returns None if dst is not reachable from src
        """
        dst = Grid(A.m, A.n)
        # initiates the queue with the source node and the initial path(only the first node).
        queue = [(A, [A])]
        visited = []
        while queue:
            # Deletes the first element of the queue (node and associated path)
            current_node, path = queue.pop(0)
            # Checks if the node is the final destination:
            if current_node == dst:
                return path
                # Returns the first path found (which is the shortest)
                # Explore all neighbor nodes
            for neighbor in current_node.Reachable_states():
                # Checks if the neighbor is not already in the path
                if neighbor not in visited:
                    # Adds the neighbor to the queue with the actualized path
                    queue.append((neighbor, path + [neighbor]))
            visited= visited + [current_node]

    def Heuristique_Manhattan(self, A):
        """
        A heuristic defined by the sum of every number's Manhattan distance to its final position plus the grid's existing cost

        Parameter:
        -----------
        A, a Grid
        or
        (A, something), where A is a Grid

        Output:
        -----------
        int
        """
        H = 0
        if type(A) is tuple:
            for i in range(A[0].m*A[0].n):
                x1, y1 = self.trouve_pos_init(A[0], i + 1)
                x2, y2 = self.trouve_pos_finale(A[0], i + 1)
                H = H + abs(x1 - x2) + abs(y1 - y2) 
            H = H/2 + A[0].cout
        else:
            for i in range(A.m * A.n):
                x1, y1 = self.trouve_pos_init(A, i + 1)
                x2, y2 = self.trouve_pos_finale(A, i + 1)
                H = H + abs(x1 - x2) + abs(y1 - y2)
            H = H/2 + A.cout
        return H

    def Heuristique_simple(self, A):
        """
        A heuristic defined by counting the number of numbers which are not at the right place plus the Grid's existing cost

        Parameter:
        -----------
        A, a Grid
        or
        (A, something), where A is a Grid

        Output:
        -----------
        int
        """
        H = 0
        if type(A) is tuple:
            for i in range(A[0].m*A[0].n):
                if self.trouve_pos_init(A[0], i+1) != self.trouve_pos_finale(A[0], i + 1):#checks if the cell is at the right position
                    H = H + 1 
            H = H + A[0].cout
        else:
            for i in range(A.m*A.n):
                if self.trouve_pos_init(A, i+1) != self.trouve_pos_finale(A, i + 1):#checks if the cell is at the right position
                    H = H + 1 
            H = H + A.cout
        return H

    def A_star(self, A, Heuristique) :
        dst = Grid(A.m, A.n)
        queue = [(Heuristique(A), (A, [A]))]# initiates the queue with the source node and the initial path(only the first node).
        visited = []
        while queue:
            current_node, path = heapq.heappop(queue)[1]
            if current_node == dst:# Checks if the node is the final destination:
                return path # Returns the first path found (which is the shortest)
            for neighbor in current_node.Reachable_states(): # Explore all neighbor nodes
                if neighbor not in visited: # Checks if the neighbor has already been visited
                    queue0= [queue[i][1][0] for i in range(len(queue))] # makes a copy only containing nodes
                    if neighbor in queue0:#checks if it is not already present with a lower cost
                        neighbor_position = queue0.index(neighbor)
                        if 0 < current_node.cout +1 < queue0[neighbor_position].cout: 
                            queue.pop(neighbor_position)
                            neighbor.cout = current_node.cout + 1
                            heapq.heappush(queue, (Heuristique(neighbor), (neighbor, path + [neighbor])))
                    else:
                        neighbor.cout = current_node.cout +1
                        heapq.heappush(queue, (Heuristique(neighbor), (neighbor, path + [neighbor]))) #adds the neighbor to the list
            visited = visited + [current_node] 

    def compromis(self, A, Heuristique):
        """
        Solves a grid, by applying A* with a certain heuristic to a progressively built graph.
        Parameter:
        -----------
        (A, Solver().Heur) where A is a Grid and Heur a heuristic
        Output:
        -----------
        path: list[Grid] | None
            The shortest path from src to dst. Returns None if dst is not reachable from src
        """
        dst = Grid(A.m, A.n)
        # initiates the queue with the source node and the initial path(only the first node).
        queue = [(A, [A])]
        visited = []
        while queue:
            queue = sorted(queue, key=Heuristique)
            # Deletes the first element of the queue (node and associated path)
            current_node, path = queue.pop(0)
            # Checks if the node is the final destination:
            if current_node == dst:
                return path
                # Returns the first path found (which is the shortest)
                # Explore all neighbor nodes
            for neighbor in current_node.Reachable_states():
                # Checks if the neighbor has already been visited
                if neighbor not in visited:
                    # Adds the neighbor to the queue with the actualized path
                    queue.append((neighbor, path + [neighbor]))
            visited = visited + [current_node]