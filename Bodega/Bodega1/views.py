from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Importaciones ódigo legacy
from Bodega1.legacy.conexion import ConexionBD
from Bodega1.legacy.servicios.categoria_servicio import CategoriaServicio
from Bodega1.legacy.repositorios.categoria_repositorio import CategoriaRepositorio

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