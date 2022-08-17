from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.metrics import  dp, sp
from kivymd.uix.snackbar import Snackbar
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.button import MDIconButton
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from kivymd.color_definitions import palette
from UClasses import logic, bd
from kivy.properties import StringProperty, ObjectProperty
from getpass import getuser
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

Builder.load_string("""
#<KvLang>
#:include Interfaces\Passwords.kv
#:include Interfaces\Setting.kv
#:include Interfaces\Lock.kv
#:include Interfaces\MasterInterfaces.kv

<MainScreenManager>:
    LockInter:
    MasterInterfaces:
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
    paleta = StringProperty(paleta)
    tema = StringProperty(tema)
    title = 'PassGestion'
    
    def build(self):
        #Window.size = (1200, 700)
        self.theme_cls.material_style = 'M3'
        self.theme_cls.primary_palette = self.paleta
        Window.bind(on_dropfile=self.on_filedrop)
        self.sm = MainScreenManager()
        return self.sm

    def on_filedrop(self, window, pathname: bytes):
        pathname = pathname.decode()

        if self.formatBD.replace('.', '') == pathname.split(".")[-1]:
            self.pathBD = self.sm.current_screen.ids['DB path'].text = pathname
            SnackbarPers(text=f'Tiraste una base de datos: {os.path.basename(pathname)}',
            bg_color = Aplicacion.theme_cls.primary_light if Aplicacion.theme_cls.theme_style == 'Dark' else Aplicacion.theme_cls.primary_dark,
            ).open()
        elif self.formatKey.replace('.', '') == pathname.split(".")[-1]:
            self.pathKey = self.sm.current_screen.ids['Key path'].text = pathname
            SnackbarPers(text=f'Tiraste una llave: {os.path.basename(pathname)}',
            bg_color = Aplicacion.theme_cls.primary_light if Aplicacion.theme_cls.theme_style == 'Dark' else Aplicacion.theme_cls.primary_dark,
            ).open()
        else:
            SnackbarPers(text=f'El archivo {os.path.basename(pathname)} no se reconoce como un archivo valido.',
            bg_color = Aplicacion.theme_cls.primary_light if Aplicacion.theme_cls.theme_style == 'Dark' else Aplicacion.theme_cls.primary_dark,
            ).open()

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
    
    def on_kv_post(self, base_widget):
        for i in self.ids['sms'].screens:
            if i.name != 'Error':
                iconClick = Icondock(icon='android',screenState=i.name, instance=self, icon_size=dp(60))
                self.ids['dock'].add_widget(iconClick)
        return super().on_kv_post(base_widget)

class ErrorInter(MDScreen):
    name = 'Error'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Builder.load_string("""
#<KvLang>
#</KvLang>
""")

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

    def on_enter(self, *args):
        #bd.query(Aplicacion.pathBD, f"CREATE TABLE IF NOT EXISTS {self.table[0]} {self.table[1]}")
        return super().on_pre_enter(*args)

    def on_kv_post(self, base_widget):
        for i in range(0, 100):
            self.ids['stacklayout'].add_widget(Button(text=str(i+1), size_hint=(1, None), height=dp(50)))
        return super().on_kv_post(base_widget)

class LockInter(MDScreen):
    name = 'Lock'

    def on_kv_post(self, base_widget):
        self.listPaletteColors = [
           {
            "viewclass": "IconListItem",
            "text": i,
            "height": dp(40),
            "on_release": lambda x=i: self.PaletteColorsSelect(self.menu.caller, x)
            } 
            for i in palette
            ]
        self.listThemes = [
           {
            "viewclass": "IconListItem",
            "text": i,
            "height": dp(40),
            "on_release": lambda x=i: self.ThemeSelect(self.menu.caller, x)
            }
            for i in ['Light', 'Dark', 'Automatic For SO']
            ]
        self.menu = DropMenuPers()
        return super().on_kv_post(base_widget)

    def Browser(self, instance, BDorKey: bool, broserFolders: bool):
        """BDorKey: True is BD and False is Key
            selectOrfind: True is select and find is False"""
        if broserFolders:
            if BDorKey:
                instance.text = Aplicacion.pathBD = os.path.join(logic.browsePath(broserFolders, 'Selecciona la base de datos'), f'DB_of_{getuser()}{Aplicacion.formatBD}')
            else:
                instance.text = Aplicacion.pathKey = os.path.join(logic.browsePath(broserFolders,'Selecciona la llave de la base de datos'), f'Key_of_{getuser()}{Aplicacion.formatKey}')
        else:
            if BDorKey:
                instance.text = Aplicacion.pathBD = logic.browsePath(broserFolders, 'Selecciona la base de datos', 'Base de datos PG files', f'*{Aplicacion.formatBD}')
            else:
                instance.text = Aplicacion.pathKey = logic.browsePath(broserFolders,'Selecciona la llave de la base de datos', 'Key files', f'*{Aplicacion.formatKey}')

    def Login(self):
        Aplicacion.pathBD = self.ids['DB path'].text
        Aplicacion.pathKey = self.ids['Key path'].text

        verifyIntegrity = logic.verifyBD(Aplicacion.pathBD, Aplicacion.pathKey, SettingInter.table)
        if verifyIntegrity == True:
            Aplicacion.sm.switch_to(Aplicacion.sm.get_screen(MasterInterfaces.name))
            Aplicacion.sm.get_screen(MasterInterfaces().name).ids['sms'].current = PasswordsInter().name
        elif verifyIntegrity == [False, True]:
            SnackbarPers(text='La llave no es correspondiente a la base de datos',
            bg_color = Aplicacion.theme_cls.primary_light if Aplicacion.theme_cls.theme_style == 'Dark' else Aplicacion.theme_cls.primary_dark,
            ).open()
        elif verifyIntegrity == [True, False]:
            SnackbarPers(text='La llave esta dañada',
            bg_color = Aplicacion.theme_cls.primary_light if Aplicacion.theme_cls.theme_style == 'Dark' else Aplicacion.theme_cls.primary_dark,
            ).open()
        elif verifyIntegrity == [False, False]:
            SnackbarPers(text='La base de datos no funciona',
            bg_color = Aplicacion.theme_cls.primary_light if Aplicacion.theme_cls.theme_style == 'Dark' else Aplicacion.theme_cls.primary_dark,
            ).open()
        elif verifyIntegrity == False:
            SnackbarPers(text='La base de datos no existe',
            bg_color = Aplicacion.theme_cls.primary_light if Aplicacion.theme_cls.theme_style == 'Dark' else Aplicacion.theme_cls.primary_dark,
            ).open()
        else:
            SnackbarPers(text='Error desconocido',
            bg_color = Aplicacion.theme_cls.primary_light if Aplicacion.theme_cls.theme_style == 'Dark' else Aplicacion.theme_cls.primary_dark,
            ).open()

    def CreateBD(self):
        verificationCreateDB = False
        verificationCreateDBs = False

        if Aplicacion.formatBD in os.path.basename(self.ids['DB path'].text):
            Aplicacion.pathBD = self.ids['DB path'].text
            verificationCreateDB = True
        else:
            verificationCreateDB = False
            self.error(self.ids['DB path'])

        if Aplicacion.formatKey in os.path.basename(self.ids['Key path'].text):
            Aplicacion.pathKey = self.ids['Key path'].text
            verificationCreateDBs = True
        else:
            verificationCreateDBs = False
            self.error(self.ids['Key path'])
        
        if verificationCreateDB & verificationCreateDBs:
            verification = logic.initDB(Aplicacion.pathBD, Aplicacion.pathKey, SettingInter.table, Aplicacion.initWord)
            if verification == None:
                pass
            elif verification == '2':
                SnackbarPers(text='ya existen los dos archivos en la ruta indicada',
                            bg_color = Aplicacion.theme_cls.primary_light if Aplicacion.theme_cls.theme_style == 'Dark' else Aplicacion.theme_cls.primary_dark).open()


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

class MDAnchorLayoutPers(MDAnchorLayout, RoundedRectangularElevationBehavior):
    pass

class SnackbarPers(Snackbar):
    snackbar_animation_dir = 'Top'
    font_size = sp(20)
    duration = 1

class DropMenuPers(MDDropdownMenu):
    hor_growth = "right"
    elevation = 16
    position = "center"
    radius = [10, 40, 10, 40]
    max_height = 500

class Icondock(MDIconButton):
    screenState = StringProperty()
    instance = ObjectProperty()

    def on_release(self):
        self.instance.ids['sms'].current = self.screenState
        return super().on_release()

Aplicacion = AppMain()
Aplicacion.run()