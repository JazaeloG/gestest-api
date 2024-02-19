from django.db import models
from users.models import CustomUser

# Create your models here.
class Tests(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    autor = models.CharField(max_length=100, default="Anónimo")
    bibliografia = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Dimensiones(models.Model):
    id_test = models.ForeignKey(Tests, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Preguntas(models.Model):
    id_dimension = models.ForeignKey(Dimensiones, on_delete=models.CASCADE)
    pregunta = models.TextField()
    valorMin = models.IntegerField()
    valorMax = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Respuestas(models.Model):
    id_pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Proyecto(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tests = models.ManyToManyField(Tests)
    dimensiones = models.ManyToManyField(Dimensiones)
    preguntas = models.ManyToManyField(Preguntas)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
