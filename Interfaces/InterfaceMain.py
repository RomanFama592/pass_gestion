from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder

KV = """
#<KvLang>

#</KvLang>
"""

class InterfaceMain(Screen):
    name = 'InterfaceMain'
    Builder.load_string(KV)