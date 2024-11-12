from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.utils import timezone
from django.urls import reverse  
from ckeditor.fields import RichTextField
from django.conf import settings
import uuid 
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'  # Usar el email para el login
    REQUIRED_FIELDS = ['username']  # Aquí añades otros campos obligatorios si es necesario
    rol = models.CharField(max_length=20, default='cliente')
    
class Cliente(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()

    def __str__(self):
        return self.nombre


class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, default="Sin apellido")
    documento = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, blank=True, null=True) 
    tipo_sangre = models.CharField(
        max_length=3, 
        choices=[
            ('O+', 'O+'), ('O-', 'O-'), 
            ('A+', 'A+'), ('A-', 'A-'), 
            ('B+', 'B+'), ('B-', 'B-'), 
            ('AB+', 'AB+'), ('AB-', 'AB-')
        ]
    )
    alergias = models.TextField(blank=True, null=True)
    enfermedades = models.TextField(blank=True, null=True)
    medicacion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateField(default=timezone.now)
    foto = models.ImageField(upload_to='fotos_pacientes/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Tratamiento(models.Model):
    TIPO_TRATAMIENTO_CHOICES = [
        ('limpieza', 'Limpieza'),
        ('extraccion', 'Extracción'),
        ('ortodoncia', 'Ortodoncia'),
        ('endodoncia', 'Endodoncia'),
        ('implante', 'Implante'),
        # Agrega otros tipos de tratamiento aquí según sea necesario
    ]

    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=100, choices=TIPO_TRATAMIENTO_CHOICES)
    codigo = models.CharField(max_length=20, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.tipo} ({self.codigo})"
    
  
    
class Cita(models.Model): 
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    tratamiento = models.ForeignKey('Tratamiento', on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField()
    motivo = models.CharField(max_length=255)
    confirmada = models.BooleanField(default=False)
    solicitud_reprogramacion = models.BooleanField(default=False)
    nueva_fecha = models.DateField(null=True, blank=True)
    nueva_hora = models.TimeField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Cita para {self.paciente.nombre} el {self.fecha}"
    
class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=32, blank=True, null=True)  # Campo para almacenar el token

    def __str__(self):
        return f"Perfil de {self.user.username}"

class Factura(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tratamientos = models.ManyToManyField(Tratamiento)
    fecha_emision = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.CharField(max_length=20, choices=[('Pendiente', 'Pendiente'), ('Pagada', 'Pagada')], default='Pendiente')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Factura de {self.paciente.nombre} - {self.fecha_emision}"
    
    
class Reserva(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"{self.nombre_cliente} - {self.fecha} {self.hora}"
    
class BlogArticle(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=300)
    main_content = RichTextField()  # Contenido introductorio o general con editor enriquecido
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id)])

class ArticleSection(models.Model):
    article = models.ForeignKey(BlogArticle, on_delete=models.CASCADE, related_name="sections")
    section_title = models.CharField(max_length=200, blank=True)  # Título de la sección
    section_content = RichTextField()  # Contenido de la sección con editor enriquecido (CKEditor)

    def __str__(self):
        return f"{self.article.title} - {self.section_title}"
    
class Producto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE) 
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.PositiveIntegerField(default=0)  # Cantidad disponible en inventario
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre



class MiModelo(models.Model):
    fecha = models.DateTimeField(default=timezone.now)    