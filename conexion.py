import pyodbc
from dotenv import load_dotenv
import os

class ConexionBD:
    def __init__(self):
        load_dotenv()
        self.driver = os.getenv("DRIVER")
        self.servidor = os.getenv("SERVER")
        self.base_datos = os.getenv("DATABASE")
        self.usuario = os.getenv("DB_USERNAME")    # CAMBIADO
        self.password = os.getenv("DB_PASSWORD")   # CAMBIADO
        self.conexion = None
        
    def conectar(self):
        if not all([self.driver, self.servidor, self.base_datos, self.usuario, self.password]):
            raise ValueError("Faltan variables en .env")
        
        cadena_conexion = (
            f"DRIVER={{{self.driver}}};"
            f"SERVER={self.servidor};"
            f"DATABASE={self.base_datos};"
            f"UID={self.usuario};"
            f"PWD={self.password};"
            f"Encrypt=no;"
            f"TrustServerCertificate=yes;"
        )
        self.conexion = pyodbc.connect(cadena_conexion)

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()