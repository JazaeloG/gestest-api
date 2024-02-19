from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, correo, nombre, apellido_paterno, apellido_materno, password=None, institucion=None, isAdmin=False):
        if not correo:
            raise ValueError("El campo 'correo' es obligatorio.")
        
        user = self.model(
            correo=self.normalize_email(correo),
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            institucion=institucion,
            isAdmin=isAdmin
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, nombre, apellido_paterno, apellido_materno, password=None):
        user = self.create_user(
            correo=correo,
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            password=password,
            isAdmin=True
        )
        return user

class CustomUser(AbstractBaseUser):
    correo = models.EmailField(unique=True)
    nombre = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30, blank=True)
    institucion = models.CharField(max_length=100, blank=True, null=True)
    isAdmin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido_paterno']

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"

    def has_perm(self, perm, obj=None):
        return self.isAdmin

    def has_module_perms(self, app_label):
        return self.isAdmin
