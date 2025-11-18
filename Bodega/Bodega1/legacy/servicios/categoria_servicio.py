# servicios/categoria_servicio.py - Lógica de negocio para la gestión de categorías

# Importamos el repositorio de categorías que maneja el acceso a la base de datos
from Bodega1.legacy.repositorios.categoria_repositorio import CategoriaRepositorio
# Clase que contiene la lógica de negocio para operaciones con categorías
class CategoriaServicio:
    # Constructor que recibe un repositorio de categorías
    def __init__(self, categoria_repositorio: CategoriaRepositorio):
        # Guardamos el repositorio en un atributo para usarlo en los métodos
        self.repositorio = categoria_repositorio

    # Método para crear una nueva categoría
    # Recibe el nombre de la categoría
    # Devuelve el ID de la categoría creada
    def crear_categoria(self, nombre: str) -> int:
        # Llamamos al repositorio para crear la categoría en la base de datos
        return self.repositorio.crear(nombre)

    # Método para obtener todas las categorías
    # Devuelve una lista de objetos Categoria
    def listar_categorias(self):
        # Llamamos al repositorio para obtener todas las categorías
        return self.repositorio.obtener_todos()

    # Método para actualizar una categoría existente
    # Recibe el ID de la categoría y el nuevo nombre
    # Devuelve True si se actualizó correctamente, False si no se encontró
    def actualizar_categoria(self, id: int, nombre: str) -> bool:
        # Llamamos al repositorio para actualizar la categoría
        return self.repositorio.actualizar(id, nombre)

    # Método para eliminar una categoría
    # Recibe el ID de la categoría a eliminar
    # Devuelve True si se eliminó correctamente, False si no se encontró o tiene productos
    def eliminar_categoria(self, id: int) -> bool:
        # Llamamos al repositorio para eliminar la categoría
        return self.repositorio.eliminar(id)