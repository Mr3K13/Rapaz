from django.core import signing
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Usuario
from .serializers import LoginSerializer, UsuarioSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'erros': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data['email']
        senha = serializer.validated_data['senha']

        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response(
                {'erro': 'Email ou senha inválidos.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Atenção: isso compara senha em texto puro.
        # Funciona se a tabela Usuario estiver salvando senha normal.
        if usuario.senha != senha:
            return Response(
                {'erro': 'Email ou senha inválidos.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = signing.dumps({
            'id': usuario.id,
            'email': usuario.email,
            'tipo': usuario.tipo,
        })

        return Response(
            {
                'mensagem': 'Login realizado com sucesso.',
                'token': token,
                'usuario': UsuarioSerializer(usuario).data,
            },
            status=status.HTTP_200_OK
        )


class ProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return Response(
                {'erro': 'Token não enviado.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            token_type, token = auth_header.split(' ', 1)
        except ValueError:
            return Response(
                {'erro': 'Formato do token inválido.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if token_type.lower() != 'bearer':
            return Response(
                {'erro': 'Use Authorization: Bearer <token>.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            dados = signing.loads(token, max_age=60 * 60 * 24)
            usuario = Usuario.objects.get(id=dados['id'])
        except Exception:
            return Response(
                {'erro': 'Token inválido ou expirado.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            {
                'usuario': UsuarioSerializer(usuario).data
            },
            status=status.HTTP_200_OK
        )
