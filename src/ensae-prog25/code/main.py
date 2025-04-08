from grid import Grid
from solver import *
import time

def teste_glouton(nom_grille):
    grid = Grid.grid_from_file(nom_grille,read_values=True)
    solver = SolverGreedy(grid)
    solver.run()
    print(solver.score())

def teste_ford(nom_grille):
    grid = Grid.grid_from_file(nom_grille,read_values=True)
    solver = Solver_Ford(grid)
    solver.run()
    print(solver.score())

def teste_mwm(nom_grille):
    grid = Grid.grid_from_file(nom_grille,read_values=True)
    solver = SolverMaxWeightMatching(grid)
    solver.run()
    print(solver.score())

gride = "input/grid11.in"


start_time = time.time()  
teste_glouton(gride)
end_time = time.time() 
temps = end_time - start_time
print(f"Temps pour la glouton: {temps:.2f} secondes")



start_time = time.time()  
teste_ford(gride)
end_time = time.time()  
temps = end_time - start_time
print(f"Temps pour le Ford Fulkerson: {temps:.2f} secondes")


 
start_time = time.time()  
teste_mwm(gride)
end_time = time.time()  
temps = end_time - start_time
print(f"Temps pour le maximum weight matching: {temps:.2f} secondes")