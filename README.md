# Programacion Orientada al Objeto seguro
# Trabajo Inventario Bodega 

Proyecto para gestionar el inventario de una bodega usando SQL Server y Python.

# Este trabajo se realizara con 

- SQL Server 2022 Express
- Python 
- VS code como editor de codigo
- SQL Server Manager studio 20 como visualizador 

# Configuracion

1. Se creara una base de datos en SQL server managment studio 20.

2. Configurar archivo ".env".

3. Instala dependencias: pip install pyodbc python-dotenv


# .env
# conexion.py
- el archivo conecion.py contiene la clase ConexionBD, responsable de gestionar la conexion con la base de datos 
- contiene variables del archivo .env(DRIVER, SERVER, DATABASE) para configurar la conexion.
- Funciona con autenticacion de Windows (Trusted_Connecction=yes) por lo que no requiere usuario y contraseña
- contiene metodos como:
° conectar(): que abre la conexion y valida que las variables del entorno esten presentes.
° cerrar_conexion(): cierra la conexion de forma segura.
° ejecutar_consulta(): ejecuta sentencias  (SELECT) y devuelve resultados.
° ejecutar_instruccion(): (INSERT, UPDATE, DELETE) con manejo de transacciones (commit/ rollback).
° implementa manejo de errores con (TRY/EXCEPT) para evitar que el programa se detenga ante fallos.
- Esta clase esta diseñada para ser reutilizable con otros modulos del proyecto, pueden importar desde la clase sin duplicar codigo


# crear_tabla.py
- este archivo se utiliza solo una vez para preparar la estructura de base de datos al inicio del proyecto

° Conecta a InventarioBodegaBD usando la clase ConexionBD.
° Ejecuta una instruccion SQL que crea la tabla Productos si no existe
° La tabla incluye los campos: id (clave primaria), nombre, id y stock.
° No inserta datos ni modifica, solo define la estructura.
° Esto solo esta destinado a verificar que la base de datos esté lista para operaciones posteriores


# A partir de ahora empezaremos con el codigo funcional exluyendo la conexion a DB

- Carpeta Models
Categoria.py:
contiene una clase llamda categoria, que cumple la funcion de agrupar productos segun su categoria, "lacteos", "cereales", "cecinas" etc..
esto nos permite hacer busquedas mas eficientes entre productos.

- Producto.py

- Movimiento.py
