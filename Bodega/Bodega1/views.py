import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
from .decorators import admin_required, bodeguero_required, puede_ver_productos, puede_egresar, puede_crear_categorias, puede_crear_productos

# Importaciones código legacy
from Bodega1.legacy.conexion import ConexionBD
from Bodega1.legacy.servicios.categoria_servicio import CategoriaServicio
from Bodega1.legacy.repositorios.categoria_repositorio import CategoriaRepositorio

from Bodega1.legacy.servicios.producto_servicio import ProductoServicio
from Bodega1.legacy.repositorios.producto_repositorio import ProductoRepositorio
from Bodega1.legacy.repositorios.categoria_repositorio import CategoriaRepositorio
from Bodega1.legacy.repositorios.movimiento_repositorio import MovimientoRepositorio
from Bodega1.models import Usuario

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
        
        # Buscar en usuarios.txt
        usuarios_path = os.path.join(settings.BASE_DIR, 'usuarios.txt')
        
        try:
            with open(usuarios_path, 'r') as f:
                for linea in f:
                    linea = linea.strip()
                    if linea and ',' in linea:
                        user_file, pass_file, rol = linea.split(',', 2)
                        
                        if username == user_file and password == pass_file:
                            # Usuario encontrado
                            user, created = Usuario.objects.get_or_create(
                                username=username,
                                defaults={'tipo_usuario': rol, 'is_active': True}
                            )
                            
                            if not created:
                                user.tipo_usuario = rol
                                user.save()
                            
                            user.backend = 'django.contrib.auth.backends.ModelBackend'
                            login(request, user)
                            request.session['rol_usuario'] = rol
                            
                            messages.success(request, f'Bienvenido {username}')
                            return redirect('dashboard')
            
            # Si llegó aquí, no encontró el usuario
            messages.error(request, 'Usuario o contraseña incorrectos')
            
        except FileNotFoundError:
            messages.error(request, 'Archivo usuarios.txt no encontrado')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'login.html')

# Vista de logout 
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('login')

# Vista de gestión de categorías
@puede_crear_categorias
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
@puede_ver_productos
def ver_productos(request):
    """Vista para VER productos (todos los roles)"""
    db = ConexionBD()
    try:
        db.conectar()
        repo_productos = ProductoRepositorio(db)
        
        productos = repo_productos.obtener_todos()
        return render(request, 'ver_productos.html', {
            'productos': productos
        })
        
    except Exception as e:
        messages.error(request, f'Error de conexión: {e}')
        return render(request, 'ver_productos.html', {
            'productos': []
        })
    finally:
        db.cerrar_conexion()



@puede_crear_productos
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

@bodeguero_required
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

@puede_ver_productos
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

@admin_required
def informes(request):
    db = ConexionBD()
    try:
        db.conectar()
        repo_productos = ProductoRepositorio(db)
        
        productos = repo_productos.obtener_todos()
        total_productos = len(productos)
        total_stock = sum(p.stock for p in productos)
        valor_inventario = sum(p.stock * p.precio for p in productos)
        
        # Productos con stock bajo (menos de 10 unidades)
        productos_stock_bajo = [p for p in productos if p.stock < 10]
        
        return render(request, 'informes.html', {
            'total_productos': total_productos,
            'total_stock': total_stock,
            'valor_inventario': valor_inventario,
            'productos_stock_bajo': productos_stock_bajo,
        })
        
    except Exception as e:
        messages.error(request, f'Error en informes: {e}')
        return render(request, 'informes.html', {
            'total_productos': 0,
            'total_stock': 0,
            'valor_inventario': 0,
            'productos_stock_bajo': [],
        })
    finally:
        db.cerrar_conexion()