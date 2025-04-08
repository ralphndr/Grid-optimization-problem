from collections import deque
from collections import defaultdict


import networkx as nx


class Solver:
    """
    A solver class. 

    Attributes: 
    -----------
    grid: Grid
        The grid
    pairs: list[tuple[tuple[int]]]
        A list of pairs, each being a tuple ((i1, j1), (i2, j2))
    """

    def __init__(self, grid):
        """
        Initializes the solver.

        Parameters: 
        -----------
        grid: Grid
            The grid
        """
        self.grid = grid
        self.pairs = list()

    def valid_pairs(self):
        """
        Returns a list of valid pairs that can be formed in the grid.
        
        Output:
        -------
        list of tuples: [(cell1, cell2), ...]
            Each pair (cell1, cell2) is a tuple of coordinates ((i1, j1), (i2, j2))
            where the colors and adjacency constraints are satisfied.
        """
        
        l = self.grid.all_pairs()

        possible_pair = [c for c in l if self.grid.compatible_color(*c)]  
        """
        possible_pair: list of tuples
            A list of pairs filtered from the list `l`. It contains only those pairs where the cells' colors are compatible.
        """

        if not self.pairs:          
            return possible_pair

        used_elmts = []                          
  
        #This ensures that no cell that has already been used in a pair will be considered in the new valid pairs.
        for couple in self.pairs:
            used_elmts.append(couple[0])
            used_elmts.append(couple[1])
        
        
        final_pair = []

        for c in possible_pair:
            x, y = c
            if x not in used_elmts and y not in used_elmts:
                final_pair.append(c)
        """
        Loop through each pair in possible_pair, and for each pair (x, y), check if neither x nor y is present in
        the used_elmts list.
        If both cells are unused, the pair is added to final_pair.
        """
        return final_pair
            
 
    def score(self):
        
        """
        Computes the score based on selected pairs and remaining unpaired cells.
        
        Output:
        -------
        int
            The total cost computed as the sum of absolute differences of values in pairs,
            plus the sum of values of unpaired non-black cells.
        """
        
        l = [ (i, j) for i in range(self.grid.n) for j in range(self.grid.m) if self.grid.color[i][j] != 4 ] 
        """
        Computes the score of the list of pairs in self.pairs
        Does not consider the cells that are not black
        """

        tot= 0
        # adds the score of each pair that has been considered during the loop
        for couple in self.pairs : 
            tot += self.grid.cost(couple)
            p1 , p2 = couple
            if p1 in l : 
                l.remove(p1)
            if p2 in l :
                l.remove(p2)

        # adds the score of the remaining cells
        for p in l : 
            a,b = p
            tot+=self.grid.value[a][b]
        return tot


class SolverEmpty(Solver):
    def run(self):
        pass


class SolverGreedy(Solver):
    """
    Sure! Here's a polished version you can directly include in a `README.md` file:

---

### Question 4 – Complexity Analysis

Let n and m be the dimensions of the grid.

- The complexity of the 'valid_pairs' function is O(n*m)

Now, let’s analyze the complexity of the greedy solver:
    - Computing the array c takes O(n*m)
    - Finding the minimum also takes O(n*m),
    - Therefore, the overall complexity of the greedy solver is O((n*m)^2).

Note: The solution returned by the greedy algorithm isn't always optimal.
For instance, for the grid `00`, the greedy algorithm returns a score of 14, whereas an optimal solution can achieve a score of 12 by selecting the following pairs:
 (0, 0), (1, 0), (0, 1), (0, 2), ((1, 1), (1, 2)

To find the optimal solution, one can test all possible pair combinations and evaluate their corresponding scores.  
There are 2^(n*m/2) possible combinations, resulting in a complexity of O(n*m*2^(n*m/2))

    """

    def run(self) : 
        """
        Executes the greedy algorithm to select the best pairs iteratively.
        
        The method selects the pair that minimizes the total score at each step until no
        more valid pairs can be chosen.
        
        Output:
        -------
        nothing
        """
        l = self.valid_pairs()
        while l:
            scores = [(self.grid.cost(couple), couple) for couple in l]
            
            
            min_score, best_pair = scores[0]  
            for score, pair in scores:
                if score < min_score:
                    min_score, best_pair = score, pair

            self.pairs.append(best_pair)
            l = self.valid_pairs()
        

class Graph:

    def __init__(self, graph):
        """
        Initializes the graph with an adjacency matrix.
        
        Parameters:
        -----------
        graph: list[list[int]]
            The adjacency matrix representation of the graph.
        """
        self.graph = graph
        self.row = len(graph)
        self.collum =len(graph[0])


    # Using BFS as a searching algorithm 
    def searching_algo_BFS(self, s, t, parent):
        """
        Implements BFS to find an augmenting path in the residual graph.
        
        Parameters:
        -----------
        s: int
            The source node.
        t: int
            The sink node.
        parent: list[int]
            An array to store the path found by BFS.
        
        Output:
        -------
        bool
            True if a path from source to sink exists, False otherwise.
        """

        visited = [False] * (self.row)
        queue = []

        queue.append(s)
        visited[s] = True

        while queue:

            u = queue.pop(0)

            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False

    # Applies the Ford-Fulkerson algorithm
    def ford_fulkerson(self, source, sink):
        """
        Implements the Ford-Fulkerson algorithm to find the maximum flow.
        
        Parameters:
        -----------
        source: int
            The index of the source node. This is where the flow begins.
        
        sink: int
            The index of the sink node. This is where the flow is intended to reach.

        Output:
        -------
        tuple (int, list[tuple[int, int, int]]):
            max_flow: The maximum flow value found from source to sink.
            flow_edges: A list of edges along with the flow used in each edge, represented as tuples (u, v, flow).
        """
        
        parent = [-1] * self.row
        """
        parent: list[int]
            It will store the parent node of each node in the path found during the BFS algorithm.
            It helps in reconstructing the path once an augmenting path is found.
        """
        
        max_flow = 0
        """
        max_flow: int
            The total flow from the source to the sink. This is the accumulated flow from all augmenting paths found.
        """
        
        flow_edges = []  
        """
        flow_edges: list[tuple[int, int, int]]
            A list to store the edges that are part of the augmenting paths and the flow used in each of them.
            Each element is a tuple (u, v, flow), where u and v are the nodes connected by the edge, and flow is the amount of flow sent through the edge.
        """

        while self.searching_algo_BFS(source, sink, parent):

            # Find the maximum flow in the path found by BFS
            path_flow = float("Inf")
            """
            path_flow: int
                The flow value that can be sent along the augmenting path found by BFS. 
                Initially set to infinity, it will be updated to the minimum capacity along the path.
            """
            
            v = sink
            
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, self.graph[u][v])
                """
                Updates the path_flow to the minimum capacity along the current path segment (from u to v).
                This ensures that the flow is limited by the smallest capacity on the path.
                """
                v = parent[v]

            #Updates the total max_flow by adding the flow of the current augmenting path.
            max_flow += path_flow
            
            # Updates the residual capacities of the graph and store the edges with their flow
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow  # Reduces the capacity on the forward edge
                self.graph[v][u] += path_flow  # Increases the capacity on the backward edge (reverse flow)
                flow_edges.append((u, v, path_flow))  # Stores the edge and the flow through it
                v = parent[v]

        return max_flow, flow_edges


class Solver_Ford(Solver):
    """
    Got it! Here's a clean, GitHub-README-ready version of your **Question 6**, written in Markdown:

---

### Question 6 – Optimal Solver for Grids with Only 1s

This solver computes the **optimal solution** for grids where all values are equal to `1`.

A comparison between the greedy and optimal solvers is provided in [`main.py`](./main.py).

---

### Complexity Analysis

Let V (number of vertices) and E (number of edges).

We analyze the complexity of each step:
    - `searching_algo_BFS` runs in O(E + V), which is O(n²) in our case  
    - `build_adjacency_matrix` runs in O(n × m)

The Ford-Fulkerson algorithm:
    - Requires at most O(V) = O(n × m) flow augmentations
    - Each iteration (BFS + update) takes O(n × m)
    - Therefore, the overall complexity is:  
  O(V × n × m) = O((n × m)²)
    """
    
    def build_adjacency_matrix(self, grid):
        """
        Constructs an adjacency matrix from the given grid representation.
        
        Parameters:
        -----------
        grid: Grid
            The grid representing the problem domain.
        
        Output:
        -------
        tuple (list[list[int]], dict)
            The adjacency matrix and a mapping of grid coordinates to node indices.
        """
        
        rows, cols = len(grid.value), len(grid.value[0])
 
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] 
        """
        directions: list[tuple[int, int]]
            List of tuples representing the four possible directions of movement on the grid: 
            right (0, 1), down (1, 0), left (0, -1), and up (-1, 0).
        """

        node_index = {}  
        index = 0
        """
        node_index: dict
            A dictionary mapping each valid grid cell (i, j) to a unique index.
        """

        # Creates the dictionnary giving the index of the cells
        for i in range(rows):
            for j in range(cols):
                node_index[(i, j)] = index
                index += 1

        # Creates the adjacency matric
        N = len(node_index)  # Total number of valid cells
        adjacency_matrix = [[0 for _ in range(N + 2)] for _ in range(N + 2)] 
        """
        adjacency_matrix: list[list[int]]
            An (N + 2) x (N + 2) adjacency matrix initialized with zeros, where N is the number of valid grid cells.
            The extra two rows/columns correspond to the source (s) and sink (t) nodes.
        """

        # s will be N and t: N+1
        # Fill the adjacency matrix
        for (i, j), u in node_index.items():  # u is the index of (i, j)
            if (i + j) % 2 == 0:  # Only for even cells
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if (ni, nj) in node_index and self.grid.compatible_color((ni, nj), (i, j)):  # Checks if the neighbour is valid
                        v = node_index[(ni, nj)]  # Index of the neighbour
                        adjacency_matrix[u][v] = 1  # Adds un edge
                adjacency_matrix[N][u] = 1  # Links s with even cells    
            else: 
                adjacency_matrix[u][N + 1] = 1  # Links t with odd cells
        
        return adjacency_matrix, node_index
    
    def run(self):
    
        graph, dico = self.build_adjacency_matrix(self.grid)
        """
        graph: list[list[int]]
            The adjacency matrix representing the graph, returned by the build_adjacency_matrix method.
        dico: dict
            A dictionary mapping grid coordinates to node indices, returned by the build_adjacency_matrix method.
        """

        graph1 = Graph(graph)

        source, sink = len(graph) - 2, len(graph) - 1  

        """
        source: int
            The index of the source node in the graph.
        sink: int
            The index of the sink node in the graph.
        """
        
        _, flow_edges = graph1.ford_fulkerson(source, sink)  # Finds the edges of flot max
        """
        flow_edges: list[tuple[int, int, int]]
            A list of edges (u, v, flow) where flow is the amount of flow sent through edge (u, v) from source to sink.
        """
        
        # Ajouter les arêtes aux paires du solveur
        for u, v, flow in flow_edges:
            if flow > 0 and u < source and v < sink:  # Ignores source and sink
                for k, val in dico.items(): 
                    if val == u: 
                        case1 = k
                    elif val == v:
                        case2 = k
                self.pairs.append((case1, case2))
        """
        Iterates over the flow edges, appends valid pairs (case1, case2) to self.pairs if the flow through them is positive,
        and the nodes are not the source or sink. The dictionary dico is used to map node indices back to grid coordinates.
        """

    

class SolverMaxWeightMatching(Solver):
    def build_weighted_graph(self):
        """
        Creates a weighted graph based on the grid.
        Vertices are cells, edges represent valid pairs,
        and edge weights are defined by the absolute difference between cell values.
        """
        G = nx.Graph()
        for (i1, j1), (i2, j2) in self.grid.all_pairs():
            weight = self.grid.value[i1][j1] + self.grid.value[i2][j2] -self.grid.cost(((i1, j1), (i2, j2)))  # On minimise donc poids négatif
            G.add_edge((i1, j1), (i2, j2), weight=weight)
        return G
    
    def run(self):
        """
        Runs the Maximum Weight Matching algorithm.   
        """
        G = self.build_weighted_graph()
        matching = nx.max_weight_matching(G, maxcardinality=False)
        self.pairs = list(matching)


class SolverV2(Solver):
    def build_weighted_graph(self):
        """
        Creates a weighted graph based on the grid.
        Vertices are cells, edges represent valid pairs,
        and edge weights are defined by the absolute difference between cell values.
        """
        G = nx.Graph()
        white_cells = []
        
        for (i1, j1), (i2, j2) in self.grid.all_pairs():
            weight = self.grid.value[i1][j1] + self.grid.value[i2][j2] -self.grid.cost(((i1, j1), (i2, j2)))   
            G.add_edge((i1, j1), (i2, j2), weight=weight)
            
            
            if self.grid.color[i1][j1] == 0:
                white_cells.append((i1, j1))
            if self.grid.color[i2][j2] == 0:
                white_cells.append((i2, j2))
        
      #add the edge due to the new rules
        for cell1 in white_cells:
            (i1,j1) = cell1
            for i in range(self.grid.n):
                for j in range(self.grid.m):
                    if self.grid.color[i][j] != 4 and cell1 != (i, j):  
                        weight = self.grid.value[i1][j1] + self.grid.value[i][j] -self.grid.cost((cell1, (i, j))) 
                        G.add_edge(cell1, (i, j), weight=weight)
        
        return G
    
    def run(self):
        """
        Runs the Maximum Weight Matching algorithm.     
       """
        G = self.build_weighted_graph()
        matching = nx.max_weight_matching(G, maxcardinality=False)
        self.pairs = list(matching)



class solver_a_2_glouton(Solver): 

    def run(self, joueur ):
        j = joueur
        s0=0
        s1=0 
        while self.valid_pairs():
            if j ==0 : 
                x1= int(input("x1"))
                y1= int(input("y1"))
                x2= int(input("x2"))
                y2= int(input("y2"))
                paire =((x1,y1),(x2,y2))
                while( not(paire in self.valid_pairs())):
                    x1= int(input("x1"))
                    y1= int(input("y1"))
                    x2= int(input("x2"))
                    y2= int(input("y2"))
                    paire =((x1,y1),(x2,y2))
                self.pairs.append(paire)
                s0+= self.grid.cost(paire) 
                print(f"coup joué :{paire}")
            if j==1 : 
                l = self.valid_pairs()
                c= [ self.grid.cost(couple) for couple in l]
                
                min_index, mini = 0, c[0]
                for i in range(len(c)):
                    if c[i] < mini:
                        mini =c[i]
                        min_index = i
                couple= l[min_index]
                s1+= mini
                self.pairs.append(couple)
                print(f"coup joué :{couple}")
            j = 1 - j  
                


class SolverMaxWeightMatching_a_2(Solver):

    def __init__(self, grid):
        super().__init__(grid)
        self.player_scores = {1: 0, 2: 0}  # Scores des deux joueurs
        self.current_player = 1  # Joueur 1 commence
        self.remaining_pairs = self.grid.all_pairs()  
    
    def build_weighted_graph(self):
        """
        Creates a grid-based weighted graph for the automatic player (Player 1).
        Vertices are cells, edges represent valid pairs,
        and edge weights are defined by the absolute difference between cell values.
        """
        G = nx.Graph()
        
        for (i1, j1), (i2, j2) in self.remaining_pairs:
            weight = self.grid.value[i1][j1] + self.grid.value[i2][j2] -self.grid.cost(((i1, j1), (i2, j2)))  # Optimisation pour minimisation du score
            G.add_edge((i1, j1), (i2, j2), weight=weight)
        
        return G
    
    def optimal_move(self):
        """
        Selects the move with the minimal score amoug the moves that are in the solution
        """
        G = self.build_weighted_graph()
        matching = nx.max_weight_matching(G, maxcardinality=False)
        l = list(matching)
        min_index, mini = 0, self.grid.cost(l[0]) 
        for i in range(len(l)):
            if self.grid.cost(l[i]) < mini:
                mini = self.grid.cost(l[i])
                min_index = i
                # adds the move that minimizes the score
        couple= l[min_index]
        if matching:
            return couple  # Retourne la meilleure paire trouvée
        return None
    
    def player_move(self, pair):
        """
        Allows the player to play the move
        """
        if pair in self.remaining_pairs:
            self.pairs.append(pair)
            self.remaining_pairs = self.valid_pairs()
            cost = self.grid.cost(pair)
            self.player_scores[2] += cost
            return True
        return False
    
    def run(self):
        """
        Runs the game with one player and an Ia who follows the maximum_weight_matching  algorithm.
        """
        while self.remaining_pairs:
            if self.current_player == 1:
                move = self.optimal_move()
                if move:
                    self.pairs.append(move)
                    self.remaining_pairs = self.valid_pairs()
                    cost = self.grid.cost(move)
                    self.player_scores[1] += cost
                    print(f"Joueur 1 choisit la paire {move} (coût: {cost})")
            else:
                print("Joueur 2, choisissez une paire parmi:", self.remaining_pairs)
                x1= int(input("x1"))
                y1= int(input("y1"))
                x2= int(input("x2"))
                y2= int(input("y2"))
                paire =((x1,y1),(x2,y2))
                while( not(paire in self.remaining_pairs)):
                    x1= int(input("x1"))
                    y1= int(input("y1"))
                    x2= int(input("x2"))
                    y2= int(input("y2"))
                    paire =((x1,y1),(x2,y2))
                self.player_move(paire)
               
            
            self.current_player = 3 - self.current_player  
        
        print("Scores finaux:")
        print(f"Joueur 1: {self.player_scores[1]}")
        print(f"Joueur 2: {self.player_scores[2]}")
        winner = 1 if self.player_scores[1] < self.player_scores[2] else 2
        print(f"Le gagnant est le Joueur {winner} !")





class SolverMinimax(Solver):
    
    def __init__(self, grid, depth=3):
        super().__init__(grid)
        self.depth = depth  # Profondeur de recherche pour Minimax
        self.player_scores = {1: 0, 2: 0}  
        self.current_player = 1  # Joueur 1 (IA) commence
        self.remaining_pairs = self.grid.all_pairs()  
    
    def evaluate(self):
        """
        Gives an evaluation of the state of the game 
        """
        return self.player_scores[1] - self.player_scores[2]  
    
    def minimax(self, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        
        if depth == 0 or not self.remaining_pairs:
            return self.evaluate()
        
        if is_maximizing:
            best_score = float('-inf')
            for pair in self.remaining_pairs:
                cost = self.grid.cost(pair)
                self.player_scores[2] += cost
                self.pairs.append(pair)
                self.remaining_pairs = self.valid_pairs()
                score = self.minimax(depth - 1, False, alpha, beta)
                self.pairs.remove(pair)
                self.remaining_pairs = self.valid_pairs()
                self.player_scores[2] -= cost
                best_score = max(best_score, score)
                
                if best_score >=beta:
                    return best_score # Élagage bêta
                alpha = max(alpha, best_score)
            return best_score
        else:
            best_score = float('inf')
            for pair in self.remaining_pairs:
                cost = self.grid.cost(pair)
                self.player_scores[1] += cost
                self.pairs.append(pair)
                self.remaining_pairs = self.valid_pairs()
                score = self.minimax(depth - 1, True, alpha, beta)
                self.pairs.remove(pair)
                self.remaining_pairs = self.valid_pairs()
                self.player_scores[1] -= cost
                best_score = min(best_score, score)
                if best_score <= alpha:
                    return best_score # Élagage alpha
                beta = min(beta, best_score)
            return best_score
    
    def best_move(self):
        """
        Finds the best move with the minimax algorithm
        """
        best_score = float('inf')
        best_pair = None
        
        for pair in self.remaining_pairs:
            cost = self.grid.cost(pair)
            self.player_scores[1] += cost
            self.remaining_pairs.remove(pair)
            score = self.minimax(self.depth - 1, True, float('-inf'), float('inf'))
            self.remaining_pairs.append(pair)
            self.player_scores[1] -= cost
            
            if score < best_score:
                best_score = score
                best_pair = pair
        
        return best_pair
    
    def player_move(self, pair):
        """
        Plays the move for the player
        """
        if pair in self.remaining_pairs:
            self.pairs.append(pair)
            self.remaining_pairs = self.valid_pairs()
            cost = self.grid.cost(pair)
            self.player_scores[2] += cost
            return True
        return False
    
    def run(self):
        """
        Runs the game with one player and one ia , who follow the minimax strategie
        """
        while self.remaining_pairs:
            if self.current_player == 1:
                move = self.best_move()
                if move:
                    self.pairs.append(move)
                    self.remaining_pairs = self.valid_pairs()
                    cost = self.grid.cost(move)
                    self.player_scores[1] += cost
                    print(f" IA choisit la paire {move} (coût: {cost})")
            else:
                print("Joueur, choisissez une paire parmi:", self.remaining_pairs)
                x1 = int(input("x1: "))
                y1 = int(input("y1: "))
                x2 = int(input("x2: "))
                y2 = int(input("y2: "))
                paire = ((x1, y1), (x2, y2))
                while not (paire in self.remaining_pairs):
                    print("Paire invalide, réessayez.")
                    x1 = int(input("x1: "))
                    y1 = int(input("y1: "))
                    x2 = int(input("x2: "))
                    y2 = int(input("y2: "))
                    paire = ((x1, y1), (x2, y2))
                self.player_move(paire)
            
            self.current_player = 3 - self.current_player  
        
        print("Scores finaux:")
        print(f"IA: {self.player_scores[1]}")
        print(f"Joueur: {self.player_scores[2]}")
        winner = 1 if self.player_scores[1] < self.player_scores[2] else 2
        print(f"Le gagnant est {'IA' if winner == 1 else 'Joueur'} !")
