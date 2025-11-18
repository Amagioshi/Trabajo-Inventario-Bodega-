from django.urls import path
from . import views  

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('categorias/', views.gestion_categorias, name='gestion_categorias'),
]