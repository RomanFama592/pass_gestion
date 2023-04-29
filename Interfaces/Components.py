from kivymd.uix.behaviors import CommonElevationBehavior
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
from kivy.animation import Animation

from kivymd.app import App
from kivy.lang import Builder

from kivy.properties import (
    NumericProperty,
    StringProperty,
    ListProperty,
    BooleanProperty,
)
from kivy.metrics import dp, sp

import Utils.logic as logic

get_app = App.get_running_app


# Componentes personalizados
class MDBoxLayoutPers(MDBoxLayout, CommonElevationBehavior):
    pass


class SnackbarPers(Snackbar):
    snackbar_animation_dir = "Top"
    font_size = sp(20)
    duration = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = (
            get_app().theme_cls.primary_light
            if get_app().theme_cls.theme_style == "Dark"
            else get_app().theme_cls.primary_dark
        )


class DropMenuPers(MDDropdownMenu):
    position = "bottom"
    border_margin = dp(24)
    radius = [10, 40, 10, 40]
    max_height = 500

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.elevation = get_app().elevation


# veresta clase y arreglar el return super()
class MDTooltipPers(MDTooltip):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.showOnce = True

    def on_dismiss(self):
        super().on_dismiss()
        if self.showOnce:
            self.tooltip_text = ""

    def on_double_tap(self, *args):
        pass

    def on_triple_tap(self, *args):
        pass

    def on_quad_touch(self, *args):
        pass


class FloatingButton(MDFloatingActionButton, MDTooltipPers):
    icon = "plus"
    tooltip_text = "Añade un elemento en la lista en cualquier pantalla"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
<<<<<<< HEAD
        self.pos_hint = {"center_x": 0.9}
        self.pos = (0, dp(50))
=======
        self.pos_hint = {"center_x": 0.95}
        self.pos_y_origin = dp(40)
        self.pos = (0, self.pos_y_origin)
>>>>>>> main
        self.size = (dp(10), dp(10))
        self.elevation = get_app().elevation
        self.tooltip_bg_color = get_app().theme_cls.primary_color
        self.seeButton = True
<<<<<<< HEAD
        
=======

>>>>>>> main
    def on_release(self):
        screen = get_app().sm.get_screen("MI").children[1].children[1].current_screen
        try:
            screen.showdata.addRow()  # modificar hacia polimorfismo
        except:
            print(f"En {screen.name} no se puede usar este boton")
        return super().on_release()

    def hideButton(self):
        if self.seeButton:
            self.disabled = True
<<<<<<< HEAD
            animate = Animation(pos=(0, dp(15)+self.pos[1]), duration=0.05)
            animate += Animation(pos=(0, dp(-100)), duration=0.2)
            animate.start(self)
            self.seeButton = False
    
    def showButton(self):
        if not self.seeButton:
            def disableOff(*args):
                self.disabled = False
            animate = Animation(pos=(0, dp(70)), duration=0.2)
            animate.start(self)
            animate.bind(on_complete = disableOff)
            self.seeButton = True

class MDBottomNavigationItemPers(MDBottomNavigationItem):
    name = ''
    kv = ''
=======
            animate = Animation(pos=(0, self.pos[1] + dp(15)), duration=0.05)
            animate += Animation(pos=(0, -self.pos_y_origin * 2), duration=0.2)
            animate.start(self)
            self.seeButton = False

    def showButton(self):
        if not self.seeButton:

            def disableOff(*args):
                self.disabled = False

            animate = Animation(pos=(0, self.pos_y_origin), duration=0.2)
            animate.start(self)
            animate.bind(on_complete=disableOff)
            self.seeButton = True


class ScreenCustomizable(MDBottomNavigationItem):
    name = ""
    kv = ""
>>>>>>> main
    hiddenInputs = ListProperty()
    loadShowdata = True
    initTable = True
    saveNameInJSON = True

    def __init__(self, *args, **kwargs):
        self.text = self.name
        Builder.load_string(self.kv)
        super().__init__(*args, **kwargs)

    def on_enter(self, *args):
        super().on_enter(*args)
        if self.initTable:
            logic.createTable(get_app().pathBD, self.table)
            self.initTable = False

        if self.loadShowdata:
            self.loadTheShowData()
            self.loadShowdata = False

        if self.saveNameInJSON:
            get_app().primaryScreen = self.name

    def loadTheShowData(self):  # WIP reference
        self.showdata = Showdata(
            tableName=self.table[0], hiddenInputs=self.hiddenInputs
        )
        columns = ListItemPers(
            self.showdata.rows_name,
            self.showdata.rows_name,
            True,
            size_hint=(0.9, 0.1),
            pos_hint={"center_x": 0.5},
            md_bg_color=get_app().theme_cls.primary_dark,
            padding=5,
            radius=10,
        )
        # TODO: reorganizar
        self.children[0].padding = 5
        self.children[0].add_widget(columns)
        self.children[0].add_widget(self.showdata)


# mostrador desplazable de filas
class Showdata(MDScrollView):
    size_hint = (0.9, 1)
    pos_hint = {"center_x": 0.5, "center_y": 0.5}
    spacing = 10
    tableName = StringProperty()
    hiddenInputs = ListProperty()
    amountRows = 5
<<<<<<< HEAD
    search = ''
    
    #modificar en base a logic.extracData()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stacklayout = MDStackLayout(orientation='bt-lr',
                                        size_hint_y=None)        
=======
    search = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stacklayout = MDStackLayout(orientation="bt-lr", size_hint_y=None)
>>>>>>> main
        self.add_widget(self.stacklayout)
        self.paintingRows()

    """ 
    (
        [
            [1, 'gdfgdf', 'fdgdf', 'dfgdf', 'dfgdf'],
            [2, 'sdfsdf', 'sdfsdfs', 'sdfsdf', 'sdfsdf'],
        ],
        ['id', 'namepages', 'urls', 'users', 'passwords']
    )
    """

    # TODO: Añadir el uso de paginas en base a self.amountRows
    # TODO: Añadir el uso del buscador
    @logic.measure_time
    def paintingRows(self):
        self.data = self.loadData()
<<<<<<< HEAD
        print(list(self.data.keys()))
        for datos in [data for data in self.data]:
            self.stacklayout.add_widget(ListItemPers(table=self.tableName, id=str(datos[0]), idex=list(self.data.keys()), datos=datos, withHideIcon=self.hiddenInputs))
        self.stacklayout.height = sum(x.height for x in self.stacklayout.children)
=======
        self.rows_name = self.data[1]
>>>>>>> main

        for row in self.data[0]:
            row = ListItemPers(
                idex=self.rows_name.copy(),
                datos=row,
                all_label=True if row == self.data[1] else False,
                withHideIcon=self.hiddenInputs,
            )
            self.stacklayout.add_widget(row)

        self.calc_height()

    @logic.measure_time
    def addRow(self):
        logic.createEmptyRow(get_app().pathBD, self.tableName, self.rows_name.copy())
        # logic.countRowsInTable(get_app().pathBD, self.tableName)
        datos = [
            ""
            if datos != "id"
            else str(int(self.data[0][-1][self.rows_name.index(datos)]) + 1)
            for datos in self.rows_name
        ]
        row = ListItemPers(
            idex=self.rows_name.copy(),
            datos=datos,
            withHideIcon=self.hiddenInputs,
            initPassword=False,
        )
        self.data[0].append(datos)
        self.stacklayout.add_widget(row)

        self.calc_height()

    def calc_height(self):
        self.stacklayout.height = sum(x.height for x in self.stacklayout.children)

    def reloadRows(self):
        self.stacklayout.clear_widgets()
        self.paintingRows()

<<<<<<< HEAD
    def loadData(self): #finalizar
        rows = logic.extractData(get_app().pathBD, get_app().pathKey,
        self.tableName)
        if rows == '1.bd':
            SnackbarPers(text='La base de datos se encuentra fuera de su lugar').open()
        elif rows == '1.query': #la query no se pudo hacer
            SnackbarPers(text='Error desconocido que viene de la base de datos').open()
=======
    @logic.measure_time
    def loadData(self):
        rows = logic.extractData(get_app().pathBD, get_app().pathKey, self.tableName)
        if rows == "1.bd":
            SnackbarPers(text="La base de datos se encuentra fuera de su lugar").open()
        elif rows == "1.query":  # la query no se pudo hacer
            SnackbarPers(text="Error desconocido que viene de la base de datos").open()
>>>>>>> main
        else:
            return rows


# contenedor de textFields
class ListItemPers(MDBoxLayout):
    orientation = "horizontal"
    size_hint = (1, None)
    height = NumericProperty(dp(30))
    spacing = 10
    withHideIcon = ListProperty()
    initPassword = BooleanProperty(True)

    # TODO: OPTIMIZAR
    def __init__(self, datos: list, idex: list, all_label=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if all_label:
            for text, id in zip(datos, idex):
                if id != "id":
                    self.add_widget(MDLabel(text=str(text)))
        else:
            for text, id in zip(datos, idex):
                if id == "id":
                    self.id = str(text)
                    # ver ids
                    self.add_widget(MDLabel(text=str(text)))
                else:
                    self.add_widget(
                        MDTextFieldRows(
                            idex=str(id),
                            text=str(text if text != None else ""),
                            password=self.initPassword
                            if id in self.withHideIcon
                            else False,
                        )
                    )
        if not all_label:
            eye = MDIconButton(
                icon="eye" if self.initPassword else "eye-off",
                on_release=self.hidePasswords,
            )
            trash = MDIconButton(
                icon="trash-can",
                on_release=self.deleteRow,
            )
            self.icons = {"eye": eye, "trash": trash}
            for icon in self.icons.values():
                self.add_widget(icon)

    def deleteRow(self, instance):
        parent = self.parent
        logic.deleteRow(get_app().pathBD, parent.parent.tableName, self.id)
        parent.remove_widget(self)
        parent.calc_height()

    def hidePasswords(self, instance):
        for child in self.children:
            if isinstance(child, MDTextFieldRows) and child.idex in self.withHideIcon:
                child.password = not child.password

        instance.icon = "eye" if instance.icon == "eye-off" else "eye-off"


# TextField para Showdata
# TODO: arreglar los Tooltips
class MDTextFieldRows(MDTextField, MDTooltipPers):
    idex = StringProperty()
    mode = "fill"

    def __init__(self, password, **kwargs):
        super().__init__(**kwargs)
        self.showOnce = False
        self.AncientText = ""
        self.password = password
        self.touchIn = False

        if self.password:
            self.tooltip_text = ""
        else:
            self.tooltip_text = self.text

    def on_focus(self, instance_text_field, focus: bool):
        if focus:
            self.AncientText = self.text
            self.touchIn = True
        else:
            if not self.touchIn:
                # return super().on_focus(instance_text_field, focus)
                return True
            if not self.parent.initPassword:
                if not self.password:
                    self.parent.icons["eye"].dispatch("on_release")
                self.parent.initPassword = not self.parent.initPassword

            if self.AncientText != self.text:
                logic.insertData(
                    get_app().pathBD,
                    get_app().pathKey,
                    self.parent.parent.parent.tableName,
                    self.parent.id,
                    self.idex,
                    self.text,
                )
            self.touchIn = False
        return super().on_focus(instance_text_field, focus)

    def on_enter(self, *args):
        if self.password:
            self.tooltip_text = ""
        else:
            self.tooltip_text = self.text
        return super().on_enter(*args)
