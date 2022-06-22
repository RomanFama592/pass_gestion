import os, sqlite3 as sql, pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#añadir boton de 'ver contraseñas'
#añadir sistema de paginas para la visualizacion de la informacion
#implementar el copiado de usuario y contraseña a portapapeles
#cifrar la informacion
    #usar contraseña hashed para desbloquear BDs
#sistem cambiar datos

class bd():
    pass

class util():

    def createPassword(self, password, salt):
        '''Salt == 0 se genera uno nuevo'''
        from bcrypt import gensalt, hashpw
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
        from tkinter import filedialog as filed
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
        from time import localtime
        tiempo = localtime()
        #tiempo = str(tiempo.tm_hour) + ':' + str(tiempo.tm_min) + ':' + str(tiempo.tm_sec) + '.'
        tiempo = (tiempo.tm_min*60) + tiempo.tm_sec
        return tiempo

class Aplication(util, bd):
    bgu = '#363636'
    bgu2 = '#575757'
    fgu = '#FFFFFF'
    pathBD = os.path.join(os.path.dirname(__file__),'pass.db')
    pathPass = os.path.join(os.path.dirname(__file__),'pass.cock')

    def __init__(self):
        self.window = Tk()

        (screensidex, screensidey) = self.resolucionPantallawithcentered(self.window)
        self.window.geometry('{}x{}+{}+{}'.format(int(screensidex//1.5), int(screensidey//1.5),
        screensidex//6, screensidey//6))
        self.window.minsize(640,480)
        self.window.title('PassGestion')
        self.window.config(bg=self.bgu)
        self.window.attributes('-topmost', True)
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=2)
        self.window.rowconfigure(0,weight=1)

        self.unlock()

        self.window.protocol("WM_DELETE_WINDOW", self.validacionCerrar)
        self.window.mainloop()

    def interface(self):
        FrameOptions = Frame(self.window, bg=self.bgu2)
        FrameOptions.grid(row=0,column=1,sticky=NSEW)
        FrameOptions.rowconfigure(1,weight=1)
        FrameOptions.columnconfigure(0,weight=1)

        if os.path.exists(self.pathBD) == False:
            self.buttonImportPasswords = Button(FrameOptions, 
            text='Importar\ncontraseñas\nde Opera', justify="center", 
            font=('Times',10),
            command= self.LoadPasswordOpera)
            self.buttonImportPasswords.grid(column=5,row=0,sticky=NSEW,padx=10,pady=10)
        else: None


        FrameList = Frame(self.window,bg=self.bgu, relief="flat")
        FrameList.grid(row=0,column=0,sticky=NSEW)
        FrameList.rowconfigure(1,weight=2)
        FrameList.columnconfigure(0,weight=1)


        self.listaTipos = ['Account', 'Card']
        self.valuemenuTipos = StringVar(FrameList)
        self.menuTipos = ttk.OptionMenu(FrameList, self.valuemenuTipos, 'Seleccione el tipo', *self.listaTipos, command= self.AccionMenuTipos)
        self.menuTipos.grid(row=0,column=0,sticky=NSEW,padx=10,pady=10)


        FrameInList = Frame(FrameList,bg=self.bgu2)
        FrameInList.grid(row=1,column=0,sticky=NSEW,padx=10,pady=10)

    def unlock(self):
        self.frameUnlock = Frame(self.window, bg=self.bgu)
        self.frameUnlock.grid()
        
        self.entryPass = Entry(self.frameUnlock,show='*')
        self.entryPass.grid(column=0,row=1,ipady=5)
        self.entryPass.focus_set()

        if os.path.exists(self.pathPass):
            Label(self.frameUnlock, text='Ingrese la contraseña existente:', bg=self.bgu, fg=self.fgu).grid(column=0, row=0,pady=10)
            self.checkPassCreation = False

        else:
            Label(self.frameUnlock, text='Cree una contraseña', bg=self.bgu, fg=self.fgu).grid(column=0, row=0,pady=10)
            self.entryPassVeri = Entry(self.frameUnlock,show='*')
            self.entryPassVeri.grid(column=0,row=2,ipady=5, pady=5)
            self.checkPassCreation = True
        
        self.hideOption = True

        botonShowPass = Button(self.frameUnlock, text='*', command=self.AccionbotonShowPass)
        botonShowPass.grid(column=1,row=2,padx=10)

        self.botonEnter = Button(self.frameUnlock, text='Enter',command= self.AccionbotonEnter)
        self.botonEnter.grid(column=1,row=1,padx=10)

#optimizar AccionbotonEnter y AccionbotonShowPass
    def AccionbotonShowPass(self):
        if self.checkPassCreation:
            if self.hideOption:
                self.entryPass.config(show='')
                self.entryPassVeri.config(show='')
                self.hideOption = False
            else:
                self.entryPass.config(show='*')
                self.entryPassVeri.config(show='*')
                self.hideOption = True
        else:
            if self.hideOption:
                self.entryPass.config(show='')
                self.hideOption = False
            else:
                self.entryPass.config(show='*')
                self.hideOption = True

    def AccionbotonEnter(self):
        canCheck = True
        if self.checkPassCreation:
            self.entryPassVeri.config(state=DISABLED)
        self.botonEnter.config(state=DISABLED)
        self.entryPass.config(state=DISABLED)

        if self.checkPassCreation:
            if (self.entryPass.get() == self.entryPassVeri.get()) == False:
                messagebox.showerror(message='contraseñas no coinciden')
                self.botonEnter.config(state=NORMAL)
                self.entryPass.config(state=NORMAL)
                self.entryPassVeri.config(state=NORMAL)
                canCheck = False

        if canCheck:
            if self.passVerification(self.pathPass, self.entryPass.get()) == False:
                messagebox.showerror(message='contraseña incorrecta')
                self.botonEnter.config(state=NORMAL)
                self.entryPass.config(state=NORMAL)
                if self.checkPassCreation:
                    self.entryPassVeri.config(state=NORMAL)
            else:
                self.frameUnlock.destroy()
                self.interface()

    def AccionMenuTipos(self, *args):
        if self.valuemenuTipos.get() == self.listaTipos[0]:
            print(self.listaTipos[0])
        elif self.valuemenuTipos.get() == self.listaTipos[1]:
            print(self.listaTipos[1])

    def LoadPasswordOpera(self):
        """Devuelve un Data frame"""
        path = self.browsePath(False, 'Select Opera password file', 'CSV files', '*.csv')
        PasswordsOri = pd.read_csv(path,sep=',', index_col=False)
        PasswordsOri = PasswordsOri.fillna('')
        PasswordsOri.to_excel(self.pathBD, sheet_name='Account', index=False)
        self.buttonImportPasswords.grid_forget()

    def validacionCerrar(self):
        if messagebox.askokcancel("Quit", "Seguro que quieres salir?"):
            self.window.destroy()

App = Aplication()
