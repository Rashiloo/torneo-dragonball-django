from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError


# --- MÓDULO 1: USUARIOS (Administradores del sistema) ---
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nombre, password, **extra_fields)


class Usuario(AbstractUser):
    username = None
    nombre = models.CharField(max_length=150, verbose_name="Nombre completo")
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.email})"


# --- MÓDULO 2: PELEADORES ---
class Peleador(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre del peleador")
    alias = models.CharField(max_length=100, verbose_name="Alias o nombre de combate")
    universo_planeta = models.CharField(max_length=100, verbose_name="Universo o planeta de procedencia")
    raza = models.CharField(max_length=80, verbose_name="Raza o especie")
    edad = models.PositiveIntegerField(verbose_name="Edad")
    categoria = models.CharField(max_length=100, verbose_name="Categoría de combate")
    nivel_experiencia = models.CharField(max_length=100, verbose_name="Nivel de experiencia")
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo', verbose_name="Estado de participación")

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.alias})"


# --- MÓDULO 3: DUELOS ---
class Duelo(models.Model):
    ESTADO_DUELO_CHOICES = [
        ('programado', 'Programado'),
        ('en_curso', 'En curso'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]

    peleador_1 = models.ForeignKey(Peleador, on_delete=models.CASCADE, related_name='duelos_p1', verbose_name="Peleador 1")
    peleador_2 = models.ForeignKey(Peleador, on_delete=models.CASCADE, related_name='duelos_p2', verbose_name="Peleador 2")
    fecha = models.DateField(verbose_name="Fecha del combate")
    hora = models.TimeField(verbose_name="Hora del combate")
    arena = models.CharField(max_length=150, verbose_name="Lugar o arena")
    ronda = models.CharField(max_length=100, verbose_name="Ronda del torneo")
    estado = models.CharField(max_length=15, choices=ESTADO_DUELO_CHOICES, default='programado', verbose_name="Estado del duelo")

    class Meta:
        ordering = ['fecha', 'hora']

    def clean(self):
        if self.peleador_1_id and self.peleador_2_id and self.peleador_1 == self.peleador_2:
            raise ValidationError("Un peleador no puede enfrentarse contra sí mismo.")

    def __str__(self):
        return f"{self.peleador_1.nombre} vs {self.peleador_2.nombre} - {self.ronda}"


# --- MÓDULO 4: RESULTADOS ---
class Resultado(models.Model):
    TIPO_VICTORIA_CHOICES = [
        ('rendicion', 'Rendición'),
        ('nocaut', 'Nocaut'),
        ('decision', 'Decisión del juez'),
    ]

    duelo = models.OneToOneField(Duelo, on_delete=models.CASCADE, related_name='resultado', verbose_name="Duelo")
    ganador = models.ForeignKey(Peleador, on_delete=models.CASCADE, related_name='victorias', verbose_name="Peleador ganador")
    tipo_victoria = models.CharField(max_length=15, choices=TIPO_VICTORIA_CHOICES, verbose_name="Tipo de victoria")
    duracion_minutos = models.PositiveIntegerField(verbose_name="Duración del combate (minutos)")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones del enfrentamiento")
    estado_final = models.CharField(max_length=20, default='finalizado', verbose_name="Estado final del duelo")

    def clean(self):
        if self.duelo_id:
            if self.duelo.estado == 'cancelado':
                raise ValidationError("No se pueden registrar resultados para enfrentamientos cancelados.")
            if self.ganador_id and self.ganador not in [self.duelo.peleador_1, self.duelo.peleador_2]:
                raise ValidationError("El ganador debe ser uno de los dos peleadores registrados en el duelo.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        # Sincronizar el estado del duelo a finalizado
        self.duelo.estado = self.estado_final
        self.duelo.save()

    def __str__(self):
        return f"Ganador: {self.ganador.nombre} ({self.duelo})"