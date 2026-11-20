from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Peleador, Duelo, Resultado


class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Bulma Brief'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'usuario@capsula.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado. Inicia sesión o usa otro correo.")
        return email


class LoginUsuarioForm(AuthenticationForm):
    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'})
    )


class PeleadorForm(forms.ModelForm):
    class Meta:
        model = Peleador
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Son Goku'}),
            'alias': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Kakarotto'}),
            'universo_planeta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Universo 7 / Planeta Tierra'}),
            'raza': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Saiyajin'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10000}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Peso Pesado / Dioses'}),
            'nivel_experiencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Maestro / Ultra Instinto'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://ejemplo.com/imagen.jpg'}),
        }


class DueloForm(forms.ModelForm):
    class Meta:
        model = Duelo
        fields = '__all__'
        widgets = {
            'peleador_1': forms.Select(attrs={'class': 'form-select'}),
            'peleador_2': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'arena': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Plataforma del Torneo de la Fuerza'}),
            'ronda': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Cuartos de Final'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('peleador_1')
        p2 = cleaned_data.get('peleador_2')
        if p1 and p2 and p1 == p2:
            raise forms.ValidationError("Debes seleccionar dos peleadores distintos para el duelo.")
        return cleaned_data

class ResultadoForm(forms.ModelForm):
    class Meta:
        model = Resultado
        fields = ['ganador', 'tipo_victoria', 'duracion_minutos', 'observaciones', 'estado_final']
        widgets = {
            'ganador': forms.Select(attrs={'class': 'form-select'}),
            'tipo_victoria': forms.Select(attrs={'class': 'form-select'}),
            'duracion_minutos': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado_final': forms.Select(
                choices=[('finalizado', 'Finalizado')],
                attrs={'class': 'form-select'}
            ),
        }

    def __init__(self, *args, duelo=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.duelo = duelo
        if duelo:
            self.fields['ganador'].queryset = Peleador.objects.filter(
                id__in=[duelo.peleador_1.id, duelo.peleador_2.id]
            )

    def clean(self):
        cleaned_data = super().clean()
        ganador = cleaned_data.get('ganador')
        if self.duelo:
            if self.duelo.estado == 'cancelado':
                raise forms.ValidationError("No se puede registrar resultado para un duelo cancelado.")
            if ganador and ganador not in [self.duelo.peleador_1, self.duelo.peleador_2]:
                raise forms.ValidationError("El ganador debe ser uno de los dos peleadores del duelo.")
        return cleaned_data