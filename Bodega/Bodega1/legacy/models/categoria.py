class Categoria: # definimos la clase Categoria
    def __init__(self, id: int, nombre: str): # contruimos la clase con los atributos y señala el tipo de dato que deberia contener
        if id < 0: # rechaza id negativos
            raise ValueError(f"El ID {id} no puede ser negativo.") # detiene la ejecucion y muestra un mensaje de error si la regla no se cumple
        if not nombre or not nombre.strip(): # rechaza nombre vacios o con solo espacios
            raise ValueError("El nombre no puede estar vacio.")
        if len(nombre.strip()) < 2: # nos asegura que tenga por lo menos 2 caracteres validos
            raise ValueError("El nombre debe tener almenos 2 caracteres.")
        self.__id = id # se guarda Guarda los valores de forma privada e impedimos que se modificquen desde afuera
        self.__nombre = nombre.strip()
        
    @property # permite leer el valor del atributo pero no modificarlo
    def id(self):
        return self.__id
    
    @property
    def nombre(self):
        return self.__nombre