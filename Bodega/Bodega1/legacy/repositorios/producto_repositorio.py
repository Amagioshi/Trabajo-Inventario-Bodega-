from Bodega1.legacy.conexion import ConexionBD
from Bodega1.legacy.models.producto import Producto

class ProductoRepositorio:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, nombre, precio, categoria_id):
        cursor = self.conexion.conexion.cursor()
        cursor.execute("""
            INSERT INTO Producto (nombre, precio, stock, categoria_id, activo)
            OUTPUT INSERTED.id
            VALUES (?, ?, 0, ?, 1)
        """, (nombre, precio, categoria_id))
        nuevo_id = cursor.fetchone()[0]
        self.conexion.conexion.commit()
        cursor.close()
        return nuevo_id

    def obtener_todos(self):
        cursor = self.conexion.conexion.cursor()
        cursor.execute("""
            SELECT id, nombre, precio, stock, categoria_id, activo
            FROM Producto
            WHERE activo = 1
        """)
        filas = cursor.fetchall()
        cursor.close()
        return [
            Producto(
                id=f[0], nombre=f[1], precio=f[2],
                stock=f[3], categoria_id=f[4], activo=bool(f[5])
            )
            for f in filas
        ]

    def obtener_por_id(self, id):
        cursor = self.conexion.conexion.cursor()
        cursor.execute("""
            SELECT id, nombre, precio, stock, categoria_id, activo
            FROM Producto
            WHERE id = ? AND activo = 1
        """, (id,))
        fila = cursor.fetchone()
        cursor.close()
        if fila:
            return Producto(
                id=fila[0], nombre=fila[1], precio=fila[2],
                stock=fila[3], categoria_id=fila[4], activo=bool(fila[5])
            )
        return None

    def actualizar(self, id, nombre, precio, categoria_id):
        cursor = self.conexion.conexion.cursor()
        cursor.execute("""
            UPDATE Producto
            SET nombre = ?, precio = ?, categoria_id = ?
            WHERE id = ? AND activo = 1
        """, (nombre, precio, categoria_id, id))
        filas = cursor.rowcount
        self.conexion.conexion.commit()
        cursor.close()
        return filas > 0

    def eliminar(self, id):
        cursor = self.conexion.conexion.cursor()
        cursor.execute("""
            UPDATE Producto
            SET activo = 0
            WHERE id = ? AND activo = 1
        """, (id,))
        filas = cursor.rowcount
        self.conexion.conexion.commit()
        cursor.close()
        return filas > 0
    