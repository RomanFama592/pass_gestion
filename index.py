from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty

from Interfaces.Components import SnackbarPers, get_app
from Interfaces.Screens import LockInter, MasterInterfaces

import os, darkdetect, json, Utils.logic as logic

"""f'C:/Users/{getuser()}/Documents'"""
#self.query(f"CREATE TABLE IF NOT EXISTS {self.tables[-1][0]} {self.tables[-1][1]}")
# root.manager.resibleFont(self.height, self.width, 0.5)

def createJSON(pathSetting, pathBD, pathKey, initWord, paleta, tema):
    settingJson = json.dumps({'pathBD': pathBD,
                                'pathKey': pathKey,
                                'initWord': initWord,
                                'paleta': paleta,
                                'tema': tema},
                                ensure_ascii=True,
                                indent=1)
    with open(pathSetting, 'w') as settingFile:
        settingFile.write(settingJson)

#create variable initialization
pathOrigin = os.getcwd()
formatBD = f'.bdpg'
formatKey = f'.key'
pathSetting = os.path.join(pathOrigin, 'setting.json')

if os.path.exists(pathSetting):
    with open(pathSetting, 'r') as settingFile:
        settingJson = json.load(settingFile)
    initWord = settingJson.get('initWord', 'nene que se porta mal')
    pathBD = settingJson.get('pathBD', f'{pathOrigin}\Database{formatBD}')
    pathKey = settingJson.get('pathKey', f'{pathOrigin}\encryptionKey{formatKey}')
    paleta = settingJson.get('paleta', 'Cyan')
    tema = settingJson.get('tema', '')
else:
    initWord = 'nene que se porta mal'
    pathBD = f'{pathOrigin}\Database{formatBD}'
    pathKey = f'{pathOrigin}\encryptionKey{formatKey}'
    paleta = 'Cyan'
    tema = ''
    createJSON(pathSetting, pathBD, pathKey, initWord, paleta, tema)

#Aplicacion
class AppMain(MDApp):
    #variable initialization
    pathOrigin = StringProperty(pathOrigin)
    pathSetting = StringProperty(pathSetting)
    initWord = StringProperty(initWord)
    formatBD = StringProperty(formatBD)
    formatKey = StringProperty(formatKey)
    pathBD = StringProperty(pathBD)
    pathKey = StringProperty(pathKey)
    paleta = StringProperty(paleta)
    tema = StringProperty(tema)

    title = 'PassGestion'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.material_style = 'M3'
        self.theme_cls.primary_palette = self.paleta

    
    def build(self):
        Window.bind(on_drop_file=self._on_drop_file)
        self.sm = MainScreenManager()
        if tema == '':
            self.sm.validateThemeUpdate = True
        else:
            self.sm.validateThemeUpdate = False
            self.theme_cls.theme_style = tema
        return self.sm

    def _on_drop_file(self, window, pathname: bytes, x, y):
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

        if self.sm.current == LockInter.LockInter.name:
            if self.formatBD.replace('.', '') == pathname.split(".")[-1]:
                self.pathBD = self.sm.current_screen.ids['DB path'].text = pathname
                SnackbarPers(text = f'Tiraste una base de datos: {os.path.basename(pathname)}').open()
            elif self.formatKey.replace('.', '') == pathname.split(".")[-1]:
                self.pathKey = self.sm.current_screen.ids['Key path'].text = pathname
                SnackbarPers(text=f'Tiraste una llave: {os.path.basename(pathname)}').open()
            else:
                SnackbarPers(text=f'El archivo {os.path.basename(pathname)} no se reconoce como un archivo valido.').open()

    def on_stop(self):
        self.writeJSON()
        return super().on_stop()

    def writeJSON(self):
        if self.sm.validateThemeUpdate:
            createJSON(self.pathSetting, self.pathBD, self.pathKey, self.initWord, self.theme_cls.primary_palette, '')
        else:
            createJSON(self.pathSetting, self.pathBD, self.pathKey, self.initWord, self.theme_cls.primary_palette, self.theme_cls.theme_style)

#screenmanager
class MainScreenManager(MDScreenManager):
    kv = """
#<KvLang>
<MainScreenManager>:
    LockInter:
    MasterInterfaces:
#</KvLang>
"""
    
    def __init__(self, **kwargs):
        Builder.load_string(self.kv)
        self.validateThemeUpdate = True
        Clock.schedule_once(self.themeUpdate)
        Clock.schedule_interval(self.themeUpdate, 30)
        super().__init__(**kwargs)

    def themeUpdate(self, *args):
        """
        If the user has the dark mode enabled, the app will automatically change to the dark mode
        """
        if self.validateThemeUpdate:
            if darkdetect.theme() is not None:
                get_app().theme_cls.theme_style = darkdetect.theme()

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

AppMain().run()