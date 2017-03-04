import numpy as np
import random as rm

from cellauto.core import Grid

class MultiAntGrid(Grid):

    def __init__(self, y_size, x_size, ant_y_list=None, ant_x_list=None):
        Grid.__init__(self, y_size, x_size)

        self.ant_number = 0

        if ant_y_list is not None and ant_x_list is not None:
            self.ant_y_list = ant_y_list
            self.ant_x_list = ant_x_list
            assert len(self.ant_y_list) == len(self.ant_x_list)
            self.ant_number = len(self.ant_y_list)
            self.ant_dir_list = [0 for i in range(self.ant_number)]
        else:
            self.ant_y_list = []
            self.ant_x_list = []
            self.ant_dir_list = []

        for i in range(self.ant_number):
            self.grid[self.ant_y_list[i]][self.ant_x_list[i]] = 3

    def random_grid(self, threshold):
        super(MultiAntGrid, self).random_grid(threshold)
        for i in range(self.ant_number):
            self.ant_y_list[i] = rm.randint(0, self.y_size - 1)
            self.ant_x_list[i] = rm.randint(0, self.x_size - 1)
            self.ant_dir_list[i] = 0
            self.grid[self.ant_y_list[i]][self.ant_x_list[i]] = 3

    def clear_grid(self):
        super(MultiAntGrid, self).clear_grid()
        self.ant_dir_list = []
        self.ant_y_list = []
        self.ant_x_list = []
        self.ant_number = 0

    def rebuild(self, y_size, x_size):
        super(MultiAntGrid, self).rebuild(y_size, x_size)
        for i in range(self.ant_number):
            if self.y_size <= self.ant_y_list[i] or self.x_size <= self.ant_x_list[i]:
                del self.ant_y_list[i]
                del self.ant_x_list[i]
                del self.ant_dir_list[i]
                self.ant_number -= 1

    def evolve(self):
        new_ant_colour = lambda x: 3 if x == 0 else 2
        new_ant_dir = lambda x, y: (x - 1) % 4 if y == 0 else (x + 1) % 4
        for i in range(self.ant_number):
            if self.collision_check(i):
                self.ant_dir_list[i] = (self.ant_dir_list[i] + 2) % 4
            else:
                self.grid[self.ant_y_list[i]][self.ant_x_list[i]] -= 2
                if self.ant_dir_list[i] == 0: # NORTH
                    self.ant_y_list[i] = (self.ant_y_list[i] - 1) % self.y_size
                elif self.ant_dir_list[i] == 1: # EAST
                    self.ant_x_list[i] = (self.ant_x_list[i] + 1) % self.x_size
                elif self.ant_dir_list[i] == 2: # SOUTH
                    self.ant_y_list[i] = (self.ant_y_list[i] + 1) % self.y_size
                else: # WEST
                    self.ant_x_list[i] = (self.ant_x_list[i] - 1) % self.x_size

                self.ant_dir_list[i] = new_ant_dir(self.ant_dir_list[i], self.grid[self.ant_y_list[i]][self.ant_x_list[i]])
                self.grid[self.ant_y_list[i]][self.ant_x_list[i]] = new_ant_colour(self.grid[self.ant_y_list[i]][self.ant_x_list[i]])

    def collision_check(self, i):
        if self.ant_dir_list[i] == 0:
            if self.grid[(self.ant_y_list[i] - 1) % self.y_size][self.ant_x_list[i]] > 1:
                return True
        elif self.ant_dir_list[i] == 1:
            if self.grid[self.ant_y_list[i]][(self.ant_x_list[i] + 1) % self.x_size] > 1:
                return True
        elif self.ant_dir_list[i] == 2:
            if self.grid[(self.ant_y_list[i] + 1) % self.y_size][self.ant_x_list[i]] > 1:
                return True
        else:
            if self.grid[self.ant_y_list[i]][(self.ant_x_list[i] - 1) % self.x_size] > 1:
                return True
        return False

    def char_map(self, y, x):
        if self.grid[y][x] == 1:
            return '@'
        elif self.grid[y][x] > 1:
            index = self.ant_y_list.index(y)
            if self.ant_dir_list[index] == 0:
                return '^'
            elif self.ant_dir_list[index] == 1:
                return '>'
            elif self.ant_dir_list[index] == 2:
                return 'V'
            else:
                return '<'
        else:
            return ' '

    def edit_map(self, y, x, code):
        if code == 120:
            if self.grid[y][x] > 1:
                index = self.ant_y_list.index(y)
                del self.ant_y_list[index]
                del self.ant_x_list[index]
                del self.ant_dir_list[index]
                self.ant_number -= 1
            self.grid[y][x] = 0
        elif code == 99:
            if self.grid[y][x] > 1:
                index = self.ant_y_list.index(y)
                del self.ant_y_list[index]
                del self.ant_x_list[index]
                del self.ant_dir_list[index]
                self.ant_number -= 1
            self.grid[y][x] = 1
        elif code == 118:
            self.ant_y_list.append(y)
            self.ant_x_list.append(x)
            self.ant_dir_list.append(0)
            self.ant_number += 1
            self.grid[y][x] = 3
