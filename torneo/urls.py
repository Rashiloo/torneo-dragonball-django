from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginUsuarioForm

urlpatterns = [
    # Módulo 1: Autenticación
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', auth_views.LoginView.as_view(
        template_name='torneo/login.html',
        authentication_form=LoginUsuarioForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]