from django.contrib import admin
from .models import Usuario, Paciente, Tratamiento, Cita

admin.site.register(Usuario)
admin.site.register(Paciente)
admin.site.register(Tratamiento)
admin.site.register(Cita)
