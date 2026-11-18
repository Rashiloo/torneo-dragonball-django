from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegistroUsuarioForm


# --- MÓDULO 1: AUTENTICACIÓN ---
def registro_usuario(request):
    if request.user.is_authenticated:
        return redirect('lista_peleadores')
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f"Cuenta creada con éxito. ¡Bienvenido, {usuario.nombre}!")
            return redirect('lista_peleadores')
        messages.error(request, "Error al registrar la cuenta. Verifica los datos ingresados.")
    else:
        form = RegistroUsuarioForm()
    return render(request, 'torneo/registro.html', {'form': form})