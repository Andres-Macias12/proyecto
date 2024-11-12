from django import forms
from .models import Tratamiento, Paciente

from django import forms
from .models import Factura, Tratamiento, Paciente, Producto, Cliente
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class ClienteForm(forms.ModelForm):
    email = forms.EmailField(required=True)  # Campo para el correo electrónico
    password = forms.CharField(widget=forms.PasswordInput, required=True)  # Campo para la contraseña
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)  # Confirmación de contraseña

    class Meta:
        model = Cliente
        fields = ['nombre', 'fecha_nacimiento', 'telefono', 'direccion']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data

    def save(self, commit=True):
        # Primero creamos el usuario
        user_data = self.cleaned_data
        user = get_user_model().objects.create_user(
            username=user_data['email'],
            email=user_data['email'],
            password=user_data['password']
        )

        # Luego creamos el cliente asociado al usuario
        cliente = super().save(commit=False)
        cliente.user = user  # Asociamos el usuario creado al cliente
        if commit:
            cliente.save()
        return cliente


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'documento', 'fecha_nacimiento', 'telefono', 'correo', 'direccion', 'ciudad', 'tipo_sangre', 'alergias', 'enfermedades', 'medicacion', 'foto']


class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['paciente', 'tipo', 'codigo', 'costo', 'observaciones']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),  # Cambiar a Select para el menú desplegable
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código del tratamiento'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if Tratamiento.objects.filter(codigo=codigo).exists():
            raise forms.ValidationError("Este código ya está en uso. Por favor, ingresa un código único.")
        return codigo
        
class ReservationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    role = forms.ChoiceField(choices=[
        ('dentist', 'Dentista'),
        ('assistant', 'Asistente Dental'),
        ('manager', 'Gerente de Clínica'),
        ('other', 'Otro')
    ])
    region = forms.CharField(max_length=100)
    current_stage = forms.ChoiceField(choices=[
        ('startup', 'Inicio'),
        ('growth', 'Crecimiento'),
        ('established', 'Establecida')
    ])
    software = forms.ChoiceField(choices=[
        ('yes', 'Sí'),
        ('no', 'No')
    ])    
    
class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['paciente', 'tratamientos', 'fecha_emision', 'total', 'estado_pago', 'observaciones']
        widgets = {
            'fecha_emision': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'tratamientos': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

    # Validación personalizada para el campo "total"
    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total <= 0:
            raise forms.ValidationError("El total no puede ser menor o igual a cero.")
        return total

    # Validación para el campo "tratamientos", asegurando que al menos uno sea seleccionado
    def clean_tratamientos(self):
        tratamientos = self.cleaned_data.get('tratamientos')
        if not tratamientos:
            raise forms.ValidationError("Debe seleccionar al menos un tratamiento.")
        return tratamientos

    # Validación personalizada para el campo "paciente", asegurando que esté seleccionado
    def clean_paciente(self):
        paciente = self.cleaned_data.get('paciente')
        if not paciente:
            raise forms.ValidationError("Debe seleccionar un paciente.")
        return paciente

    
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'cantidad', 'precio']   
        
class AuthenticationForm(forms.Form):
    # Tu código de formulario aquí (no es necesario definirlo)
    pass