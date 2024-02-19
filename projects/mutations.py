import graphene
from graphene import DateTime, Int, String, Mutation, InputObjectType, ObjectType, List, Field
from graphql import GraphQLError
from .queries import DimensionType, PreguntaType, TestType
from .models import Dimensiones, Preguntas, Proyecto
from users.models import CustomUser
from .models import Tests

class PreguntaType(ObjectType):
    id = Int()
    pregunta = String()
    valor_min = Int()
    valor_max = Int()
    dimension_id = Int()

    def resolve_id(self, info):
        return self.id
    
    def resolve_dimension_id(self, info):
        return self.dimension.id if self.dimension else None

class DimensionType(ObjectType):
    id = Int()
    nombre = String()
    descripcion = String()
    test_id = Int()

    def resolve_id(self, info):
        return self.id
    
    def resolve_test_id(self, info):
        return self.test.id if self.test else None

class DimensionInput(InputObjectType):
    id_test = Int(required=True)
    nombre = String(required=True)
    descripcion = String(required=True)

class PreguntaInput(InputObjectType):
    id_dimension = Int(required=True)
    pregunta = String(required=True)
    valor_min = Int(required=True)
    valor_max = Int(required=True)


class TestInput(InputObjectType):
    nombre = String(required=True)
    descripcion = String(required=True)
    autor = String()
    bibliografia = String()

class ProyectoInput(InputObjectType):
    nombre = String(required=True)
    descripcion = String(required=True)
    idUsuario = Int(required=True)
    tests = List(Int)
    dimensiones = List(Int)
    preguntas = List(Int)

class ProyectoType(ObjectType):
    id = Int()
    nombre = String()
    descripcion = String()
    usuario_id = Int()
    tests = Field(List(TestType))
    preguntas = Field(List(PreguntaType))
    dimensiones = Field(List(DimensionType))

    def resolve_id(self, info):
        return self.id

    def resolve_usuario_id(self, info):
        return self.usuario.id if self.usuario else None

class CrearProyecto(Mutation):
    class Arguments:
        input = ProyectoInput(required=True)

    proyecto = Field(ProyectoType)

    def mutate(self, info, input):
        # Obtener la instancia del usuario usando el ID proporcionado
        usuario_id = input.pop('idUsuario')
        try:
            usuario = CustomUser.objects.get(pk=usuario_id)
        except CustomUser.DoesNotExist:
            raise GraphQLError(f"Usuario con ID {usuario_id} no encontrado.")

        # Crear la instancia del Proyecto relacionándola con el usuario
        proyecto = Proyecto(usuario=usuario, **input)
        proyecto.save()

        return CrearProyecto(proyecto=proyecto)


class CreateTest(Mutation):
    class Arguments:
        input = TestInput(required=True)

    test = Field(TestType)

    def mutate(self, info, input):
        test = Tests(**input)
        test.save()
        return CreateTest(test=test)

class UpdateTest(Mutation):
    class Arguments:
        id = Int(required=True)
        input = TestInput(required=True)

    test = Field(TestType)

    def mutate(self, info, id, input):
        test = Tests.objects.get(id=id)
        for key, value in input.items():
            setattr(test, key, value)
        test.save()
        return UpdateTest(test=test)

class DeleteTest(Mutation):
    class Arguments:
        id = Int(required=True)

    success = String()

    def mutate(self, info, id):
        test = Tests.objects.get(id=id)
        test.delete()
        return DeleteTest(success="Test deleted successfully")
    
class CreateDimension(Mutation):
    class Arguments:
        input = DimensionInput(required=True)

    dimension = Field(DimensionType)

    def mutate(self, info, input):
        # Obtener la instancia del Test usando el ID proporcionado
        test_id = input.pop('id_test')
        try:
            test = Tests.objects.get(pk=test_id)
        except Tests.DoesNotExist:
            raise GraphQLError(f"Test con ID {test_id} no encontrado.")

        # Crear la instancia de la Dimension relacionándola con el Test
        dimension = Dimensiones(**input, id_test=test)
        dimension.save()

        return CreateDimension(dimension=dimension)
    
class UpdateDimension(Mutation):
    class Arguments:
        id = Int(required=True)
        input = DimensionInput(required=True)

    dimension = Field(DimensionType)

    def mutate(self, info, id, input):
        dimension = Dimensiones.objects.get(id=id)
        for key, value in input.items():
            setattr(dimension, key, value)
        dimension.save()
        return UpdateDimension(dimension=dimension)
    
class DeleteDimension(Mutation):
    class Arguments:
        id = Int(required=True)

    success = String()

    def mutate(self, info, id):
        dimension = Dimensiones.objects.get(id=id)
        dimension.delete()
        return DeleteDimension(success="Dimension deleted successfully")
    
class CreatePregunta(Mutation):
    class Arguments:
        input = PreguntaInput(required=True)

    pregunta = Field(PreguntaType)

    def mutate(self, info, input):
        # Obtener la instancia de la Dimension usando el ID proporcionado
        dimension_id = input.pop('id_dimension')
        try:
            dimension = Dimensiones.objects.get(pk=dimension_id)
        except Dimensiones.DoesNotExist:
            raise GraphQLError(f"Dimension con ID {dimension_id} no encontrada.")

        # Crear la instancia de la Pregunta relacionándola con la Dimension
        pregunta = Preguntas(
            id_dimension=dimension,
            pregunta=input.pregunta,
            valorMin=input.valor_min,
            valorMax=input.valor_max
        )
        pregunta.save()

        return CreatePregunta(pregunta=pregunta)

    
class UpdatePregunta(Mutation):
    class Arguments:
        id = Int(required=True)
        input = PreguntaInput(required=True)

    pregunta = Field(PreguntaType)

    def mutate(self, info, id, input):
        pregunta = Preguntas.objects.get(id=id)
        for key, value in input.items():
            setattr(pregunta, key, value)
        pregunta.save()
        return UpdatePregunta(pregunta=pregunta)

class DeletePregunta(Mutation):
    class Arguments:
        id = Int(required=True)

    success = String()

    def mutate(self, info, id):
        pregunta = Preguntas.objects.get(id=id)
        pregunta.delete()
        return DeletePregunta(success="Pregunta deleted successfully")

class Mutation(ObjectType):
    create_proyecto = CrearProyecto.Field()
    create_test = CreateTest.Field()
    update_test = UpdateTest.Field()
    delete_test = DeleteTest.Field()
    create_dimension = CreateDimension.Field()
    update_dimension = UpdateDimension.Field()
    delete_dimension = DeleteDimension.Field()
    create_pregunta = CreatePregunta.Field()
    update_pregunta = UpdatePregunta.Field()
    delete_pregunta = DeletePregunta.Field()