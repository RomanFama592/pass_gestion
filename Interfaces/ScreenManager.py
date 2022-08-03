from kivy.uix.screenmanager import ScreenManager

#Screens
if __name__ != '__main__':
    from Interfaces.InterfaceMain import InterfaceMain
    from Interfaces.Setting import Settings
    from Interfaces.Unlock import Unlock


class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for screen in [Unlock(), InterfaceMain(), Settings()]:
            self.add_widget(screen)
        #print(self._get_screen_names())