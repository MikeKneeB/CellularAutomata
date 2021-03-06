#Commmmmmmment

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

from cellauto.grids.life import LifeGrid
from cellauto.grids.generations import GeneGrid
#from cellauto.grids.probable_life import ProbLifeGrid
#from cellauto.grids.ant import AntGrid

class CellGrid(Widget):
    def __init__(self, game_grid=None, game_id=0, **kwargs):
        super(CellGrid, self).__init__(**kwargs)

        self.cell_size = 4
        self.threshold = 0.3

        self.cell_x = self.width / self.cell_size
        self.cell_y = self.height / self.cell_size

        if game_grid == None:
            self.game_grid = LifeGrid(50, 50, [1,2,5], [3,6])
        else:
            self.game_grid = game_grid

        self.game_id = game_id

        self.game_grid.rebuild(int(self.cell_y), int(self.cell_x))
        # self.game_grid.random_grid(self.threshold)

    def update(self, dt):
        self.game_grid.evolve()
        self.draw_once()

    def draw_once(self):
        with self.canvas:
            self.canvas.clear()
            for i, row in enumerate(self.game_grid.grid):
                for j, val in enumerate(row):
                    #val = self.game_grid.step_evolve(i, j)
                    if val == 1:
                        Color(1.0,1.0,1.0)
                        Rectangle(pos=(j*self.cell_size,i*self.cell_size + 50), size=(self.cell_size, self.cell_size))
                    elif val == 2:
                        Color(1.0,0,0)
                        Rectangle(pos=(j*self.cell_size,i*self.cell_size + 50), size=(self.cell_size, self.cell_size))
                    elif val == 3:
                        Color(1.0,0.5,0)
                        Rectangle(pos=(j*self.cell_size,i*self.cell_size + 50), size=(self.cell_size, self.cell_size))
                    elif val == 4:
                        Color(1.0,1.0,0)
                        Rectangle(pos=(j*self.cell_size,i*self.cell_size + 50), size=(self.cell_size, self.cell_size))
                    elif val == 5:
                        Color(0.5,1.0,0)
                        Rectangle(pos=(j*self.cell_size,i*self.cell_size + 50), size=(self.cell_size, self.cell_size))
                    elif val == 6:
                        Color(0,1.0,0)
                        Rectangle(pos=(j*self.cell_size,i*self.cell_size + 50), size=(self.cell_size, self.cell_size))
                    elif val == 7:
                        Color(0,1.0,0.5)
                        Rectangle(pos=(j*self.cell_size,i*self.cell_size + 50), size=(self.cell_size, self.cell_size))
                    elif val == 8:
                        Color(0,1.0,1.0)
                        Rectangle(pos=(j*self.cell_size,i*self.cell_size + 50), size=(self.cell_size, self.cell_size))
                    elif val == 9:
                        Color(0,0.5,1.0)
                        Rectangle(pos=(j*self.cell_size,i*self.cell_size + 50), size=(self.cell_size, self.cell_size))
                    elif val == 10:
                        Color(0,0,1.0)
                        Rectangle(pos=(j*self.cell_size,i*self.cell_size + 50), size=(self.cell_size, self.cell_size))
                    elif val == 11:
                        Color(0.5,0,1.0)
                        Rectangle(pos=(j*self.cell_size,i*self.cell_size + 50), size=(self.cell_size, self.cell_size))
                    elif val == 12:
                        Color(1.0,0,1.0)
                        Rectangle(pos=(j*self.cell_size,i*self.cell_size + 50), size=(self.cell_size, self.cell_size))
                    elif val == 13:
                        Color(1.0,0,0.5)
                        Rectangle(pos=(j*self.cell_size,i*self.cell_size + 50), size=(self.cell_size, self.cell_size))

    def test_action(self):
        self.square_pos = (self.square_pos[0]+10, self.square_pos[1]+10)

    def random_grid(self):
        self.game_grid.random_grid(self.threshold)

    def clear_grid(self):
        self.game_grid.clear_grid()

    def change_game_type(self, game_type):
        if game_type == 'Life':
            self.game_grid = LifeGrid(10,10)
            self.game_id = 0
        elif game_type == 'Generations':
            self.game_grid = GeneGrid(10,10, survive_list=[], birth_list=[2], generations=3)
            self.game_id = 1
        self.game_grid.rebuild(int(self.cell_y), int(self.cell_x))

    def size_callback(self, instance, value):
        self.cell_x = self.width / self.cell_size
        self.cell_y = self.height / self.cell_size
        self.game_grid.rebuild(int(self.cell_y), int(self.cell_x))
        # print('{} {}'.format(self.cell_x, self.cell_y))

    def on_touch_down(self, touch):
        if touch.y >= 50:
            self.game_grid.grid[int((touch.y - 50) / self.cell_size)][int(touch.x / self.cell_size)] = ((self.game_grid.grid[int((touch.y - 50) / self.cell_size)][int(touch.x / self.cell_size)] + 1) % 2)
            self.draw_once()
            touch.grab(self)
            # print('Clicky {} {} {}'.format(int((touch.y - 50) / self.cell_size), int(touch.x / self.cell_size), self.game_grid.grid[int((touch.y - 50) / self.cell_size)][int(touch.x / self.cell_size)]))

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            if touch.y >= 50:
                self.game_grid.grid[int((touch.y - 50) / self.cell_size)][int(touch.x / self.cell_size)] = 1
                self.draw_once()
            # print('Clicky')
        else:
            pass

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
        else:
            pass

class CellControl(BoxLayout):
    def __init__(self, cell_grid, **kwargs):
        super(CellControl, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        self.button_random = Button(text='Random')
        self.button_clear = Button(text='Clear')
        self.button_pause = Button(text='Pause')
        self.button_edit = Button(text='Edit')

        self.button_type = Button(text='Game Type')
        self.button_threshold = Button(text='Random\nthreshold')
        self.button_rules = Button(text='Rules')
        self.button_back = Button(text='Back')

        self.add_widget(self.button_random)
        self.add_widget(self.button_clear)
        self.add_widget(self.button_pause)
        self.add_widget(self.button_edit)

        self.cell_grid = cell_grid

        self.button_random.bind(on_press=self.re_roll)
        self.button_clear.bind(on_press=self.clear)

        self.run_event = Clock.schedule_interval(self.cell_grid.update, 0.2)
        self.running = True
        self.button_pause.bind(on_press=self.toggle_pause)

        self.button_edit.bind(on_press=self.edit_controls)
        self.button_back.bind(on_press=self.restore_controls)

        self.button_type.bind(on_press=self.change_type)
        self.button_threshold.bind(on_press=self.change_threshold)
        self.button_rules.bind(on_press=self.change_rules)

    def toggle_pause(self, instance):
        if self.running:
            self.run_event.cancel()
            self.running = False
            self.button_pause.text = 'Play'
        else:
            self.run_event = Clock.schedule_interval(self.cell_grid.update, 0.2)
            self.running = True
            self.button_pause.text = 'Pause'

    def re_roll(self, instance):
        self.cell_grid.random_grid()
        if not self.running:
            self.cell_grid.draw_once()

    def clear(self, instance):
        self.cell_grid.clear_grid()
        if not self.running:
            self.cell_grid.draw_once()

    def edit_controls(self, instance):
        self.remove_widget(self.button_random)
        self.remove_widget(self.button_clear)
        self.remove_widget(self.button_pause)
        self.remove_widget(self.button_edit)

        self.add_widget(self.button_type)
        self.add_widget(self.button_threshold)
        self.add_widget(self.button_rules)
        self.add_widget(self.button_back)

    def restore_controls(self, instance):
        self.remove_widget(self.button_type)
        self.remove_widget(self.button_threshold)
        self.remove_widget(self.button_rules)
        self.remove_widget(self.button_back)

        self.add_widget(self.button_random)
        self.add_widget(self.button_clear)
        self.add_widget(self.button_pause)
        self.add_widget(self.button_edit)

    def change_type(self, instance):

        def finished(instance):
            self.cell_grid.change_game_type(type_select.text)
            popup.dismiss()

        content = BoxLayout(orientation='horizontal')
        type_select = Spinner(text='Life',
            values=('Life', 'Generations'),
            size_hint=(1,1))
        close_button = Button(text='OK', size_hint=(None, 1), size=(50,100))
        content.add_widget(type_select)
        content.add_widget(close_button)
        close_button.bind(on_press=finished)

        popup = Popup(title='Choose Game Type', content=content, size=(300,100), size_hint=(None,None))
        popup.open()


    def change_threshold(self, instance):

        def finished(instance):
            try:
                inp_value = float(input_field.text)
                if 0 < inp_value < 1:
                    self.cell_grid.threshold = inp_value
            except ValueError:
                pass
            popup.dismiss()

        content = BoxLayout(orientation='horizontal')
        input_field = TextInput(size_hint=(1,1))
        close_button = Button(text='OK', size_hint=(None, 1), size=(50,100))
        content.add_widget(input_field)
        content.add_widget(close_button)
        close_button.bind(on_press=finished)

        popup = Popup(title='Enter New Threshold', content=content, size=(300,100), size_hint=(None,None))
        popup.open()

    def change_rules(self, instance):

        def all_unique(inp_list):
            seen = set()
            return not any(i in seen or seen.add(i) for i in inp_list)

        def finished(instance):
            try:
                survive_list = list(survive_input.text)
                create_list = list(create_input.text)
                survive_list = map(int, survive_list)
                create_list = map(int, create_list)
                if saved_selections.text == 'Manual Input':
                    if self.cell_grid.game_id == 1:
                        new_gen = int(generation_input.text)
                        if 0 < new_gen < 14:
                            self.cell_grid.game_grid.generations = new_gen
                    if any(i > 8 or i < 0 for i in survive_list) or not all_unique(survive_list):
                        pass
                    else:
                        self.cell_grid.game_grid.survive_list = survive_list

                    if any(i > 8 or i < 0 for i in create_list) or not all_unique(create_list):
                        pass
                    else:
                        self.cell_grid.game_grid.birth_list = create_list
                else:
                    if self.cell_grid.game_id == 0:
                        if saved_selections.text == 'Conway\'s Life':
                            self.cell_grid.game_grid.survive_list = [2,3]
                            self.cell_grid.game_grid.birth_list = [3]
                        elif saved_selections.text == '34 Life':
                            self.cell_grid.game_grid.survive_list = [3,4]
                            self.cell_grid.game_grid.birth_list = [3,4]
                        elif saved_selections.text == '2x2 Life':
                            self.cell_grid.game_grid.survive_list = [1,2,5]
                            self.cell_grid.game_grid.birth_list = [3,6]
                        elif saved_selections.text == 'Gnarl':
                            self.cell_grid.game_grid.survive_list = [1]
                            self.cell_grid.game_grid.birth_list = [1]
                        elif saved_selections.text == 'HighLife':
                            self.cell_grid.game_grid.survive_list = [2,3]
                            self.cell_grid.game_grid.birth_list = [3,6]
                        elif saved_selections.text == 'Maze':
                            self.cell_grid.game_grid.survive_list = [1,2,3,4,5]
                            self.cell_grid.game_grid.birth_list = [3]
                        elif saved_selections.text == 'Psuedo Life':
                            self.cell_grid.game_grid.survive_list = [2,3,8]
                            self.cell_grid.game_grid.birth_list = [3,5,7]
                        elif saved_selections.text == 'Serviettes':
                            self.cell_grid.game_grid.survive_list = []
                            self.cell_grid.game_grid.birth_list = [2,3,4]
                        elif saved_selections.text == 'Cities':
                            self.cell_grid.game_grid.survive_list = [2,3,4,5]
                            self.cell_grid.game_grid.birth_list = [4,5,6,7,8]
                        elif saved_selections.text == 'Mazectric':
                            self.cell_grid.game_grid.survive_list = [1,2,3,4]
                            self.cell_grid.game_grid.birth_list = [3]
            except ValueError:
                pass
            popup.dismiss()

        content = BoxLayout(orientation='vertical')
        content_manual = BoxLayout(orientation='horizontal')

        survive_input = TextInput(size_hint=(1,1))
        create_input = TextInput(size_hint=(1,1))
        close_button = Button(text='OK', size_hint=(None, 1), size=(50,100))
        content_manual.add_widget(survive_input)
        content_manual.add_widget(create_input)
        if self.cell_grid.game_id == 1:
            generation_input = TextInput(size_hint=(1,1))
            content_manual.add_widget(generation_input)
        content_manual.add_widget(close_button)
        close_button.bind(on_press=finished)

        saved_selections = Spinner(text='Manual Input')

        if self.cell_grid.game_id == 1:
            title = 'Enter New Generation Rules'
            size = (320,130)
            saved_selections.values = ('Manual Input')
        elif self.cell_grid.game_id == 0:
            title = 'Enter New Survive and Create Rules'
            size = (300,130)
            saved_selections.values = ('Manual Input', 'Conway\'s Life', '34 Life', '2x2 Life', 'Gnarl', 'HighLife', 'Maze', 'Mazectric', 'Psuedo Life', 'Serviettes', 'Cities')

        content.add_widget(saved_selections)
        content.add_widget(content_manual)

        popup = Popup(title=title, content=content, size=size, size_hint=(None,None))
        popup.open()

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.grid = CellGrid(size_hint=(1,1))
        self.grid.bind(size=self.grid.size_callback)
        self.cont = CellControl(self.grid, size=(200,50), size_hint=(1,None))
        self.add_widget(self.grid)
        self.add_widget(self.cont)

class CellApp(App):
    def build(self):
        main = MainScreen()
        #Window.size = (450, 500)
        return main

if __name__ == '__main__':
    CellApp().run()
