import os
from tkinter import filedialog as filed
from tkinter import Tk
from time import localtime
from bcrypt import gensalt, hashpw

class util():

    def createPassword(self, password, salt):
        '''Salt == 0 se genera uno nuevo'''
        password = bytes(password, 'utf-8')
        if salt == 0:
            salts = gensalt(16)
        else:
            salts = salt
        hashed = hashpw(password,salts)
        return [hashed, salts]

    def passcreation(self, pathPass, inputPass):
        with open(pathPass, 'wb') as passwordHash:
            contraHash = self.createPassword(inputPass,0)
            passwordHash.write(contraHash[0])
            passwordHash.write(b' ')
            passwordHash.write(contraHash[1])

    def passExistverification(self, pathPass, inputPass):
        if os.path.exists(pathPass) == False:
            self.passcreation(pathPass, inputPass)
        else:
            with open(pathPass, 'rb') as passwordHash:
                passHashedcompro = passwordHash.readline().split(b' ')
            if len(passHashedcompro) != 2:
                self.passcreation(pathPass, inputPass)

    def passVerification(self, pathPass, inputPass):
        self.passExistverification(pathPass, inputPass)

        with open(pathPass, 'rb') as passwordHash:
            passHashed = passwordHash.readline().split(b' ')
        passInput = self.createPassword(inputPass, passHashed[1])
        return passHashed[0] == passInput[0]

    def browsePath(self, browseCarpeta, title, mainTypeText: str=..., mainType: str=...):
        """- str(title) = titulo de ventana por ejemplo 'Seleccione un archivo...' [obligatorio]
        - bool(browseCarpeta) = si lo buscado es una carpeta tendria que ingresar True, de lo contrario False [obligatorio]
        - str(mainTypeText) = lo que dice el selector de archivos por ejemplo 'txt files [opcional si browseCarpeta es False]'
        - str(mainType) = el tipo de archivo por ejemplo '*txt' [opcional si browseCarpeta es False]"""
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        if browseCarpeta == True:
            path = filed.askdirectory(initialdir = os.path.dirname(os.path.abspath(__file__)),title = title)
        else:
            path = filed.askopenfilename(initialdir = os.path.dirname(os.path.abspath(__file__)),title = title, filetypes = ((mainTypeText, mainType),("All files", "*.*")))
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
