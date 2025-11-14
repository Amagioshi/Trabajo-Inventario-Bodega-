# Importamos la clase ConexionBD para acceder a la conexión de la base de datos
from conexion import ConexionBD
# Importamos la clase Producto para crear objetos a partir de los datos de la base de datos
from models.producto import Producto

# Definimos la clase ProductoRepositorio que manejará todas las operaciones con la tabla Producto
class ProductoRepositorio:
    # Constructor de la clase que recibe una conexión a la base de datos
    def __init__(self, conexion):
        # Guardamos la conexión recibida en un atributo de la instancia para usarla en los métodos
        self.conexion = conexion

    # Método para crear un nuevo producto en la base de datos
    # Recibe el nombre, precio y el ID de la categoría del producto
    # Devuelve el ID del nuevo producto creado
    def crear(self, nombre, precio, categoria_id):
        # Creamos un cursor para ejecutar comandos SQL
        cursor = self.conexion.conexion.cursor()
        # Ejecutamos la consulta SQL para insertar un nuevo producto
        # El stock inicial es 0 y el estado activo es 1 (verdadero)
        # OUTPUT INSERTED.id devuelve el ID generado automáticamente por la base de datos
        cursor.execute("""
            INSERT INTO Producto (nombre, precio, stock, categoria_id, activo)
            OUTPUT INSERTED.id
            VALUES (?, ?, 0, ?, 1)
        """, (nombre, precio, categoria_id))
        # Obtenemos el ID del nuevo producto desde el resultado de la consulta
        nuevo_id = cursor.fetchone()[0]
        # Confirmamos la transacción para guardar los cambios en la base de datos
        self.conexion.conexion.commit()
        # Cerramos el cursor para liberar recursos
        cursor.close()
        # Devolvemos el ID del producto recién creado
        return nuevo_id

    # Método para obtener todos los productos activos de la base de datos
    # Devuelve una lista de objetos Producto
    def obtener_todos(self):
        # Creamos un cursor para ejecutar comandos SQL
        cursor = self.conexion.conexion.cursor()
        # Ejecutamos la consulta SQL para seleccionar todos los productos activos
        cursor.execute("""
            SELECT id, nombre, precio, stock, categoria_id, activo
            FROM Producto
            WHERE activo = 1
        """)
        # Obtenemos todos los resultados de la consulta como una lista de tuplas
        filas = cursor.fetchall()
        # Cerramos el cursor para liberar recursos
        cursor.close()
        # Convertimos cada tupla en un objeto Producto y devolvemos la lista completa
        return [
            Producto(
                id=f[0], nombre=f[1], precio=f[2],
                stock=f[3], categoria_id=f[4], activo=bool(f[5])
            )
            for f in filas
        ]

    # Método para obtener un producto específico por su ID
    # Recibe el ID del producto a buscar
    # Devuelve un objeto Producto si se encuentra, o None si no existe
    def obtener_por_id(self, id):
        # Creamos un cursor para ejecutar comandos SQL
        cursor = self.conexion.conexion.cursor()
        # Ejecutamos la consulta SQL para buscar un producto por su ID y que esté activo
        cursor.execute("""
            SELECT id, nombre, precio, stock, categoria_id, activo
            FROM Producto
            WHERE id = ? AND activo = 1
        """, (id,))
        # Obtenemos una sola fila del resultado (la primera coincidencia)
        fila = cursor.fetchone()
        # Cerramos el cursor para liberar recursos
        cursor.close()
        # Si se encontró una fila, creamos y devolvemos un objeto Producto
        if fila:
            return Producto(
                id=fila[0], nombre=fila[1], precio=fila[2],
                stock=fila[3], categoria_id=fila[4], activo=bool(fila[5])
            )
        # Si no se encontró ninguna fila, devolvemos None
        return None

    # Método para actualizar los datos de un producto existente
    # Recibe el ID del producto y los nuevos valores de nombre, precio y categoría
    # Devuelve True si se actualizó correctamente, False si no se encontró el producto
    def actualizar(self, id, nombre, precio, categoria_id):
        # Creamos un cursor para ejecutar comandos SQL
        cursor = self.conexion.conexion.cursor()
        # Ejecutamos la consulta SQL para actualizar los datos del producto
        cursor.execute("""
            UPDATE Producto
            SET nombre = ?, precio = ?, categoria_id = ?
            WHERE id = ? AND activo = 1
        """, (nombre, precio, categoria_id, id))
        # Obtenemos el número de filas afectadas por la actualización
        filas = cursor.rowcount
        # Confirmamos la transacción para guardar los cambios en la base de datos
        self.conexion.conexion.commit()
        # Cerramos el cursor para liberar recursos
        cursor.close()
        # Devolvemos True si al menos una fila fue actualizada, False en caso contrario
        return filas > 0

    # Método para eliminar lógicamente un producto (marcarlo como inactivo)
    # Recibe el ID del producto a eliminar
    # Devuelve True si se desactivó correctamente, False si no se encontró el producto
    def eliminar(self, id):
        # Creamos un cursor para ejecutar comandos SQL
        cursor = self.conexion.conexion.cursor()
        # Ejecutamos la consulta SQL para actualizar el estado del producto a inactivo (activo = 0)
        cursor.execute("""
            UPDATE Producto
            SET activo = 0
            WHERE id = ? AND activo = 1
        """, (id,))
        # Obtenemos el número de filas afectadas por la actualización
        filas = cursor.rowcount
        # Confirmamos la transacción para guardar los cambios en la base de datos
        self.conexion.conexion.commit()
        # Cerramos el cursor para liberar recursos
        cursor.close()
        # Devolvemos True si al menos una fila fue actualizada, False en caso contrario
        return filas > 0