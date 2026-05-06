"""Rotas da aplicação de autenticação."""
from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    UpdateProfileView,
    UserDetailView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    path('profile/', ProfileView.as_view(), name='auth-profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='auth-profile-update'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='auth-user-detail'),
]
