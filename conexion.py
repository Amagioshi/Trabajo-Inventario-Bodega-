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
        load_dotenv()
        user = os.getenv("sa")
        password = os.getenv("Amagioshi@")
        encrypt = os.getenv("ENCRYPT","no")

        if not all([self.driver, self.servidor, self.base_datos]):
            raise ValueError("Faltan variables en .env")
        cadena_conexion = (
            f"DRIVER={{{self.driver}}};"
            f"SERVER={self.servidor};"
            f"DATABASE={self.base_datos};"
            f"UID={user;}"
            f"PWD={password};"
            f"Encrypt={encrypt};"
            f"TrustServerCertificate=yes;"
        )
        self.conexion = pyodbc.connect(cadena_conexion)

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()

    