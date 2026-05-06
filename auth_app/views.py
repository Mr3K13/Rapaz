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
    """Endpoint para registro de novos usuários."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            UserProfile.objects.create(user=user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'mensagem': 'Usuário registrado com sucesso.',
                    'token': token.key,
                    'usuario': UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Endpoint para autenticação de usuários."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
            )
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        'mensagem': 'Login realizado com sucesso.',
                        'token': token.key,
                        'usuario': UserSerializer(user).data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {'erro': 'Credenciais inválidas.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Endpoint para encerramento de sessão do usuário."""

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
    """Endpoint para visualização do perfil do usuário autenticado."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileView(APIView):
    """Endpoint para atualização do perfil do usuário autenticado."""

    permission_classes = [IsAuthenticated]

    def put(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        user = request.user

        # Atualizar campos do usuário
        user_fields = ['first_name', 'last_name', 'email']
        for field in user_fields:
            if field in request.data:
                setattr(user, field, request.data[field])
        user.save()

        # Atualizar campos do perfil
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
    """Endpoint para visualização de detalhes de um usuário específico."""

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
