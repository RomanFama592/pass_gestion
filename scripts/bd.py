import sqlite3 as sql

class bd():

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
                            password blob not null,
                            salt blob not null  
                            )""")]

    def initDB(self, bd):
        conexion = sql.connect(bd)
        for i in range(len(self.tables)): self.query(bd, f"CREATE TABLE IF NOT EXISTS {self.tables[i][0]} {self.tables[i][1]}")
        conexion.close()
    
    def verifyBD(self, bd):
        #tablesInBD = self.query(bd,'SELECT * FROM sqlite_master WHERE type = "table";', returnData=True)
        tablesInBD = self.query(bd,"SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';", returnData=True)
        #print(tablesInBD)
        for item1, item2 in zip(tablesInBD, self.tables):
            print(item1[0], item2[0])
            if item1[0] == item2[0]:
                pass
            else: return False

        (password, salt) = self.query(bd, f'select password, salt from userconfigs', returnData=True)
        #print(password, salt)
        if password == None and salt == None:
            return False
        return True

    def query(self, bd, command, parameters = (), returnData = False, executeMany = False):
        """si returnData es True retornara una lista con tuplas de las filas y si es False no retorna nada."""
        conexion = sql.connect(bd)
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