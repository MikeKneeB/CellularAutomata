import numpy as np

from cellauto.core import Grid

class LifeGrid(Grid):

    def __init__(self, y_size, x_size, survive_list=[2,3], birth_list=[3]):
        Grid.__init__(self, y_size, x_size)
        self.survive_list = survive_list
        self.birth_list = birth_list

        self.temp_grid = None

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
        self.grid = np.copy(new_grid)

    def step_evolve(self, i, j):
        if i == 0 and j == 0:
            self.temp_grid = np.copy(self.grid)
        neighbours = self.count_neighbours(i, j)
        if self.temp_grid[i][j] == 1:
            if neighbours not in self.survive_list:
                self.temp_grid[i][j] = 0
                ret_val = 0
            else:
                ret_val = 1
        else:
            if neighbours in self.birth_list:
                self.temp_grid[i][j] = 1
                ret_val = 1
            else:
                ret_val = 0

        if i == self.y_size - 1 and j == self.x_size - 1:
            self.grid = np.copy(self.temp_grid)

        return ret_val

    def count_neighbours(self, y, x):
        total = 0
        if x > 0:
            if y > 0:
                total += self.grid[y-1][x-1] if self.grid[y-1][x-1] == 1 else 0
            total += self.grid[y][x-1] if self.grid[y][x-1] == 1 else 0
            if y < len(self.grid)-1:
                total += self.grid[y+1][x-1] if self.grid[y+1][x-1] == 1 else 0
        if y > 0:
            total += self.grid[y-1][x] if self.grid[y-1][x] == 1 else 0
        if y < len(self.grid)-1:
            total += self.grid[y+1][x] if self.grid[y+1][x] == 1 else 0
        if x < len(self.grid[0])-1:
            if y > 0:
                total += self.grid[y-1][x+1] if self.grid[y-1][x+1] == 1 else 0
            total += self.grid[y][x+1] if self.grid[y][x+1] == 1 else 0
            if y < len(self.grid)-1:
                total += self.grid[y+1][x+1] if self.grid[y+1][x+1] == 1 else 0
        return total

    def char_map(self, y, x):
        if self.grid[y][x] == 1:
            return '@'
        else:
            return ' '

    def edit_map(self, y, x, code):
        if code == 120:
            self.grid[y][x] = 0
        elif code == 99:
            self.grid[y][x] = 1
