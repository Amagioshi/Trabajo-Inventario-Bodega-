from conexion import ConexionBD
db = ConexionBD()
db.conectar()
if db.conexion:
    sql = """
    if not exists (select * from sysobjects where name= 'Productos' and xtype= 'U')
    create table productos ( 
        id int Identity (1,1) primary key,
        nombre nvarchar(100) not null,
        precio decimal(10,2) not null,
        stock int not null
    )
    """
    db.ejecutar_instruccion(sql)
    db.cerrar_conexion()
else:
    print("No se puedo conectar a la base de datos.")
    