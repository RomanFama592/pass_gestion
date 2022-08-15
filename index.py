from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.metrics import  dp
from kivymd.uix.snackbar import Snackbar
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.clock import Clock
from kivymd.color_definitions import palette
from UClasses import logic, bd
from kivy.properties import StringProperty
from getpass import getuser
import os, darkdetect

"""f'C:/Users/{getuser()}/Documents'"""
#self.query(f"CREATE TABLE IF NOT EXISTS {self.tables[-1][0]} {self.tables[-1][1]}")
# root.manager.resibleFont(self.height, self.width, 0.5)

pathOrigin = os.getcwd()
initWord = f'nene que se porta mal'
formatBD = f'.bdpg'
formatKey = f'.key'
pathBD = f'{pathOrigin}\Database{formatBD}'
pathKey = f'{pathOrigin}\encryptionKey{formatKey}'

Builder.load_string("""
#<KvLang>
#:include Interfaces\Passwords.kv
#:include Interfaces\Setting.kv
#:include Interfaces\Lock.kv

<MainScreenManager>:
    LockInter:
    PasswordsInter:
    SettingInter:
#</KvLang>
""")

#Aplicacion
class AppMain(MDApp):
    pathOrigin = StringProperty(pathOrigin)
    initWord = StringProperty(initWord)
    formatBD = StringProperty(formatBD)
    formatKey = StringProperty(formatKey)
    pathBD = StringProperty(pathBD)
    pathKey = StringProperty(pathKey)
    title = 'PassGestion'

    def build(self):
        #Window.size = (1200, 700)
        self.theme_cls.material_style = 'M3'
        Window.bind(on_dropfile=self.on_filedrop)
        self.sm = MainScreenManager()
        return self.sm

    def on_filedrop(self, window, pathname: bytes):
        pathname = pathname.decode()
        snackbar = SnackbarPers()
        snackbar.bg_color = self.theme_cls.primary_dark
        snackbar.size_hint_x = (Window.width - 20.0) / Window.width
        if self.formatBD.replace('.', '') == pathname.split(".")[-1]:
            self.pathBD = self.sm.current_screen.ids['DB path'].text = pathname
            snackbar.text = f'Tiraste una base de datos: {os.path.basename(pathname)}'
            snackbar.open()
        elif self.formatKey.replace('.', '') == pathname.split(".")[-1]:
            self.pathKey = self.sm.current_screen.ids['Key path'].text = pathname
            snackbar.text = f'Tiraste una llave: {os.path.basename(pathname)}'
            snackbar.open()
        else: 
            snackbar.text = f'El archivo {os.path.basename(pathname)} no se reconoce como un archivo valido.'
            snackbar.open()

    def on_stop(self):
        print('y se acabo')
        return super().on_stop()
    
#screenmanager
class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validateThemeUpdate = True
        Clock.schedule_once(self.themeUpdate)
        Clock.schedule_interval(self.themeUpdate, 30)
        #print(self._get_screen_names())

    def themeUpdate(self, *args):
        if self.validateThemeUpdate:
            if darkdetect.theme() is not None:
                Aplicacion.theme_cls.theme_style = darkdetect.theme()

    def resibleFont(self, x, y, font):
        """font tiene que ser del 0 al 1."""
        if x < y:
            return x * font
        elif x > y:
            return y * font
        else: 
            return y * font

#screens
class MasterInterfaces(MDScreen):
    name = 'MI'
    def __init__(self, **kw):
        super().__init__(**kw)

class SettingInter(MDScreen):
    name = 'Settings'
    table = ('userconfigs',"""(
                                id integer not null primary key autoincrement,
                                initWord blob not null,
                                hashInitWord blob not null
                                )""")

class PasswordsInter(MDScreen):
    name = 'Passwords'
    table = ('accounts', """(
                            id integer not null primary key autoincrement,
                            namepages blob not null,
                            urls blob not null,
                            users blob,
                            passwords blob
                            )""")
    
    def on_pre_enter(self, *args):
        bd.query(pathBD, f"CREATE TABLE IF NOT EXISTS {self.table[0]} {self.table[1]}")
        print('a')
        return super().on_pre_enter(*args)

class LockInter(MDScreen):
    name = 'Lock'

    def on_kv_post(self, base_widget):
        self.listPaletteColors = [
           {
            "viewclass": "IconListItem",
            "text": f"Tema {i}",
            "height": dp(40),
            "on_release": lambda x=i: self.PaletteColorsSelect(self.menu.caller, x)
            } 
            for i in palette
            ]
        themes = ['Light', 'Dark', 'Automatic For SO']
        self.listThemes = [
           {
            "viewclass": "IconListItem",
            "text": f"Tema {i}",
            "height": dp(40),
            "on_release": lambda x=i: self.ThemeSelect(self.menu.caller, x)
            } 
            for i in themes
            ]
        self.menu = DropMenuPers()
        return super().on_kv_post(base_widget)

    def Browser(self, instance, BDorKey: bool, broserFolders: bool):
        """BDorKey: True is BD and False is Key
            selectOrfind: True is select and find is False"""
        if broserFolders:
            if BDorKey:
                instance.text = Aplicacion.pathBD = logic.browsePath(True, 'Selecciona la base de datos', 'Base de datos PG files', f'*{Aplicacion.formatBD}')
            else:
                instance.text = Aplicacion.pathKey = logic.browsePath(True,'Selecciona la llave de la base de datos', 'Key files', f'*{Aplicacion.formatKey}')
        else:
            if BDorKey:
                instance.text = Aplicacion.pathBD = os.path.join(logic.browsePath(False, 'Selecciona la base de datos'), f'DBof{getuser()}')
            else:
                instance.text = Aplicacion.pathKey = os.path.join(logic.browsePath(False,'Selecciona la llave de la base de datos'), f'Keyof{getuser()}')

    def Login(self):
        snackbar = SnackbarPers()
        snackbar.bg_color = Aplicacion.theme_cls.primary_dark
        snackbar.size_hint_x = (Window.width - 20.0) / Window.width
        Aplicacion.pathBD = self.ids['DB path'].text
        Aplicacion.pathKey = self.ids['Key path'].text
        
        verifyIntegrity = logic.verifyBD(Aplicacion.pathBD, Aplicacion.pathKey, SettingInter.table)
        if verifyIntegrity == True:
            Aplicacion.sm.switch_to(Aplicacion.sm.get_screen(PasswordsInter().name))
        elif verifyIntegrity == [False, True]:
            snackbar.text = 'La llave no es correspondiente a la base de datos'
            snackbar.open()        
        elif verifyIntegrity == [True, False]:
            snackbar.text = 'La llave esta dañada'
            snackbar.open()    
        elif verifyIntegrity == [False, False]:
            snackbar.text = 'La base de datos no funciona'
            snackbar.open()
        elif verifyIntegrity == False:
            snackbar.text = 'La base de datos no existe'
            snackbar.open()
        else:
            snackbar.text = 'Error desconocido'
            snackbar.open()

    def CreateBD(self):
        verificationCreateDB = False
        verificationCreateDBs = False

        if Aplicacion.formatBD in os.path.basename(self.ids['DB path'].text):
            Aplicacion.pathBD = self.ids['DB path'].text
            verificationCreateDB = True
        else:
            verificationCreateDB = False
            self.error(self.ids['DB path'])

        if Aplicacion.formatBD in os.path.basename(self.ids['DB path'].text):
            Aplicacion.pathBD = self.ids['Key path'].text
            verificationCreateDBs = True
        else:
            verificationCreateDBs = False
            self.error(self.ids['Key path'])
        
        if verificationCreateDB & verificationCreateDBs:
            logic.initDB(Aplicacion.pathBD, Aplicacion.pathKey, SettingInter.table, Aplicacion.initWord)
        else:
            print('ta mal')

    def error(self, instance):
        instance.error == True

    def PaletteColorsSelect(self, Dropitem, text_item):
        Dropitem.set_item = text_item
        Dropitem.text = text_item
        Aplicacion.theme_cls.primary_palette = text_item
        self.menu.dismiss()
    
    def ThemeSelect(self, Dropitem, text_item):
        Dropitem.set_item = text_item
        Dropitem.text = text_item
        if text_item == 'Automatic For SO':
            Aplicacion.sm.validateThemeUpdate = True
            Aplicacion.theme_cls.theme_style = darkdetect.theme()
        else:
            Aplicacion.sm.validateThemeUpdate = False
            Aplicacion.theme_cls.theme_style = text_item
        self.menu.dismiss()

#presets de kv
class MDBoxLayoutPers(MDBoxLayout, RoundedRectangularElevationBehavior):
    pass

class SnackbarPers(Snackbar):
    snackbar_x=dp(10)
    snackbar_y = Window.height - 70
    snackbar_animation_dir = 'Top'
    font_size = '20sp'

class DropMenuPers(MDDropdownMenu):
    hor_growth = "right"
    elevation = 16
    position = "center"
    radius = [10, 40, 10, 40]
    max_height = 500

Aplicacion = AppMain()
Aplicacion.run()