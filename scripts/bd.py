import sqlite3 as sql

class bd():

    def initDB(self, bd):
        conexion = sql.connect(bd)
        self.tables = (('accounts', """(
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
                                        )"""))
        self.query(bd,"""create table ? ?""",executeMany=True, parameters=(self.tables))
        conexion.close()
    
    def query(self, bd, command, returnData: bool = False, executeMany: bool = False, parameters: tuple = ()):
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
        lista = []
        for row in Cursor:
            lista.append(row)
        if len(lista) == 0:
            return None
        elif len(lista) == 1:
            return lista[0]
        else: 
            return lista 

if __name__ == '__main__':
    pass