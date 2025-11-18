from datetime import date

class Movimiento:
    def __init__(self, id: int, producto_id: int, tipo: str, cantidad: int, motivo: str, fecha: date):
        if id < 0: 
            raise ValueError(f"Entrada invalida: {id}. El ID debe ser positivo y mayor a 0.")
        if producto_id < 0: 
            raise ValueError(f"Entrada invalida: {producto_id}. El ID del producto debe ser positivo y mayor a 0.")
        if not tipo or tipo.strip().lower() not in ("ingreso", "egreso"):
            raise ValueError(f"Entrada invalida: {tipo}. El tipo debe ser 'ingreso o egreso'.")
        if cantidad <= 0:
            raise ValueError(f"Entrada invalida: {cantidad}. La cantidad debe ser mayor a 0.")
        motivo_limpio = motivo.strip()
        if len(motivo_limpio) < 5:
            raise ValueError(f"Entrada invalida: {motivo}. El motivo debe tener al menos 5 caracteres.")
        if len(motivo_limpio) > 200:
            raise ValueError(f"Entrada invalida: {motivo}. El motivo debe tener como maximo 200 caracteres.")
        self.__id = id
        self.__producto_id = producto_id
        self.__tipo = tipo
        self.__cantidad = cantidad
        self.__motivo = motivo
        self.__fecha = fecha    
        
    @property
    def id(self):
        return self.__id

    @property 
    def producto_id(self):
        return self.__producto_id
    
    @property 
    def tipo(self):
        return self.__tipo
    
    @property 
    def cantidad(self):
        return self.__cantidad
    
    @property
    def motivo(self):
        return self.__motivo
    
    @property
    def fecha(self):
        return self.__fecha
    
    
    
    
    
        