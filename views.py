# dentalcare/views.py
from django.shortcuts import render

def agendar_cita_odontologo(request):
    # Lógica para agendar cita
    return render(request, 'odontologo/agendar_cita.html')

def obtener_citas(request):
    # Lógica para obtener citas
    return render(request, 'gestion/lista_citas.html')
