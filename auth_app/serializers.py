"""Serializers da aplicação de autenticação."""
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Serializer básico para o modelo User do Django."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para o perfil estendido do usuário."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'phone', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class RegisterSerializer(serializers.Serializer):
    """Serializer para registro de novos usuários."""

    username = serializers.CharField(
        max_length=150,
        error_messages={'required': 'O nome de usuário é obrigatório.'},
    )
    email = serializers.EmailField(
        error_messages={'required': 'O e-mail é obrigatório.'},
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            'required': 'A senha é obrigatória.',
            'min_length': 'A senha deve ter pelo menos 8 caracteres.',
        },
    )
    password_confirm = serializers.CharField(
        write_only=True,
        error_messages={'required': 'A confirmação de senha é obrigatória.'},
    )
    first_name = serializers.CharField(max_length=150, required=False, default='')
    last_name = serializers.CharField(max_length=150, required=False, default='')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Este nome de usuário já está em uso.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Este e-mail já está cadastrado.')
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm': 'As senhas não coincidem.'}
            )
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        UserProfile.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer para autenticação de usuários."""

    username = serializers.CharField(
        error_messages={'required': 'O nome de usuário é obrigatório.'},
    )
    password = serializers.CharField(
        write_only=True,
        error_messages={'required': 'A senha é obrigatória.'},
    )
