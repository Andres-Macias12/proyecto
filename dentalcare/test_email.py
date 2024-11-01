import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'andresmacias978@gmail.com'
EMAIL_HOST_PASSWORD = 'zmxj yrij iulw ypsd'  # Asegúrate de que esta sea correcta

# Crear el mensaje
msg = MIMEMultipart()
msg['From'] = EMAIL_HOST_USER
msg['To'] = 'andrescuesta978@gmail.com'  # Cambia esto por un correo válido
msg['Subject'] = 'Prueba de correo'

# Cuerpo del mensaje
body = 'Este es un correo de prueba.'
msg.attach(MIMEText(body, 'plain'))

try:
    # Iniciar conexión
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()  # Iniciar TLS
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    server.send_message(msg)
    print("Correo enviado con éxito.")
except Exception as e:
    print(f"Error al enviar correo: {e}")
finally:
    server.quit()
