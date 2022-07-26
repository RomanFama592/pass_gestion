import sqlite3 as sql, os

class bd():
    bgu = '#363636'
    bgu2 = '#575757'
    fgu = '#FFFFFF'

    #mantener userconfigs en el ultimo puesto.
    tables = [('accounts', """(
                            id integer not null primary key autoincrement,
                            namepages blob not null,
                            urls blob not null,
                            users blob,
                            passwords blob
                            )"""),
                ('cards', """(
                            id integer not null primary key autoincrement,
                            nameCards blob not null,
                            numberCards blob not null,
                            expirationDate blob not null,
                            codSeg blob not null
                            )"""),
                ('userconfigs',"""(
                            id integer not null primary key autoincrement,
                            initWord blob not null
                            hashOfInitWord blob not null,
                            )""")]

    pathOrigin = os.getcwd()
    initWord = 'nene que se porta mal'
    formatBD = '.bdpg'
    formatKey = '.key'
    pathBD = f'{pathOrigin}\index{formatBD}'
    pathKey = f'{pathOrigin}\GuardalaBien{formatKey}'

    def initDB(self):
        if not os.path.exists(self.pathBD) & os.path.exists(self.pathKey):
            self.query(f"CREATE TABLE IF NOT EXISTS {self.tables[-1][0]} {self.tables[-1][1]}")
            self.generateKey()
            self.query(f"insert into {self.tables[-1][0]}(initWord, hashOfInitWord) values (?, ?)" (self.initWord, self.encryptData(bytes(self.initWord))))

    
    def verifyBD(self):
        print(self.query(f"SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%'", returnData=True))
        return True

    def query(self, command, parameters = (), returnData = False, executeMany = False):
        """si returnData es True retornara una lista con tuplas de las filas y si es False no retorna nada."""
        conexion = sql.connect(self.pathBD)
        if executeMany:
            cursor = conexion.executemany(command, parameters)
        else:
            cursor = conexion.execute(command, parameters)
        conexion.commit()
        if returnData:
            return self.cursorToListInList(cursor)
        conexion.close()

    def cursorToListInList(self, Cursor: sql.Cursor):
        lista = [row for row in Cursor]
        if len(lista) == 0:
            return None
        elif len(lista) == 1:
            return lista[0]
        else:
            return lista 

if __name__ == '__main__':
    pass