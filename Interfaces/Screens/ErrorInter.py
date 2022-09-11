from Interfaces.Components import MDBottomNavigationItemPers
from Interfaces.Components import get_app

class ErrorInter(MDBottomNavigationItemPers):
    name = 'Error'
    textInformation = 'No se porque estas viendo esto pero te diria que no te voltees'
    kv = """
#<KvLang>
<ErrorInter>:
    MDLabel:
        text: root.textInformation
        halign: 'center'
#</KvLang>
        """
    loadShowdata = False
    initTable = False
    saveNameInJSON = False
