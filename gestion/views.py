# Importaciones estándar de Python
from django.db.models import Sum
import os
import csv
import json
import random
import string
import smtplib
import ssl
import datetime
from datetime import date, timedelta, datetime
import calendar
from io import BytesIO
from django.contrib.auth import get_user_model 

# Importaciones de Django
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db.models import Q, Count, functions, Sum
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from decimal import Decimal
from django.utils.dateparse import parse_datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from gestion.models import Usuario


# Importaciones de terceros
import certifi
from email.mime.image import MIMEImage
import requests  # Para descargar el reporte en PDF desde Django Report Builder

# Importaciones de la aplicación actual
from .models import Usuario, Paciente, Cita, Tratamiento, Factura, Reserva, BlogArticle, Cliente
from .forms import PacienteForm, TratamientoForm, ReservationForm, FacturaForm, AuthenticationForm, ClienteForm
from django_tenants.utils import schema_context

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.conf import settings
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import os
from .models import Cita, Factura, Tratamiento
from django.db.models import Sum
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.pagesizes import letter
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image


from .models import Producto
from .forms import ProductoForm

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Verificar si el correo ya existe
            if get_user_model().objects.filter(email=email).exists():
                messages.error(request, "El correo electrónico ya está registrado.")
                return redirect('crear_cliente')  # Redirigir de nuevo al formulario

            # Si el correo no existe, se crea el cliente
            cliente = form.save()
            messages.success(request, "Cliente creado exitosamente.")
            return redirect('lista_clientes')  # Redirigir a la lista de clientes
    else:
        form = ClienteForm()
    return render(request, 'gestion/crear_cliente.html', {'form': form})

def ver_cliente(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    return render(request, 'gestion/ver_cliente.html', {'cliente': cliente})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('lista_clientes')  # Redirige a la lista de clientes

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    # Lógica para editar el cliente (formulario, validaciones, etc.)
    return render(request, 'gestion/editar_cliente.html', {'cliente': cliente})

def lista_clientes(request):
    # Verificar que el usuario sea superadministrador
    if not request.user.is_superuser:
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')

    # Obtener todos los clientes
    clientes = Cliente.objects.all()  # Recupera todos los objetos de Cliente

    return render(request, 'gestion/lista_clientes.html', {'clientes': clientes})

def lista_pacientes(request):
    pacientes = Paciente.objects.all()  # Obtiene todos los pacientes de la base de datos
    return render(request, 'gestion/lista_pacientes.html', {'pacientes': pacientes})

def ver_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)  # Obtiene el paciente por su ID
    return render(request, 'gestion/ver_paciente.html', {'paciente': paciente})

# Vista para editar un paciente
def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    
    # Si el formulario fue enviado
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()  # Guarda los cambios en el paciente
            return redirect('lista_pacientes')  # Redirige a la lista de pacientes
    else:
        form = PacienteForm(instance=paciente)  # Si no, muestra el formulario de edición
    
    return render(request, 'gestion/editar_paciente.html', {'form': form})

# Vista para eliminar un paciente
def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    
    if request.method == 'POST':
        paciente.delete()  # Elimina el paciente de la base de datos
        return redirect('lista_pacientes')  # Redirige a la lista de pacientes
    
    return render(request, 'gestion/eliminar_paciente.html', {'paciente': paciente})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('cliente_dashboard')  # Redirige al dashboard del cliente
    else:
        form = AuthenticationForm()
    return render(request, 'iniciar_sesion.html', {'form': form})

def registro_cliente(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear perfil de cliente asociado
            Cliente.objects.create(
                user=user,
                nombre=request.POST['nombre'],
                fecha_nacimiento=request.POST['fecha_nacimiento'],
                telefono=request.POST['telefono'],
                direccion=request.POST['direccion']
            )
            messages.success(request, 'Cuenta creada con éxito.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registro_cliente.html', {'form': form})



def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'gestion/registro.html', {'form': form})


def registrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES)  # Incluye request.FILES para manejar archivos
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente registrado exitosamente.')
            return redirect('lista_pacientes')  # Redirige a la lista de pacientes
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = PacienteForm()
    
    return render(request, 'gestion/registrar_paciente.html', {'form': form})


def lista_pacientes(request):
    pacientes = Paciente.objects.all().order_by('nombre')  # Ordenar por el campo 'nombre' o por cualquier otro campo relevante
    paginator = Paginator(pacientes, 10)  # Mostrar 10 pacientes por página
    page_number = request.GET.get('page')
    pacientes_page = paginator.get_page(page_number)
    return render(request, 'gestion/lista_pacientes.html', {'pacientes': pacientes_page})


def registrar_cita(request):
    pacientes = Paciente.objects.all()  # Obtener los pacientes para mostrarlos en el formulario
    if request.method == 'POST':
        paciente_id = request.POST['paciente']
        fecha = request.POST['fecha']
        motivo = request.POST['motivo']

        paciente = Paciente.objects.get(id=paciente_id)
        cita = Cita(paciente=paciente, fecha=fecha, motivo=motivo)
        cita.save()
        
        # Enviar el correo de recordatorio
        enviar_recordatorio(paciente.correo, cita.fecha)

        messages.success(request, 'Cita registrada exitosamente.')
        return redirect('lista_citas')

    return render(request, 'gestion/registrar_cita.html', {'pacientes': pacientes})


def lista_citas(request):
    citas = Cita.objects.all()  # Obtener todas las citas desde la base de datos
    return render(request, 'gestion/lista_citas.html', {'citas': citas})


def panel_reportes(request):
    # Consulta de citas confirmadas y no confirmadas
    citas_confirmadas = Cita.objects.filter(confirmada=True).count()
    citas_no_confirmadas = Cita.objects.filter(confirmada=False).count()

    # Consulta de pacientes nuevos (por ejemplo, del último mes)
    pacientes_nuevos = Paciente.objects.filter(fecha_registro__month=timezone.now().month).count()

    # Consulta de tratamientos por mes (últimos 6 meses)
    tratamientos_por_mes = Tratamiento.objects.filter(
        fecha__year=timezone.now().year
    ).values('fecha__month').annotate(total=Count('id')).order_by('fecha__month')

    # Pasar datos al contexto
    context = {
        'citas_confirmadas': citas_confirmadas,
        'citas_no_confirmadas': citas_no_confirmadas,
        'pacientes_nuevos': pacientes_nuevos,
        'tratamientos_por_mes': [t['total'] for t in tratamientos_por_mes],
        'meses': [t['fecha__month'] for t in tratamientos_por_mes]
    }

    return render(request, 'gestion/panel_reportes.html', context)


def exportar_citas_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_citas.csv"'

    writer = csv.writer(response)
    writer.writerow(['Paciente', 'Fecha', 'Motivo', 'Confirmada'])

    citas = Cita.objects.all().values_list('paciente__nombre', 'fecha', 'motivo', 'confirmada')
    for cita in citas:
        writer.writerow(cita)

    return response


def enviar_recordatorio(paciente_email, fecha_cita):
    asunto = 'Recordatorio de Cita'
    mensaje = f'Tienes una cita programada para el {fecha_cita}.'
    send_mail(asunto, mensaje, 'andresmacias978@gmail.com', [paciente_email])


# Vista para obtener las citas en formato JSON
def obtener_citas_json(request):
    citas = Cita.objects.all()
    citas_list = []
    for cita in citas:
        citas_list.append({
            'title': cita.paciente.nombre,
            'start': cita.fecha.strftime("%Y-%m-%dT%H:%M:%S"),
            'end': (cita.fecha + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            'url': f"/citas/{cita.id}/"
        })
    return JsonResponse(citas_list, safe=False)


def calendario_citas(request):
    # Obtener el mes y año actual
    now = datetime.now()
    year = now.year
    month = now.month

    # Obtener el calendario del mes actual
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)

    # Obtener la fecha actual para comparar en la plantilla
    today = now.date()

    # Generar una lista de días con estado ('pasado', 'hoy', 'futuro')
    month_dates = []
    for week in month_days:
        week_dates = []
        for day in week:
            if day == 0:
                week_dates.append({'day': 0, 'status': 'empty'})  # Días vacíos (no pertenecen al mes)
            else:
                full_date = datetime(year, month, day).date()
                if full_date < today:
                    week_dates.append({'day': day, 'status': 'pasado', 'full_date': full_date})
                elif full_date == today:
                    week_dates.append({'day': day, 'status': 'hoy', 'full_date': full_date})
                else:
                    week_dates.append({'day': day, 'status': 'futuro', 'full_date': full_date})
        month_dates.append(week_dates)

    context = {
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'month_days': month_dates,  # Lista de días con estados
        'today': today,  # Fecha actual
    }
    
    return render(request, 'gestion/calendario_citas.html', context)

def dashboard(request):
    hoy = date.today()
    total_pacientes = Paciente.objects.count()
    total_citas = Cita.objects.count()
    total_tratamientos = Tratamiento.objects.count()
    cantidad_citas_hoy = Cita.objects.filter(fecha=hoy).count()
    
    context = {
        'total_pacientes': total_pacientes,
        'total_citas': total_citas,
        'total_tratamientos': total_tratamientos,
        'cantidad_citas_hoy': cantidad_citas_hoy,
    }

    return render(request, 'gestion/dashboard.html', context)


def cambiar_logo(request):
    if request.method == 'POST' and 'nuevo_logo' in request.FILES:
        nuevo_logo = request.FILES['nuevo_logo']
        logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'logo.png')
        
        # Sobrescribimos el logo existente
        with open(logo_path, 'wb+') as destination:
            for chunk in nuevo_logo.chunks():
                destination.write(chunk)
        return redirect('dashboard')

    return redirect('dashboard')


def lista_tratamientos(request):
    tratamientos = Tratamiento.objects.all()  
    return render(request, 'lista_tratamientos.html', {'tratamientos': tratamientos})


def configuraciones(request):
    return render(request, 'gestion/configuraciones.html')


def usuarios(request):
    return render(request, 'gestion/usuarios.html')


def facturacion(request):
    return render(request, 'gestion/facturacion.html')

def guardar_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_facturas')  # Redirige a la lista de facturas después de guardar
    else:
        form = FacturaForm()

    return render(request, 'gestion/crear_factura.html', {'form': form})

def inventario(request):
    # Lógica para manejar la vista del inventario
    return render(request, 'gestion/inventario.html')


def ver_historia_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Cálculo de la edad
    today = timezone.now().date()
    age = today.year - paciente.fecha_nacimiento.year - ((today.month, today.day) < (paciente.fecha_nacimiento.month, paciente.fecha_nacimiento.day))

    contexto = {
        'paciente': paciente,
        'edad': age,
        # Añadir otros contextos necesarios
    }
    
    return render(request, 'gestion/historia_paciente.html', contexto)


def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    # Lógica para editar los datos del paciente
    return render(request, 'gestion/editar_paciente.html', {'paciente': paciente})


def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('lista_pacientes')  # Redirigir a la lista de pacientes después de eliminar
    return render(request, 'gestion/eliminar_paciente.html', {'paciente': paciente})


def get_citas(request):
    citas = Cita.objects.all()  # Puedes aplicar filtros si deseas solo ciertas citas
    citas_list = [
        {
            'title': cita.paciente.nombre,  # El nombre del paciente aparece en el evento
            'start': cita.fecha.isoformat(),  # Fecha de la cita en formato ISO
            'end': (cita.fecha + timedelta(hours=1)).isoformat(),  # Fecha de fin si tienes un campo de duración
            'id': cita.id  # Id para referencia si quieres editar o eliminar
        } for cita in citas
    ]
    return JsonResponse(citas_list, safe=False)


def home(request):
    return render(request, 'home.html')


def agendar_cita(request):
    fecha = request.GET.get('fecha')
    pacientes = Paciente.objects.all()  

    context = {
        'fecha': fecha,
        'pacientes': pacientes,  
    }
    return render(request, 'gestion/agendar_cita.html', context)

def obtener_citas_json(request):
    citas = Cita.objects.all()
    citas_list = []
    for cita in citas:
        citas_list.append({
            'title': cita.paciente.nombre,
            'start': cita.fecha.strftime("%Y-%m-%dT%H:%M:%S"),
            'end': (cita.fecha + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            'url': f"/citas/{cita.id}/"
        })
    return JsonResponse(citas_list, safe=False)

def get_week_days():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())  # Lunes como el primer día
    return [(start_of_week + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

def get_working_hours():
    return [f"{hour}:00" for hour in range(9, 19)]  # Horario de 9:00 a 18:00

def lista_citas(request):
    citas = Cita.objects.all()  # Obtener todas las citas de la base de datos
    return render(request, 'gestion/lista_citas.html', {'citas': citas})

def guardar_cita(request):
    if request.method == "POST":
        try:
            print(request.POST)  # Imprimir todos los datos enviados por el formulario

            paciente_id = request.POST.get('paciente')
            motivo = request.POST.get('motivo')
            fecha = request.POST.get('fecha')
            hora = request.POST.get('hora')

            print(f"Paciente ID: {paciente_id}, Motivo: {motivo}, Fecha: {fecha}, Hora: {hora}")

            if not paciente_id or not motivo or not fecha or not hora:
                messages.error(request, 'Todos los campos son obligatorios.')
                return redirect('agendar_cita')

            fecha_hora_str = f"{fecha} {hora}"
            fecha_hora = datetime.strptime(fecha_hora_str, '%b. %d, %Y %H:%M')
            paciente = Paciente.objects.get(id=paciente_id)

            Cita.objects.create(
                paciente=paciente,
                motivo=motivo,
                fecha=fecha_hora,
                confirmada=False
            )

            messages.success(request, 'La cita se guardó correctamente.')
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, f'Ocurrió un error al guardar la cita: {str(e)}')

        return redirect('lista_citas')

    
def buscar_pacientes(request):
    query = request.GET.get('q', '')
    if query:
        pacientes = Paciente.objects.filter(nombre__icontains=query) | Paciente.objects.filter(apellido__icontains=query)
        pacientes_data = [{"nombre": paciente.nombre, "apellido": paciente.apellido, "documento": paciente.documento} for paciente in pacientes]
        return JsonResponse(pacientes_data, safe=False)
    return JsonResponse([], safe=False)    

def citas_del_dia(request, fecha):
    # Convertir la fecha del string a objeto datetime
    fecha_datetime = datetime.strptime(fecha, '%Y-%m-%d').date()

    # Obtener todas las citas del día específico
    citas = Cita.objects.filter(fecha__date=fecha_datetime)

    context = {
        'citas': citas,
        'fecha': fecha_datetime,
    }

    return render(request, 'gestion/citas_del_dia.html', context)



def enviar_notificaciones(request):
    if request.method == "POST":
        # Obtener la fecha de mañana
        manana = datetime.now().date() + timedelta(days=1)

        # Buscar todas las citas que ocurren mañana
        citas = Cita.objects.filter(fecha__date=manana)

        if not citas.exists():
            return JsonResponse({'status': 'error', 'message': 'No hay citas para enviar notificaciones.'})

        try:
            for cita in citas:
                enviar_correo_recordatorio(cita)
            return JsonResponse({'status': 'success', 'message': 'Notificaciones enviadas con éxito.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error al enviar notificaciones: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'})

def enviar_correo_recordatorio(cita):
    # Crear los enlaces de confirmación y rechazo
    confirm_url = f"{settings.SITE_URL}{reverse('confirmar_cita', args=[cita.id, 'si'])}"
    reject_url = f"{settings.SITE_URL}{reverse('confirmar_cita', args=[cita.id, 'no'])}"

    # Renderizar la plantilla HTML
    mensaje_html = render_to_string('emails/recordatorio_cita.html', {
        'cita': cita,
        'confirm_url': confirm_url,
        'reject_url': reject_url,
    })

    # Versión de texto plano
    mensaje_texto = strip_tags(mensaje_html)

    # Crear el correo con HTML y texto alternativo
    subject = 'Recordatorio de su cita'
    from_email = settings.EMAIL_HOST_USER
    to_email = [cita.paciente.correo]
    email = EmailMultiAlternatives(subject, mensaje_texto, from_email, to_email)
    email.attach_alternative(mensaje_html, "text/html")

    # Adjuntar el logo como archivo relacionado y usar el CID en el HTML
    logo_path = settings.BASE_DIR / 'static/img/logo.png'
    with open(logo_path, 'rb') as logo_file:
        logo = MIMEImage(logo_file.read())
        logo.add_header('Content-ID', '<logo_cid>')
        email.attach(logo)

    # Enviar el correo
    email.send()

def confirmar_cita(request, cita_id, confirmacion):
    cita = get_object_or_404(Cita, id=cita_id)

    if confirmacion == 'si':
        cita.confirmada = True
    elif confirmacion == 'no':
        cita.confirmada = False

    cita.save()

    # Redirigir a la lista de citas
    return redirect('lista_citas')

def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    if request.method == 'POST':
        observacion = request.POST.get('observacion')
        cita.confirmada = False
        cita.observacion = observacion  # Almacena la observación
        cita.save()
        return redirect('lista_citas')  # Redirige a la lista de citas
    return render(request, 'confirmar_cancelar.html', {'cita': cita})

def reprogramar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    
    if request.method == 'POST':
        nueva_fecha = request.POST.get('fecha')
        nueva_hora = request.POST.get('hora')
        observacion = request.POST.get('observacion', '')

        # Guardar solicitud sin modificar la fecha original
        cita.solicitud_reprogramacion = True
        cita.nueva_fecha = nueva_fecha
        cita.nueva_hora = nueva_hora
        cita.observacion = observacion
        cita.save()

    return render(request, 'gestion/solicitar_reprogramacion.html', {'cita': cita})   
        
def solicitar_reprogramacion(request, id):
    try:
        cita = Cita.objects.get(id=id)
    except Cita.DoesNotExist:
        messages.error(request, "La cita no existe.")
        return redirect('error_page')

    if request.method == "POST":
        nueva_fecha = request.POST.get('fecha')
        nueva_hora = request.POST.get('hora')
        observacion = request.POST.get('observacion', '')

        # Guardar solicitud de reprogramación sin modificar la fecha de la cita original
        cita.solicitud_reprogramacion = True
        cita.nueva_fecha = nueva_fecha
        cita.nueva_hora = nueva_hora
        cita.observacion = observacion
        cita.save()

        messages.success(request, "Tu solicitud de reprogramación ha sido enviada. Nos comunicaremos contigo pronto.")
        return redirect('confirmacion_solicitud')  # Redirige a una página de confirmación

    return render(request, 'solicitar_reprogramacion.html', {'cita': cita})       
        
def actualizar_cita(request, id):
    if request.method == 'POST':
        cita = get_object_or_404(Cita, id=id)
        nueva_fecha = request.POST.get('nueva_fecha')
        nueva_hora = request.POST.get('nueva_hora')

        if nueva_fecha and nueva_hora:
            # Actualiza la fecha y hora de la cita
            cita.fecha = f"{nueva_fecha} {nueva_hora}"
            cita.solicitud_reprogramacion = False  # Resetea la solicitud de reprogramación
            cita.save()
            messages.success(request, "La cita ha sido actualizada exitosamente.")
        else:
            messages.error(request, "La fecha o la hora no son válidas.")
        
        return redirect('lista_citas')  # Redirige de vuelta a la lista de citas        
        
def registrar_tratamiento(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            tratamiento = form.save(commit=False)
            tratamiento.paciente = paciente  # Asignar el paciente al tratamiento
            tratamiento.save()
            return redirect('lista_tratamientos', paciente_id=paciente.id)
    else:
        form = TratamientoForm()
    return render(request, 'gestion/registrar_tratamiento.html', {'form': form, 'paciente': paciente})

def lista_tratamientos(request):
    tratamientos = Tratamiento.objects.all()  # Obtén todos los tratamientos de la base de datos
    return render(request, 'gestion/lista_tratamientos.html', {'tratamientos': tratamientos})

def agregar_tratamiento(request):
    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el tratamiento en la base de datos
            return redirect('lista_tratamientos')  # Redirige a la lista de tratamientos
    else:
        form = TratamientoForm()  # Muestra el formulario vacío

    return render(request, 'gestion/agregar_tratamiento.html', {'form': form})

def editar_tratamiento(request, id):
    tratamiento = get_object_or_404(Tratamiento, id=id)
    if request.method == 'POST':
        form = TratamientoForm(request.POST, instance=tratamiento)
        if form.is_valid():
            form.save()
            return redirect('lista_tratamientos')  # Ajusta esta redirección según tus URLs
    else:
        form = TratamientoForm(instance=tratamiento)
    return render(request, 'gestion/editar_tratamiento.html', {'form': form, 'tratamiento': tratamiento})

def eliminar_tratamiento(request, id):
    tratamiento = get_object_or_404(Tratamiento, id=id)
    if request.method == 'POST':
        tratamiento.delete()
        return redirect('lista_tratamientos')  # Ajusta esta redirección según tus URLs
    return render(request, 'gestion/eliminar_tratamiento.html', {'tratamiento': tratamiento})


def confirmar_cita(request, cita_id, confirmacion):
    # Lógica para confirmar o rechazar la cita
    cita = get_object_or_404(Cita, id=cita_id)
    
    if confirmacion == 'si':
        # Confirmar la cita
        cita.confirmada = True
        cita.save()
        return render(request, 'confirmacion_satisfaccion.html', {'cita': cita})
    
    elif confirmacion == 'no':
        # Rechazar la cita y pedir razón
        return render(request, 'rechazo_cita.html', {'cita': cita})
    
    else:
        return HttpResponse('Solicitud inválida')
    
# Citas confirmadas por mes
def citas_confirmadas_por_mes():
    citas = Cita.objects.filter(confirmada=True).annotate(mes=models.functions.TruncMonth('fecha')).values('mes').annotate(total_citas=Count('id'))
    return citas

# Tratamientos por mes
def tratamientos_por_mes():
    tratamientos = Tratamiento.objects.annotate(mes=models.functions.TruncMonth('fecha')).values('mes').annotate(total_tratamientos=Count('id'))
    return tratamientos    

# Costo total de tratamientos por mes
def costo_total_tratamientos_por_mes():
    costos = Tratamiento.objects.annotate(mes=models.functions.TruncMonth('fecha')).values('mes').annotate(total_costo=Sum('costo'))
    return costos    


def exportar_citas_csv(request):
    citas = Cita.objects.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="citas.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Paciente', 'Fecha', 'Motivo', 'Confirmada'])
    
    for cita in citas:
        writer.writerow([cita.paciente.nombre, cita.fecha, cita.motivo, cita.confirmada])
    
    return response

def exportar_csv(request):
    # Obtener los datos
    citas = Cita.objects.all()
    pacientes = Paciente.objects.all()
    tratamientos = Tratamiento.objects.all()

    # Crear la respuesta como archivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_completo.csv"'

    writer = csv.writer(response)
    writer.writerow(['Citas Confirmadas', 'Citas No Confirmadas'])
    writer.writerow([citas.filter(confirmada=True).count(), citas.filter(confirmada=False).count()])

    writer.writerow(['Paciente', 'Fecha de Nacimiento', 'Correo'])
    for paciente in pacientes:
        writer.writerow([paciente.nombre, paciente.fecha_nacimiento, paciente.correo])

    writer.writerow(['Tratamiento', 'Fecha', 'Costo'])
    for tratamiento in tratamientos:
        writer.writerow([tratamiento.tipo, tratamiento.fecha, tratamiento.costo])

    return response



def panel_reportes_data(request):
    # Datos que necesitas enviar al frontend
    citas_confirmadas = Cita.objects.filter(confirmada=True).count()
    citas_no_confirmadas = Cita.objects.filter(confirmada=False).count()
    pacientes_nuevos = Paciente.objects.filter(fecha_registro__month=timezone.now().month).count()
    tratamientos_por_mes = Tratamiento.objects.filter(fecha__year=timezone.now().year).values('fecha__month').annotate(total=Count('id')).order_by('fecha__month')

    # Envía los datos como JSON
    data = {
        'citas_confirmadas': citas_confirmadas,
        'citas_no_confirmadas': citas_no_confirmadas,
        'pacientes_nuevos': pacientes_nuevos,
        'tratamientos_por_mes': list(tratamientos_por_mes)  # Convertir a lista para JSON
    }

    return JsonResponse(data)

def registrar_factura(request, tratamiento_id):
    tratamiento = get_object_or_404(Tratamiento, id=tratamiento_id)
    paciente = tratamiento.paciente
    monto_total = tratamiento.costo
    
    if request.method == 'POST':
        metodo_pago = request.POST.get('metodo_pago')
        estado = request.POST.get('estado')
        
        # Crear factura
        factura = Factura.objects.create(
            paciente=paciente,
            tratamiento=tratamiento,
            monto_total=monto_total,
            metodo_pago=metodo_pago,
            estado=estado,
            fecha=timezone.now()
        )
        # Redirige a la página de detalles o historial
        return redirect('detalle_factura', factura_id=factura.id)
    
    return render(request, 'facturacion/crear_factura.html', {
        'tratamiento': tratamiento,
        'monto_total': monto_total
    })
    
def enviar_factura_correo(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    paciente = factura.paciente

    # Crear PDF en memoria
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(100, 750, f"Factura ID: {factura.id}")
    pdf.drawString(100, 730, f"Paciente: {paciente.nombre}")
    pdf.drawString(100, 710, f"Fecha de Emisión: {factura.fecha_emision}")
    pdf.drawString(100, 690, f"Total: ${factura.total}")
    pdf.drawString(100, 670, f"Estado de Pago: {'Pagada' if factura.estado_pago else 'Pendiente'}")
    pdf.showPage()
    pdf.save()

    # Preparar el PDF como archivo adjunto
    buffer.seek(0)
    email = EmailMessage(
        'Factura de su consulta',
        f'Estimado/a {paciente.nombre}, adjuntamos la factura de su consulta.',
        'tu_correo@gmail.com',
        [paciente.email],  # Asegúrate de que `paciente.email` existe en tu modelo
    )
    email.attach(f"factura_{factura.id}.pdf", buffer.getvalue(), 'application/pdf')
    email.send()
    buffer.close()

    return redirect('lista_facturas')    
    
    
def obtener_reservas(request):
    reservas = Reserva.objects.all()
    eventos = [
        {
            "title": "Reservado",
            "start": f"{reserva.fecha}T{reserva.hora}",
        }
        for reserva in reservas
    ]
    return JsonResponse(eventos, safe=False)

@csrf_exempt
def reservar(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        fecha = data['fecha']
        hora = data['hora']
        nombre_cliente = data['nombre_cliente']
        correo = data['correo']

        # Crear reserva en la base de datos
        Reserva.objects.create(fecha=fecha, hora=hora, nombre_cliente=nombre_cliente)

        # Enviar correo de confirmación
        send_mail(
            'Confirmación de Cita',
            f'Estimado/a {nombre_cliente},\n\nSu cita ha sido confirmada para el {fecha} a las {hora} hrs.\n\nGracias por elegirnos.',
            'tu-correo@dominio.com',  # Remitente
            [correo],  # Destinatario
            fail_silently=False,
        )

        return JsonResponse({'message': 'Reserva creada y correo enviado'}, status=201)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def reservas(request):
    return render(request, 'reservas.html')

def obtener_horas_disponibles(request):
    fecha = request.GET.get('fecha')
    horas_disponibles = ["9:45 am", "10:00 am", "10:15 am", "10:30 am", "10:45 am", "11:00 am"]
    
    # Filtra las horas ya reservadas para la fecha
    reservas = Reserva.objects.filter(fecha=fecha).values_list('hora', flat=True)
    horas_disponibles = [hora for hora in horas_disponibles if hora not in reservas]
    
    return JsonResponse(horas_disponibles, safe=False)

def home(request):
    return render(request, 'home.html')  # Renderiza la plantilla home.html
    
def reservas(request):
    return render(request, 'reservas.html')  # Renderiza la plantilla reservas.html

def blog(request):
    articles = BlogArticle.objects.order_by('-published_date')  # Ordena por fecha de publicación
    return render(request, 'blog.html', {'articles': articles})

def blog_list(request):
    articles = BlogArticle.objects.order_by('-published_date')
    return render(request, 'blog_list.html', {'articles': articles})

def blog_detail(request, pk):
    article = get_object_or_404(BlogArticle, pk=pk)
    return render(request, 'blog_detail.html', {'article': article})

def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Recoge los datos del formulario
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            role = form.cleaned_data['role']
            region = form.cleaned_data['region']
            current_stage = form.cleaned_data['current_stage']
            software = form.cleaned_data['software']
            
            # Configura el mensaje de correo
            asunto = f"Nueva solicitud de reserva de {first_name} {last_name}"
            mensaje_email = (
                f"Nombre: {first_name} {last_name}\n"
                f"Correo: {email}\n"
                f"Teléfono: {phone}\n"
                f"Cargo: {role}\n"
                f"Región: {region}\n"
                f"Etapa: {current_stage}\n"
                f"Software: {software}"
            )
            destinatario = 'andresmacias978@gmail.com'  # Dirección donde quieres recibir el correo

            try:
                # Envía el correo
                send_mail(
                    asunto,
                    mensaje_email,
                    settings.EMAIL_HOST_USER,  # Remitente correcto usando settings
                    [destinatario],   # Destinatario
                    fail_silently=False,
                )
                messages.success(request, 'Tu solicitud de reserva ha sido enviada exitosamente.')
                return redirect('reservation')
            except Exception as e:
                print(f"Error al enviar correo: {e}")  # Útil para depuración
                messages.error(request, 'Hubo un error al enviar la solicitud. Inténtalo nuevamente.')
    else:
        form = ReservationForm()

    return render(request, 'reservas.html', {'form': form})

def crear_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)  # Procesar el formulario con los datos POST
        if form.is_valid():
            # Guardamos la factura en la base de datos
            factura = form.save()

            # Redirigimos a una página de éxito o a la lista de facturas
            return redirect('lista_facturas')  # Redirige a la lista de facturas, que ya debes haber creado

    else:
        form = FacturaForm()  # Si es GET, mostramos el formulario vacío

    return render(request, 'gestion/crear_factura.html', {'form': form})

def factura_detalle(request, factura_id):
    factura = Factura.objects.get(id=factura_id)
    return render(request, 'factura_detalle.html', {'factura': factura})

def enviar_factura(factura):
    asunto = f"Factura {factura.id} - DentalCare"
    mensaje = f"Estimado {factura.paciente.nombre},\n\nAdjunto encontrará su factura por los tratamientos realizados."
    destinatario = factura.paciente.contacto  # Aquí se usa el contacto como correo, debe ser un correo real

    send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [destinatario])

def factura_detalle(request, factura_id):
    factura = Factura.objects.get(id=factura_id)
    enviar_factura(factura)  # Enviar la factura por correo
    return render(request, 'factura_detalle.html', {'factura': factura})

def generar_factura_pdf(request, factura_id):
    # Obtener la factura
    factura = Factura.objects.get(id=factura_id)

    # Crear un objeto HttpResponse para devolver el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{factura.id}.pdf"'

    # Crear el documento PDF
    document = SimpleDocTemplate(response, pagesize=letter)

    # Crear los estilos para el documento
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_bold = ParagraphStyle(name='Bold', fontSize=12, fontName='Helvetica-Bold')
    style_title = ParagraphStyle(name='Title', fontSize=16, fontName='Helvetica-Bold')

    # Crear contenido para el PDF
    content = []

    # Título de la factura
    content.append(Paragraph(f'Factura {factura.id}', style_title))

    # Información del paciente
    content.append(Paragraph(f'Paciente: {factura.paciente.nombre}', style_normal))
    content.append(Paragraph(f'Fecha de emisión: {factura.fecha_emision}', style_normal))
    content.append(Paragraph(f'Total: ${factura.total}', style_normal))

    # Tratamientos realizados - Tabla de tratamientos
    content.append(Paragraph('<b>Tratamientos realizados:</b>', style_bold))

    # Crear la tabla de tratamientos realizados
    data = [['Tratamiento', 'Costo']]  # Encabezado de la tabla
    for tratamiento in factura.tratamientos.all():
        data.append([tratamiento.nombre, f'${tratamiento.costo}'])  # Datos de los tratamientos

    # Crear el objeto Table
    table = Table(data)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # Añadir bordes a las celdas
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),  # Fondo gris para la fila de encabezado
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrar el texto
    ]))

    # Agregar la tabla al contenido
    content.append(table)

    # Estado de pago
    estado_pago = 'Pagada' if factura.estado_pago else 'Pendiente'
    content.append(Paragraph(f'Estado de pago: {estado_pago}', style_normal))

    # Crear el PDF
    document.build(content)

    return response

def lista_facturas(request):
    # Obtener todas las facturas
    facturas = Factura.objects.all()

    return render(request, 'lista_facturas.html', {'facturas': facturas})

def editar_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)  # Carga la factura
    if request.method == 'POST':
        form = FacturaForm(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            return redirect('lista_facturas')  # Redirige a la lista de facturas después de la edición
    else:
        form = FacturaForm(instance=factura)
    
    return render(request, 'gestion/editar_factura.html', {'form': form})

def format_number(num):
    # Usar Decimal para manejar el redondeo de forma precisa
    num = Decimal(num)

    if num >= 1_000_000:
        return f"${num / 1_000_000:,.2f}M"  # Mostrar en millones con 2 decimales
    elif num >= 1_000:
        return f"${num / 1_000:,.2f}K"  # Mostrar en miles con 2 decimales
    else:
        return f"${num:,.2f}"  # Mostrar con 2 decimales en formato de moneda
    
def panel_reportes(request):
    # Resumen de citas
    total_citas = Cita.objects.count()
    citas_completadas = Cita.objects.filter(confirmada=True).count()
    citas_canceladas = Cita.objects.filter(confirmada=False).count()

    # Ingresos totales
    ingresos = Tratamiento.objects.aggregate(total=Sum('costo'))['total'] or 0

    # Citas por día para gráficos
    citas_por_dia = (
        Cita.objects.filter(fecha__month=timezone.now().month)
        .extra(select={'day': 'DATE(fecha)'}).values('day')
        .annotate(count=Count('id'))
    )

    dias = [entry['day'] for entry in citas_por_dia]
    conteos = [entry['count'] for entry in citas_por_dia]

    # Tratamientos realizados (tipo y cantidad)
    tratamientos_realizados = (
        Tratamiento.objects.values('tipo')
        .annotate(cantidad=Count('id'))
        .order_by('-cantidad')
    )
    tratamiento_tipos = [tratamiento['tipo'] for tratamiento in tratamientos_realizados]
    tratamiento_cantidades = [tratamiento['cantidad'] for tratamiento in tratamientos_realizados]

    context = {
        'total_citas': total_citas,
        'citas_completadas': citas_completadas,
        'citas_canceladas': citas_canceladas,
        'ingresos': ingresos,
        'dias': dias,
        'conteos': conteos,
        'tratamiento_tipos': tratamiento_tipos,
        'tratamiento_cantidades': tratamiento_cantidades,
    }

    return render(request, 'gestion/panel_reportes.html', context)


def generar_grafico(citas_confirmadas, citas_canceladas):
    # Configurar el gráfico
    fig, ax = plt.subplots()
    etiquetas = ['Confirmadas', 'Canceladas']
    valores = [citas_confirmadas, citas_canceladas]
    ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Para un círculo perfecto

    # Convertir el gráfico a base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    chart_data = base64.b64encode(image_png).decode('utf-8')
    return chart_data

def descargar_reporte_pdf(request):
    # Crear respuesta de PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_consultorio.pdf"'

    # Configurar el documento PDF
    pdf = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Encabezado
    logo_path = os.path.join(settings.BASE_DIR, 'static/img/logo.png')
    header = Paragraph("<b>Reporte Completo de Actividades del Consultorio</b>", styles['Title'])
    subtitle = Paragraph("Este informe detalla todas las actividades realizadas en el consultorio.", styles['Normal'])
    elements.append(header)
    elements.append(subtitle)
    elements.append(Spacer(1, 12))

    # Agregar logo
    if os.path.exists(logo_path):
        elements.append(Image(logo_path, width=100, height=100))
        elements.append(Spacer(1, 20))

    # Resumen General de Estadísticas
    total_citas = Cita.objects.count()
    citas_confirmadas = Cita.objects.filter(confirmada=True).count()
    citas_canceladas = Cita.objects.filter(confirmada=False).count()
    ingresos_totales = Factura.objects.filter(estado_pago="pagado").aggregate(total=Sum('total'))['total'] or 0
    tratamientos_realizados = Tratamiento.objects.count()

    data_summary = [
        ["Métrica", "Valor"],
        ["Total de Citas", total_citas],
        ["Citas Confirmadas", citas_confirmadas],
        ["Citas Canceladas", citas_canceladas],
        ["Ingresos Totales", f"${ingresos_totales}"],
        ["Tratamientos Realizados", tratamientos_realizados],
    ]
    table_summary = Table(data_summary, colWidths=[200, 200])
    table_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.25, 0.25, 0.5)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table_summary)
    elements.append(Spacer(1, 20))

    # Gráfico de barras de ingresos por mes
    elements.append(Paragraph("Ingresos por Mes", styles['Heading2']))
    drawing_bar = Drawing(400, 200)
    bar_chart = VerticalBarChart()
    bar_chart.x = 50
    bar_chart.y = 50
    bar_chart.height = 125
    bar_chart.width = 300

    # Corrección: Usar 'total' en lugar de 'monto_total'
    ingresos_mensuales = [
        Factura.objects.filter(fecha_emision__month=month, estado_pago="pagado").aggregate(Sum('total'))['total__sum'] or 0
        for month in range(1, 13)
    ]
    bar_chart.data = [ingresos_mensuales]
    bar_chart.categoryAxis.categoryNames = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    bar_chart.valueAxis.valueMin = 0
    bar_chart.valueAxis.valueMax = max(ingresos_mensuales) + 100
    bar_chart.valueAxis.valueStep = 100
    bar_chart.bars[0].fillColor = colors.green
    drawing_bar.add(bar_chart)
    elements.append(drawing_bar)
    elements.append(Spacer(1, 20))

    # Gráfico de pastel de tipos de tratamientos
    elements.append(Paragraph("Distribución de Tipos de Tratamientos", styles['Heading2']))
    drawing_pie = Drawing(400, 200)
    pie_chart = Pie()
    pie_chart.x = 150
    pie_chart.y = 40
    pie_chart.data = list(Tratamiento.objects.values('tipo').annotate(count=Count('tipo')).values_list('count', flat=True))
    pie_chart.labels = [t['tipo'] for t in Tratamiento.objects.values('tipo').annotate(count=Count('tipo'))]
    pie_chart.slices[0].fillColor = colors.blue
    pie_chart.slices[1].fillColor = colors.green
    drawing_pie.add(pie_chart)
    elements.append(drawing_pie)

    # Generar el PDF
    pdf.build(elements)
    return response

def citas_del_dia(request, fecha):
    # Convertir la fecha del formato recibido en el URL a un objeto de fecha
    fecha_obj = parse_datetime(fecha)

    # Verificar que la fecha se ha convertido correctamente
    if fecha_obj is None:
        # Si la fecha es inválida, redirigir a otra página o mostrar un mensaje
        return render(request, 'gestion/error.html', {'message': 'Fecha inválida'})

    # Filtrar las citas de ese día específico
    citas = Cita.objects.filter(fecha__date=fecha_obj.date())

    context = {
        'citas': citas,
        'fecha': fecha_obj,
    }
    
    return render(request, 'gestion/citas_del_dia.html', context)

def enviar_factura_correo(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    paciente = factura.paciente

    # Crear un archivo PDF en memoria
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Estilos de texto
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.textColor = colors.HexColor('#007bff')
    normal_style = styles['BodyText']
    normal_style.fontSize = 12

    # Contenido del PDF
    elements = []

    # Encabezado
    elements.append(Paragraph("Consultorio Odontológico", title_style))
    elements.append(Paragraph("Dirección: Calle Falsa 123, Ciudad", normal_style))
    elements.append(Paragraph("Teléfono: +123 456 7890", normal_style))
    elements.append(Paragraph(f"Fecha de Emisión: {factura.fecha_emision.strftime('%d %b %Y')}", normal_style))
    elements.append(Paragraph("<br/>", normal_style))  # Espacio

    # Información del paciente
    elements.append(Paragraph(f"<b>Factura ID:</b> {factura.id}", normal_style))
    elements.append(Paragraph(f"<b>Paciente:</b> {paciente.nombre}", normal_style))
    elements.append(Paragraph("<br/>", normal_style))  # Espacio

    # Tabla de detalles de la factura
    data = [
        ['Descripción', 'Cantidad', 'Precio Unitario', 'Total'],
        # Ejemplo de fila de servicio. Puedes agregar más filas según los servicios de la factura.
        ['Consulta general', '1', f"${factura.total}", f"${factura.total}"]
    ]
    
    # Estilo de la tabla
    table = Table(data, colWidths=[2 * inch, 1 * inch, 1.5 * inch, 1.5 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    elements.append(table)

    # Total de la factura
    elements.append(Paragraph("<br/>", normal_style))
    elements.append(Paragraph(f"<b>Total a Pagar:</b> ${factura.total}", title_style))

    # Crear el PDF
    doc.build(elements)

    # Preparar el PDF para enviar
    buffer.seek(0)
    email = EmailMessage(
        'Factura de su consulta',
        f'Estimado/a {paciente.nombre}, adjuntamos la factura de su consulta.',
        'tu_correo@gmail.com',
        [paciente.email],  # Asegúrate de que `paciente.email` exista en el modelo
    )
    email.attach(f"factura_{factura.id}.pdf", buffer.getvalue(), 'application/pdf')
    email.send()
    buffer.close()

    return redirect('lista_facturas')

def lista_inventario(request):
    productos = Producto.objects.all()  # Obtener todos los productos en el inventario
    return render(request, 'gestion/lista_inventario.html', {'productos': productos})

def inventario(request):
    productos = Producto.objects.all()  # Obtén todos los productos del inventario
    return render(request, 'gestion/inventario.html', {'productos': productos})

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado exitosamente!')
            return redirect('lista_inventario')
    else:
        form = ProductoForm()
    return render(request, 'gestion/agregar_producto.html', {'form': form})

def editar_producto(request, producto_id):
    # Obtener el producto o lanzar un error 404 si no existe
    producto = get_object_or_404(Producto, id=producto_id)

    # Si el método es GET, creamos el formulario con los datos actuales del producto
    form = ProductoForm(instance=producto)

    # Si el método es POST, procesamos la actualización del producto
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        
        # Validamos el formulario
        if form.is_valid():
            # Guardamos los cambios en la base de datos
            form.save()
            
            # Enviamos un mensaje de éxito
            messages.success(request, 'Producto actualizado exitosamente!')
            
            # Redirigimos a la vista de inventario
            return redirect('inventario')  # Asegúrate de que 'inventario' esté en tus URLs

        else:
            # Si el formulario no es válido, mostramos un mensaje de error
            messages.error(request, 'Hubo un error al actualizar el producto. Por favor, revisa los datos.')

    # Renderizamos la plantilla con el formulario
    return render(request, 'gestion/editar_producto.html', {'form': form, 'producto': producto})

def eliminar_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    producto.delete()
    messages.success(request, 'Producto eliminado exitosamente!')
    return redirect('gestion/lista_inventario')

def login_cliente(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Autenticar al usuario
            usuario = form.get_user()
            login(request, usuario)
            # Redirigir al cliente a su dashboard
            return redirect('cliente_dashboard')  # Cambia esto según tu URL de dashboard
        else:
            messages.error(request, "Credenciales incorrectas. Intenta de nuevo.")
            return redirect('login')
    else:
        form = AuthenticationForm()
    
    return render(request, 'gestion/login.html', {'form': form})

def cliente_dashboard(request):
    # Obtén los detalles del cliente a partir del usuario autenticado
    cliente = request.user.cliente  # Suponiendo que has creado un modelo Cliente relacionado con el usuario
    return render(request, 'gestion/dashboard.html', {'cliente': cliente})

from django.shortcuts import render

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            # Reemplaza 'User' con 'Usuario'
            user = Usuario.objects.get(email=email)  # Usar Usuario en lugar de User
            
            # Generar un token de recuperación
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Crear la URL para el restablecimiento de la contraseña
            reset_url = f"http://127.0.0.1:8000/reset_password/{uid}/{token}/"

            # Enviar el correo con el enlace para restablecer la contraseña
            email_subject = "Recuperación de Contraseña"
            email_message = render_to_string('gestion/email_template.html', {'reset_url': reset_url})
            send_mail(email_subject, email_message, settings.DEFAULT_FROM_EMAIL, [user.email])

            # Redirigir a la página de éxito
            return render(request, 'gestion/forgot_password_success.html')

        except Usuario.DoesNotExist:
            # Si el correo no se encuentra en la base de datos
            return render(request, 'gestion/forgot_password.html', {'error': 'Correo no registrado.'})

    return render(request, 'gestion/forgot_password.html')


def reset_password(request, uidb64, token):
    try:
        # Decodificar el ID del usuario desde el URL
        uid = urlsafe_base64_decode(uidb64).decode()
        User = get_user_model()
        user = User.objects.get(pk=uid)

        # Verificar si el token es válido
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()  # Guarda la nueva contraseña
                    return redirect('login')  # Redirige a la página de login
            else:
                form = SetPasswordForm(user)

            return render(request, 'reset_password.html', {'form': form})

        else:
            # Si el token es inválido o expirado
            return render(request, 'reset_password.html', {'error': 'El enlace ha expirado o es inválido.'})

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return redirect('forgot_password') 