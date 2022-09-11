from kivymd.uix.screen import MDScreen
from kivy.app import Builder
import os
from Interfaces.Components import FloatingButton, get_app
from Interfaces.Screens import CardsInter, ErrorInter, PasswordsInter, SettingInter

class MasterInterfaces(MDScreen):
    name = 'MI'
    kv = """
#<KvLang>
<MasterInterfaces>:
    MDBottomNavigation:
        id: sms
        ErrorInter:
        PasswordsInter:
        CardsInter:
        SettingInter:
#</KvLang>
"""
    def __init__(self, **kw):
        Builder.load_string(self.kv)
        super().__init__(**kw)

    def on_kv_post(self, base_widget):
        self.add_widget(FloatingButton())
        return super().on_kv_post(base_widget)