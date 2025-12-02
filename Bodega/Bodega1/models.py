from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class Usuario(AbstractUser):
    TIPO_USUARIO = [
        ('administrador', 'Administrador'),
        ('bodeguero', 'Bodeguero'),
        ('invitado', 'Invitado'),
    ]
    
    tipo_usuario = models.CharField(max_length=15, choices=TIPO_USUARIO, default='invitado')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def es_administrador(self):
        return self.tipo_usuario == 'administrador'
    
    def es_bodeguero(self):
        return self.tipo_usuario == 'bodeguero'
    
    def es_invitado(self):
        return self.tipo_usuario == 'invitado'

    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"
