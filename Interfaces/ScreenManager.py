from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder
from kivy.properties import *
#from kivymd.icon_definitions import md_icons

# root.manager.resibleFont(self.height, self.width, 0.5)

Builder.load_string("""
#<KvLang>
#:include Interfaces\Menu.kv
#:include Interfaces\Setting.kv
#:include Interfaces\Lock.kv
#:include Interfaces\MasterInterfaces.kv

<MainScreenManager>:
    LockInter:
    MasterInterfaces:
#</KvLang>
""")

class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #print(self._get_screen_names())

    def ChangeScreen(self, screen):
        screen = self.get_screen(screen)
        self.switch_to(screen)

    def resibleFont(self, x, y, font):
        """font tiene que ser del 0 al 1."""
        if x < y:
            return x * font
        elif x > y:
            return y * font
        else: 
            return y * font

class MasterInterfaces(MDScreen):
    name = 'MI'
    def __init__(self, **kw):
        super().__init__(**kw)

class SettingInter(MDScreen):
    name = 'Settings'
    def __init__(self, **kw):
        super().__init__(**kw)

class MenuInter(MDScreen):
    name = 'Menu'
    def __init__(self, **kw):
        super().__init__(**kw)

class LockInter(MDScreen):
    name = 'Lock'
    def __init__(self, **kw):
        super().__init__(**kw)