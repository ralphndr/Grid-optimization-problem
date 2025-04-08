# This will work if ran from the root folder (the folder in which there is the subfolder code/)
import sys 
sys.path.append("code/")

import unittest 
from grid import Grid
from solver import *

class Test_GridLoading(unittest.TestCase):
    def test_grid0(self):
        grid = Grid.grid_from_file("input/grid00.in",read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]])
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]])


    def test_grid0_novalues(self):
        grid = Grid.grid_from_file("input/grid00.in",read_values=False)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]])
        self.assertEqual(grid.value, [[1, 1, 1], [1, 1, 1]])
        

    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 4, 3], [2, 1, 0]])
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]])

    def test_grid2(self):
        grid = Grid.grid_from_file("input/grid02.in",read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 4, 3], [2, 1, 0]])
        self.assertEqual(grid.value, [[1, 1, 1], [1, 1, 1]])


class Test_methods(unittest.TestCase):
    def test_grid0(self):
        grid = Grid.grid_from_file("input/grid00.in",read_values=True)

        #test for is_forbiden
        self.assertFalse(grid.is_forbidden(0,0))
        self.assertFalse(grid.is_forbidden(0,2))
        self.assertFalse(grid.is_forbidden(1,2))

        #test for cost
        self.assertEqual(grid.cost( ((0,0),(1,0)) ),6)
        self.assertEqual(grid.cost( ((1,0),(1,1)) ),10)
        self.assertEqual(grid.cost( ((0,2),(1,2)) ),1)

        #test for depassement
        self.assertTrue(grid.depasser((0,4)))
        self.assertFalse(grid.depasser((1,2)))

        #test for compatible_color
        self.assertTrue(grid.compatible_color((1,1), (1,2)))

        #test for all_pairs
        self.assertEqual(grid.all_pairs(),[((0, 0), (0, 1)), ((0, 0), (1, 0)), ((0, 1), (0, 2)), ((0, 1), (1, 1)), ((0, 2), (1, 2)), ((1, 0), (1, 1)), ((1, 1), (1, 2))])

    def test_grid0_novalues(self):

        grid = Grid.grid_from_file("input/grid00.in",read_values=False)

        #test for is_forbiden
        self.assertFalse(grid.is_forbidden(0,0))
        self.assertFalse(grid.is_forbidden(0,2))
        self.assertFalse(grid.is_forbidden(1,2))

        #test for cost
        self.assertEqual(grid.cost( ((0,0),(1,0)) ),0)
        self.assertEqual(grid.cost( ((1,0),(1,1)) ),0)
        self.assertEqual(grid.cost( ((0,2),(1,2)) ),0)

        #test for depassement
        self.assertTrue(grid.depasser((0,4)))
        self.assertFalse(grid.depasser((1,2)))

        #test for compatible_color
        self.assertTrue(grid.compatible_color((1,1), (1,2)))

        #test for all_pairs
        self.assertEqual(grid.all_pairs() ,[((0, 0), (0, 1)), ((0, 0), (1, 0)), ((0, 1), (0, 2)), ((0, 1), (1, 1)), ((0, 2), (1, 2)), ((1, 0), (1, 1)), ((1, 1), (1, 2))])


    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)

        #test for is_forbiden
        self.assertFalse(grid.is_forbidden(0,0))
        self.assertFalse(grid.is_forbidden(1,2))
        self.assertTrue(grid.is_forbidden(0,1))

        #test for cost
        self.assertEqual(grid.cost( ((0,0),(1,0)) ),6)
        self.assertEqual(grid.cost( ((1,0),(1,1)) ),10)
        self.assertEqual(grid.cost( ((0,2),(1,2)) ),1)

        #test for depassement
        self.assertTrue(grid.depasser((0,4)))
        self.assertFalse(grid.depasser((1,2)))

        #test for compatible_color
        self.assertFalse(grid.compatible_color((0,0), (0,1)))
        self.assertFalse(grid.compatible_color((0,2), (1,1)))
        self.assertTrue(grid.compatible_color((1,1), (1,2)))
        self.assertTrue(grid.compatible_color((0,0), (0,2)))

        #test de all_pairs
        self.assertEqual(grid.all_pairs(),[((0,0), (1,0)), ((0,2), (1,2)), ((1,0), (1,1)), ((1,1), (1,2))])

    def test_grid2(self):
        grid = Grid.grid_from_file("input/grid02.in",read_values=True)

        #test for is_forbiden
        self.assertFalse(grid.is_forbidden(0,0))
        self.assertFalse(grid.is_forbidden(1,2))
        self.assertTrue(grid.is_forbidden(0,1))

        #test for cost
        self.assertEqual(grid.cost( ((0,0),(1,0)) ),0)
        self.assertEqual(grid.cost( ((1,0),(1,1)) ),0)
        self.assertEqual(grid.cost( ((0,2),(1,2)) ),0)

        #test for depassement
        self.assertTrue(grid.depasser((0,4)))
        self.assertFalse(grid.depasser((1,2)))

        #test for compatible_color
        self.assertFalse(grid.compatible_color((0,0), (0,1)))
        self.assertFalse(grid.compatible_color((0,2), (1,1)))
        self.assertTrue(grid.compatible_color((1,1), (1,2)))
        self.assertTrue(grid.compatible_color((0,0), (0,2)))
        
        #test for all_pairs
        self.assertEqual(grid.all_pairs(),[((0,0), (1,0)), ((0,2), (1,2)), ((1,0), (1,1)), ((1,1), (1,2))])

class Test_solver_Greedy(unittest.TestCase):
    def test_grid0(self):

        grid = Grid.grid_from_file("input/grid00.in",read_values=True)
        solver = SolverGreedy(grid)
        solver.run()
        self.assertEqual(solver.score(), 14)


    def test_grid0_novalues(self):

        grid = Grid.grid_from_file("input/grid00.in",read_values=False)
        solver = SolverGreedy(grid)
        solver.run()
        self.assertEqual(solver.score(), 0)


    def test_grid1(self):
        
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        solver = SolverGreedy(grid)
        solver.run()
        self.assertEqual(solver.score(), 8)
        
    
    def test_grid2(self):
        
        grid = Grid.grid_from_file("input/grid02.in",read_values=True)
        solver = SolverGreedy(grid)
        solver.run()
        self.assertEqual(solver.score(), 1) 

class Test_solver_Ford_Fulkerson(unittest.TestCase):
    def test_grid0_novalues(self):
        grid = Grid.grid_from_file("input/grid00.in",read_values=False)
        solver1 = Solver_Ford(grid)
        solver1.run()
        self.assertEqual(solver1.score(),0)
        self.assertEqual(solver1.pairs,[((0, 0), (0, 1)), ((0, 2), (1, 2)), ((1, 1), (1, 0))])

    def test_grid1(self):
        
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        solver1 = Solver_Ford(grid)
        solver1.run()
        self.assertEqual(solver1.score(),8)
        self.assertEqual(solver1.pairs,[((0, 0), (1, 0)), ((0, 2), (1, 2))])

    def test_grid2(self):
        grid = Grid.grid_from_file("input/grid02.in",read_values=True)
        solver1 = Solver_Ford(grid)
        solver1.run()
        self.assertEqual(solver1.score(),1)
        self.assertEqual(solver1.pairs,[((0, 0), (1, 0)), ((0, 2), (1, 2))])
    
    
class Test_solver_Maximum_weight_matching(unittest.TestCase):
    def test_grid0(self):

        grid = Grid.grid_from_file("input/grid00.in",read_values=True)
        solver = SolverMaxWeightMatching(grid)
        solver.run()
        self.assertEqual(solver.score(), 12)


    def test_grid0_novalues(self):

        grid = Grid.grid_from_file("input/grid00.in",read_values=False)
        solver = SolverMaxWeightMatching(grid)
        solver.run()
        self.assertEqual(solver.score(), 0)
        

    def test_grid1(self):
        
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        solver = SolverMaxWeightMatching(grid)
        solver.run()
        self.assertEqual(solver.score(), 8)
    
    def test_grid2(self):
        
        grid = Grid.grid_from_file("input/grid02.in",read_values=True)
        solver = SolverMaxWeightMatching(grid)
        solver.run()
        self.assertEqual(solver.score(), 1) 

    def test_grid17(self):
        
        grid = Grid.grid_from_file("input/grid17.in",read_values=True)
        solver = SolverMaxWeightMatching(grid)
        solver.run()
        self.assertEqual(solver.score(), 256) 
    
    


    
class Test_solver_MWM_Grid_with_new_rules(unittest.TestCase):
    def test_grid0(self):

        grid = Grid.grid_from_file("input/grid00.in",read_values=True)
        solver = SolverV2(grid)
        solver.run()
        self.assertEqual(solver.score(), 6)


    def test_grid0_novalues(self):

        grid = Grid.grid_from_file("input/grid00.in",read_values=False)
        solver = SolverV2(grid)
        solver.run()
        self.assertEqual(solver.score(), 0)
        

    def test_grid1(self):
        
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        solver = SolverV2(grid)
        solver.run()
        self.assertEqual(solver.score(), 8)    


    def test_grid2(self):
        
        grid = Grid.grid_from_file("input/grid02.in",read_values=True)
        solver = SolverV2(grid)
        solver.run()
        self.assertEqual(solver.score(), 1) 

   


if __name__ == '__main__':
    unittest.main()
    
