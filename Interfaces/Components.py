from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDIconButton

from kivymd.app import App
from kivy.lang import Builder

from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.metrics import  dp, sp

import Utils.logic as logic

get_app = App.get_running_app

#Componentes personalizados
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
    position = "bottom"
    border_margin = dp(24)
    elevation = 16
    radius = [10, 40, 10, 40]
    max_height = 500

class MDTooltipPers(MDTooltip):
    showOnce = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_dismiss(self):
        if self.showOnce:   
            self.tooltip_text = ''
        return super().on_dismiss()

    def on_double_tap(self, *args):
        pass

    def on_triple_tap(self, *args):
        pass

    def on_quad_touch(self, *args):
        pass

class FloatingButton(MDFloatingActionButton, MDTooltipPers):
    icon = "plus"
    tooltip_text = "Añade un elemento en la lista en cualquier pantalla"
    shift_y = dp(100)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {"center_x": 0.9}
        self.pos = (0, "70dp")
        self.size = (dp(10), dp(10))
        self.elevation = 10
        self.tooltip_bg_color = get_app().theme_cls.primary_color
        
    def on_release(self):
        screen = get_app().sm.get_screen("MI").children[1].children[1].current_screen
        try:    
            screen.showdata.addRow()
        except:
            print(f'En {screen.name} no se puede usar este boton')
        return super().on_release()

class MDBottomNavigationItemPers(MDBottomNavigationItem):
    name = ''
    kv = ''
    hiddenInputs = ListProperty()
    loadShowdata = True
    initTable = True
    saveNameInJSON = True

    def __init__(self, *args, **kwargs):
        self.text = self.name
        Builder.load_string(self.kv)
        super().__init__(*args, **kwargs)
        
    def on_enter(self, *args):
        if self.initTable:
            logic.createTable(get_app().pathBD, self.table)
            self.initTable = False
        
        if self.loadShowdata: 
            self.loadTheShowData()
            self.loadShowdata = False

        if self.saveNameInJSON:
            get_app().primaryScreen = self.name
        return super().on_enter(*args)

    def loadTheShowData(self): #WIP reference
        self.showdata = Showdata(tableName = self.table[0], hiddenInputs=self.hiddenInputs)
        self.children[0].add_widget(self.showdata)




#mostrador desplazable de filas
class Showdata(MDScrollView):
    size_hint = (0.9, 1)
    pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    spacing = 10
    tableName = StringProperty()
    hiddenInputs = ListProperty()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = self.loadData()
        self.stacklayout = MDStackLayout(orientation='bt-lr',
                                        size_hint_y=None)        
        self.add_widget(self.stacklayout)
        self.paintingRows()

    def paintingRows(self):
        self.data = self.loadData()
        for datos in reversed(self.data[0]):
            self.stacklayout.add_widget(ListItemPers(table=self.tableName, id=str(datos[0]), idex=self.data[1], datos=datos, withHideIcon=self.hiddenInputs))
        self.stacklayout.height = sum(x.height for x in self.stacklayout.children)

    def addRow(self):
        logic.createEmptyRow(get_app().pathBD, self.tableName, self.data[1])
        self.stacklayout.add_widget(ListItemPers(table=self.tableName, id=str(logic.countRowsInTable(get_app().pathBD, self.tableName)), idex=self.data[1], datos=['' if datos != 'id' else logic.countRowsInTable(get_app().pathBD, self.tableName) for datos in self.data[1]], withHideIcon=self.hiddenInputs, initPassword=False))
        self.stacklayout.height = sum(x.height for x in self.stacklayout.children)

    def reloadRows(self):
        self.stacklayout.clear_widgets()
        self.paintingRows()

    def loadData(self): #finalizar
        rows = logic.extractData(get_app().pathBD, get_app().pathKey, self.tableName, 5)
        if rows == '1.bd':
            SnackbarPers(text='La base de datos se encuentra fuera de su lugar').open()
        elif rows == '1.query': #la query no se pudo hacer
            SnackbarPers(text='Error desconocido que viene de la base de datos').open()
        else:
            return rows

#contenedor de textFields
class ListItemPers(MDBoxLayout):
    orientation = 'horizontal'
    size_hint = (1, None)
    height = NumericProperty(dp(30))
    spacing = 10
    table = StringProperty()
    withHideIcon = ListProperty()
    initPassword = BooleanProperty(True)

    def __init__(self, datos: list, idex: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for text, id in zip(datos, idex):
            if id == 'id':
                self.add_widget(MDLabel(id=id, text=str(text)))
            elif id in self.withHideIcon:
                self.add_widget(MDTextFieldRows(idex=str(id), text=str(text if text != None else ''), password=self.initPassword))
            else:
                self.add_widget(MDTextFieldRows(idex=str(id), text=str(text if text != None else '')))
        self.hideIcon = MDIconButton(icon="eye" if self.initPassword else "eye-off", on_release=self.hidePasswords)
        self.add_widget(self.hideIcon)

    def hidePasswords(self, instance):
        print(instance)
        for child in self.children:
            if isinstance(child, MDTextFieldRows):
                if child.idex in self.withHideIcon:
                    child.password = not child.password
                    instance.icon = "eye" if instance.icon == "eye-off" else "eye-off"

#TextField para Showdata
class MDTextFieldRows(MDTextField, MDTooltipPers):
    idex = StringProperty()
    mode = 'fill'
    showOnce = False

    def __init__(self, **kwargs):
        self.AncientText = ''
        super().__init__(**kwargs)
        if not self.password:
            self.tooltip_text = self.text
        else:
            self.tooltip_text = ''

#WIP
    def on_focus(self, instance_text_field, focus: bool):
        if focus:
            self.AncientText = self.text
        else:
            if self.AncientText != self.text: 
                logic.insertData(get_app().pathBD, get_app().pathKey,
                instance_text_field.parent.table, instance_text_field.parent.id,
                instance_text_field.idex, instance_text_field.text)
        return super().on_focus(instance_text_field, focus)

    def on_enter(self, *args):
        if self.password:
            self.tooltip_text = ''
        else:
            self.tooltip_text = self.text
        return super().on_enter(*args)

