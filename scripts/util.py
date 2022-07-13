import os, pandas as pd
import sqlite3
from tkinter import filedialog as filed
from tkinter import Tk
from time import localtime
from bcrypt import gensalt, hashpw
from cryptography.fernet import Fernet
if __name__ != '__main__': from scripts.bd import bd
else: from bd import bd

class util(bd):

#encriptado
    def generateKey(self, path):
        with open(path, 'wb') as key:
            key.write(Fernet.generate_key())

    def encryptData(self, data: bytes, keypath):
        with open(keypath, 'rb') as keyfile:
            f = Fernet(keyfile.read())
        return f.encrypt(data)

    def desEncryptData(self, data: bytes, keypath):
        with open(keypath, 'rb') as keyfile:
            f = Fernet(keyfile.read())
        return f.decrypt(data)

#password
    def createPassword(self, password, salt):
        '''Salt == 0 se genera uno nuevo'''
        password = bytes(password, 'utf-8')
        if salt == 0:
            salts = gensalt(16)
        else:
            salts = salt
        hashed = hashpw(password, salts)
        return (hashed, salts)

    def passSave(self, pathBD, inputPass):
        (self.password, self.salt) = self.createPassword(inputPass, 0)
        self.query(pathBD, """insert into userconfigs (password, salt) values (?, ?)""", (self.password, self.salt))

    #BUG01
    def passExistverification(self, pathBD, inputPass):
        if os.path.exists(pathBD) == False:
            self.initDB(pathBD)
            self.passSave(pathBD, inputPass)
        else:
            passwordAndSalt = self.query(pathBD, """select password, salt from userconfigs""", True)
            a = self.query(pathBD, """SELECT name from sqlite_master where type= 'table'""", True)
            print(a)
            for table in a:
                if table[0] != "sqlite_sequence":
                    self.query(pathBD, f"DROP TABLE {table[0]}")
            self.initDB(pathBD)
                
            if passwordAndSalt[0][0] == '' and passwordAndSalt[0][1] == '':
                self.query(pathBD, """delete * from userconfigs""")
                self.passSave(pathBD, inputPass)
            self.passSave(pathBD, inputPass)

            
    def passVerification(self, pathBD, inputPass):
        self.passExistverification(pathBD, inputPass)
        return self.createPassword(inputPass, self.salt) == (self.password, self.salt)
        del self.password, self.salt

    def browsePath(self, browseCarpeta, title, mainTypeText: str=..., mainType: str=...):
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

    def resolucionPantallawithcentered(self, r):
        ''' r = Ventana de Tkinker '''
        altura_pantalla = r.winfo_screenheight()
        anchura_pantalla = r.winfo_screenwidth()
        pantalla = [anchura_pantalla, altura_pantalla]
        return pantalla

    def timeNow(self):
        tiempo = localtime()
        #tiempo = str(tiempo.tm_hour) + ':' + str(tiempo.tm_min) + ':' + str(tiempo.tm_sec) + '.'
        tiempo = (tiempo.tm_min*60) + tiempo.tm_sec
        return tiempo

    def LoadPasswordOpera(self):
        """Devuelve un Data frame"""
        path = self.browsePath(False, 'Select Opera password file', 'CSV files', '*.csv')
        PasswordsOri = pd.read_csv(path,sep=',', index_col=False)
        PasswordsOri = PasswordsOri.fillna('')
        PasswordsOri.to_excel(self.pathBD, sheet_name='Account', index=False)

if __name__ == '__main__':
    pass