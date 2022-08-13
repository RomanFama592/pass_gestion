from tkinter import Tk, filedialog as filed
from time import localtime
import os
if __name__ != '__main__':
    import UClasses.bd as bd
else: import bd


def initDB(pathBD, pathKey, table, initWord):
    if not os.path.exists(pathBD) & os.path.exists(pathKey):
        bd.query(pathBD, f"CREATE TABLE IF NOT EXISTS {table[0]} {table[1]}")
        bd.generateKey(pathKey)
        hashinitWord = bd.encryptData(pathKey, initWord.encode())
        if hashinitWord != (None):
            bd.query(pathBD, f"insert into {table[0]} (initWord, hashInitWord) values (?, ?)", (initWord.encode(), hashinitWord))
    elif os.path.exists(pathBD) & os.path.exists(pathKey):
        pass
    elif os.path.exists(pathBD):
        pass
    elif os.path.exists(pathKey):
        pass


def verifyBD(pathBD, pathKey, table):
    if os.path.exists(pathBD) & os.path.exists(pathKey):
        print('a')
        if table[0] in bd.query(pathBD, f"SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%'", returnData=True):
            print('b')
            initWordAndHash = bd.query(pathBD, f"SELECT initWord, hashInitWord FROM {table[0]};", returnData=True)
            print('c')
            if initWordAndHash[0] == bd.desEncryptData(pathKey, initWordAndHash[1]):
                return 
            elif initWordAndHash == None:
                return [False, True]
        else:
            return [False, False]
    else:
        return False

#funciones utiles
def browsePath(browseCarpeta, title, mainTypeText: str=..., mainType: str=...):
    """- str(title) = titulo de ventana por ejemplo 'Seleccione un archivo...' [obligatorio]
    - bool(browseCarpeta) = si lo buscado es una carpeta tendria que ingresar True, de lo contrario False [obligatorio]
    - str(mainTypeText) = lo que dice el selector de archivos por ejemplo 'txt files [opcional si browseCarpeta es False]'
    - str(mainType) = el tipo de archivo por ejemplo '*txt' [opcional si browseCarpeta es False]"""
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    if browseCarpeta == True:
        path = filed.askdirectory(title = title)
    else:
        path = filed.askopenfilename(title = title, filetypes = ((mainTypeText, mainType),("All files", "*.*")))
    return path

def timeNow():
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