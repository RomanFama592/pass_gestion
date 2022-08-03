from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder

KV = """
#<KvLang>
MDScreen:
<MDScreen>:
    BoxLayout:
        id: boxlayoutCentral
        Button:
            text: '2'
            on_release: root.hi(*args)
        Button:
            text: '1'
            on_release: root.hi(*args)
#</KvLang>
"""

class Unlock(MDScreen):
    name = 'Unlock'
    Builder.load_string(KV)
    
    def hi(self, a):
        bt = Button(text=a.text, on_release=self.hi)
        self.ids.boxlayoutCentral.add_widget(bt)