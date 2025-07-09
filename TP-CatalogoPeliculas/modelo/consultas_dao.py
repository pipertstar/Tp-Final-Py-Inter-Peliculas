import sqlite3

class Conneccion():
    def __init__(self):
        self.base_datos = 'ddbb/peliculas.db'
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar_con(self):
        self.conexion.commit()
        self.conexion.close()

def crear_tabla():
    conn = Conneccion()

    sql_genero = '''
        CREATE TABLE IF NOT EXISTS Genero(
            ID INTEGER NOT NULL,
            Nombre VARCHAR(50),
            PRIMARY KEY (ID AUTOINCREMENT)
        );
    '''

    sql_director = '''
        CREATE TABLE IF NOT EXISTS Director(
            ID INTEGER NOT NULL,
            Nombre VARCHAR(100) UNIQUE,
            PRIMARY KEY (ID AUTOINCREMENT)
        );
    '''

    sql_peliculas = '''
    CREATE TABLE IF NOT EXISTS Peliculas(
            ID INTEGER NOT NULL,
            Nombre VARCHAR(150),
            Duracion VARCHAR(4),
            Genero INTEGER,
            Director INTEGER,
            Anio_lanzamiento INTEGER,
            PRIMARY KEY (ID AUTOINCREMENT),
            FOREIGN KEY (Genero) REFERENCES Genero(ID),
            FOREIGN KEY (Director) REFERENCES Director(ID) 
            );
    '''
    try:
        conn.cursor.execute(sql_genero)
        conn.cursor.execute(sql_director)
        conn.cursor.execute(sql_peliculas)
        conn.cerrar_con()
    except Exception:
        pass

class Peliculas():
    def __init__(self, nombre, duracion, genero_id, director_id, anio_lanzamiento):
        self.nombre = nombre
        self.duracion = duracion
        self.genero_id = genero_id
        self.director_id = director_id
        self.anio_lanzamiento = anio_lanzamiento

    def __str__(self):
        return f'Pelicula[Nombre:{self.nombre}, Duracion:{self.duracion}, Genero_ID:{self.genero_id}, Director_ID:{self.director_id}, Año Lanzamiento:{self.anio_lanzamiento}]'

def guardar_peli(pelicula):
    conn = Conneccion()

    sql = f'''
        INSERT INTO Peliculas(Nombre, Duracion, Genero, Director, Anio_lanzamiento)
        VALUES('{pelicula.nombre}', '{pelicula.duracion}', {pelicula.genero_id}, {pelicula.director_id}, {pelicula.anio_lanzamiento});
    '''
    try:
        conn.cursor.execute(sql)
        conn.cerrar_con()
    except Exception:
        pass

def listar_peli():
    conn = Conneccion()
    listar_peliculas = []

    sql = f'''
        SELECT p.ID, p.Nombre, p.Duracion, g.Nombre, d.Nombre, p.Anio_lanzamiento
        FROM Peliculas AS p
        INNER JOIN Genero AS g ON p.Genero = g.ID
        INNER JOIN Director AS d ON p.Director = d.ID; -- JOIN con tabla Director
    '''
    try:
        conn.cursor.execute(sql)
        listar_peliculas = conn.cursor.fetchall()
        conn.cerrar_con()
        return listar_peliculas
    except Exception:
        return []
        pass

def listar_generos():
    conn = Conneccion()
    listar_genero = []
    sql= f'''
        SELECT * FROM Genero;
    '''
    try:
        conn.cursor.execute(sql)
        listar_genero = conn.cursor.fetchall()
        conn.cerrar_con()
        return listar_genero
    except Exception:
        pass


def obtener_o_crear_director(nombre_director):
    conn = Conneccion()
    director_id = None
    try:
        conn.cursor.execute(f"SELECT ID FROM Director WHERE Nombre = '{nombre_director}' COLLATE NOCASE;")
        result = conn.cursor.fetchone()

        if result:
            director_id = result[0]
        else:
            conn.cursor.execute(f"INSERT INTO Director(Nombre) VALUES('{nombre_director}');")
            director_id = conn.cursor.lastrowid

        conn.cerrar_con()
        return director_id
    except Exception:
        conn.cerrar_con()
        return None


def listar_directores():
    conn = Conneccion()
    listar_director = []
    sql= f'''
        SELECT * FROM Director;
    '''
    try:
        conn.cursor.execute(sql)
        listar_director = conn.cursor.fetchall()
        conn.cerrar_con()
        return listar_director
    except Exception:
        return []
        pass

def editar_peli(pelicula, id):
    conn = Conneccion()

    sql = f'''
        UPDATE Peliculas
        SET Nombre = '{pelicula.nombre}',
            Duracion = '{pelicula.duracion}',
            Genero = {pelicula.genero_id},
            Director = {pelicula.director_id},
            Anio_lanzamiento = {pelicula.anio_lanzamiento}
        WHERE ID = {id};
    '''
    try:
        conn.cursor.execute(sql)
        conn.cerrar_con()
    except Exception:
        pass

def borrar_peli(id):
    conn = Conneccion()

    sql= f'''
        DELETE FROM Peliculas
        WHERE ID = {id};
    '''
    try:
        conn.cursor.execute(sql)
        conn.cerrar_con()
    except Exception:
        pass