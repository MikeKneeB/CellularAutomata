from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.core.window import Window

from cellauto.grids.life import LifeGrid
from cellauto.grids.ant import AntGrid

class CellGrid(Widget):
    def __init__(self, game_grid=None, **kwargs):
        super(CellGrid, self).__init__(**kwargs)

        self.cell_size = 3

        self.cell_x = self.width / self.cell_size
        self.cell_y = self.height / self.cell_size

        if game_grid == None:
            self.game_grid = LifeGrid(50, 50, [1,2,5], [3,6])
        else:
            self.game_grid = game_grid

        self.game_grid.rebuild(int(self.cell_y), int(self.cell_x))
        self.game_grid.random_grid(0.4)

        self.square_pos = (200, 200)

        with self.canvas:
            Color(1.0,0,0)
            Rectangle(pos=self.square_pos, size=(10,10))

    def update(self):
        self.game_grid.evolve()
        with self.canvas:
            self.canvas.clear()
            for i, row in enumerate(self.game_grid.grid):
                for j, item in enumerate(row):
                    if item != 0:
                        Rectangle(pos=(j*self.cell_size,i*self.cell_size + 50), size=(self.cell_size, self.cell_size))


    def test_action(self):
        self.square_pos = (self.square_pos[0]+10, self.square_pos[1]+10)

    def random_grid(self):
        self.game_grid.random_grid(0.4)

    def size_callback(self, instance, value):
        self.cell_x = self.width / self.cell_size
        self.cell_y = self.height / self.cell_size
        self.game_grid.rebuild(int(self.cell_y), int(self.cell_x))
        # print('{} {}'.format(self.cell_x, self.cell_y))

class CellControl(BoxLayout):
    def __init__(self, cell_grid, **kwargs):
        super(CellControl, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.button_one = Button(text='Button!')
        self.button_two = Button(text='Button"')
        self.add_widget(self.button_one)
        self.add_widget(self.button_two)

        self.button_one.bind(on_press=self.re_roll)

        self.cell_grid = cell_grid

    def re_roll(self, instance):
        self.cell_grid.random_grid()

class MainScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.grid = CellGrid(size_hint=(1,1))
        self.grid.bind(size=self.grid.size_callback)
        self.cont = CellControl(self.grid, size=(200,50), size_hint=(1,None))
        self.add_widget(self.grid)
        self.add_widget(self.cont)

    def update(self, dt):
        self.grid.update()

class CellApp(App):

    def build(self):
        main = MainScreen()
        Clock.schedule_interval(main.update, 0.2)
        Window.size = (400, 400)
        return main

if __name__ == '__main__':
    CellApp().run()
