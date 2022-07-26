from scripts.util import util
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

"""from getpass import getuser
f'C:/Users/{getuser()}/Documents'"""

#self.query(f"CREATE TABLE IF NOT EXISTS {self.tables[-1][0]} {self.tables[-1][1]}")

#añadir boton de 'ver contraseñas'
#añadir sistema de paginas para la visualizacion de la informacion
#implementar el copiado de usuario y contraseña a portapapeles
#cifrar la informacion
    #usar contraseña hashed para desbloquear BDs
#sistem cambiar datos

class Aplication(util):
    def __init__(self, window: Tk):
        self.window = window
        #inicializando la ventana
        (screensidex, screensidey) = self.resolucionPantallawithcentered(self.window)
        self.window.geometry('{}x{}+{}+{}'.format(int(screensidex//1.5), int(screensidey//1.5), screensidex//6, screensidey//6))
        self.window.minsize(640,480)
        self.window.title('PassGestion')
        self.window.config(bg=self.bgu)

        self.unlock() #pantalla de login
        #self.interface()

        self.window.protocol("WM_DELETE_WINDOW", self.validacionCerrar)

    def interface(self): #interface no finalizada
        frameInterface = Frame(self.window, bg=self.bgu)
        frameInterface.grid()
        frameInterface.columnconfigure(0,weight=3)
        
        self.listaTipos = [self.tables[x][0] for x in range(0, len(self.tables))]
        self.valuemenuTipos = StringVar(frameInterface)
        self.menuTipos = ttk.OptionMenu(frameInterface, self.valuemenuTipos, 'Seleccione el tipo', *self.listaTipos, command= self.AccionMenuTipos)
        self.menuTipos.grid(column=0, columnspan=2,row=0)
        
    def unlock(self): #unlock finalizado pero no retocado
        self.frameUnlock = Frame(self.window)
        self.frameUnlock.grid()

        entryPathKey = ttk.Entry(self.frameUnlock)
        entryPathKey.insert(0, self.pathKey)
        entryPathKey.grid(row=1, column=0)

        entryPathBD = ttk.Entry(self.frameUnlock)
        entryPathBD.insert(0, self.pathBD)
        entryPathBD.grid(row=0, column=0)

        labelBD = ttk.Label(self.frameUnlock, text=f'Ubicacion de BD: {self.pathBD}')
        labelBD.grid(row=0, column=2)

        botonconectBD = ttk.Button(self.frameUnlock, text='conectar la BD', command= self.AccionbotonconectBD)
        botonconectBD.grid(row=1, column=2)

        botonLogin = ttk.Button(self.frameUnlock, text='Login')
        botonLogin.grid(row=1, column=1)

        botonCreateBD = ttk.Button(self.frameUnlock, text='Crear base de datos', )
        botonCreateBD.grid(row=2, column=2)

#botones y acciones de aplicacion

    def AccionbotonLogin(self):
        pass

    def AccionbotonconectBD(self):
        newpathBD = self.browsePath('Conectar base de datos:', False, f'{self.formatBD} files', f'*{self.formatBD}')
        if newpathBD != '':
            if self.verifyBD():
                self.pathBD = newpathBD
                self.frameUnlock.destroy()
                self.unlock()
            else:
                messagebox.showerror(message='base de datos dañada o no funcional')
        else: messagebox.showerror(message='base de datos no seleccionada')

    def AccionMenuTipos(self, seleccion):
        print(seleccion)

    def validacionCerrar(self):
        if messagebox.askokcancel("Quit", "Seguro que quieres salir?"):
            self.window.destroy()

window = Tk()
app = Aplication(window)
window.mainloop()
