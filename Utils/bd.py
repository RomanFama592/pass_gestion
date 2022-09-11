import os
from re import A
import sqlite3 as sql
#from cryptography.fernet import fernet.Fernet
import cryptography.fernet as fernet
import base64 as b64
from hashlib import sha256

#mantener userconfigs en el ultimo puesto.
#RESOLVER

def returnRownames(cursorDescripcion):
    """
    It takes a cursor object as input and returns a list of column names
    
    :param cursorDescripcion: This is the cursor object that is returned from the query
    :return: A list of the first column of the cursorDescripcion
    """
    rowsname = [row[0] for row in cursorDescripcion]
    return rowsname

def dictWithRownamesAsKey(rows: list or tuple, cursorDescripcion):
    """
    It takes a list of tuples and a cursor description and returns a dictionary of lists
    
    :param rows: the result of the query
    :param cursorDescripcion: This is the cursor description of the cursor that you're using to fetch
    the data
    :return: A dictionary with the column names as keys and the values as a list of values.
    """
    diccionario = {}
    rowsname = returnRownames(cursorDescripcion)

    if isinstance(rows, list):
        for i in rowsname:
            diccionario[i] = [row[rowsname.index(i)] for row in rows]
    elif isinstance(rows, tuple):
        for i in rowsname:
            diccionario[i] = rows[rowsname.index(i)]
    
    return diccionario

#base de datos
def query(pathBD: str, command: str, parameters: tuple = (),
          returnData: bool = False, sizeReturn: str or int = '' or 0,
          executeMany: bool = False, createDB: bool = False,
          returnNameofColumns: bool = False, dictwithrowaskey: bool = False):
    """
    It's a function that allows you to execute a query in a database, and return the data if you want
    
    :param pathBD: str, command: str, parameters: tuple = (),
    :type pathBD: str
    :param command: str
    :type command: str
    :param parameters: tuple = (),
    :type parameters: tuple
    :param returnData: bool = False, sizeReturn: str or int = '' or 0,, defaults to False
    :type returnData: bool (optional)
    :param sizeReturn: str or int = '' or 0,
    :type sizeReturn: str or int
    :param executeMany: if you want to execute many commands at once, you must pass the commands in a
    list of tuples, and the parameters in a list of tuples, and set this parameter to True, defaults to
    False
    :type executeMany: bool (optional)
    :param createDB: if you want to create the database if it doesn't exist, defaults to False
    :type createDB: bool (optional)
    :param returnNameofColumns: bool = False, dictwithrowaskey: bool = False, defaults to False
    :type returnNameofColumns: bool (optional)
    :param dictwithrowaskey: bool = False, defaults to False
    :type dictwithrowaskey: bool (optional)
    :return: a tuple with the data and the names of the columns, False if not execute good the query or None if not exist the data base.
    """

    verifyPath = os.path.exists(pathBD)
    
    if createDB:
        verifyPath = True

    if verifyPath:
        conexion = sql.connect(pathBD)
        cursor = conexion.cursor()
        try:
            if executeMany:
                cursor.executemany(command, parameters)
            else:
                cursor.execute(command, parameters)
            conexion.commit()
        except:
            print(f'Error en ejecutar la query {command}')
            return False
        else:    
            if returnData: 
                if returnNameofColumns:
                    if sizeReturn == 'one':
                        return (cursor.fetchone(), returnRownames(cursor.description))
                    elif isinstance(sizeReturn, int):
                        return (cursor.fetchmany(sizeReturn), returnRownames(cursor.description))
                    elif sizeReturn == 'all':
                        return (cursor.fetchall(), returnRownames(cursor.description))
                    else:
                        raise Exception(f'la variable sizeReturn no tiene un valor correspondiente, valor: {sizeReturn} en la consulta: {command}')
                elif dictwithrowaskey:
                    if sizeReturn == 'one':
                        return dictWithRownamesAsKey(cursor.fetchone(), cursor.description)
                    elif isinstance(sizeReturn, int):
                        return dictWithRownamesAsKey(cursor.fetchmany(sizeReturn), cursor.description)
                    elif sizeReturn == 'all':
                        return dictWithRownamesAsKey(cursor.fetchall(), cursor.description)
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
    else:
        return None

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
    try:
        with open(pathKey, 'wb') as key:
            if mensaje == "":
                key.write(fernet.Fernet.generate_key())
            else:
                key.write(b64.urlsafe_b64encode(createPassword(mensaje)))
    except:
        return False

def encryptData(pathKey: str, data: str):
    """
    It takes a path to a key file and a byte array of data, and returns a byte array of encrypted data
    
    :param pathKey: The path to the key file
    :type data: str
    
    :param data: bytes
    :type data: bytes
    
    :return: The encrypted data, None in case of error or False in case of not exist key file.
    """
    try:
        with open(pathKey, 'rb') as keyfile:
            f = fernet.Fernet(keyfile.read())
        return f.encrypt(str(data).encode())
    except ValueError:
        return None
    except fernet.InvalidToken:
        return None
    except FileNotFoundError:
        return False

def desEncryptData(pathKey: str, data: bytes):
    """
    It takes a path to a key file and a byte array of data, and returns the decrypted data
    
    :param pathKey: The path to the key file
    :type data: str
    
    :param data: The data to be encrypted
    :type data: bytes
    
    :return: The encrypted data, None in case of error or False in case of not exist key file.
    """
    try:
        with open(pathKey, 'rb') as keyfile:
            f = fernet.Fernet(keyfile.read())
        return f.decrypt(data).decode()
    except ValueError:
        return None
    except fernet.InvalidToken:
        return None
    except FileNotFoundError:
        return False

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
    for i in range(100):
        i = encryptData(r'C:\Users\famar\Desktop\proyectos de programacion\Python\GuardarContrasenas\ConfigsInternal\Key_of_famar.key', str(i))
        query(r'C:\Users\famar\Desktop\proyectos de programacion\Python\GuardarContrasenas\ConfigsInternal\DB_of_famar.bdpg',
        f"INSERT INTO accounts (namepages, urls, users, passwords) VALUES (?, ?, ?, ?);", (i, i, i,i))