from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Importaciones ódigo legacy
from Bodega1.legacy.conexion import ConexionBD
from Bodega1.legacy.servicios.categoria_servicio import CategoriaServicio
from Bodega1.legacy.repositorios.categoria_repositorio import CategoriaRepositorio

from Bodega1.legacy.servicios.producto_servicio import ProductoServicio
from Bodega1.legacy.repositorios.producto_repositorio import ProductoRepositorio
from Bodega1.legacy.repositorios.categoria_repositorio import CategoriaRepositorio
from Bodega1.legacy.repositorios.movimiento_repositorio import MovimientoRepositorio
# Vista del dashboard 
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})

# Vista de login 
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

# Vista de logout 
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('login')

# Vista de gestión de categorías
@login_required
def gestion_categorias(request):
    db = ConexionBD()
    try:
        db.conectar()
        repositorio = CategoriaRepositorio(db)
        servicio = CategoriaServicio(repositorio)
        
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            try:
                id_nuevo = servicio.crear_categoria(nombre)
                messages.success(request, f'Categoría creada con ID: {id_nuevo}')
            except Exception as e:
                messages.error(request, f'Error al crear categoría: {e}')
        
        categorias = servicio.listar_categorias()
        return render(request, 'gestion_categorias.html', {
            'categorias': categorias
        })
        
    except Exception as e:
        messages.error(request, f'Error de conexión: {e}')
        return render(request, 'gestion_categorias.html', {
            'categorias': []
        })
    finally:
        db.cerrar_conexion()




@login_required
def gestion_productos(request):
    db = ConexionBD()
    try:
        db.conectar()
        repo_productos = ProductoRepositorio(db)
        repo_categorias = CategoriaRepositorio(db)
        servicio = ProductoServicio(repo_productos)
        
        # Obtener categorías para el formulario
        categorias = repo_categorias.obtener_todos()
        
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            precio = float(request.POST.get('precio'))
            categoria_id = int(request.POST.get('categoria_id'))
            
            try:
                id_nuevo = servicio.crear_producto(nombre, precio, categoria_id)
                messages.success(request, f'Producto creado con ID: {id_nuevo}')
            except Exception as e:
                messages.error(request, f'Error al crear producto: {e}')
        
        productos = servicio.listar_productos()
        return render(request, 'gestion_productos.html', {
            'productos': productos,
            'categorias': categorias
        })
        
    except Exception as e:
        messages.error(request, f'Error de conexión: {e}')
        return render(request, 'gestion_productos.html', {
            'productos': [],
            'categorias': []
        })
    finally:
        db.cerrar_conexion()



@login_required
def gestion_movimientos(request):
    db = ConexionBD()
    try:
        db.conectar()
        repo_movimientos = MovimientoRepositorio(db)
        repo_productos = ProductoRepositorio(db)
        
        productos = repo_productos.obtener_todos()
        
        if request.method == 'POST':
            producto_id = int(request.POST.get('producto_id'))
            tipo = request.POST.get('tipo')
            cantidad = int(request.POST.get('cantidad'))
            motivo = request.POST.get('motivo')
            
            try:
                movimiento_id = repo_movimientos.crear(
                    producto_id, tipo, cantidad, motivo, "2025-11-18"
                )
                messages.success(request, f'Movimiento registrado con ID: {movimiento_id}')
                
                # Actualizar info del producto
                producto_actualizado = repo_productos.obtener_por_id(producto_id)
                messages.info(request, f'Nuevo stock: {producto_actualizado.stock}')
                
            except Exception as e:
                messages.error(request, f'Error al registrar movimiento: {e}')
        
        return render(request, 'gestion_movimientos.html', {
            'productos': productos
        })
        
    except Exception as e:
        messages.error(request, f'Error de conexión: {e}')
        return render(request, 'gestion_movimientos.html', {
            'productos': []
        })
    finally:
        db.cerrar_conexion()

@login_required
def historial_movimientos(request):
    db = ConexionBD()
    try:
        db.conectar()
        repo_movimientos = MovimientoRepositorio(db)
        repo_productos = ProductoRepositorio(db)
        
        producto_id = request.GET.get('producto_id')
        movimientos = []
        
        if producto_id:
            movimientos = repo_movimientos.obtener_por_producto(int(producto_id))
        
        productos = repo_productos.obtener_todos()
        
        return render(request, 'historial_movimientos.html', {
            'movimientos': movimientos,
            'productos': productos,
            'producto_seleccionado': producto_id
        })
        
    except Exception as e:
        messages.error(request, f'Error de conexión: {e}')
        return render(request, 'historial_movimientos.html', {
            'movimientos': [],
            'productos': []
        })
    finally:
        db.cerrar_conexion()