from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder

KV = """
#<KvLang>
<Unlock>:
    Button:
        text: "a"

#</KvLang>
"""

class Unlock(Screen):
    name = 'Unlock'
    Builder.load_string(KV)