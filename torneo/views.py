from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroUsuarioForm, PeleadorForm, DueloForm
from .models import Peleador, Duelo


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


# --- MÓDULO 2: PELEADORES (CRUD) ---
def lista_peleadores(request):
    peleadores = Peleador.objects.all()
    return render(request, 'torneo/peleadores/lista.html', {'peleadores': peleadores})


def detalle_peleador(request, pk):
    peleador = get_object_or_404(Peleador, pk=pk)
    return render(request, 'torneo/peleadores/detalle.html', {'peleador': peleador})


@login_required
def crear_peleador(request):
    if request.method == 'POST':
        form = PeleadorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Peleador registrado correctamente en el torneo.")
            return redirect('lista_peleadores')
        messages.error(request, "No se pudo registrar el peleador. Revisa los campos.")
    else:
        form = PeleadorForm()
    return render(request, 'torneo/peleadores/form.html', {'form': form, 'titulo': 'Registrar Peleador'})


@login_required
def editar_peleador(request, pk):
    peleador = get_object_or_404(Peleador, pk=pk)
    if request.method == 'POST':
        form = PeleadorForm(request.POST, instance=peleador)
        if form.is_valid():
            form.save()
            messages.success(request, f"Información de {peleador.nombre} actualizada.")
            return redirect('lista_peleadores')
        messages.error(request, "Error al actualizar los datos del peleador.")
    else:
        form = PeleadorForm(instance=peleador)
    return render(request, 'torneo/peleadores/form.html', {'form': form, 'titulo': f'Editar: {peleador.nombre}'})


@login_required
def eliminar_peleador(request, pk):
    peleador = get_object_or_404(Peleador, pk=pk)
    if request.method == 'POST':
        nombre = peleador.nombre
        peleador.delete()
        messages.success(request, f"Peleador {nombre} eliminado del sistema.")
        return redirect('lista_peleadores')
    return render(request, 'torneo/peleadores/confirmar_eliminar.html', {'peleador': peleador})


# --- MÓDULO 3: DUELOS (CRUD + Próximos/Concluidos) ---
def lista_duelos(request):
    proximos = Duelo.objects.filter(estado__in=['programado', 'en_curso'])
    concluidos = Duelo.objects.filter(estado__in=['finalizado', 'cancelado']).order_by('-fecha', '-hora')
    return render(request, 'torneo/duelos/lista.html', {
        'proximos': proximos,
        'concluidos': concluidos,
    })


@login_required
def crear_duelo(request):
    if request.method == 'POST':
        form = DueloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Duelo programado correctamente.")
            return redirect('lista_duelos')
        messages.error(request, "Error al programar el duelo.")
    else:
        form = DueloForm()
    return render(request, 'torneo/duelos/form.html', {'form': form, 'titulo': 'Programar Nuevo Duelo'})


@login_required
def editar_duelo(request, pk):
    duelo = get_object_or_404(Duelo, pk=pk)
    if request.method == 'POST':
        form = DueloForm(request.POST, instance=duelo)
        if form.is_valid():
            form.save()
            messages.success(request, "Duelo actualizado correctamente.")
            return redirect('lista_duelos')
        messages.error(request, "Error al actualizar el duelo.")
    else:
        form = DueloForm(instance=duelo)
    return render(request, 'torneo/duelos/form.html', {'form': form, 'titulo': 'Editar Duelo'})


@login_required
def eliminar_duelo(request, pk):
    duelo = get_object_or_404(Duelo, pk=pk)
    if request.method == 'POST':
        duelo.delete()
        messages.success(request, "Duelo eliminado correctamente.")
        return redirect('lista_duelos')
    return render(request, 'torneo/duelos/confirmar_eliminar.html', {'duelo': duelo})
