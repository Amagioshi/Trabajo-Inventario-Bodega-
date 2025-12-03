from django.urls import path
from . import views  

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('categorias/', views.gestion_categorias, name='gestion_categorias'),
    path('productos/', views.gestion_productos, name='gestion_productos'),
    path('movimientos/', views.gestion_movimientos, name='gestion_movimientos'),
    path('movimientos/historial/', views.historial_movimientos, name='historial_movimientos'),
    path('informes/', views.informes, name='informes'),
    path('productos/ver/', views.ver_productos, name='ver_productos'),
]