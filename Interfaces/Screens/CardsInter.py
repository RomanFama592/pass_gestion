from Interfaces.Components import ScreenCustomizable
from Interfaces.Components import get_app

class CardsInter(ScreenCustomizable):
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
#</KvLang>
"""
