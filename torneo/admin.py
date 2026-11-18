from django.contrib import admin
from .models import Usuario, Peleador, Duelo, Resultado

admin.site.register(Usuario)
admin.site.register(Peleador)
admin.site.register(Duelo)
admin.site.register(Resultado)