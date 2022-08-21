from kivymd.uix.screen import MDScreen
from kivymd.color_definitions import palette
from kivy.app import Builder

from kivy.metrics import  dp, sp
from kivy.app import App
from Interfaces.Components import *
from UClasses import logic
from kivy.properties import StringProperty, NumericProperty
from getpass import getuser
import os, darkdetect

#screens
class LockInter(MDScreen):
    name = 'Lock'
    kv = """
#<KvLang>
<LockInter>:
    MDAnchorLayout: 
        anchor_y: 'center'
        anchor_x: 'center'
        md_bg_color: app.theme_cls.bg_light
        MDBoxLayoutPers:
            size_hint: 0.97, 0.97
            md_bg_color: app.theme_cls.primary_dark if app.theme_cls.theme_style == 'Dark' else app.theme_cls.primary_light
            radius: [10, 100, 10, 100]
            style: 'filled'
            elevation: 10
            MDLabel:
                text: 'Drop the files in this window.'
                font_size: '40sp'
                halign: "center"
                pos_hint: {"center_y": 0.7}
                opacity: 0.2
                color: app.theme_cls.primary_light if app.theme_cls.theme_style == 'Dark' else app.theme_cls.primary_dark
    MDBoxLayout:
        orientation: 'horizontal'
        size_hint: 0.4, 0.1
        pos_hint: {'x': 0.05, 'y': 0.85}
        padding: 10
        spacing: 10
        MDDropDownItem:
            id: PaletteColors
            text: 'Select a color: ' + app.theme_cls.primary_palette
            text_color: app.theme_cls.primary_light if app.theme_cls.theme_style == 'Dark' else app.theme_cls.primary_dark
            on_release:
                root.menu.caller = self
                root.menu.items = root.listPaletteColors
                root.menu.width_mult = 3.5
                root.menu.open()
        MDDropDownItem:
            id: Theme
            text: 'Select a theme: Automatic For SO' if app.tema == '' else ('Select a theme: ' + app.theme_cls.theme_style)
            text_color: app.theme_cls.primary_light if app.theme_cls.theme_style == 'Dark' else app.theme_cls.primary_dark
            on_release:
                root.menu.caller = self
                root.menu.items = root.listThemes
                root.menu.width_mult = 4.5
                root.menu.open()
    MDRelativeLayout:
        size: root.width, root.height
        MDBoxLayout:
            orientation: 'vertical'
            size_hint: 0.6, 0.5
            pos_hint: {'x': 0.1, 'y': 0.1}
            spacing: 20
            MDBoxLayout:
                orientation: 'vertical'
                spacing: 20
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: 5
                    MDTextField:
                        id: DB path
                        hint_text: 'Path of DB:'
                        text: app.pathBD
                        helper_text: "Double tap: Buscar Base de datos."
                        on_double_tap: root.Browser(self, True, False)
                        helper_text_mode: "on_focus"
                    MDIconButton:
                        icon: "plus"
                        icon_color: app.theme_cls.primary_color
                        on_release: root.Browser(self, True, True)
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: 5
                    MDTextField:
                        id: Key path
                        hint_text: 'Path of Key of the BD:'
                        text: app.pathKey
                        helper_text: "Double tap: Buscar una llave para la Base de datos."
                        on_double_tap: root.Browser(self, False, False)
                        helper_text_mode: "on_focus"
                    MDIconButton:
                        icon: "plus"
                        icon_color: app.theme_cls.primary_color
                        on_release: root.Browser(self, False, True)
            MDBoxLayout:
                size_hint: 1, 0.3
                orientation: 'horizontal'
                padding: 10
                spacing: 20
                MDRectangleFlatButton:
                    text: 'Login to this BD'
                    on_release: root.Login()
                    text_color: app.theme_cls.primary_light if app.theme_cls.theme_style == 'Dark' else app.theme_cls.primary_dark
                    line_color: app.theme_cls.primary_light if app.theme_cls.theme_style == 'Dark' else app.theme_cls.primary_dark
                MDRectangleFlatButton:
                    text: 'Create a new BD'
                    on_release: root.CreateBD()
                    text_color: app.theme_cls.primary_light if app.theme_cls.theme_style == 'Dark' else app.theme_cls.primary_dark
                    line_color: app.theme_cls.primary_light if app.theme_cls.theme_style == 'Dark' else app.theme_cls.primary_dark
#</KvLang>
    """

    def __init__(self, *args, **kwargs):
        Builder.load_string(self.kv)
        super().__init__(*args, **kwargs)
        
    def on_kv_post(self, base_widget):
        """
        It creates a list of dictionaries for the dropdown menu.
        
        :param base_widget: The widget that the menu is attached to
        :return: The super().on_kv_post(base_widget) is returning the super class of the class that is
        being called.
        """
        self.listPaletteColors = [
           {
            "viewclass": "OneLineIconListItem",
            "text": i,
            "height": dp(40),
            "on_release": lambda x=i: self.PaletteColorsSelect(self.menu.caller, x)
            } 
            for i in palette
            ]
        self.listThemes = [
           {
            "viewclass": "OneLineIconListItem",
            "text": i,
            "height": dp(40),
            "on_release": lambda x=i: self.ThemeSelect(self.menu.caller, x)
            }
            for i in ['Light', 'Dark', 'Automatic For SO']
            ]
        self.menu = DropMenuPers()
        return super().on_kv_post(base_widget)

    def Browser(self, instance, BDorKey: bool, broserFolders: bool):
        """
        It's a function that allows you to select a file or folder, depending on the value of the
        variable broserFolders, and depending on the value of the variable BDorKey, it will assign the
        path to the variable get_app().pathBD or get_app().pathKey.
        
        :param instance: is the text input
        :param BDorKey: True is BD and False is Key
        :type BDorKey: bool
        :param broserFolders: True is select folder and False is select file
        :type broserFolders: bool
        """
        """BDorKey: True is BD and False is Key
            selectOrfind: True is select and find is False"""
        if broserFolders:
            if BDorKey:
                instance.text = get_app().pathBD = os.path.join(logic.browsePath(broserFolders, 'Selecciona la base de datos'), f'DB_of_{getuser()}{get_app().formatBD}')
            else:
                instance.text = get_app().pathKey = os.path.join(logic.browsePath(broserFolders,'Selecciona la llave de la base de datos'), f'Key_of_{getuser()}{get_app().formatKey}')
        else:
            if BDorKey:
                instance.text = get_app().pathBD = logic.browsePath(broserFolders, 'Selecciona la base de datos', 'Base de datos PG files', f'*{get_app().formatBD}')
            else:
                instance.text = get_app().pathKey = logic.browsePath(broserFolders,'Selecciona la llave de la base de datos', 'Key files', f'*{get_app().formatKey}')

    def Login(self):
        """
        It verifies the integrity of the database and the key, and if it's correct, it switches to the
        main screen.
        """
        get_app().pathBD = self.ids['DB path'].text
        get_app().pathKey = self.ids['Key path'].text

        verifyIntegrity = logic.verifyBD(get_app().pathBD, get_app().pathKey, SettingInter.table)
        if verifyIntegrity == True:
            a = get_app().sm.get_screen(MasterInterfaces().name).ids['sms']
            a.children[1].remove_widget(a.children[1].current_screen)
            a.refresh_tabs()
            a.switch_tab(PasswordsInter().name)
            get_app().sm.switch_to(get_app().sm.get_screen(MasterInterfaces.name))
            get_app().sm.remove_widget(get_app().sm.get_screen(LockInter.name))
            del a
        elif verifyIntegrity == [False, True]:
            SnackbarPers(text='La llave no es correspondiente a la base de datos').open()
        elif verifyIntegrity == [True, True]:
            SnackbarPers(text='La llave esta dañada').open()
        elif verifyIntegrity == [False, False]:
            SnackbarPers(text='La base de datos no funciona').open()
        elif verifyIntegrity == False:
            SnackbarPers(text='La base de datos no existe').open()
        else:
            SnackbarPers(text='Error desconocido').open()

    def CreateBD(self):
        """
        It creates a database and a key file in the path that the user has indicated
        """
        verificationCreateDB = False
        verificationCreateDBs = False

        if get_app().formatBD in os.path.basename(self.ids['DB path'].text):
            get_app().pathBD = self.ids['DB path'].text
            verificationCreateDB = True
        else:
            verificationCreateDB = False
            self.error(self.ids['DB path'])

        if get_app().formatKey in os.path.basename(self.ids['Key path'].text):
            get_app().pathKey = self.ids['Key path'].text
            verificationCreateDBs = True
        else:
            verificationCreateDBs = False
            self.error(self.ids['Key path'])
        
        if verificationCreateDB & verificationCreateDBs:
            verification = logic.initDB(get_app().pathBD, get_app().pathKey, SettingInter.table, get_app().initWord)
            if verification == None:
                pass
            elif verification == '2':
                SnackbarPers(text='ya existen los dos archivos en la ruta indicada').open()
        else:
            print('ta mal')

    def error(self, instance):
        """
        It sets the error attribute of the instance to True.
        
        :param instance: The instance of the model that is being validated
        """
        instance.error = True

    def PaletteColorsSelect(self, Dropitem, text_item):
        """
        It sets the primary palette of the theme to the text_item that was selected in the dropdown menu
        
        :param Dropitem: The dropdown item that will be changed
        :param text_item: The text that will be displayed in the dropdown menu
        """
        Dropitem.set_item = text_item
        get_app().theme_cls.primary_palette = text_item
        self.menu.dismiss()
    
    def ThemeSelect(self, Dropitem, text_item):
        """
        It changes the theme of the application
        
        :param Dropitem: is the dropdown item that will be updated with the selected theme
        :param text_item: The text of the item selected in the dropdown menu
        """
        Dropitem.set_item = text_item
        if text_item == 'Automatic For SO':
            get_app().sm.validateThemeUpdate = True
            get_app().theme_cls.theme_style = darkdetect.theme()
            Dropitem.text = 'Select a theme: Automatic For SO'
        else:
            get_app().sm.validateThemeUpdate = False
            get_app().theme_cls.theme_style = text_item
            Dropitem.text = f'Select a theme: {text_item}'
        self.menu.dismiss()

class MasterInterfaces(MDScreen):
    name = 'MI'
    def __init__(self, **kw):
        Builder.load_string("""
#<KvLang>
<MasterInterfaces>:
    #añadir relative layout para el boton de +
    MDBottomNavigation:
        id: sms
        ErrorInter:
        PasswordsInter:
        SettingInter:
#</KvLang>
        """)
        super().__init__(**kw)

class ErrorInter(MDBottomNavigationItemPers):
    name = 'Error'
    kv = """
#<KvLang>
MDLabel:
    text: 'No se porque estas viendo esto ni que paso, pero dejame decirte que o sos suertudo o una locura informatica'
    halign: 'center'
#</KvLang>
        """
    loadShowdata = False
    initTable = False

class SettingInter(MDBottomNavigationItemPers):
    name = 'Settings'
    icon = 'minus'
    table = ('userconfigs',"""(
                                id integer not null primary key autoincrement,
                                initWord blob not null,
                                hashInitWord blob not null
                                )""")
    kv = """
#<KvLang>
<SettingInter>:
    MDBoxLayout:
#</KvLang>
    """

class PasswordsInter(MDBottomNavigationItemPers):
    name = 'Passwords'
    icon = 'plus'
    table = ('accounts', """(
                            id integer not null primary key autoincrement,
                            namepages blob not null,
                            urls blob not null,
                            users blob,
                            passwords blob
                            )""")
    kv = """
#<KvLang>
<PasswordsInter>:
    MDBoxLayout:
        orientation: 'vertical'
        MDRelativeLayout:
            size_hint: 1, 0.2
#</KvLang>
    """

