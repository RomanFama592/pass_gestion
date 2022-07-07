import sqlite3 as sql

class bd():

    def initDB(self, bd):
        self.query(bd, """create table acounts (
                            id integer not null primary key autoincrement,
                            namepages text not null,
                            urls text not null,
                            users text,
                            passwords text
                            )""")
        self.query(bd, """create table cards (
                            id integer not null primary key autoincrement,
                            nameCards text not null,
                            numberCards int not null,
                            expirationDate text not null,
                            codSeg text not null
                            )""")
        self.query(bd, """create table userconfig (
                            id integer not null primary key autoincrement,
                            password blob not null,
                            salt blob not null
                            )""")
    
    def query(self, bd, command, parameters = ()):
        with sql.connect(bd) as conexion:
            cursor = conexion.cursor()
            result = cursor.execute(command, parameters)
            conexion.commit()
        return result

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