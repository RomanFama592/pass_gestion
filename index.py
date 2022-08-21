from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty

from Interfaces.Components import *
from Interfaces.Screens import *

import os, darkdetect

"""f'C:/Users/{getuser()}/Documents'"""
#self.query(f"CREATE TABLE IF NOT EXISTS {self.tables[-1][0]} {self.tables[-1][1]}")
# root.manager.resibleFont(self.height, self.width, 0.5)

if not os.path.exists('indexddsfsdfsdf.py'):
    pathOrigin = os.getcwd()
    initWord = f'nene que se porta mal'
    formatBD = f'.bdpg'
    formatKey = f'.key'
    pathBD = f'{pathOrigin}\Database{formatBD}'
    pathKey = f'{pathOrigin}\encryptionKey{formatKey}'
    paleta = 'Cyan'
    tema = ''
else:
    pass

#Aplicacion
class AppMain(MDApp):
    pathOrigin = StringProperty(pathOrigin)
    initWord = StringProperty(initWord)
    formatBD = StringProperty(formatBD)
    formatKey = StringProperty(formatKey)
    pathBD = StringProperty(pathBD)
    pathKey = StringProperty(pathKey)
    paleta = StringProperty(paleta)
    tema = StringProperty(tema)
    title = 'PassGestion'
    version = StringProperty('alpha')
    
    def build(self):
        #Window.size = (1200, 700)
        #SnackbarPers() = SnackbarPers()
        #Clock.schedule_interval(self.updatePaletteSnackbar, 1)
        Window.bind(on_dropfile=self.on_filedrop)

        self.theme_cls.material_style = 'M3'
        self.theme_cls.primary_palette = self.paleta
        self.sm = MainScreenManager()

        if tema == '':
            self.sm.validateThemeUpdate = True
        else:
            self.sm.validateThemeUpdate = False
            self.theme_cls.theme_style = tema
        
        return self.sm

    def updatePaletteSnackbar(self, *args):
        if SnackbarPers().bg_color != Aplicacion.theme_cls.primary_light if Aplicacion.theme_cls.theme_style == 'Dark' else Aplicacion.theme_cls.primary_dark:
            SnackbarPers().bg_color = Aplicacion.theme_cls.primary_light if Aplicacion.theme_cls.theme_style == 'Dark' else Aplicacion.theme_cls.primary_dark

    def on_filedrop(self, window, pathname: bytes):
        """
        If the file dropped is a database, then the path of the database is saved in the variable
        self.pathBD, and the text of the textinput is changed to the path of the database.
        If the file dropped is a key, then the path of the key is saved in the variable self.pathKey,
        and the text of the textinput is changed to the path of the key.
        If the file dropped is neither a database nor a key, then a snackbar is shown saying that the
        file is not a valid file.
        
        :param window: The window that the file was dropped on
        :param pathname: The path to the file that was dropped
        :type pathname: bytes
        """
        pathname = pathname.decode()

        if self.formatBD.replace('.', '') == pathname.split(".")[-1]:
            self.pathBD = self.sm.current_screen.ids['DB path'].text = pathname
            SnackbarPers(text = f'Tiraste una base de datos: {os.path.basename(pathname)}').open()
        elif self.formatKey.replace('.', '') == pathname.split(".")[-1]:
            self.pathKey = self.sm.current_screen.ids['Key path'].text = pathname
            SnackbarPers(text=f'Tiraste una llave: {os.path.basename(pathname)}').open()
        else:
            SnackbarPers(text=f'El archivo {os.path.basename(pathname)} no se reconoce como un archivo valido.').open()

    def on_stop(self):
        print('y se acabo')
        return super().on_stop()

#screenmanager
class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        Builder.load_string("""
#<KvLang>
<MainScreenManager>:
    LockInter:
    MasterInterfaces:
#</KvLang>
""")
        self.validateThemeUpdate = True
        Clock.schedule_once(self.themeUpdate)
        Clock.schedule_interval(self.themeUpdate, 30)
        super().__init__(**kwargs)
        #print(self._get_screen_names())

    def themeUpdate(self, *args):
        """
        If the user has the dark mode enabled, the app will automatically change to the dark mode
        """
        if self.validateThemeUpdate:
            if darkdetect.theme() is not None:
                Aplicacion.theme_cls.theme_style = darkdetect.theme()

    def resibleFont(self, x, y, font):
        """
        If the width is less than the height, return the width multiplied by the font size. If the width
        is greater than the height, return the height multiplied by the font size. If the width is equal
        to the height, return the height multiplied by the font size
        
        :param x: The width of the screen
        :param y: The height of the screen
        :param font: The font size
        :return: the value of the font size.
        """
        """font tiene que ser del 0 al 1."""
        if x < y:
            return x * font
        elif x > y:
            return y * font
        else: 
            return y * font

Aplicacion = AppMain()
Aplicacion.run()