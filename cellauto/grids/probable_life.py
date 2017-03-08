import numpy as np
import random as rm

from cellauto.grids.life import LifeGrid

class ProbLifeGrid(LifeGrid):

    def __init__(self, y_size, x_size, survive_list=[2,3], birth_list=[3], probability=0.1):
        LifeGrid.__init__(self, y_size, x_size, survive_list, birth_list)
        self.probability = probability

    def evolve(self):
        new_grid = np.copy(self.grid)
        for i, row in enumerate(self.grid):
            for j, item in enumerate(row):
                neighbours = self.count_neighbours(i, j)
                if item == 1:
                    if neighbours not in self.survive_list:
                        new_grid[i][j] = 0
                else:
                    if neighbours in self.birth_list:
                        new_grid[i][j] = 1
                if rm.random() < self.probability:
                    new_grid[i][j] = (new_grid[i][j] + 1) % 2

        self.grid = np.copy(new_grid)
