# prueba.py
from conexion import ConexionBD
from repositorios.categoria_repositorio import CategoriaRepositorio
from repositorios.producto_repositorio import ProductoRepositorio
from repositorios.movimiento_repositorio import MovimientoRepositorio
import time

if __name__ == "__main__":
    db = ConexionBD()
    try:
        db.conectar()
        print("Conexión exitosa.")
        
        # Usamos un nombre único para la categoría
        nombre_categoria = f"Prueba Categoria {int(time.time())}"
        categoria_repo = CategoriaRepositorio(db)
        id_cat = categoria_repo.crear(nombre_categoria)
        print(f"Categoría creada con ID: {id_cat}")
        
        categorias = categoria_repo.obtener_todos()
        print("Categorías obtenidas:")
        for cat in categorias:
            if cat.nombre == nombre_categoria:
                print(f"   ID: {cat.id}, Nombre: {cat.nombre}")
        
        # Creamos un producto con nombre único
        nombre_producto = f"Prueba Producto {int(time.time())}"
        producto_repo = ProductoRepositorio(db)
        id_prod = producto_repo.crear(nombre_producto, 2.5, id_cat)
        print(f"Producto creado con ID: {id_prod}")
        
        productos = producto_repo.obtener_todos()
        print("Productos obtenidos:")
        for prod in productos:
            if prod.nombre == nombre_producto:
                print(f"   ID: {prod.id}, Nombre: {prod.nombre}, Stock: {prod.stock}")
        
        movimiento_repo = MovimientoRepositorio(db)
        id_mov = movimiento_repo.crear(id_prod, "ingreso", 10, "Compra inicial", "2025-10-16")
        print(f"Movimiento creado con ID: {id_mov}")
        
        prod_actualizado = producto_repo.obtener_por_id(id_prod)
        print(f"Stock actualizado: {prod_actualizado.stock}")
        
        movimientos = movimiento_repo.obtener_por_producto(id_prod)
        print("Historial de movimientos:")
        for mov in movimientos:
            print(f"   Tipo: {mov.tipo}, Cantidad: {mov.cantidad}, Fecha: {mov.fecha}")
    
    except Exception as e:
        print(f"ERROR: {e}")
    
    finally:
        db.cerrar_conexion()
        print("Conexión cerrada.")