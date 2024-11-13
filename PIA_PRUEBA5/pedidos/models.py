from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Tabla de USUARIO
class USUARIO(models.Model):
    ROLES = (
        (1, 'MESERO'),
        (2, 'CHEF'),
    )

    idUsuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    cuenta = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=25)
    rol = models.IntegerField(choices=ROLES)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')

    # Sobreescribir el método save() para convertir todos los campos a mayúsculas antes de guardar
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.cuenta = self.cuenta.upper()
        super(USUARIO, self).save(*args, **kwargs)
    
    class Meta:
        # Asegurarse de que no haya cuentas duplicadas, sin importar mayúsculas/minúsculas
        constraints = [
            models.UniqueConstraint(fields=['cuenta'], name='unique_cuenta')
        ]

    def __str__(self):
        return f"ID: {self.idUsuario} - {self.nombre.upper()}"
    
# Tabla de PEDIDO
class PEDIDO(models.Model):
    ESTATUS = (
        (1, 'CREADO'),
        (2, 'ACEPTADO'),
    )

    idPedido = models.AutoField(primary_key=True)
    mesa = models.IntegerField()
    platillo = models.CharField(max_length=200)
    estatus = models.IntegerField(choices=ESTATUS, default=1)
    idUsuarioRegistro = models.ForeignKey(USUARIO, on_delete=models.SET_NULL, null=True)
    fechaRegistro = models.DateTimeField(auto_now_add=True)

    # Sobreescribir el método save() para convertir todos los campos a mayúsculas antes de guardar
    def save(self, *args, **kwargs):
        self.platillo = self.platillo.upper()
        super(PEDIDO, self).save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.idPedido} - Mesa {self.mesa}".upper()