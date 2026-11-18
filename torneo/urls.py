# torneo/urls.py
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

 # Módulo 2: Peleadores
    path('', views.lista_peleadores, name='lista_peleadores'),
    path('peleadores/<int:pk>/', views.detalle_peleador, name='detalle_peleador'),
    path('peleadores/nuevo/', views.crear_peleador, name='crear_peleador'),
    path('peleadores/<int:pk>/editar/', views.editar_peleador, name='editar_peleador'),
    path('peleadores/<int:pk>/eliminar/', views.eliminar_peleador, name='eliminar_peleador'),

    # Módulo 3: Duelos
    path('duelos/', views.lista_duelos, name='lista_duelos'),
    path('duelos/nuevo/', views.crear_duelo, name='crear_duelo'),
    path('duelos/<int:pk>/editar/', views.editar_duelo, name='editar_duelo'),
    path('duelos/<int:pk>/eliminar/', views.eliminar_duelo, name='eliminar_duelo'),
]