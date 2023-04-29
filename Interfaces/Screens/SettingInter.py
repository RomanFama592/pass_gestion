from Interfaces.Components import ScreenCustomizable
from Interfaces.Components import get_app

class SettingInter(ScreenCustomizable):
    name = 'Settings'
    icon = 'minus'
    table = ('userconfigs',"""(
                                id integer not null primary key autoincrement,
                                initWord blob not null,
                                hashInitWord blob not null
                                )""")
    kv = """
#<KvLang>
<SettingInter>:
    MDBoxLayout:
#</KvLang>
    """
    loadShowdata = False
    initTable = False
    saveNameInJSON = False

    def on_tab_press(self, *args):
        get_app().sm.get_screen("MI").children[0].hideButton()
        return super().on_tab_press(*args)

    def on_pre_leave(self, *args):
        get_app().sm.get_screen("MI").children[0].showButton()
        return super().on_pre_leave(*args)