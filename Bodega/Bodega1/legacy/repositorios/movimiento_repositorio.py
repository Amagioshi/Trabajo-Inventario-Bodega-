from Bodega1.legacy.conexion import ConexionBD
from Bodega1.legacy.models.movimiento import Movimiento

class MovimientoRepositorio:
    def __init__(self, conexion):
        self.conexion = conexion

    def crear(self, producto_id, tipo, cantidad, motivo, fecha):
        cursor = self.conexion.conexion.cursor()
        
        try:
            cursor.execute("""
                SELECT stock FROM Producto WHERE id = ? AND activo = 1
            """, (producto_id,))
            fila = cursor.fetchone()
            
            if not fila:
                raise ValueError("Producto no encontrado o inactivo.")
            
            stock_actual = fila[0]
            
            if tipo == "egreso":
                if cantidad > stock_actual:
                    raise ValueError("Stock insuficiente para realizar el egreso.")
            
            if tipo == "ingreso":
                nuevo_stock = stock_actual + cantidad
            else:
                nuevo_stock = stock_actual - cantidad
            
            cursor.execute("UPDATE Producto SET stock = ? WHERE id = ?", (nuevo_stock, producto_id))
            
            cursor.execute("""
                INSERT INTO Movimiento (producto_id, tipo, cantidad, motivo, fecha)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?)
            """, (producto_id, tipo, cantidad, motivo, fecha))
            
            movimiento_id = cursor.fetchone()[0]
            self.conexion.conexion.commit()
            return movimiento_id
        
        except Exception as e:
            self.conexion.conexion.rollback()
            raise e
        
        finally:
            cursor.close()

    def obtener_por_producto(self, producto_id):
        cursor = self.conexion.conexion.cursor()
        cursor.execute("""
            SELECT id, producto_id, tipo, cantidad, motivo, fecha
            FROM Movimiento
            WHERE producto_id = ?
            ORDER BY fecha DESC
        """, (producto_id,))
        filas = cursor.fetchall()
        cursor.close()
        return [
            Movimiento(
                id=f[0], producto_id=f[1], tipo=f[2],
                cantidad=f[3], motivo=f[4], fecha=f[5]
            )
            for f in filas
        ]
