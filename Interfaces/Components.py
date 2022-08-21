from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.snackbar import Snackbar
from kivymd.app import App
from kivy.lang import Builder
from sys import getsizeof

from kivy.properties import StringProperty, NumericProperty
from kivy.metrics import  dp, sp

import UClasses.logic as logic, os

get_app = App.get_running_app

#presets de kv
class MDBottomNavigationItemPers(MDBottomNavigationItem):
    name = ''
    kv = ''
    loadShowdata = True
    initTable = True

    def __init__(self, *args, **kwargs):
        self.text = self.name
        Builder.load_string(self.kv)
        super().__init__(*args, **kwargs)
        
    def on_enter(self, *args):
        """
        It creates a table if it doesn't exist
        :return: The return value of the superclass's on_pre_enter method.
        """
        if self.initTable:
            logic.createTable(get_app().pathBD, self.table)
            self.initTable = False
        
        if self.loadShowdata:
            rows = logic.extractData(get_app().pathBD, get_app().pathKey, self.table[0], withColumnsnames=False)
            if not rows == None: 
                self.showdata = Showdata()
                self.children[0].add_widget(self.showdata)
                self.showdata.paintingRows(rows)
                self.loadShowdata = False
        
        return super().on_enter(*args)

class MDBoxLayoutPers(MDBoxLayout, RoundedRectangularElevationBehavior):
    pass

class SnackbarPers(Snackbar):
    snackbar_animation_dir = 'Top'
    font_size = sp(20)
    duration = 1
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = get_app().theme_cls.primary_light if get_app().theme_cls.theme_style == 'Dark' else get_app().theme_cls.primary_dark

class DropMenuPers(MDDropdownMenu):
    hor_growth = "right"
    elevation = 16
    position = "center"
    radius = [10, 40, 10, 40]
    max_height = 500

class ListItemPers(MDBoxLayout):
    orientation = 'horizontal'
    size_hint = (1, None)
    height = NumericProperty(dp(30))
    spacing = 10

    def __init__(self, datos: list ,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for text in datos:
            self.add_widget(MDTextField(text=str(text), mode='fill'))

class Showdata(MDScrollView):
    size_hint = (0.9, 1)
    pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stacklayout = MDStackLayout(orientation='tb-lr',
                                        size_hint_y=None) #cada que se añada un item recalcular el height
        #self.stacklayout.height = sum(x.height for x in self.stacklayout.children)
        self.add_widget(self.stacklayout)
    
    def paintingRows(self, data: list):
        for datos in data:
            self.stacklayout.add_widget(ListItemPers(datos=datos))
        self.stacklayout.height = sum(x.height for x in self.stacklayout.children)
