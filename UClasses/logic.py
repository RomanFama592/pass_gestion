from tkinter import Tk, filedialog as filed
from time import localtime
import os
if __name__ != '__main__':
    import UClasses.bd as bd
else: import bd


def initDB(pathBD: str, pathKey: str, table: tuple, initWord: str):
    if not os.path.exists(pathBD) & os.path.exists(pathKey):
        createTable(pathBD, table)
        bd.generateKey(pathKey)
        hashinitWord = bd.encryptData(pathKey, initWord.encode())
        if hashinitWord != (None):
            bd.query(pathBD, f"insert into {table[0]} (initWord, hashInitWord) values (?, ?)", (initWord.encode(), hashinitWord))
    elif os.path.exists(pathBD) & os.path.exists(pathKey):
        return '2'
    elif os.path.exists(pathBD):
        return '1.bd'
    elif os.path.exists(pathKey):
        return '1.key'

def verifyBD(pathBD, pathKey, table):
    if os.path.exists(pathBD) & os.path.exists(pathKey):
        if table[0] in bd.query(pathBD, "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%'", returnData=True, sizeReturn='all')['name']:
            initWordAndHash = bd.query(pathBD, f"SELECT initWord, hashInitWord FROM {table[0]};", returnData=True, sizeReturn='one')
            if initWordAndHash['initWord'] == bd.desEncryptData(pathKey, initWordAndHash['hashInitWord']):
                return True
            elif initWordAndHash == None:
                return [True, False]
            else:
                return [True, True]
        else:
            return [False, False]
    else:
        return False

def extractData(pathBD, pathKey, tableName, withColumnsnames: bool = True):
    if os.path.exists(pathBD):
        return bd.query(pathBD, f'SELECT * FROM {tableName}', returnData=True, sizeReturn='all', withColumnsnames=withColumnsnames)
    else:
        print('no existe')

def createTable(pathBD: str, table: tuple):
    bd.query(pathBD, f"CREATE TABLE IF NOT EXISTS {table[0]} {table[1]}")

#funciones utiles
def browsePath(browseFolder: bool, title: str, mainTypeText: str=..., mainType: str=...):
    """
    It opens a window that allows you to select a file or folder and returns the path of the selected
    file or folder
    
    :param browseFolder: If you want to browse a folder, set this to True. If you want to browse a file,
    set this to False
    :type browseFolder: bool
    :param title: The title of the window
    :type title: str
    :param mainTypeText: The text that appears in the file type selector
    :type mainTypeText: str
    :param mainType: The type of file you want to open. For example, if you want to open a text file,
    you would put "*.txt"
    :type mainType: str
    :return: The path of the file or folder selected by the user.
    
    - str(title) = titulo de ventana por ejemplo 'Seleccione un archivo...' [obligatorio]
    - bool(browseFolder) = si lo buscado es una carpeta tendria que ingresar True, de lo contrario False [obligatorio]
    - str(mainTypeText) = lo que dice el selector de archivos por ejemplo 'txt files [opcional si browseFolder es False]'
    - str(mainType) = el tipo de archivo por ejemplo '*txt' [opcional si browseFolder es False]"""
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    if browseFolder:
        path = filed.askdirectory(title = title)
    else:
        path = filed.askopenfilename(title = title, filetypes = ((mainTypeText, mainType),("All files", "*.*")))
    return path

def timeNow():
    """
    It returns the number of seconds since the start of the current minute
    
    :return: The time in seconds.
    """
    tiempo = localtime()
    #tiempo = str(tiempo.tm_hour) + ':' + str(tiempo.tm_min) + ':' + str(tiempo.tm_sec) + '.'
    tiempo = (tiempo.tm_min*60) + tiempo.tm_sec
    return tiempo

'''def LoadPasswordOpera():
    """Devuelve un Data frame"""
    path = browsePath(False, 'Select Opera password file', 'CSV files', '*.csv')
    PasswordsOri = pd.read_csv(path,sep=',', index_col=False)
    PasswordsOri = PasswordsOri.fillna('')
    PasswordsOri.to_excel(pathBD, sheet_name='Account', index=False)'''

if __name__ == '__main__':
    pass