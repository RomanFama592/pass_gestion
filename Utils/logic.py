from tkinter import Tk, filedialog as filed
from time import localtime
import os, sqlite3
if __name__ != '__main__':
    import Utils.bd as bd
else: import bd


def initDB(pathBD: str, pathKey: str, table, initWord: str):
    if (not os.path.exists(pathBD)) & (not os.path.exists(pathKey)):
        if createTable(pathBD, table) == '1.bd':
            return '2.bd' # error al crear la base de datos
        if bd.generateKey(pathKey) == False:
            return '2.key' # error al crear la clave
        hashinitWord = bd.encryptData(pathKey, initWord)
        if hashinitWord == None:
            return '3.key' # error al encriptar
        elif hashinitWord == False:
            return '4.key' # error no existe la llave
        else:
            if bd.query(pathBD, f"insert into {table[0]} (initWord, hashInitWord) values (?, ?);", (initWord.encode(), hashinitWord)) == False:
                return '3.bd'
    elif os.path.exists(pathBD) & os.path.exists(pathKey):
        return '1'
    elif os.path.exists(pathBD):
        return '1.bd'
    elif os.path.exists(pathKey):
        return '1.key'

def verifyBD(pathBD, pathKey, tableName):
    """
    It checks if the database exists, if the key exists, if the table exists, and if the table has the
    correct password
    
    :param pathBD: The path to the database
    :param pathKey: The path to the key file
    :param table: a list with the name of the table
    :return: A list with two elements. The first element is a boolean value. The second element is a
    boolean value.
    """
    if os.path.exists(pathBD) & os.path.exists(pathKey):
        verifyTable = bd.query(pathBD, "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';", returnData=True, sizeReturn='all', dictwithrowaskey=True)['name']
        if tableName in verifyTable:
            initWordAndHash = bd.query(pathBD, f"SELECT initWord, hashInitWord FROM {tableName};", returnData=True, sizeReturn='one', dictwithrowaskey=True)
            if initWordAndHash == False:
                return '2.bd' #la base de datos esta dañada
            elif initWordAndHash == {}:
                return '2.bd'
            
            desEncryptReturn = bd.desEncryptData(pathKey, initWordAndHash['hashInitWord'])
            if desEncryptReturn == None:
                return '2.key' #la key no es valida
            
            if desEncryptReturn.encode() == initWordAndHash['initWord']:
                pass
            else:
                return '2.key'
        else:
            return '2.bd'
    elif (not os.path.exists(pathBD)) & (not os.path.exists(pathKey)):
        return '1'
    elif not os.path.exists(pathBD):
        return '1.bd'
    elif not os.path.exists(pathKey):
        return '1.key'
    
def extractData(pathBD, pathKey, tableName, quantityRows):
    data = bd.query(pathBD, f'SELECT * FROM {tableName} ORDER BY id desc', returnData=True, sizeReturn=quantityRows, returnNameofColumns=True)
    #WIP
    if data != False:
        dataNew = []
        for rows in data[0]:
            if isinstance(rows, tuple) or isinstance(rows, list):
                dataNew2 = []
                for columnValue in rows:
                    if isinstance(columnValue, bytes): 
                        dataNew2.append(bd.desEncryptData(pathKey, columnValue)) #puede error
                    else:
                        dataNew2.append(columnValue)
                dataNew.append(dataNew2)
        return (dataNew, data[1])
    elif data == False:
        return '1.query'
    elif data == None:
        return '1.bd'

def insertData(pathBD, pathKey, tableName, rowId, column, data):
    """
    It encrypts the data and then inserts it into the database
    
    :param pathBD: The path to the database file
    :param pathKey: The path to the key file
    :param tableName: The name of the table you want to insert data into
    :param rowId: The id of the row you want to update
    :param column: The column name in the table
    :param data: the data to be inserted
    """
    dataenc = bd.encryptData(pathKey, str(data))
    if dataenc == None:
        print('error encrypt')
    else:
        bd.query(pathBD, f"UPDATE {tableName} SET {column} = ? WHERE id = {rowId};", (dataenc,))
    print('insertado satis')

def createEmptyRow(pathBD, tableName, columns):
    """
    It creates an empty row in a table
    
    :param pathBD: The path to the database
    :param tableName: The name of the table you want to create a row in
    :param columns: a list of the columns in the table
    """
    bd.query(pathBD, f'INSERT INTO "{tableName}" {str([column for column in columns]).replace("[", "(").replace("]", ")")} VALUES {str(["" if column != "id" else str(countRowsInTable(pathBD, tableName)+1) for column in columns]).replace("[", "(").replace("]", ")")};')

def createTable(pathBD: str, table):
    """
    It creates a table in a database if it doesn't exist
    
    :param pathBD: The path to the database
    :type pathBD: str
    :param table: a list of two elements, the first is the name of the table, the second is the
    structure of the table
    """
    error = bd.query(pathBD, f"CREATE TABLE IF NOT EXISTS {table[0]} {table[1]};", createDB=True)
    if error == False:
        return '1.bd'

def countRowsInTable(pathBD: str, tableName):
    """
    It returns the number of rows in a table
    
    :param pathBD: str - path to the database
    :type pathBD: str
    :param tableName: the name of the table you want to count the rows of
    :return: The number of rows in the table.
    """
    countRows = bd.query(pathBD, f"SELECT COUNT(id) from {tableName}", returnData=True, dictwithrowaskey=True,sizeReturn='one')
    return countRows.get('COUNT(id)')


#funciones utiles
def verifyCodeError(result, dictWithErrors: dict, snackbar):
    if result == None:
        try:
            snackbar(text=dictWithErrors['None']).open()
        except:
            pass
    else:
        try:
            snackbar(text=dictWithErrors[result]).open()
        except:
            snackbar(text='error desconocido, consulte el LOG').open()

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