from kivy.lang.builder import Builder
from kivymd.app import MDApp
import os
from Interfaces.ScreenManager import MainScreenManager

"""from getpass import getuser
f'C:/Users/{getuser()}/Documents'"""

#self.query(f"CREATE TABLE IF NOT EXISTS {self.tables[-1][0]} {self.tables[-1][1]}")

pathOrigin = os.getcwd()
initWord = 'nene que se porta mal'
formatBD = '.bdpg'
formatKey = '.key'
pathBD = f'{pathOrigin}\index{formatBD}'
pathKey = f'{pathOrigin}\GuardalaBien{formatKey}'

class AppMain(MDApp):
    title = 'PassGestion'
    def build(self):
        return MainScreenManager()

AppMain().run()