# Importamos la clase de conexión a la base de datos
from conexion import ConexionBD
# Importamos la función que muestra el menú principal
from menus.menu_principal import mostrar_menu_principal
# Importamos los servicios y repositorios necesarios para categorías
from servicios.categoria_servicio import CategoriaServicio
from repositorios.categoria_repositorio import CategoriaRepositorio
# Importamos los servicios y repositorios necesarios para productos
from servicios.producto_servicio import ProductoServicio
from repositorios.producto_repositorio import ProductoRepositorio
# Importamos los repositorios necesarios para movimientos
from repositorios.movimiento_repositorio import MovimientoRepositorio
# Importamos las funciones de utilidades para entrada de usuario
from utilidades import solicitar_texto, solicitar_entero
# Función que maneja el menú de gestión de categorías
def menu_categorias(db):
    # Creamos el repositorio y el servicio de categorías
    repositorio = CategoriaRepositorio(db)
    servicio = CategoriaServicio(repositorio)
    
    # Bucle principal del menú de categorías
    while True:
        print("\n=== GESTION DE CATEGORIAS ===")
        print("1. Crear categoria")
        print("2. Listar categorias")
        print("3. Actualizar categoria")
        print("4. Eliminar categoria")
        print("5. Volver al menu principal")
        print("==============================")
        
        # Solicitamos la opcion al usuario
        opcion = input("Seleccione una opcion: ").strip()
        
        # Opcion 1: Crear categoria
        if opcion == "1":
            # Solicitamos el nombre con validacion (2-50 caracteres)
            nombre = solicitar_texto("Nombre de la categoria (2-50 caracteres): ", 2, 50, solo_letras=True)
            try:
                # Intentamos crear la categoria
                id_nuevo = servicio.crear_categoria(nombre)
                print(f"Categoria creada con ID: {id_nuevo}")
            except Exception as e:
                # Mostramos cualquier error que ocurra
                print(f"Error al crear categoria: {e}")
                
        # Opcion 2: Listar categorias
        elif opcion == "2":
            # Obtenemos todas las categorias
            categorias = servicio.listar_categorias()
            if categorias:
                print("\nCategorias existentes:")
                # Mostramos cada categoria
                for cat in categorias:
                    print(f"ID: {cat.id}, Nombre: {cat.nombre}")
            else:
                print("No hay categorias registradas.")
                
        # Opcion 3: Actualizar categoria
        elif opcion == "3":
            # Solicitamos el ID de la categoria a actualizar
            id_cat = solicitar_entero("ID de la categoria a actualizar: ", 1)
            # Solicitamos el nuevo nombre
            nombre = solicitar_texto("Nuevo nombre (2-50 caracteres): ", 2, 50, solo_letras=True)
            # Intentamos actualizar la categoria
            if servicio.actualizar_categoria(id_cat, nombre):
                print("Categoria actualizada correctamente.")
            else:
                print("No se encontro la categoria o el nombre ya existe.")
                
        # Opcion 4: Eliminar categoria
        elif opcion == "4":
            # Solicitamos el ID de la categoria a eliminar
            id_cat = solicitar_entero("ID de la categoria a eliminar: ", 1)
            # Intentamos eliminar la categoria
            if servicio.eliminar_categoria(id_cat):
                print("Categoria eliminada correctamente.")
            else:
                print("No se puede eliminar: categoria no existe o tiene productos asociados.")
                
        # Opcion 5: Volver al menu principal
        elif opcion == "5":
            break
        else:
            print("Opcion invalida.")

# Funcion que maneja el menu de gestion de productos
def menu_productos(db):
    # Creamos el repositorio y el servicio de productos
    repositorio = ProductoRepositorio(db)
    servicio = ProductoServicio(repositorio)
    # Creamos tambien el repositorio de categorias para listarlas
    repo_categorias = CategoriaRepositorio(db)
    
    # Bucle principal del menu de productos
    while True:
        print("\n=== GESTION DE PRODUCTOS ===")
        print("1. Crear producto")
        print("2. Listar productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Volver al menu principal")
        print("=============================")
        
        opcion = input("Seleccione una opcion: ").strip()
        
        # Opcion 1: Crear producto
        if opcion == "1":
            # Primero mostramos las categorias disponibles
            categorias = repo_categorias.obtener_todos()
            if not categorias:
                print("No hay categorias disponibles. Cree una categoria primero.")
                continue
            
            print("\nCategorias disponibles:")
            for cat in categorias:
                print(f"ID: {cat.id}, Nombre: {cat.nombre}")
            
            # Solicitamos los datos del producto
            nombre = solicitar_texto("Nombre del producto (2-100 caracteres): ", 2, 100, solo_letras=True)
            precio = float(solicitar_entero("Precio del producto (en centavos, ej: 1500 para $15.00): ", 1)) / 100
            categoria_id = solicitar_entero("ID de la categoria: ", 1)
            
            try:
                # Verificamos que la categoria exista
                categoria = repo_categorias.obtener_por_id(categoria_id)
                if not categoria:
                    print("La categoria especificada no existe.")
                    continue
                
                # Creamos el producto
                id_nuevo = servicio.crear_producto(nombre, precio, categoria_id)
                print(f"Producto creado con ID: {id_nuevo}")
            except Exception as e:
                print(f"Error al crear producto: {e}")
                
        # Opcion 2: Listar productos
        elif opcion == "2":
            productos = servicio.listar_productos()
            if productos:
                print("\nProductos existentes:")
                for prod in productos:
                    print(f"ID: {prod.id}, Nombre: {prod.nombre}, Precio: ${prod.precio:.2f}, Stock: {prod.stock}, Categoria ID: {prod.categoria_id}")
            else:
                print("No hay productos registrados.")
                
        # Opcion 3: Actualizar producto
        elif opcion == "3":
            id_prod = solicitar_entero("ID del producto a actualizar: ", 1)
            # Verificamos que el producto exista
            producto_actual = servicio.obtener_producto(id_prod)
            if not producto_actual:
                print("Producto no encontrado.")
                continue
            
            nombre = solicitar_texto("Nuevo nombre (2-100 caracteres): ", 2, 100, solo_letras=True)
            precio = float(solicitar_entero("Nuevo precio (en centavos): ", 1)) / 100
            categoria_id = solicitar_entero("Nuevo ID de categoria: ", 1)
            
            # Verificamos que la categoria exista
            categoria = repo_categorias.obtener_por_id(categoria_id)
            if not categoria:
                print("La categoria especificada no existe.")
                continue
            
            if servicio.actualizar_producto(id_prod, nombre, precio, categoria_id):
                print("Producto actualizado correctamente.")
            else:
                print("No se pudo actualizar el producto.")
                
        # Opcion 4: Eliminar producto
        elif opcion == "4":
            id_prod = solicitar_entero("ID del producto a eliminar: ", 1)
            if servicio.eliminar_producto(id_prod):
                print("Producto eliminado correctamente.")
            else:
                print("No se encontro el producto o ya estaba eliminado.")
                
        # Opcion 5: Volver al menu principal
        elif opcion == "5":
            break
        else:
            print("Opcion invalida.")
# Funcion que maneja el registro de movimientos
def menu_movimientos(db):
    # Creamos los repositorios necesarios
    repo_productos = ProductoRepositorio(db)
    repo_movimientos = MovimientoRepositorio(db)
    
    while True:
        print("\n=== REGISTRO DE MOVIMIENTOS ===")
        print("1. Registrar ingreso")
        print("2. Registrar egreso")
        print("3. Ver historial de un producto")
        print("4. Volver al menu principal")
        print("================================")
        
        opcion = input("Seleccione una opcion: ").strip()
        
        if opcion == "1" or opcion == "2":
            # Listar productos disponibles
            productos = repo_productos.obtener_todos()
            if not productos:
                print("No hay productos disponibles.")
                continue
            
            print("\nProductos disponibles:")
            for prod in productos:
                print(f"ID: {prod.id}, Nombre: {prod.nombre}, Stock: {prod.stock}")
            
            producto_id = solicitar_entero("ID del producto: ", 1)
            producto = repo_productos.obtener_por_id(producto_id)
            if not producto:
                print("Producto no encontrado.")
                continue
            
            cantidad = solicitar_entero("Cantidad: ", 1)
            motivo = solicitar_texto("Motivo (5-200 caracteres): ", 5, 200)
            
            tipo = "ingreso" if opcion == "1" else "egreso"
            
            try:
                # Registrar el movimiento (el stock se actualiza automaticamente)
                movimiento_id = repo_movimientos.crear(producto_id, tipo, cantidad, motivo, "2025-10-21")
                print(f"Movimiento registrado con ID: {movimiento_id}")
                
                # Mostrar nuevo stock
                producto_actualizado = repo_productos.obtener_por_id(producto_id)
                print(f"Nuevo stock: {producto_actualizado.stock}")
                
            except Exception as e:
                print(f"Error al registrar movimiento: {e}")
                
        elif opcion == "3":
            producto_id = solicitar_entero("ID del producto: ", 1)
            movimientos = repo_movimientos.obtener_por_producto(producto_id)
            if movimientos:
                print(f"\nHistorial de movimientos para producto ID {producto_id}:")
                for mov in movimientos:
                    print(f"ID: {mov.id}, Tipo: {mov.tipo}, Cantidad: {mov.cantidad}, Motivo: {mov.motivo}, Fecha: {mov.fecha}")
            else:
                print("No hay movimientos registrados para este producto.")
                
        elif opcion == "4":
            break
        else:
            print("Opcion invalida.")
            
        # Funcion que maneja los informes
def menu_informes(db):
    repo_productos = ProductoRepositorio(db)
    repo_movimientos = MovimientoRepositorio(db)
    
    while True:
        print("\n=== INFORMES ===")
        print("1. Productos con stock bajo")
        print("2. Historial de movimientos por producto")
        print("3. Volver al menu principal")
        print("================")
        
        opcion = input("Seleccione una opcion: ").strip()
        
        if opcion == "1":
            productos = repo_productos.obtener_todos()
            stock_minimo = solicitar_entero("Ingrese el stock minimo para considerar bajo: ", 0)
            productos_bajo_stock = [p for p in productos if p.stock <= stock_minimo]
            
            if productos_bajo_stock:
                print(f"\nProductos con stock <= {stock_minimo}:")
                for prod in productos_bajo_stock:
                    print(f"ID: {prod.id}, Nombre: {prod.nombre}, Stock: {prod.stock}, Categoria ID: {prod.categoria_id}")
            else:
                print(f"No hay productos con stock <= {stock_minimo}.")
                
        elif opcion == "2":
            producto_id = solicitar_entero("ID del producto: ", 1)
            movimientos = repo_movimientos.obtener_por_producto(producto_id)
            if movimientos:
                print(f"\nHistorial de movimientos para producto ID {producto_id}:")
                for mov in movimientos:
                    print(f"ID: {mov.id}, Tipo: {mov.tipo}, Cantidad: {mov.cantidad}, Motivo: {mov.motivo}, Fecha: {mov.fecha}")
            else:
                print("No hay movimientos registrados para este producto.")
                
        elif opcion == "3":
            break
        else:
            print("Opcion invalida.")    
# Funcion principal que inicia el programa
def main():
    # Creamos la conexion a la base de datos
    db = ConexionBD()
    try:
        # Nos conectamos
        db.conectar()
        print("Conexion a la base de datos establecida.")
        
        # Bucle principal del programa
        while True:
            # Mostramos el menu principal
            mostrar_menu_principal()
            opcion = input("Seleccione una opcion: ").strip()
            
            # Opcion 5: Salir
            if opcion == "5":
                print("Saliendo del sistema...")
                break
            # Opcion 1: Gestion de Categorias
            elif opcion == "1":
                menu_categorias(db)
            # Opcion 2: Gestion de Productos
            elif opcion == "2":
                menu_productos(db)
            
            elif opcion == "3":
                menu_movimientos(db)
                
            elif opcion == "4":
                menu_informes(db)
    
    except KeyboardInterrupt:
        print("\nEjecucion interrumpida por el usuario.")
    except Exception as e:
        print(f"Error critico: {e}")
    
    finally:
        # Cerramos la conexion
        db.cerrar_conexion()
        print("Conexion cerrada.")

# Punto de entrada del programa
if __name__ == "__main__":
    main()