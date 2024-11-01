from django.core.management.base import BaseCommand
from gestion.utils import enviar_notificaciones

class Command(BaseCommand):
    help = 'Envía notificaciones el día anterior a las citas'

    def handle(self, *args, **kwargs):
        enviar_notificaciones()
        self.stdout.write(self.style.SUCCESS('Notificaciones enviadas correctamente.'))
