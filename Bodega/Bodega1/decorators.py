from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo_usuario == 'administrador':
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Acceso restringido: Se requiere rol de Administrador')
        return redirect('dashboard')
    return wrapper

def bodeguero_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo_usuario in ['administrador', 'bodeguero']:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Acceso restringido: Se requiere rol de Bodeguero o superior')
        return redirect('login')
    return wrapper

def puede_ver_productos(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')  # Cambiado de 'login_view' a 'login'
    return wrapper

def puede_egresar(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo_usuario in ['administrador', 'bodeguero']:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'No tienes permiso para hacer egresos')
        return redirect('dashboard')
    return wrapper

def puede_crear_categorias(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo_usuario == 'administrador':
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Solo administradores pueden crear categorías')
        return redirect('dashboard')
    return wrapper

def puede_crear_productos(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo_usuario == 'administrador':
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Solo administradores pueden crear productos')
        return redirect('dashboard')
    return wrapper