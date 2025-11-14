from conexion import ConexionBD
from models.categoria import Categoria

class CategoriaRepositorio:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, nombre):
        cursor = self.conexion.conexion.cursor()
        cursor.execute("INSERT INTO Categoria (nombre) OUTPUT INSERTED.id VALUES (?)", (nombre,))
        nuevo_id = cursor.fetchone()[0]
        self.conexion.conexion.commit()
        cursor.close()
        return nuevo_id

    def obtener_todos(self):
        cursor = self.conexion.conexion.cursor()
        cursor.execute("SELECT id, nombre FROM Categoria")
        filas = cursor.fetchall()
        cursor.close()
        return [Categoria(id=f[0], nombre=f[1]) for f in filas]

    def obtener_por_id(self, id):
        cursor = self.conexion.conexion.cursor()
        cursor.execute("SELECT id, nombre FROM Categoria WHERE id = ?", (id,))
        fila = cursor.fetchone()
        cursor.close()
        if fila:
            return Categoria(id=fila[0], nombre=fila[1])
        return None

    def actualizar(self, id, nombre):
        cursor = self.conexion.conexion.cursor()
        cursor.execute("UPDATE Categoria SET nombre = ? WHERE id = ?", (nombre, id))
        filas = cursor.rowcount
        self.conexion.conexion.commit()
        cursor.close()
        return filas > 0

    def eliminar(self, id):
        cursor = self.conexion.conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM Producto WHERE categoria_id = ?", (id,))
        tiene_productos = cursor.fetchone()[0] > 0
        if tiene_productos:
            cursor.close()
            return False
        cursor.execute("DELETE FROM Categoria WHERE id = ?", (id,))
        filas = cursor.rowcount
        self.conexion.conexion.commit()
        cursor.close()
        return filas > 0