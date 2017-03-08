import numpy as np
import random as rm

class Grid(object):

    def __init__(self, y_size, x_size):
        self.x_size = x_size
        self.y_size = y_size

        self.grid = np.zeros((y_size, x_size), dtype=np.int)
        self.grid_count = y_size * x_size

    def rebuild(self, y_size, x_size):
        self.x_size = x_size
        self.y_size = y_size
        self.grid_count = y_size * x_size

        new_grid = np.zeros((y_size, x_size), dtype=np.int)

        for i, row in enumerate(new_grid):
            for j, item in enumerate(row):
                if i >= len(self.grid) or j >= len(self.grid[0]):
                    new_grid[i][j] = 0
                else:
                    new_grid[i][j] = self.grid[i][j]

        self.grid = new_grid

    def random_grid(self, threshold):
        assert 0. < threshold < 1.
        for i, row in enumerate(self.grid):
            for j, item in enumerate(row):
                if rm.random() <= threshold:
                    self.grid[i][j] = 1
                else:
                    self.grid[i][j] = 0

    def clear_grid(self):
        self.grid = np.zeros((self.y_size, self.x_size), dtype=np.int)

    def evolve(self):
        pass

    def char_map(self, y, x):
        return ' '

    def edit_map(self, y, x, code):
        pass

    def print_grid(self):
        print(self.grid)

class GameWin(object):

    def __init__(self):
        self.game_grid = None
        self.title = ""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_game(self, game_grid):
        self.game_grid = game_grid

    def run_prog(self):
        pass
