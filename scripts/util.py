import os, pandas as pd, base64 as b64
from tkinter import filedialog as filed
from tkinter import Tk
from time import localtime
from hashlib import sha256
from cryptography.fernet import Fernet
if __name__ != '__main__': from scripts.bd import bd
else: from bd import bd

class util(bd):

#encriptado
    def generateKey(self, path):
        with open(path, 'wb') as key:
            key.write(Fernet.generate_key())

    def generateClavePorPass(path, mensaje: str):
        b6432b = b64.urlsafe_b64encode(sha256(mensaje.encode()).digest())
        with open(path, 'wb') as key:
            key.write(b6432b)

    def encryptData(self, data: bytes, keypath):
        with open(keypath, 'rb') as keyfile:
            f = Fernet(keyfile.read())
        return f.encrypt(data)

    def desEncryptData(self, data: bytes, keypath):
        with open(keypath, 'rb') as keyfile:
            f = Fernet(keyfile.read())
        return f.decrypt(data)

#password
    def createPassword(self, password: str):
        return sha256(password.encode()).digest()

    def passSave(self, pathBD, inputPass):
        self.password = self.createPassword(inputPass, 0)
        print(self.password)
        self.query(pathBD, "insert into userconfigs (password) values (?)", (self.password))

    def passExistverification(self, pathBD, inputPass):
        if os.path.exists(pathBD) == False:
            self.initDB(pathBD)
            self.passSave(pathBD, inputPass)
            return True
        else:
            if self.verifyBD(pathBD):
                self.password = self.query(pathBD, 'select password from userconfigs', returnData=True)
                return True
            else:
                return False

    def passVerification(self, pathBD, inputPass):
        if self.passExistverification(pathBD, inputPass):
            return self.createPassword(inputPass) == self.password
            del self.password
        else:
            return [False, False]
            del self.password

#funciones utiles
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