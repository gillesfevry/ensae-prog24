"""
This is the grid module. It contains the Grid class and its associated methods.
"""
import math
import itertools
import random
from graph import Graph
from copy import deepcopy
import matplotlib.pyplot as plt


class Grid():
    """
    A class representing the grid from the swap puzzle. It supports rectangular grids.

    Attributes:
    -----------
    m: int
        Number of lines in the grid
    n: int
        Number of columns in the grid
    state: list[list[int]]
        The state of the grid, a list of list such that state[i][j] is
        the number in the cell (i, j), i.e., in the i-th line and j-th column.
        Note: lines are numbered 0..m and columns are numbered 0..n.
    """
    def __init__(self, m, n, initial_state=[], cout=0):
        """
        Initializes the grid.

        Parameters:
        -----------
        m: int
            Number of lines in the grid
        n: int
            Number of columns in the grid
        initial_state: list[list[int]]
            The initial state of the grid. Default is empty (then the grid is created sorted).
        """
        self.m = m
        self.n = n
        if not initial_state:
            initial_state = [list(range(i*n+1, (i+1)*n+1)) for i in range(m)]
        self.state = initial_state
        self.cout = cout

    def __str__(self):
        """
        Prints the state of the grid as text.
        """
        output = f"The grid is in the following state:\n"
        for i in range(self.m):
            output += f"{self.state[i]}\n"
        return output

    def __repr__(self):
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: m={self.m}, n={self.n}>"

    def __hash__(self):
        """
        Makes the puzzle hashable using its state
        """
        return hash(str(self.state))

    def __eq__(self, other):
        """
        Permits testing A==B using A and B states as equality criterion.
        """
        return self.state == other.state
    
    def __lt__(self, other):
        assert(self.m==other.m)
        assert(self.n==other.n)
        return self.state < other.state

    def is_sorted(self):
        """
        Checks if the current state of the grid is sorted and returns the answer as a boolean.
        """
        return (self.state == [list(range(i*self.n + 1, (i + 1)*self.n + 1)) for i in range(self.m)])

    def swap(self, cell1, cell2):
        """
        Implements the swap operation between two cells.
        Raises an exception if the swap is not allowed.

        Parameters:
        -----------
        cell1, cell2: tuple[int]
            The two cells to swap. They must be in the format (i, j)
            where i is the line and j the column number of the cell.
        """
        # we check that cells can be swapped
        if abs(cell1[0]-cell2[0]) + abs(cell1[1]-cell2[1]) > 1:
            raise ValueError("cells are not swappable")
        else:
            A = self.state[cell1[0]][cell1[1]]
            self.state[cell1[0]][cell1[1]] = self.state[cell2[0]][cell2[1]]
            self.state[cell2[0]][cell2[1]] = A

    def swap_seq(self, cell_pair_list):
        """
        Executes a sequence of swaps.

        Parameters:
        -----------
        cell_pair_list: list[tuple[tuple[int]]]
            List of swaps, each swap being a tuple of two cells (a cell being a tuple of integers).
            So the format should be [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """
        for i in range(len(cell_pair_list)):
            self.swap(cell_pair_list[i][0], cell_pair_list[i][1])

    def Graphic_rep(self):
        """
        Creates a graphic representation of a Grid.
        """
        for i in range(len(self.state)):

            for j in range(len(self.state[0])):

                plt.text(j, len(self.state)-i, str(self.state[i][j]), fontsize=20, color='b')

        plt.xlim([0, len(self.state) + 1])
        plt.ylim([0, len(self.state[0]) + 1])
        plt.grid(color='black', linestyle='--', linewidth=1.0)
        plt.show()

    def Shuffle(self):
        """
        Shuffles the grid.
        """
        V = [i + 1 for i in range(self.m * self.n)]
        random.shuffle(V)
        self.state = [[V[i*self.n + j] for j in range(self.n)]for i in range(self.m)]

    def other_states(self):
        """
        Returns a list of every state possible for the given grid's size.
        """
        # we create a liste of our numbers
        V = [i + 1 for i in range(self.m * self.n)]
        # we establish all the possible permutations
        permutations = list(itertools.permutations(V))
        States = []
        m = self.m
        n = self.n
        # we apply those permutations to our numbers in order to obtain all possible grid sates
        for k in range(math.factorial(m*n)):
            NewGrid = Grid(m, n, [[permutations[k][i*n + j] for j in range(n)]for i in range(m)])
            States = States + [NewGrid]
        return (States)

    def can_be_swapped(self, B):
        """
        Checks if two grids can be swapped or not.

        Parameter:
        -----------
        Another Grid of the same size.

        Output:
        -----------
        Boolean
        """
        # checks if it's the same grid
        if self == B:
            return True
        # checks that the grids' sizes are the same
        assert (self.m == B.m and self.n == B.n)
        # creates a list of all different points in the grids
        u = []
        for i in range(self.m):
            for j in range(self.n):
                if self.state[i][j] != B.state[i][j]:
                    u = u + [(i, j)]
        # if there are more than two different points, grids can't be swapped.
        if len(u) > 2:
            return False
        # if there are 2 different points, we check that they can be swapped.
        else:
            if abs(u[0][0]-u[1][0]) + abs(u[0][1]-u[1][1]) == 1:
                return True
            else:
                return False

    def GridGraph(self):
        """
        Creates a graph where the vertices are all the states possible for a grid of the same size,
        and where the edges link two swappable vertices.

        Output:
        -----------
        Graph from Graph class
        """
        G = Graph()
        U = self.other_states()
        # adds an edge every time two states can be swapped
        for i in range(len(U)):
            for j in range(len(U)):
                if j > i and U[i].can_be_swapped(U[j]):
                    G.add_edge(U[i], U[j])
        return (G)

    def Reachable_states(self):
        """
        Returns a list of all the reachable states of the grid in one single swap.
        """
        U = []
        # adds all the horizontal swaps
        for i in range(self.m):
            for j in range(self.n - 1):
                self.swap((i, j), (i, j+1))
                B = Grid(self.m, self.n, deepcopy(self.state))
                U = U + [B]
                self.swap((i, j), (i, j+1))
        # adds all the vertical swaps
        for j in range(self.n):
            for i in range(self.m - 1):
                self.swap((i, j), (i+1, j))
                B = Grid(self.m, self.n, deepcopy(self.state))
                U = U + [B]
                self.swap((i, j), (i+1, j))
        return (U)

    @classmethod
    def grid_from_file(cls, file_name):
        """
        Creates a grid object from class Grid,
        initialized with the information from the file file_name.

        Parameters:
        -----------
        file_name: str
            Name of the file to load. The file must be of the format:
            - first line contains "m n"
            - next m lines contain n integers that represent the state of the corresponding cell

        Output:
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            m, n = map(int, file.readline().split())
            initial_state = [[] for i_line in range(m)]
            for i_line in range(m):
                line_state = list(map(int, file.readline().split()))
                if len(line_state) != n:
                    raise Exception("Format incorrect")
                initial_state[i_line] = line_state
            grid = Grid(m, n, initial_state)
        return grid
