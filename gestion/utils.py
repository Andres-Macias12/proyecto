from datetime import datetime, timedelta
from django.core.mail import send_mail
from .models import Cita

def enviar_notificaciones():
    # Obtener la fecha de mañana
    manana = datetime.now().date() + timedelta(days=1)
    
    # Buscar todas las citas que ocurren mañana
    citas = Cita.objects.filter(fecha__date=manana)

    for cita in citas:
        # Definir el mensaje
        asunto = 'Recordatorio de su cita dental'
        mensaje = f"Estimado/a {cita.paciente.nombre} {cita.paciente.apellido},\n\n" \
                  f"Este es un recordatorio de su cita agendada para el día {cita.fecha.strftime('%d/%m/%Y')} " \
                  f"a las {cita.fecha.strftime('%H:%M')}.\n\n" \
                  f"Por favor, confirme su asistencia. \n\nSaludos cordiales,\nSu equipo de DentalCare."
        
        # Enviar el correo electrónico
        send_mail(
            asunto,
            mensaje,
            'noreply@dentalcare.com',  # El correo del remitente
            [cita.paciente.correo],  # El correo del destinatario
            fail_silently=False,
        )


def format_number(num):
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"  # Para millones
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"  # Para miles
    else:
        return str(num)