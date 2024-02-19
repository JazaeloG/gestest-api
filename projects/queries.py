import graphene
from graphene import ObjectType, List, Schema, Field, Int
from graphene_django import DjangoObjectType
from .models import Dimensiones, Preguntas, Proyecto
from .models import Tests

class ProyectoType(graphene.ObjectType):
    id = Int()
    nombre = graphene.String()
    descripcion = graphene.String()
    usuario_id = Int()
    tests = List(Int)

    def resolve_id(self, info):
        return self.id
    
    def resolve_usuario_id(self, info):
        return self.usuario.id if self.usuario else None

class TestType(DjangoObjectType):
    class Meta:
        model = Tests

    id = Int()

    def resolve_id(self, info):
        return self.id

class DimensionType(DjangoObjectType):
    class Meta:
        model = Dimensiones
    
    id = Int()

    def resolve_id(self, info):
        return self.id

class PreguntaType(DjangoObjectType):
    class Meta:
        model = Preguntas
    
    id = Int()

    def resolve_id(self, info):
        return self.id

class Query(ObjectType):
    proyectos_usuario = List(ProyectoType, usuario_id=graphene.Int(required=True))
    proyecto_by_id = ProyectoType(id=graphene.Int(required=True))
    get_all_tests = List(TestType)
    get_test_by_id = Field(TestType, id=Int(required=True))
    get_all_dimensions = List(DimensionType)
    get_dimension_by_id = Field(DimensionType, id=Int(required=True))
    get_all_preguntas = List(PreguntaType)
    get_pregunta_by_id = Field(PreguntaType, id=Int(required=True))
    get_preguntas_by_dimension = List(PreguntaType, id_dimension=Int(required=True))
    

    def resolve_get_all_tests(self, info):
        return Tests.objects.all()

    def resolve_get_test_by_id(self, info, id):
        return Tests.objects.get(id=id)

    def resolve_get_all_dimensions(self, info):
        return Dimensiones.objects.all()

    def resolve_get_dimension_by_id(self, info, id):
        return Dimensiones.objects.get(id=id)

    def resolve_get_all_preguntas(self, info):
        return Preguntas.objects.all()

    def resolve_get_pregunta_by_id(self, info, id):
        return Preguntas.objects.get(id=id)

    def resolve_proyectos_usuario(self, info, usuario_id):
        # Obtener todos los proyectos asociados al usuario
        return Proyecto.objects.filter(usuario_id=usuario_id)
    
    def resolve_proyecto_by_id(self, info, id):  # Corregir el nombre del método
        # Obtener un proyecto específico por su ID
        return Proyecto.objects.get(pk=id)

    def resolve_get_preguntas_by_dimension(self, info, id_dimension):
        # Obtener todas las preguntas asociadas a una dimensión
        return Preguntas.objects.filter(id_dimension=id_dimension)