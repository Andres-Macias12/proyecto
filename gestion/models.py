from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.utils import timezone  



class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('odontologo', 'Odontólogo'),
        ('asistente', 'Asistente'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='asistente')

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"


class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, default="Sin apellido")
    documento = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    tipo_sangre = models.CharField(max_length=3, choices=[
        ('O+', 'O+'), ('O-', 'O-'), 
        ('A+', 'A+'), ('A-', 'A-'), 
        ('B+', 'B+'), ('B-', 'B-'), 
        ('AB+', 'AB+'), ('AB-', 'AB-')
    ])
    alergias = models.TextField(blank=True, null=True)
    enfermedades = models.TextField(blank=True, null=True)
    medicacion = models.TextField(blank=True, null=True)
    
    fecha_registro = models.DateField(default=timezone.now)  # Nuevo campo

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Tratamiento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    fecha = models.DateTimeField(null=True, blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField()

    def __str__(self):
        return f"Tratamiento {self.tipo} - {self.paciente.nombre}"
    
  
    
class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField()
    motivo = models.CharField(max_length=255)
    confirmada = models.BooleanField(default=False)

    def __str__(self):
        return f"Cita para {self.paciente.nombre} el {self.fecha}"    
    

class Factura(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50, choices=[
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia')
    ])
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado')
    ], default='pendiente')

    def __str__(self):
        return f"Factura #{self.id} - {self.paciente.nombre} {self.paciente.apellido} - {self.estado}"