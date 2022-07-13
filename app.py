import os
from scripts.util import util
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from getpass import getuser

f'C:/Users/{getuser()}/Documents'


#añadir boton de 'ver contraseñas'
#añadir sistema de paginas para la visualizacion de la informacion
#implementar el copiado de usuario y contraseña a portapapeles
#cifrar la informacion
    #usar contraseña hashed para desbloquear BDs
#sistem cambiar datos

class Aplication(util):
    bgu = '#363636'
    bgu2 = '#575757'
    fgu = '#FFFFFF'
    formatBD = '.bdpg'
    pathBD = f'index{formatBD}'
    key = 'SaveThisSecretKey.key'

    def __init__(self):
        self.window = Tk()

        (screensidex, screensidey) = self.resolucionPantallawithcentered(self.window)
        self.window.geometry('{}x{}+{}+{}'.format(int(screensidex//1.5), int(screensidey//1.5), screensidex//6, screensidey//6))
        self.window.minsize(640,480)
        self.window.title('PassGestion')
        self.window.config(bg=self.bgu)
        self.window.attributes('-topmost', True)

        self.unlock()

        self.window.protocol("WM_DELETE_WINDOW", self.validacionCerrar)
        self.window.mainloop()

#retocar interface
    def interface(self):
        frameMain = Frame(self.window, bg=self.bgu)
        frameMain.columnconfigure(0,weight=3)
        frameMain.grid()
        
        self.listaTipos = ['Account', 'Card']
        self.valuemenuTipos = StringVar(frameMain)
        self.menuTipos = ttk.OptionMenu(frameMain, self.valuemenuTipos, 'Seleccione el tipo', *self.listaTipos, command= self.AccionMenuTipos)
        self.menuTipos.grid(column=0, columnspan=2,row=0)
        
    def unlock(self):
        self.frameUnlock = Frame(self.window, bg=self.bgu)
        self.frameUnlock.grid()
        
        self.entryPass = Entry(self.frameUnlock,show='*')
        self.entryPass.focus_set()
        self.entryPass.grid(column=0,row=1,ipady=5)

        if os.path.exists(self.pathBD):
            Label(self.frameUnlock, text='Ingrese la contraseña existente:', bg=self.bgu, fg=self.fgu).grid(column=0, row=0,pady=10)
            self.checkPassCreation = False
        else:
            Label(self.frameUnlock, text='Cree una contraseña', bg=self.bgu, fg=self.fgu).grid(column=0, row=0,pady=10)
            self.entryPassVeri = Entry(self.frameUnlock,show='*')
            self.entryPassVeri.grid(column=0,row=2,ipady=5, pady=5)
            self.checkPassCreation = True
        
        self.hideOption = True

        botonconectBD = Button(self.frameUnlock, text='conectar base de datos', command=self.AccionbotonconectBD)
        botonconectBD.grid(column=2, row=0)

        botonShowPass = Button(self.frameUnlock, text='*', command=self.AccionbotonShowPass)
        botonShowPass.grid(column=1,row=2,padx=10)

        self.botonEnter = Button(self.frameUnlock, text='Enter',command= self.AccionbotonEnter)
        self.botonEnter.grid(column=1,row=1,padx=10)

#botones y acciones de aplicacion
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
        initT = self.timeNow()
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
            if self.passVerification(self.pathBD, self.entryPass.get()) == False:
                messagebox.showerror(message='contraseña incorrecta')
                self.botonEnter.config(state=NORMAL)
                self.entryPass.config(state=NORMAL)
                if self.checkPassCreation:
                    self.entryPassVeri.config(state=NORMAL)
            else:
                self.frameUnlock.destroy()
                self.interface()
        f = self.timeNow()
        print(f'bd {f - initT}s')

    def AccionbotonconectBD(self):
        self.pathBD = self.browsePath('Conectar base de datos:', False, f'{self.formatBD} files', f'*{self.formatBD}')
        self.frameUnlock.destroy()
        self.unlock()

    def AccionMenuTipos(self, *args):
        if self.valuemenuTipos.get() == self.listaTipos[0]:
            print(self.listaTipos[0])
        elif self.valuemenuTipos.get() == self.listaTipos[1]:
            print(self.listaTipos[1])

    def validacionCerrar(self):
        if messagebox.askokcancel("Quit", "Seguro que quieres salir?"):
            self.window.destroy()

App = Aplication()