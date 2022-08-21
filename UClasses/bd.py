import sqlite3 as sql
from traceback import print_tb
from cryptography.fernet import Fernet
import base64 as b64
from hashlib import sha256

#mantener userconfigs en el ultimo puesto.
#RESOLVER
tables = [('cards', """(
                        id integer not null primary key autoincrement,
                        nameCards blob not null,
                        numberCards blob not null,
                        expirationDate blob not null,
                        codSeg blob not null
                        )"""),]

def cursorToListInList(rows, cursorDescripcion):
    """
    It takes a list of tuples and a cursor description and returns a dictionary of lists
    
    :param rows: the result of the query
    :param cursorDescripcion: This is the cursor description of the cursor that you're using to fetch
    the data
    :return: A dictionary with the column names as keys and the values as a list of values.
    """
    diccionario = {}
    rowsname = [row[0] for row in cursorDescripcion]

    if isinstance(rows, list):
        for i in rowsname:
            diccionario[i] = [row[rowsname.index(i)] for row in rows]
    elif isinstance(rows, tuple):
        for i in rowsname:
            diccionario[i] = rows[rowsname.index(i)]
    else:
        print('error cursor')
    
    return diccionario

#base de datos
def query(pathBD: str = ':memory:', command: str = '', parameters: tuple = (), returnData: bool = False, sizeReturn: str or int = '' or 0, executeMany: bool = False, withColumnsnames: bool = True):
    """
    It connects to a database, executes a command, and returns the data if the user wants it
    
    :param pathBD: The path to the database, defaults to :memory:
    :type pathBD: str
    
    :param command: The SQL command to be executed
    :type command: str
    
    :param parameters: a tuple of values to substitute for the placeholders in the command string. There
    :type parameters: tuple (optional)
    
    :param returnData: If you want to return the data from the query, set this to True, defaults to,
    defaults to False
    :type returnData: bool (optional)
    
    :param sizeReturn: lets choose how many rows are returned if returnData is true:
        "one": returns 1 single row.
        "all": returns all rows.   
        int(x): returns x number of rows. 
    :type sizeReturn: str or int
    
    :param executeMany: If you want to execute many commands at once, set this to True, defaults to,
    defaults to False
    :type executeMany: bool (optional)
    
    :return: A dict of lists with the names columns as the key.
    """
    conexion = sql.connect(pathBD)
    cursor = conexion.cursor()
    try:
        if executeMany:
            cursor.executemany(command, parameters)
        else:
            cursor.execute(command, parameters)
        conexion.commit()
    except:
        returnData = False
        print('error sql', command) #ver el tipo de error que devuelve al tener una sentencia errornea
    else:    
        if returnData:
            if withColumnsnames:
                if sizeReturn == 'one':
                    return cursorToListInList(cursor.fetchone(), cursor.description)
                elif isinstance(sizeReturn, int):
                    return cursorToListInList(cursor.fetchmany(sizeReturn), cursor.description)
                elif sizeReturn == 'all':
                    return cursorToListInList(cursor.fetchall(), cursor.description)
                else:
                    raise Exception(f'la variable sizeReturn no tiene un valor correspondiente, valor: {sizeReturn} en la consulta: {command}')
            else:    
                if sizeReturn == 'one':
                    return cursor.fetchone()
                elif isinstance(sizeReturn, int):
                    return cursor.fetchmany(sizeReturn)
                elif sizeReturn == 'all':
                    return cursor.fetchall()
                else:
                    raise Exception(f'la variable sizeReturn no tiene un valor correspondiente, valor: {sizeReturn} en la consulta: {command}')
    conexion.close()

#encriptado
def generateKey(pathKey: str, mensaje: str = ""):
    """
    It takes a path to a file and a message, and writes a key to the file. 
    
    If the message is empty, it generates a random key. 
    
    If the message is not empty, it creates a password from the message, and then writes the key to the
    file. 
    
    The key is written in base64 format
    
    :param pathKey: The path where the key will be saved
    :type pathKey: str
    
    :param mensaje: The message you want to encrypt
    :type mensaje: str
    """
    with open(pathKey, 'wb') as key:
        if mensaje == "":
            key.write(Fernet.generate_key())
        else:
            key.write(b64.urlsafe_b64encode(createPassword(mensaje)))

def encryptData(pathKey: str, data: bytes):
    """
    It takes a path to a key file and a byte array of data, and returns a byte array of encrypted data
    
    :param pathKey: The path to the key file
    :type data: str
    
    :param data: bytes
    :type data: bytes
    
    :return: The encrypted data or None in case of error.
    """
    try:
        with open(pathKey, 'rb') as keyfile:
            f = Fernet(keyfile.read())
        return f.encrypt(data)
    except ValueError:
        return None

def desEncryptData(pathKey: str, data: bytes):
    """
    It takes a path to a key file and a byte array of data, and returns the decrypted data
    
    :param pathKey: The path to the key file
    :type data: str
    
    :param data: The data to be encrypted
    :type data: bytes
    
    :return: The decrypted data or None in case of error.
    """
    try:
        with open(pathKey, 'rb') as keyfile:
            f = Fernet(keyfile.read())
            return f.decrypt(data)
    except ValueError:
        return None

#password
def createPassword(password: str):
    """
    It takes a string, encodes it as bytes, hashes it with SHA256, and returns the hash as bytes
    
    :param password: The password to be hashed
    :type password: str
    
    :return: A byte string
    """
    return sha256(password.encode()).digest()

if __name__ == '__main__':
    print(query(r'C:\Users\famar\Desktop\proyectos de programacion\Python\GuardarContrasenas\ConfigsInternal\DB_of_famar.bdpg',
    f"SELECT * FROM userconfigs",
    returnData=True,
    sizeReturn='all'))