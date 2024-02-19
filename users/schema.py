from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.exceptions import ValidationError
import graphene
from graphene import String, Field, Mutation, ObjectType, List
from graphql import GraphQLError
from .models import CustomUser
from graphql_jwt.decorators import jwt_cookie

class UserInput(graphene.InputObjectType):
    correo = String(required=True)
    nombre = String(required=True)
    apellido_paterno = String(required=True)
    apellido_materno = String(required=True)
    password = String(required=True)
    institucion = String()
    isAdmin = graphene.Boolean()

class UserType(graphene.ObjectType):
    id = graphene.Int()
    correo = graphene.String()
    nombre = graphene.String()
    apellido_paterno = graphene.String()
    apellido_materno = graphene.String()
    institucion = graphene.String()
    isAdmin = graphene.Boolean()

    def resolve_id(self, info):
        return self.id

    def resolve_correo(self, info):
        return self.correo

    def resolve_nombre(self, info):
        return self.nombre

    def resolve_apellido_paterno(self, info):
        return self.apellido_paterno

    def resolve_apellido_materno(self, info):
        return self.apellido_materno

    def resolve_institucion(self, info):
        return self.institucion

    def resolve_isAdmin(self, info):
        return self.isAdmin


class Query(ObjectType):
    users = List(UserType)
    user = Field(UserType, correo=String())

    def resolve_users(root, info):
        return CustomUser.objects.all()

    def resolve_user(root, info, correo):
        try:
            return CustomUser.objects.get(correo=correo)
        except CustomUser.DoesNotExist:
            return None
        
class CreateUser(Mutation):
    user = Field(UserType)

    class Arguments:
        user_data = UserInput(required=True)

    @staticmethod
    def mutate(root, info, user_data=None):
        try:
            user = CustomUser.objects.create_user(**user_data)
            return CreateUser(user=user)
        except ValidationError as e:
            raise GraphQLError(str(e))

class UpdateUser(Mutation):
    user = Field(UserType)

    class Arguments:
        correo = String(required=True)
        user_data = UserInput(required=True)

    @staticmethod
    def mutate(root, info, correo, user_data=None):
        try:
            user = CustomUser.objects.get(correo=correo)
            for key, value in user_data.items():
                setattr(user, key, value)
            user.save()
            return UpdateUser(user=user)
        except CustomUser.DoesNotExist:
            raise GraphQLError(f"Usuario con correo {correo} no encontrado.")
        except ValidationError as e:
            raise GraphQLError(str(e))

class DeleteUser(Mutation):
    success = graphene.Boolean()

    class Arguments:
        correo = String(required=True)

    @staticmethod
    def mutate(root, info, correo):
        try:
            user = CustomUser.objects.get(correo=correo)
            user.delete()
            return DeleteUser(success=True)
        except CustomUser.DoesNotExist:
            raise GraphQLError(f"Usuario con correo {correo} no encontrado.")
    
def generar_codigo_recuperacion(user):
    # Generar un código de recuperación y guardarlo en el modelo del usuario
    recovery_code = default_token_generator.make_token(user)
    user.recovery_code = recovery_code
    user.recovery_code_expires = timezone.now() + timedelta(minutes=15)
    user.save()
    return recovery_code

def enviar_email(user):
    # Enviar un correo electrónico con el código de recuperación al usuario
    recovery_code = generar_codigo_recuperacion(user)
    subject = 'Gestest-Recuperación de contraseña'
    message = f'Su código de recuperación de contraseña es: {recovery_code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.correo
    send_mail(subject, message, from_email, [to_email])

def recuperar_password(email, recovery_code, new_password):
    # Validar el código de recuperación y actualizar la contraseña si es válido
    try:
        user = CustomUser.objects.get(correo=email)
        if user.recovery_code == recovery_code and user.recovery_code_expires > timezone.now():
            user.set_password(new_password)
            user.recovery_code = None
            user.recovery_code_expires = None
            user.save()
            return True
        else:
            return False
    except CustomUser.DoesNotExist:
        return False
    

class LoginUser(Mutation):
    user = Field(UserType)

    class Arguments:
        correo = String(required=True)
        password = String(required=True)

    @staticmethod
    def mutate(root, info, correo, password):
        from graphql_jwt.shortcuts import get_token

        try:
            user = CustomUser.objects.get(correo=correo)
            if user.check_password(password):
                token = get_token(user)
                return LoginUser(user=user)
            else:
                raise GraphQLError("Credenciales incorrectas.")
        except CustomUser.DoesNotExist:
            raise GraphQLError(f"Usuario con correo {correo} no encontrado.")

        
class VerifyToken(Mutation):
    success = graphene.Boolean()

    class Arguments:
        token = String(required=True)

    @staticmethod
    @jwt_cookie
    def mutate(root, info, token):
        return VerifyToken(success=True)
    
class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    login_user = LoginUser.Field()
    verify_token = VerifyToken.Field()