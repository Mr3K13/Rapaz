from django.contrib import admin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'tipo', 'data_criacao')
    search_fields = ('nome', 'email')
    list_filter = ('tipo',)
