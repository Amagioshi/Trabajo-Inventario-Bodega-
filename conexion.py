import pyodbc  # para conectar a bases de datos SQL Server
from dotenv import load_dotenv # para leer el archivo .env
import os # para acceder a las variables de entorno

class ConexionBD: # definimos la clase conexionBD que agrupara la logica de conexion
    def __init__(self): #este  metodo se ejcuta cuando creamos un objeto de esta clase (conexionBD)
        load_dotenv() # cargamos el archivo .env que esta presente el la carpeta del codigo
        self.driver = os.getenv("DRIVER") # lee el valor de la variable "DRIVER del archivo.env" y se almacena en self.driver
        self.servidor = os.getenv("SERVER") # tambien se lee y guarda la variable server presente en .env a la clase
        self.base_datos = os.getenv("DATABASE")
        self.conexion = None # aun no hay conexion abierta
        
        
    def conectar(self):
        try: # se usa try/except para manejar errores sin que el programa se detenga
            cadena_conexion = (
                f"DRIVER={{{self.driver}}};"
                f"SERVER={self.servidor};"
                f"DATABASE={self.base_datos};"
                "Trusted_Connection=yes;"
            )
            self.conexion = pyodbc.connect(cadena_conexion) # se utiliza puodbc.conect() para abrir la conexion y la guardamos en self.conexion
            print("Conexion exitosa a SQL Server.")
        
        except exception as e: # si ocurre un error, se captura y se imprime
            print("ERROR al conectar a la base de datos:", e)
            
    def cerrar_conexion(self): # para cerrar la conexion de forma segura
        if self.conexion:# verificamos si self.conexion no es none (si es que hay una conexion abierta)
            self.conexion.close() # cerramos la conexion activa
            print("Conexion cerrada con exito.")
    
    
    def ejecutar_consulta(self, consulta, parametros= ()): # forma para ejecutar consultas que devuelven datos como (select)
        try: # usamos try/except para manejar errores en la consulta
            cursor = self.conexion.cursor() # creamos un cursor para ejecutar comandos 
            cursor.execute(consulta, parametros) #ejecutamos la consulta SQL que nos pasaron con sus parametros
            return cursor.fetchall() #devolvemos todos los resultados de la consulta
        except Exception as e: # si hay un error, lo capturamos e imprimimos
            print("Error al realizar la consulta:", e)
            return []
    
    
    #para ejecutar comandos que modifican la base de datos
    def ejecutar_instruccion(self, consulta, parametros=()):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(consulta, parametros)
            self.conexion.commit()
            print("Instruccion ejecutada correctamente.")
        except exception as e: 
            print("Error al ejecutar la instruccion:", e)
            self.conexion.rollback() # deshacemos cualquier cambio parcial para mantener la consistencia de la bd