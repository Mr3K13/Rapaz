from rest_framework import serializers
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'tipo', 'data_criacao']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={'required': 'O e-mail é obrigatório.'}
    )
    senha = serializers.CharField(
        write_only=True,
        error_messages={'required': 'A senha é obrigatória.'}
    )
