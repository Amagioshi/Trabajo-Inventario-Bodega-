# repositorios/producto_repositorio.py
# Importamos la clase que maneja la conexión a la base de datos
from conexion import ConexionBD
# Importamos la clase Producto para crear objetos con los datos de la base de datos
from models.producto import Producto

# Clase que se encarga de todas las operaciones con la tabla Producto
class ProductoRepositorio:
    # Constructor: recibe una conexión ya abierta para usarla
    def __init__(self, conexion: ConexionBD):
        # Guardamos la conexión en un atributo para usarla en todos los métodos
        self.conexion = conexion

    # Crea un nuevo producto en la base de datos
    # Devuelve el ID asignado por la base de datos
    def crear(self, nombre: str, precio: float, categoria_id: int) -> int:
        # Creamos un cursor para enviar comandos a la base de datos
        cursor = self.conexion.conexion.cursor()
        # Ejecutamos la orden de insertar un producto nuevo
        # El stock inicial es 0 y activo es 1 (verdadero)
        # OUTPUT INSERTED.id nos devuelve el ID que la base de datos generó
        cursor.execute("""
            INSERT INTO Producto (nombre, precio, stock, categoria_id, activo)
            OUTPUT INSERTED.id
            VALUES (?, ?, 0, ?, 1)
        """, (nombre, precio, categoria_id))
        # Obtenemos el ID del nuevo producto
        nuevo_id = cursor.fetchone()[0]
        # Guardamos los cambios en la base de datos
        self.conexion.conexion.commit()
        # Cerramos el cursor para liberar recursos
        cursor.close()
        # Devolvemos el ID del producto creado
        return nuevo_id

    # Obtiene todos los productos que están activos (activo = 1)
    # Devuelve una lista de objetos Producto
    def obtener_todos(self) -> list:
        # Creamos un cursor
        cursor = self.conexion.conexion.cursor()
        # Pedimos todos los productos activos
        cursor.execute("""
            SELECT id, nombre, precio, stock, categoria_id, activo
            FROM Producto
            WHERE activo = 1
        """)
        # Obtenemos todos los resultados
        filas = cursor.fetchall()
        # Cerramos el cursor
        cursor.close()
        # Convertimos cada fila en un objeto Producto y devolvemos la lista
        return [
            Producto(
                id=f[0], nombre=f[1], precio=f[2],
                stock=f[3], categoria_id=f[4], activo=bool(f[5])
            )
            for f in filas
        ]

    # Obtiene un producto por su ID, solo si está activo
    # Devuelve un objeto Producto o None si no existe
    def obtener_por_id(self, id: int):
        # Creamos un cursor
        cursor = self.conexion.conexion.cursor()
        # Buscamos el producto con el ID dado y que esté activo
        cursor.execute("""
            SELECT id, nombre, precio, stock, categoria_id, activo
            FROM Producto
            WHERE id = ? AND activo = 1
        """, (id,))
        # Obtenemos una sola fila (la primera)
        fila = cursor.fetchone()
        # Cerramos el cursor
        cursor.close()
        # Si encontramos un producto, lo convertimos en objeto y lo devolvemos
        if fila:
            return Producto(
                id=fila[0], nombre=fila[1], precio=fila[2],
                stock=fila[3], categoria_id=fila[4], activo=bool(fila[5])
            )
        # Si no encontramos nada, devolvemos None
        return None

    # Actualiza los datos de un producto existente
    # Devuelve True si se actualizó, False si no se encontró
    def actualizar(self, id: int, nombre: str, precio: float, categoria_id: int) -> bool:
        # Creamos un cursor
        cursor = self.conexion.conexion.cursor()
        # Actualizamos el nombre, precio y categoría del producto
        cursor.execute("""
            UPDATE Producto
            SET nombre = ?, precio = ?, categoria_id = ?
            WHERE id = ? AND activo = 1
        """, (nombre, precio, categoria_id, id))
        # Obtenemos cuántas filas se actualizaron
        filas = cursor.rowcount
        # Guardamos los cambios
        self.conexion.conexion.commit()
        # Cerramos el cursor
        cursor.close()
        # Devolvemos True si se actualizó al menos una fila
        return filas > 0

    # "Elimina" un producto marcándolo como inactivo (activo = 0)
    # Devuelve True si se desactivó, False si no existía
    def eliminar(self, id: int) -> bool:
        # Creamos un cursor
        cursor = self.conexion.conexion.cursor()
        # Actualizamos el producto para marcarlo como inactivo
        cursor.execute("""
            UPDATE Producto
            SET activo = 0
            WHERE id = ? AND activo = 1
        """, (id,))
        # Obtenemos cuántas filas se actualizaron
        filas = cursor.rowcount
        # Guardamos los cambios
        self.conexion.conexion.commit()
        # Cerramos el cursor
        cursor.close()
        # Devolvemos True si se desactivó un producto
        return filas > 0
        
    