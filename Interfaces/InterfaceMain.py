from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder

KV = """
#<KvLang>

#</KvLang>
"""

class InterfaceMain(MDScreen):
    name = 'InterfaceMain'
    Builder.load_string(KV)