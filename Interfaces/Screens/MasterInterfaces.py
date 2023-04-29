from kivymd.uix.screen import MDScreen
from kivy.app import Builder
from Interfaces.Components import FloatingButton, get_app

from Interfaces.Screens import (
    ErrorInter,
    PasswordsInter,
    SettingInter,
    CardsInter,
    # importar nuevas pantallas aqui.
)


class MasterInterfaces(MDScreen):
    name = "MI"
    kv = """
#<KvLang>
<MasterInterfaces>:
    MDBottomNavigation:
        id: sms
        ErrorInter:
#</KvLang>
"""

    def __init__(self, **kw):
        super().__init__(**kw)
        Builder.load_string(self.kv)

    def on_kv_post(self, base_widget):
<<<<<<< HEAD
        screensToAdd = [PasswordsInter.PasswordsInter, 
        CardsInter.CardsInter, SettingInter.SettingInter]
        for screen in screensToAdd:
            self.ids['sms'].add_widget(screen())
=======
        screensToAdd = [
            PasswordsInter.PasswordsInter,
            CardsInter.CardsInter,
            SettingInter.SettingInter,
            # Una vez importadas añadir la clase de la screen aqui
        ]
        for screen in screensToAdd:
            self.ids["sms"].add_widget(screen())
>>>>>>> main
        self.add_widget(FloatingButton())
        return super().on_kv_post(base_widget)
