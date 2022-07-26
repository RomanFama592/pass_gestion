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
    def generateKey(self):
        with open(self.pathKey, 'wb') as key:
            key.write(Fernet.generate_key())

    def generateKeyPorPass(self, mensaje: str):
        with open(self.pathKey, 'wb') as key:
            key.write(b64.urlsafe_b64encode(sha256(mensaje.encode()).digest()))

    def encryptData(self, data: bytes):
        with open(self.pathKey, 'rb') as keyfile:
            f = Fernet(keyfile.read())
        return f.encrypt(data)

    def desEncryptData(self, data: bytes):
        with open(self.pathKey, 'rb') as keyfile:
            f = Fernet(keyfile.read())
        return f.decrypt(data)

#password
    def createPassword(self, password: str):
        return sha256(password.encode()).digest()

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

    def resolucionPantallawithcentered(self, window):
        altura_pantalla = window.winfo_screenheight()
        anchura_pantalla = window.winfo_screenwidth()
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