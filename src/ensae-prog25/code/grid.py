import matplotlib.pyplot as plt
import numpy as np 
from matplotlib.colors import ListedColormap
"""
This is the grid module. It contains the Grid class and its associated methods.
"""

class Grid():
    """
    A class representing the grid. 

    Attributes: 
    -----------
    n: int
        Number of lines in the grid
    m: int
        Number of columns in the grid
    color: list[list[int]]
        The color of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    value: list[list[int]]
        The value of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    colors_list: list[char]
        The mapping between the value of self.color[i][j] and the corresponding color
    """
    

    def __init__(self, n, m, color=[], value=[]):
        """
        Initializes the grid.

        Parameters: 
        -----------
        n: int
            Number of lines in the grid
        m: int
            Number of columns in the grid
        color: list[list[int]]
            The grid cells colors. Default is empty (then the grid is created with each cell having color 0, i.e., white).
        value: list[list[int]]
            The grid cells values. Default is empty (then the grid is created with each cell having value 1).
        
        The object created has an attribute colors_list: list[char], which is the mapping between the value of self.color[i][j] and the corresponding color
        """
        self.n = n
        self.m = m
        if not color:
            color = [[0 for j in range(m)] for i in range(n)]            
        self.color = color
        if not value:
            value = [[1 for j in range(m)] for i in range(n)]            
        self.value = value
        self.colors_list = ['w', 'r', 'b', 'g', 'k']

    def __str__(self): 
        """
        Prints the grid as text.
        """
        output = f"The grid is {self.n} x {self.m}. It has the following colors:\n"
        for i in range(self.n): 
            output += f"{[self.colors_list[self.color[i][j]] for j in range(self.m)]}\n"
        output += f"and the following values:\n"
        for i in range(self.n): 
            output += f"{self.value[i]}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: n={self.n}, m={self.m}>"
    
    def plot(self):
        """
        Plots the grid with the colors associated to the values
        
        Parameters: 
        -----------
        None

        Output: 
        -----------
        Displays a visual representation of the grid using a heatmap, where each cell's color 
        corresponds to the value of the cell. 
        """
        
        color_map = {
            0: 'white',
            1: 'red',
            2: 'blue',
            3: 'green',
            4: 'black'
        }
        """
        color_map: dict[int, str]
            This is used to map the color values in the grid to displayable colors.
        """

        cmap = ListedColormap([color_map[i] for i in range(5)])
        """
        cmap: ListedColormap 
            It ensures that values from 0 to 4 are mapped to specific colors in the plot.
        """

        heatmap = np.zeros((self.n, self.m))
        """
        heatmap: np.ndarray
            A 2D numpy array of shape (self.n, self.m) initialized with zeros. 
        """

        fig, ax = plt.subplots(figsize=(self.m, self.n))
        """
        fig: matplotlib.figure.Figure
            The figure object created by matplotlib, which serves as the container for the plot.

        ax: matplotlib.axes._axes.Axes
            The axes object where the grid and color map will be drawn.
        """

        for i in range(self.n):
            for j in range(self.m):
                heatmap[i, j] = self.color[i][j]
                ax.text(j, i, str(self.value[i][j]), ha='center', va='center', color='black')
        """
        Iterates over every grid cell (i, j). For each cell:
            - Assigns the corresponding color from self.color[i][j] to the heatmap array.
            - Adds the value from self.value[i][j] to the grid, placing it in the center of the cell (i, j).
            - The text is displayed in black and centered in the cell.
        """

        cax = ax.imshow(heatmap, cmap=cmap, interpolation='nearest', vmin=0, vmax=4)
        """
        cax: matplotlib.image.AxesImage
            The 'cmap' argument applies the defined colormap, and 'vmin' and 'vmax' limit the color scaling to the range 0 to 4.
            The 'interpolation' argument ensures that the cells are displayed as distinct blocks with no interpolation between them.
        """

        ax.set_xticks(np.arange(self.m))
        ax.set_yticks(np.arange(self.n))
        """
        ax.set_xticks(np.arange(self.m)): 
            Sets the x-axis tick positions to correspond to the number of columns in the grid.
        Same with set_yticks
        """

        ax.set_xticklabels(np.arange(0, self.m))
        ax.set_yticklabels(np.arange(0, self.n))
        """
        ax.set_xticklabels(np.arange(0, self.m)): 
            Sets the x-axis tick labels to represent the column numbers (0 to m-1).
        Same with set_yticklabels
        """

        ax.set_xticks(np.arange(-0.5, self.m, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.n, 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
        """
        ax.set_xticks(np.arange(-0.5, self.m, 1), minor=True):
            Sets the minor x-axis ticks at half-integer positions, ensuring that grid lines are placed between cells.
        Same with y and it's between the rows

        ax.grid(which='minor', color='black', linestyle='-', linewidth=2):
            Adds black grid lines to the plot at the minor tick positions.
        """

        plt.tick_params(axis='both', which='major', labelsize=10, labelbottom=False, bottom=False, top=False, labeltop=True)
        """
        Customizes tick parameters for both axes:
            - Hides the x-axis labels and ticks at the bottom.
            - Displays labels at the top of the plot.
            - Adjusts the size of the tick labels to 10.
        """

        plt.show()
      

    def is_forbidden(self, i, j):
        """
        Returns True if the cell (i, j) is black and False otherwise
        """
        return self.color[i][j] == 4
        

    def cost(self, pair):
        """
        Returns the cost of a pair
 
        Parameters: 
        -----------
        pair: tuple[tuple[int]]
            A pair in the format ((i1, j1), (i2, j2))

        Output: 
        -----------
        cost: int
            the cost of the pair defined as the absolute value of the difference between their values
        """
        paire1, paire2 = pair
        i1 , j1 = paire1 
        i2 , j2 = paire2 
        return abs(self.value[i1][j1]-self.value[i2][j2])

    def depasser(self, paire):
        """
        Returns if a pair is outside of the grid or not
 
        Parameters: 
        -----------
        pair: tuple[int]
            A pair in the format ((i1, j1)

        Output: 
        -----------
        depasser: boolean
        """
        a,b = paire
        return not ((a>=0) and (b>=0) and (b<self.m) and (a<self.n))

    def compatible_color(self, paire1, paire2): 
        """
        Returns the compatibility of 2 cases 
        Parameters: 
        -----------
        pair: tuple[tuple[int]]
            A pair in the format ((i1, j1), (i2, j2))

        Output: 
        -----------
        compatible_color: boolean
            accordingly to the rules, this function testsif 2 cases are allowed to be paired
            as a reminder : - green pairs with white/green
                            - blue pairs with white/blue/red
                            - red pairs with white/blue/red
                            - white pairs with every color except black
        """
        i1 , j1 = paire1 
        i2 , j2 = paire2 
        if self.color[i1][j1]==0 :
            return (self.is_forbidden(i2,j2))==False
        elif self.color[i1][j1]==1 :
            return self.color[i2][j2] in [0,1,2]
        elif self.color[i1][j1]==2 :
            return self.color[i2][j2] in [0,1,2]
        elif self.color[i1][j1]==3 :
            return self.color[i2][j2] in [0,3]
        else :
            return False


    def all_pairs(self):
        """
        Returns a list of all pairs of cells that can be taken together. 

        Outputs:
        -----------
        List of tuples of tuples [(c1, c2), (c1', c2'), ...] where each cell c1 etc. is itself a tuple (i, j)
        """
        liste_paire=[]

        for i in range(self.n):
            for j in range(self.m):
                paire=(i,j)
                l=[(i,j+1),(i+1,j)]
                for p in l : 
                    if self.depasser(p)==False and self.compatible_color(paire,p):
                        liste_paire.append( ( paire , p) )
        return liste_paire


    @classmethod
    def grid_from_file(cls, file_name, read_values=False): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "n m" 
            - next n lines contain m integers that represent the colors of the corresponding cell
            - next n lines [optional] contain m integers that represent the values of the corresponding cell
        read_values: bool
            Indicates whether to read values after having read the colors. Requires that the file has 2n+1 lines

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            color = [[] for i_line in range(n)]
            for i_line in range(n):
                line_color = list(map(int, file.readline().split()))
                if len(line_color) != m: 
                    raise Exception("Format incorrect")
                for j in range(m):
                    if line_color[j] not in range(5):
                        raise Exception("Invalid color")
                color[i_line] = line_color

            if read_values:
                value = [[] for i_line in range(n)]
                for i_line in range(n):
                    line_value = list(map(int, file.readline().split()))
                    if len(line_value) != m: 
                        raise Exception("Format incorrect")
                    value[i_line] = line_value
            else:
                value = []

            grid = Grid(n, m, color, value)
        return grid


