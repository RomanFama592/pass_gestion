from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.snackbar import Snackbar
from kivymd.app import App
from kivy.lang import Builder

from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.metrics import  dp, sp

import Utils.logic as logic

get_app = App.get_running_app

#presets de kv
class MDBottomNavigationItemPers(MDBottomNavigationItem):
    name = ''
    kv = ''
    hiddenInputs = ListProperty()
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
            rows = logic.extractData(get_app().pathBD, get_app().pathKey, self.table[0], 5)
            if not rows == None: 
                self.showdata = Showdata(data=rows, tableName = self.table[0], hiddenInputs=self.hiddenInputs)
                self.children[0].add_widget(self.showdata)
                self.loadShowdata = False
        return super().on_enter(*args)
        
class FloatingButton(MDFloatingActionButton):
    icon = "plus"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {"center_x": 0.9}
        self.pos = (0, "70dp")
        self.elevation = 10

    def on_release(self):
        screen = get_app().sm.get_screen("MI").children[1].children[1].current_screen
        try:    
            screen.showdata.addRow()
        except:
            print(f'En {screen.name} no se puede usar este boton')
        return super().on_release()

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

class MDTextFieldRows(MDTextField):
    idex = StringProperty()
    mode = 'fill'
    password = BooleanProperty(False)

    def on_focus(self, instance_text_field, focus: bool) -> None:
        if not focus:
            if self.AncientText != self.text: 
                logic.insertData(get_app().pathBD, get_app().pathKey, instance_text_field.parent.table, instance_text_field.parent.id, instance_text_field.idex, instance_text_field.text)
        else:
            self.AncientText = self.text
        return super().on_focus(instance_text_field, focus)

    def on_double_tap(self):
        if self.password:
            self.password = False
        else:
            self.password = True
        return super().on_double_tap()

class ListItemPers(MDBoxLayout):
    orientation = 'horizontal'
    size_hint = (1, None)
    height = NumericProperty(dp(30))
    spacing = 10
    table = StringProperty()
    withHideIcon = ListProperty()

    def __init__(self, datos: list, idex: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for text, id in zip(datos, idex):
            if id == 'id':
                self.add_widget(MDLabel(id=id, text=str(text)))
            elif id in self.withHideIcon:
                self.add_widget(MDTextFieldRows(idex=str(id), text=str(text if text != None else ''), password=BooleanProperty(True)))
            else:
                self.add_widget(MDTextFieldRows(idex=str(id), text=str(text if text != None else '')))

class Showdata(MDScrollView):
    size_hint = (0.9, 1)
    pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    spacing = 10
    data = ListProperty()
    tableName = StringProperty()
    hiddenInputs = ListProperty()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stacklayout = MDStackLayout(orientation='bt-lr',
                                        size_hint_y=None) #cada que se añada un item recalcular el height
        #self.stacklayout.height = sum(x.height for x in self.stacklayout.children)
        self.add_widget(self.stacklayout)
        self.paintingRows()
    
    def paintingRows(self):
        for datos in reversed(self.data[0]):
            self.stacklayout.add_widget(ListItemPers(table=self.tableName, id=str(datos[0]), idex=self.data[1], datos=datos, withHideIcon=self.hiddenInputs))
        self.stacklayout.height = sum(x.height for x in self.stacklayout.children)
    
    def addRow(self):
        logic.createEmptyRow(get_app().pathBD, self.tableName, self.data[1])
        self.stacklayout.add_widget(ListItemPers(table=self.tableName, id=str(logic.countRowsInTable(get_app().pathBD, self.tableName)), idex=self.data[1], datos=['' if datos != 'id' else logic.countRowsInTable(get_app().pathBD, self.tableName) for datos in self.data[1]], withHideIcon=self.hiddenInputs))
        self.stacklayout.height = sum(x.height for x in self.stacklayout.children)


