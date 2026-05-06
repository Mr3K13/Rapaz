from django.urls import path
from .views import LoginView, ProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth-login'),
    path('profile/', ProfileView.as_view(), name='auth-profile'),
]
