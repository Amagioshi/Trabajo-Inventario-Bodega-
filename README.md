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
# utilidades.py
Este archivo contiene herramientas de seguridad para la entrada de datos del usuario. Su función principal es evitar que el programa falle cuando el usuario ingresa información incorrecta.
1-. solicitar_entero() - Asegura que el usuario ingrese solo números enteros válidos
2-. solicitar_texto() - Garantiza que el texto ingresado cumpla con reglas específicas


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

# Carpeta Models


- Producto.py
Al igual que categoria.py, producto.py tiene la funcion de crear los parametros que tendra los "objetos productos" que sera almacenado en nuestra base de datos. Cada producto tendra los siguientes datos
1-. ID unico del producto
2-. Nombre del producto
3-. Precio del producto
4-. Stock del producto
5.- ID de la categoria a la que pertenece
6-. Actividad del producto, si es que esta disponible o no.

- Movimiento.py
El objetivo de movimiento.py es crear los parametros que seran almacenados movimientos como ingreso y egreso de productos que ingresan a la bodega. movimiento.py almacena los siguientes datos de almacenamiento.

1-. ID de movimiento
2-. ID del producto que se mueve
3-. Si es un ingreso o egreso
4-. Cuantas unidades entran o salen
5-. Motivo: Porque hizo el movimiento 
6-. Cuando hizo el movimiento con fecha
 


-categoria.py
Este archivo nos permite crear un parametro general que tendra nuestro elemento categoria, significa que define la estructura del "objeto categoria" que sera almacenado en nuestra base de datos. 
1-. ID de categoria
2-. Nombre de categoria




# Carpeta:  Menú
- Menú_principal.py



# Carpeta: Repositorio

- Categoria_repositorio.py
Este archivo cumple la funcion de hacer interacciones entre los parametros de nuestro "objeto categoria" creado y nuestra base de datos.
1-. Crea nuevas categorias, toma datos con la estructura dada por categoria.py y da la orden a la base de datos para crearla
2-. tambien puede listar todas nuestras categorias
3-. buscar por categoria especifica
4.- actualizar categoria
5-. Eliminar categorias


- Movimiento_repositorio.py
movimientor_repositorio.py comple con la funcion de tomar los datos pedidos por movimiento.py y interactuar con la base de datos para almacenarlo, en resumen registra y actualiza movimientos en nuestra base de datos.
1-. resgistra movimientos y actualiza stock
2-. ve historial de un producto


- Producto_repositorio.py
Este archivo cumple la función de hacer interacciones entre los parámetros de nuestro "objeto producto" creado y nuestra base de datos.
1-. Crea nuevos productos 
2-. Lista todos los productos 
3-. Busca productos específicos por si id


# Carpeta servicios 

- categoria_servicio.py
Este archivo actúa como un coordinador entre los menús de usuario y el repositorio de categorías. Su función principal es recibir las solicitudes desde la interfaz y delegar el trabajo al repositorio correspondiente.

1-. Recibe instrucciones desde los menús del programa
2-. Se comunica con CategoriaRepositorio para ejecutar las operaciones en la base de datos
3-. Devuelve los resultados a los menús para mostrar al usuario

- producto_servicio.py
Este archivo cumple la misma función de coordinación pero para las operaciones con productos. Sirve como intermediario entre la interfaz de usuario y el repositorio de productos.
1-. Recibe solicitudes desde los menús relacionados con productos
2-. Coordina con ProductoRepositorio para realizar las operaciones en base de datos
3-. Retorna las respuestas a la interfaz para informar al usuario


Dado a un cambio de SO se implementaron nuevos programas para poder hacer projecto

Docker-Desktop reemplaza a SQL-Express 
DBeaver reemplaza a Sql Scerver Manager Studio
Los metodos de conexion entre el programa y la base de datos se mantiene con dotenv y pyodbc


# Django

 Hoy se implemento el framework Django en la carpeta Bodega y Bodega1 y se logro conectar a la base de datos SQL Server en Docker via pyodbc y dotenv

 





