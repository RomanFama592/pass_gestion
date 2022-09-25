from Interfaces.Components import MDBottomNavigationItemPers, MDBoxLayoutPers, Showdata
from Interfaces.Components import get_app

class PasswordsInter(MDBottomNavigationItemPers):
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
            size_hint: 1, 0.2
            MDTextField:
                id: search
                mode: 'fill'
                pos_hint: {'center_x': 0.1, 'center_y': 0.5}
#</KvLang>
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_enter(self, *args):
        super().on_enter(*args)
        self.ids['search'].set_text = self.searching

    def searching(self, *args):
        if args[1] == '':
            self.showdata.amountRows = 5
            self.showdata.search = args[1]
            self.showdata.reloadRows()
        else:
            self.showdata.amountRows = 'all'
            self.showdata.search = args[1]
            self.showdata.reloadRows()
