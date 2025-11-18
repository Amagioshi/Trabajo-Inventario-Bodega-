class Producto:
    def __init__(self, id: int, nombre: str, precio: float, stock: int, categoria_id: int, activo: bool = True):
        if id < 0:
            raise ValueError(f"El ID {id} no puede ser negativo.")
        if not nombre or not nombre.strip():
            raise ValueError(f"Entrada invalida: {nombre}El nombre no puede estar vacio.")
        if len(nombre.strip()) < 2 or len(nombre.strip()) > 100:
            raise ValueError(f"Entrada invalida: {nombre}.El nombre debe tener entre 2 y 100 caracteres.")
        if precio <= 0: # el precio debe ser positivo y mayor a 0  
            raise ValueError(f"Entrada invalida {precio}. El precio debe ser mayor a 0.")
        if stock < 0: # el stock no puede ser negativo 
            raise ValueError(f"Entrada invalida {stock}. El stock no puede ser negativo.")
        if categoria_id < 0: # el id de la categoria de un producto no puede ser negativo
            raise ValueError(f"entrada invalida {categoria_id}. El ID debe ser mayor a 0.")
        if not isinstance(activo, bool):
            raise ValueError(f"Entrada invalida {activo}. el estado debe ser verdadero o falso")
        self.__id = id
        self.__nombre = nombre.strip()
        self.__precio = precio
        self.__stock = stock
        self.__categoria_id = categoria_id
        self.__activo = activo
    @property
    def id(self):
        return self.__id
    @property 
    def nombre(self):
        return self.__nombre
    @property
    def precio(self):   
        return self.__precio
    @property
    def stock(self):
        return self.__stock 
    @property
    def categoria_id(self):
        return self.__categoria_id
    @property
    def activo(self):
        return self.__activo
    