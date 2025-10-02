from datetime import date

class Movimiento:
    def __init__(self, id: int, producto_id: int, tipo: str, cantidad: int, motivo: str, fecha: date):
        self.__id = id
        self.__producto_id = producto_id
        self.__tipo = tipo
        self.__cantidad = cantidad
        self.__motivo = motivo
        self.__fecha = fecha    