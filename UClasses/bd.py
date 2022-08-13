import sqlite3 as sql
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

#base de datos
def query(pathBD, command, parameters = (), returnData = False, executeMany = False):
    """si returnData es True retornara una lista con tuplas de las filas y si es False no retorna nada."""
    conexion = sql.connect(pathBD)
    if executeMany:
        cursor = conexion.executemany(command, parameters)
    else:
        cursor = conexion.execute(command, parameters)
    conexion.commit()
    if returnData:
        return cursorToListInList(cursor)
    conexion.close()

def cursorToListInList(Cursor: sql.Cursor):
    lista = []
    for row in Cursor:
        if len(row) == 1:
            lista.append(row[0])
        elif len(row) > 1:
            lista.append(row)
    if len(lista) == 0:
        return None
    elif len(lista) == 1:
        return lista[0]
    else:
        return lista

#encriptado
def generateKey(pathKey: str, mensaje: str = ""):
    with open(pathKey, 'wb') as key:
        if mensaje == "":
            key.write(Fernet.generate_key())
        else:
            key.write(b64.urlsafe_b64encode(createPassword(mensaje)))


def encryptData(pathKey, data: bytes):
    try:
        with open(pathKey, 'rb') as keyfile:
            f = Fernet(keyfile.read())
        return f.encrypt(data)
    except ValueError:
        return None

def desEncryptData(pathKey, data: bytes):
    try:
        with open(pathKey, 'rb') as keyfile:
            f = Fernet(keyfile.read())
            return f.decrypt(data)
    except ValueError:
        return None

#password
def createPassword(password: str):
    return sha256(password.encode()).digest()

if __name__ == '__main__':
    pass