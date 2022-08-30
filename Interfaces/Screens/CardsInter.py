from Interfaces.Components import MDBottomNavigationItemPers
from Interfaces.Components import get_app

class CardsInter(MDBottomNavigationItemPers):
    name = 'Cards'
    icon = 'plus'
    hiddenInputs = ['numberCards', 'expirationDate', 'codSeg']
    table = ('cards', """(
                        id integer not null primary key autoincrement,
                        nameCards blob not null,
                        numberCards blob not null,
                        expirationDate blob not null,
                        codSeg blob not null
                        )""")
    kv = """
#<KvLang>
<CardsInter>:
    MDBoxLayout:
        orientation: 'vertical'
        MDRelativeLayout:
            size_hint: 1, 0.2
#</KvLang>
"""