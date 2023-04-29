<<<<<<< HEAD
from Interfaces.Components import MDBottomNavigationItemPers, MDBoxLayoutPers, Showdata
=======
from Interfaces.Components import ScreenCustomizable
>>>>>>> main
from Interfaces.Components import get_app

class PasswordsInter(ScreenCustomizable):
    name = 'Passwords'
    icon = 'plus'
    hiddenInputs = ['users', 'passwords']
    table = ('accounts', """(
                            id integer not null primary key autoincrement,
                            namepages blob not null,
                            urls blob not null,
                            users blob,
                            passwords blob
                            )""")
    kv = """
#<KvLang>
<PasswordsInter>:
    MDBoxLayout:
        id: base
        orientation: 'vertical'
        MDBoxLayout:
            id: top
<<<<<<< HEAD
            size_hint: 1, 0.2
            MDTextField:
                id: search
                mode: 'fill'
                pos_hint: {'center_x': 0.1, 'center_y': 0.5}
=======
            size_hint: 0.9, 0.15
            padding: 7
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            MDTextField:
                id: search
                hint_text: "Does Not Work"
                mode: 'fill'
                size_hint: 1, 1
>>>>>>> main
#</KvLang>
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
<<<<<<< HEAD
=======
        self.ids['search'].text_color = get_app().theme_cls.primary_light
        self.ids['search'].line_color_focus = get_app().theme_cls.primary_dark
        self.ids['search'].md_bg_color = get_app().theme_cls.bg_light
>>>>>>> main

    def on_enter(self, *args):
        super().on_enter(*args)
        self.ids['search'].set_text = self.searching

<<<<<<< HEAD
=======
    #sin implementar la busqueda
>>>>>>> main
    def searching(self, *args):
        if args[1] == '':
            self.showdata.amountRows = 5
            self.showdata.search = args[1]
            self.showdata.reloadRows()
        else:
            self.showdata.amountRows = 'all'
            self.showdata.search = args[1]
            self.showdata.reloadRows()
