from django.template.loader import render_to_string 
import csv, datetime, os, calendar, random, string, smtplib, ssl, certifi
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import ( Q,Count,functions)
from django.core.mail import send_mail
from django.conf import settings
from .models import Usuario, Paciente, Cita, Tratamiento, Factura
from .forms import PacienteForm, TratamientoForm
from django.core.paginator import Paginator
from datetime import date, timedelta, datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django_tenants.utils import schema_context
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.urls import reverse
from django.utils import timezone



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
        form = PacienteForm(request.POST)
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


def inventario(request):
    # Lógica para manejar la vista del inventario
    return render(request, 'gestion/inventario.html')


def ver_historia_paciente(request, paciente_id):
    # Obtener el paciente o devolver un 404 si no existe
    paciente = get_object_or_404(Paciente, id=paciente_id)
    # Agregar la lógica para obtener la historia del paciente, citas, tratamientos, etc.
    contexto = {
        'paciente': paciente,
        # Otros datos relevantes, como citas, tratamientos, etc.
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
    confirm_url = settings.SITE_URL + reverse('confirmar_cita', args=[cita.id, 'si'])
    reject_url = settings.SITE_URL + reverse('confirmar_cita', args=[cita.id, 'no'])
    
    # URL del logo
    logo_url = settings.SITE_URL + '/static/img/logo.png'

    # Cargar y renderizar la plantilla de correo electrónico
    mensaje_html = render_to_string('emails/recordatorio_cita.html', {
        'cita': cita,
        'confirm_url': confirm_url,
        'reject_url': reject_url,
        'logo_url': logo_url
    })

    # Definir el asunto del correo electrónico
    asunto = 'Recordatorio de su cita'

    # Enviar el correo electrónico en formato HTML
    send_mail(
        asunto,
        '',  # Cuerpo de texto plano vacío
        settings.EMAIL_HOST_USER,  # Dirección del remitente
        [cita.paciente.correo],  # Dirección del destinatario
        fail_silently=False,
        html_message=mensaje_html  # Usamos la plantilla HTML para el mensaje
    )

        
        
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
    tratamientos = Tratamiento.objects.all()  # Obtener todos los tratamientos
    return render(request, 'gestion/lista_tratamientos.html', {'tratamientos': tratamientos})

def agregar_tratamiento(request):
    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar el tratamiento con el paciente seleccionado
            return redirect('lista_tratamientos')  # Redirigir a la lista de tratamientos
    else:
        form = TratamientoForm()
    
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
    
    
