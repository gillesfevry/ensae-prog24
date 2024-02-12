from grid import Grid


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
        assert (0 < x <= A.n * A.m)
        i0, j0 = None, None
        for i in range(A.m):
            if x in A.state[i]:
                j0 = A.state[i].index(x)
                i0 = i
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
                if neighbor not in path:
                    # Adds the neighbor to the queue with the actualized path
                    queue.append((neighbor, path + [neighbor]))

    def Heuristique_euclidienne(self, A):
        """
        A heuristic defined by the sum of every number's Manhattan distance to its final position.

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
        else:
            for i in range(A.m * A.n):
                x1, y1 = self.trouve_pos_init(A, i + 1)
                x2, y2 = self.trouve_pos_finale(A, i + 1)
                H = H + abs(x1 - x2) + abs(y1 - y2)
        return H

    def Heuristique_simple(self, A):
        """
        A heuristic defined by counting the number of numbers which are not at the right place

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
                if self.trouve_pos_init(A[0], i+1) != self.trouve_pos_finale(A[0], i + 1):
                    H = H + 1
        else:
            for i in range(A.m*A.n):
                if self.trouve_pos_init(A, i+1) != self.trouve_pos_finale(A, i + 1):
                    H = H + 1
        return H

    def Heuristique_naif(self, A):
        """
        A heuristic defined by the length of the solution provided by naif

        Parameter:
        -----------
        A, a Grid
        or
        (A, something), where A is a Grid

        Output:
        -----------
        int
        """
        if type(A) is tuple:
            H = len(self.naif(A[0]))
        else:
            H = len(self.naif(A))
        return H

    def bfs_heuristique(self, A, Heuristique):
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
                # Checks if the neighbor is not already in the path
                if neighbor not in path:
                    # Adds the neighbor to the queue with the actualized path
                    queue.append((neighbor, path + [neighbor]))
