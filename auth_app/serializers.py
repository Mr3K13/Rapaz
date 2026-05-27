from rest_framework import serializers

from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "nome", "email", "tipo", "data_criacao"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={"required": "O e-mail é obrigatório."}
    )

    senha = serializers.CharField(
        write_only=True,
        error_messages={"required": "A senha é obrigatória."}
    )

    tipo = serializers.ChoiceField(
        choices=["crianca", "ong"],
        required=False
    )


class RegisterSerializer(serializers.Serializer):
    nome = serializers.CharField(
        max_length=100,
        error_messages={"required": "O nome é obrigatório."}
    )

    email = serializers.EmailField(
        error_messages={"required": "O e-mail é obrigatório."}
    )

    senha = serializers.CharField(
        write_only=True,
        min_length=6,
        error_messages={
            "required": "A senha é obrigatória.",
            "min_length": "A senha precisa ter pelo menos 6 caracteres.",
        }
    )

    tipo = serializers.ChoiceField(
        choices=["crianca", "ong"],
        default="crianca"
    )

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este e-mail já está cadastrado.")

        return value