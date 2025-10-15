# prueba.py → para probar funciones de conexión y modelos
# Este archivo NO se sube a GitHub. Solo es para desarrollo local.

# Importamos la clase de conexión (tu archivo se llama conexion.py)
from conexion import ConexionBD

# Importamos la clase Categoria para validar
from models.categoria import Categoria

# Bloque de prueba principal
if __name__ == "__main__":
    # Paso 1: crear objeto de conexión
    db = ConexionBD()
    
    try:
        # Paso 2: conectarse a la base de datos
        db.conectar()
        print(" Conexión exitosa.")
        
        # Paso 3: crear una categoría de prueba
        nombre_prueba = "Lácteos"
        id_nuevo = db.crear_categoria(nombre_prueba)
        print(f" Categoría creada con ID: {id_nuevo}")
        
        # Paso 4: obtener todas las categorías
        categorias = db.obtener_categorias()
        print(" Categorías obtenidas:")
        for cat in categorias:
            # cat es un OBJETO Categoria, no una tupla
            print(f"   ID: {cat.id}, Nombre: {cat.nombre}")
    
    except Exception as e:
        # Capturamos cualquier error y lo mostramos CLARAMENTE
        print(f" ERROR: {e}")
    
    finally:
        # Paso 5: cerrar conexión SIEMPRE, incluso si hubo error
        db.cerrar_conexion()
        print(" Conexión cerrada.")