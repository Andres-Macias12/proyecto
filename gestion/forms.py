from django import forms
from .models import Tratamiento, Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'documento', 'fecha_nacimiento', 'telefono', 'correo', 'direccion', 'ciudad', 'tipo_sangre', 'alergias', 'enfermedades', 'medicacion']

class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['paciente', 'tipo', 'fecha', 'costo', 'observaciones']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
        }