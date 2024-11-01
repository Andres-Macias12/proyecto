from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailAuthBackend(ModelBackend):
    """
    Backend personalizado para autenticar con el correo electrónico en lugar del nombre de usuario.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Intentar obtener el usuario por su email
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
