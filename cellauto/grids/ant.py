import numpy as np
import random as rm

from cellauto.core import Grid

class AntGrid(Grid):

    def __init__(self, y_size, x_size, ant_y=None, ant_x=None):
        Grid.__init__(self, y_size, x_size)

        if ant_y is not None and ant_x is not None:
            self.ant_y = ant_y
            self.ant_x = ant_x
        else:
            self.ant_y = y_size / 2
            self.ant_x = x_size / 2

        self.ant_dir = 0

        # Ant 3 = clear underneath, 2 = filled underneath.
        # This is so we can always just -= 2 to get correct state after ant
        # moves.
        self.grid[ant_y][ant_x] = 3

    def random_grid(self, threshold):
        super(AntGrid, self).random_grid(threshold)
        self.ant_y = rm.randint(0, self.y_size - 1)
        self.ant_x = rm.randint(0, self.x_size - 1)
        self.ant_dir = 0
        self.grid[self.ant_y][self.ant_x] = 3

    def clear_grid(self):
        super(AntGrid, self).clear_grid()
        self.ant_dir = 0
        self.grid[self.ant_y][self.ant_x] = 3

    def rebuild(self, y_size, x_size):
        super(AntGrid, self).rebuild(y_size, x_size)
        if self.y_size <= self.ant_y:
            self.ant_y = y_size / 2
        if self.x_size <= self.ant_x:
            self.ant_x = x_size / 2

    def evolve(self):
        new_ant_colour = lambda x: 3 if x == 0 else 2
        new_ant_dir = lambda x, y: (x - 1) % 4 if y == 0 else (x + 1) % 4
        self.grid[self.ant_y][self.ant_x] -= 2
        if self.ant_dir == 0: # NORTH
            self.ant_y = (self.ant_y - 1) % self.y_size
        elif self.ant_dir == 1: # EAST
            self.ant_x = (self.ant_x + 1) % self.x_size
        elif self.ant_dir == 2: # SOUTH
            self.ant_y = (self.ant_y + 1) % self.y_size
        else: # WEST
            self.ant_x = (self.ant_x - 1) % self.x_size

        self.ant_dir = new_ant_dir(self.ant_dir, self.grid[self.ant_y][self.ant_x])
        self.grid[self.ant_y][self.ant_x] = new_ant_colour(self.grid[self.ant_y][self.ant_x])

    def char_map(self, y, x):
        if self.grid[y][x] == 1:
            return '@'
        elif self.grid[y][x] > 1:
            if self.ant_dir == 0:
                return '^'
            elif self.ant_dir == 1:
                return '>'
            elif self.ant_dir == 2:
                return 'V'
            else:
                return '<'
        else:
            return ' '

    def edit_map(self, y, x, code):
        if code == 120:
            self.grid[y][x] = 0
        elif code == 99:
            self.grid[y][x] = 1
        elif code == 118:
            self.grid[self.ant_y][self.ant_x] = 0
            self.ant_y = y
            self.ant_x = x
            self.grid[y][x] = 3
