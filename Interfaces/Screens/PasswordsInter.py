from Interfaces.Components import MDBottomNavigationItemPers
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
        orientation: 'vertical'
        MDRelativeLayout:
            size_hint: 1, 0.2
#</KvLang>
    """
