# Importamos la clase ConexionBD para acceder a la conexión de la base de datos
from conexion import ConexionBD
# Importamos la clase Movimiento para crear objetos a partir de los datos de la base de datos
from models.movimiento import Movimiento

# Definimos la clase MovimientoRepositorio que manejará todas las operaciones con la tabla Movimiento
class MovimientoRepositorio:
    # Constructor de la clase que recibe una conexión a la base de datos
    def __init__(self, conexion):
        # Guardamos la conexión recibida en un atributo de la instancia para usarla en los métodos
        self.conexion = conexion

    # Método para crear un nuevo movimiento (ingreso o egreso) en la base de datos
    # Recibe el ID del producto, el tipo de movimiento ('ingreso' o 'egreso'), la cantidad, el motivo y la fecha
    # Devuelve el ID del nuevo movimiento creado
    def crear(self, producto_id, tipo, cantidad, motivo, fecha):
        # Creamos un cursor para ejecutar comandos SQL
        cursor = self.conexion.conexion.cursor()
        
        try:
            # Ejecutamos una consulta para obtener el stock actual del producto
            # Solo consideramos productos que existen y están activos
            cursor.execute("""
                SELECT stock FROM Producto WHERE id = ? AND activo = 1
            """, (producto_id,))
            # Obtenemos una sola fila del resultado
            fila = cursor.fetchone()
            
            # Si no se encontró ninguna fila, el producto no existe o está inactivo
            if not fila:
                # Lanzamos un error con un mensaje claro
                raise ValueError("Producto no encontrado o inactivo.")
            
            # Guardamos el stock actual en una variable para usarlo después
            stock_actual = fila[0]
            
            # Si el tipo de movimiento es 'egreso' (salida de productos)
            if tipo == "egreso":
                # Verificamos que haya suficiente stock para realizar la salida
                if cantidad > stock_actual:
                    # Si no hay suficiente stock, lanzamos un error
                    raise ValueError("Stock insuficiente para realizar el egreso.")
            
            # Calculamos el nuevo stock después del movimiento
            if tipo == "ingreso":
                # Si es un ingreso, sumamos la cantidad al stock actual
                nuevo_stock = stock_actual + cantidad
            else:
                # Si es un egreso, restamos la cantidad del stock actual
                nuevo_stock = stock_actual - cantidad
            
            # Ejecutamos una consulta para actualizar el stock del producto
            cursor.execute("""
                UPDATE Producto SET stock = ? WHERE id = ?
            """, (nuevo_stock, producto_id))
            
            # Ejecutamos una consulta para registrar el nuevo movimiento en la tabla Movimiento
            cursor.execute("""
                INSERT INTO Movimiento (producto_id, tipo, cantidad, motivo, fecha)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?)
            """, (producto_id, tipo, cantidad, motivo, fecha))
            
            # Obtenemos el ID del nuevo movimiento desde el resultado de la consulta
            movimiento_id = cursor.fetchone()[0]
            # Confirmamos la transacción para guardar todos los cambios en la base de datos
            self.conexion.conexion.commit()
            # Devolvemos el ID del movimiento recién creado
            return movimiento_id
        
        except Exception as e:
            # Si ocurre cualquier error durante el proceso, deshacemos todos los cambios
            self.conexion.conexion.rollback()
            # Relanzamos la excepción original para que quien llamó al método la maneje
            raise e
        
        finally:
            # Cerramos el cursor para liberar recursos, ocurra lo que ocurra
            cursor.close()

    # Método para obtener todos los movimientos de un producto específico
    # Recibe el ID del producto
    # Devuelve una lista de objetos Movimiento ordenados de más reciente a más antiguo
    def obtener_por_producto(self, producto_id):
        # Creamos un cursor para ejecutar comandos SQL
        cursor = self.conexion.conexion.cursor()
        # Ejecutamos la consulta SQL para seleccionar todos los movimientos del producto dado
        # Los ordenamos por fecha en orden descendente (los más recientes primero)
        cursor.execute("""
            SELECT id, producto_id, tipo, cantidad, motivo, fecha
            FROM Movimiento
            WHERE producto_id = ?
            ORDER BY fecha DESC
        """, (producto_id,))
        # Obtenemos todos los resultados de la consulta como una lista de tuplas
        filas = cursor.fetchall()
        # Cerramos el cursor para liberar recursos
        cursor.close()
        # Convertimos cada tupla en un objeto Movimiento y devolvemos la lista completa
        return [
            Movimiento(
                id=f[0], producto_id=f[1], tipo=f[2],
                cantidad=f[3], motivo=f[4], fecha=f[5]
            )
            for f in filas
        ]