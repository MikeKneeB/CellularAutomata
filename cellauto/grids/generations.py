import numpy as np

from cellauto.grids.life import LifeGrid

class GeneGrid(LifeGrid):

    def __init__(self, y_size, x_size, survive_list=[2,3], birth_list=[3], generations):
        LifeGrid.__init__(self, y_size, x_sizem survive_list, birth_list)
        self.generations = generations

    def evolve(self):
        new_grid = np.copy(self.grid)
        for i, row in enumerate(self.grid):
            for j, item in enumerate(row):
                neighbours = self.count_neighbours(i, j)
                if item > 0:
                    if neighbours not in self.survive_list:
                        new_grid[i][j] = (new_grid[i][j] + 1) % generations
                else:
                    if neighbours in self.birth_list:
                        new_grid[i][j] = 1
        self.grid = np.copy(new_grid)
