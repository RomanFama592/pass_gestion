from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder

KV = """
#<KvLang>

#</KvLang>
"""

class Settings(MDScreen):
    name = 'Settings'
    Builder.load_string(KV)
