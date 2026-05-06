"""Views da aplicação de autenticação."""
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    UserSerializer,
)


class RegisterView(APIView):
    """
    POST /api/auth/register/
    Registra um novo usuário e retorna o token de autenticação.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'erros': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'mensagem': 'Usuário cadastrado com sucesso.',
                'token': token.key,
                'usuario': UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    POST /api/auth/login/
    Autentica o usuário e retorna o token de acesso.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'erros': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {'erro': 'Credenciais inválidas. Verifique o usuário e a senha.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {'erro': 'Esta conta está desativada.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'mensagem': 'Login realizado com sucesso.',
                'token': token.key,
                'usuario': UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Invalida o token do usuário autenticado.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Token.DoesNotExist:
            pass

        return Response(
            {'mensagem': 'Logout realizado com sucesso.'},
            status=status.HTTP_200_OK,
        )


class ProfileView(APIView):
    """
    GET /api/auth/profile/
    Retorna o perfil do usuário autenticado.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileView(APIView):
    """
    PUT /api/auth/profile/update/
    Atualiza os dados do perfil do usuário autenticado.
    """

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)

        # Atualiza campos do User
        user_fields = ['first_name', 'last_name', 'email']
        for field in user_fields:
            if field in request.data:
                setattr(user, field, request.data[field])
        user.save()

        # Atualiza campos do UserProfile
        if 'phone' in request.data:
            profile.phone = request.data['phone']
            profile.save()

        serializer = UserProfileSerializer(profile)
        return Response(
            {
                'mensagem': 'Perfil atualizado com sucesso.',
                'perfil': serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class UserDetailView(APIView):
    """
    GET /api/auth/user/<id>/
    Retorna os detalhes de um usuário específico pelo ID.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'erro': 'Usuário não encontrado.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
