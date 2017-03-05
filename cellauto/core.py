import numpy as np
import random as rm
import curses
import time

import cellauto.grids

class Grid(object):

    def __init__(self, y_size, x_size):
        self.x_size = x_size
        self.y_size = y_size

        self.grid = np.zeros((y_size, x_size), dtype=np.int)

    def rebuild(self, y_size, x_size):
        self.x_size = x_size
        self.y_size = y_size

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

class GridWin():

    def __init__(self):
        self.game_grid = None

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(1)

        self.title = ""

        self.win_coords = self.stdscr.getmaxyx()

        # self.game_grid.rebuild(self.win_coords[0] - 2, self.win_coords[1] - 2)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        self.stdscr.keypad(0)

        curses.endwin()

    def add_game(self, game_grid):
        self.game_grid = game_grid
        self.game_grid.rebuild(self.win_coords[0] - 2, self.win_coords[1] - 2)

    def draw_welcome(self):
        try:
            self.stdscr.clear()
            if self.stdscr.getmaxyx() != self.win_coords:
                self.win_coords = self.stdscr.getmaxyx()
            self.stdscr.addstr(1,1, 'WELCOME TO THE GAME OF LIFE')
            self.stdscr.addstr(3,1, 'Please choose a game:')
            self.stdscr.addstr(4,2, '1 - Life')
            self.stdscr.addstr(5,2, '2 - Langton\'s Ant')
            self.stdscr.addstr(6,2, '3 - Multi-Ant')
            self.stdscr.addstr(7,2, 'h - Help')
            self.stdscr.addstr(8,2, 'q - quit')
            self.stdscr.refresh()
            while True:
                command = self.stdscr.getch()
                if command == 49:
                    self.add_game(cellauto.grids.life.LifeGrid(20, 20))
                    break
                elif command == 50:
                    self.add_game(cellauto.grids.ant.AntGrid(20, 20))
                    break
                elif command == 51:
                    self.add_game(cellauto.grids.multi_ant.MultiAntGrid(20,20))
                    break
                elif command == 104:
                    pass
                elif command == 113:
                    return 1
                else:
                    self.stdscr.addstr(9,1, 'Command not recognised.')
                    self.stdscr.refresh()
            self.stdscr.clear()
            self.stdscr.addstr(1,1, 'WELCOME TO THE GAME OF LIFE')
            self.stdscr.addstr(3,1, 'Please press a key:')
            self.stdscr.addstr(4,2, 'r - Random start')
            self.stdscr.addstr(5,2, 'e - Empty start')
            self.stdscr.addstr(6,2, 'h - Help')
            self.stdscr.addstr(7,2, 'q - Quit')
            self.stdscr.refresh()
            while True:
                command = self.stdscr.getch()
                if command == 114:
                    self.game_grid.random_grid(0.2)
                    return 0
                elif command == 101:
                    self.game_grid.clear_grid()
                    return 0
                elif command == 104:
                    pass
                elif command == 113:
                    return 1
                else:
                    self.stdscr.addstr(9,1, 'Command not recognised.')
                    self.stdscr.refresh()
        except curses.error:
            print('Why did you make the terminal so bloody small?')
            return 1

    def draw_grid(self):
        self.stdscr.clear()
        if self.stdscr.getmaxyx() != self.win_coords:
            self.win_coords = self.stdscr.getmaxyx()
            self.game_grid.rebuild(self.win_coords[0] - 2, self.win_coords[1] - 2)
        hori_bar = "#"*(self.game_grid.x_size)
        self.stdscr.addstr(0, 1, hori_bar)
        self.stdscr.addstr(0, 2, self.title)
        for i, row in enumerate(self.game_grid.grid):
            self.stdscr.addstr(i+1, 0, '#')
            for j, item in enumerate(row):
                if item != 0:
                    self.stdscr.addstr(i+1, j+1, self.game_grid.char_map(i, j))
            self.stdscr.addstr(i+1, self.game_grid.x_size+1, '#')
        self.stdscr.addstr(self.game_grid.y_size + 1, 1, hori_bar)
        self.stdscr.refresh()

    def edit_grid(self):
        self.title = "Editting"
        curses.curs_set(1)
        self.stdscr.move(1,1)
        cursor_pos = [0, 0]
        while True:
            time.sleep(0.03)
            self.draw_grid()
            try:
                self.stdscr.move(cursor_pos[0]+1, cursor_pos[1]+1)
            except curses.error:
                cursor_pos = [0, 0]
                self.stdscr.move(cursor_pos[0]+1, cursor_pos[1]+1)
            command = self.stdscr.getch()
            if command == 103:
                curses.curs_set(0)
                return 0
            elif command == 113:
                curses.curs_set(0)
                return 1
            # elif command == 120:
            #     self.game_grid.grid[cursor_pos[0]][cursor_pos[1]] = 0
            # elif command == 99:
            #     self.game_grid.grid[cursor_pos[0]][cursor_pos[1]] = 1
            elif command == 122:
                self.game_grid.clear_grid()
            elif command == 114:
                self.game_grid.random_grid(0.2)
            elif command == curses.KEY_UP:
                if cursor_pos[0] == 0:
                    pass
                else:
                    cursor_pos[0] = cursor_pos[0] - 1
            elif command == curses.KEY_DOWN:
                if cursor_pos[0] == len(self.game_grid.grid) - 1:
                    pass
                else:
                    cursor_pos[0] = cursor_pos[0] + 1
            elif command == curses.KEY_LEFT:
                if cursor_pos[1] == 0:
                    pass
                else:
                    cursor_pos[1] = cursor_pos[1] - 1
            elif command == curses.KEY_RIGHT:
                if cursor_pos[1] == len(self.game_grid.grid[0]) - 1:
                    pass
                else:
                    cursor_pos[1] = cursor_pos[1] + 1
            elif command == -1:
                pass
            else:
                self.game_grid.edit_map(cursor_pos[0], cursor_pos[1], command)

    def run_grid(self, time_delay=0.05):
        self.stdscr.nodelay(True)
        while True:
            self.title = "Running"
            self.draw_grid()
            command = self.stdscr.getch()
            if command == 113:
                self.stdscr.nodelay(False)
                return
            elif command == 101:
                state = self.edit_grid()
                if state == 0:
                    pass
                else:
                    self.stdscr.nodelay(False)
                    return
            elif command == 112:
                self.title = "Paused"
                self.draw_grid()
                self.stdscr.nodelay(False)
                while True:
                    command = self.stdscr.getch()
                    if command == 113:
                        return
                    elif command == 103:
                        self.stdscr.nodelay(True)
                        break
                    elif command == 101:
                        self.stdscr.nodelay(True)
                        state = self.edit_grid()
                        if state == 0:
                            break
                        else:
                            self.stdscr.nodelay(False)
                            return
                    else:
                        self.stdscr.addstr(len(self.game_grid.grid)+1, 0, 'Command not recognised.')
                        self.stdscr.refresh()
            elif command == curses.KEY_UP:
                if time_delay > 0.01:
                    time_delay -= 0.01
            elif command == curses.KEY_DOWN:
                time_delay += 0.01
            elif command == curses.KEY_RIGHT:
                time_delay = 0.05
            self.game_grid.evolve()
            time.sleep(time_delay)

    def run_prog(self):
        while True:
            if self.draw_welcome() == 0:
                self.run_grid()
            else:
                break
