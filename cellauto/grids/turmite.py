import numpy as np
import random as rm

from cellauto.core import Grid

class TurmiteGrid(Grid):

    def __init__(self, y_size, x_size, turmite_spec):
        Grid.__init__(self, y_size, x_size)

        self.tur_y = []
        self.tur_x = []
        self.tur_state = []
        self.tur_dir = []
        self.tur_number = 0

        self.turmite_spec = turmite_spec

    def random_grid(self, threshold):
        super(TurmiteGrid, self).random_grid(threshold)
        for i in range(self.tur_number):
            self.tur_y[i] = rm.randint(0, self.y_size - 1)
            self.tur_x[i] = rm.randint(0, self.x_size - 1)
            self.tur_state = []
            self.tur_dir[i] = rm.randint(0, 3)

    def clear_grid(self):
        super(TurmiteGrid, self).clear_grid()
        self.tur_y = []
        self.tur_x = []
        self.tur_state = []
        self.tur_dir = []
        self.tur_number = 0

    def rebuild(self, y_size, x_size):
        super(TurmiteGrid, self).rebuild(y_size, x_size)
        for i in range(self.tur_number):
            if self.y_size <= self.tur_y[i] or self.x_size <= self.tur_x[i]:
                del self.tur_y[i]
                del self.tur_x[i]
                del self.tur_dir[i]
                del self.tur_state[i]
                self.ant_number -= 1

    def evolve(self):
        for i in range(self.tur_number):
            if self.collision_check(i):
                self.tur_dir[i] = (self.tur_dir[i] + 2) % 4
            else:
                next_colour = self.turmite_spec.next_colour(self.tur_state[i], self.grid[self.tur_y[i]][self.tur_x[i]])
                next_state = self.turmite_spec.next_state(self.tur_state[i], self.grid[self.tur_y[i]][self.tur_x[i]])
                next_dir = self.tur_dir[i] + self.turmite_spec.turn(self.tur_state[i], self.grid[self.tur_y[i]][self.tur_x[i]])

                self.tur_state[i] = next_state
                self.grid[self.tur_y[i]][self.tur_x[i]] = next_colour

                if self.tur_dir[i] == 0: # NORTH
                    self.tur_y[i] = (self.tur_y[i] - 1) % self.y_size
                elif self.tur_dir[i] == 1: # EAST
                    self.tur_x[i] = (self.tur_x[i] + 1) % self.x_size
                elif self.tur_dir[i] == 2: # SOUTH
                    self.tur_y[i] = (self.tur_y[i] + 1) % self.y_size
                else: # WEST
                    self.tur_x[i] = (self.tur_x[i] - 1) % self.x_size

                self.tur_dir[i] = next_dir

    def collision_check(self, i):
        if self.tur_dir[i] == 0:
            if (self.tur_y[i] - 1) % self.y_size in self.tur_y:
                return True
        elif self.tur_dir[i] == 1:
            if (self.tur_x[i] + 1) % self.x_size in self.tur_x:
                return True
        elif self.tur_dir[i] == 2:
            if (self.tur_y[i] + 1) % self.y_size in self.tur_y:
                return True
        else:
            if (self.tur_x[i] - 1) % self.x_size in self.tur_x:
                return True
        return False

class TurmiteSpec(object):
    def __init__(self, states, colours):
        self.transition_table = np.zeros((self.states, self.colours, 3), dtype=np.int)

        self.states = states
        self.colours = colours

    def next_state(self, state, colour):
        return self.transition_table[state][colour][0]

    def next_colour(self, state, colour):
        return self.transition_table[state][colour][1]

    def turn(self, state, colour):
        return self.transition_table[state][colour][2]
