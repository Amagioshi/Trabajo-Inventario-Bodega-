# servicios/producto_servicio.py - Lógica de negocio para la gestión de productos

# Importamos el repositorio de productos que maneja el acceso a la base de datos
from repositorios.producto_repositorio import ProductoRepositorio

# Clase que contiene la lógica de negocio para operaciones con productos
class ProductoServicio:
    # Constructor que recibe un repositorio de productos
    def __init__(self, producto_repositorio: ProductoRepositorio):
        # Guardamos el repositorio en un atributo para usarlo en los métodos
        self.repositorio = producto_repositorio

    # Método para crear un nuevo producto
    # Recibe el nombre, precio y el ID de la categoría
    # Devuelve el ID del producto creado
    def crear_producto(self, nombre: str, precio: float, categoria_id: int) -> int:
        # Llamamos al repositorio para crear el producto en la base de datos
        return self.repositorio.crear(nombre, precio, categoria_id)

    # Método para obtener todos los productos activos
    # Devuelve una lista de objetos Producto
    def listar_productos(self):
        # Llamamos al repositorio para obtener todos los productos activos
        return self.repositorio.obtener_todos()

    # Método para obtener un producto por su ID
    # Recibe el ID del producto
    # Devuelve un objeto Producto o None si no existe
    def obtener_producto(self, id: int):
        # Llamamos al repositorio para obtener el producto por ID
        return self.repositorio.obtener_por_id(id)

    # Método para actualizar un producto existente
    # Recibe el ID del producto y los nuevos valores de nombre, precio y categoría
    # Devuelve True si se actualizó correctamente, False si no se encontró
    def actualizar_producto(self, id: int, nombre: str, precio: float, categoria_id: int) -> bool:
        # Llamamos al repositorio para actualizar el producto
        return self.repositorio.actualizar(id, nombre, precio, categoria_id)

    # Método para eliminar lógicamente un producto (marcarlo como inactivo)
    # Recibe el ID del producto a eliminar
    # Devuelve True si se desactivó correctamente, False si no se encontró
    def eliminar_producto(self, id: int) -> bool:
        # Llamamos al repositorio para eliminar (desactivar) el producto
        return self.repositorio.eliminar(id)