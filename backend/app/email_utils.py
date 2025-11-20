#-----------------------------------
#   © 2025 OxiGo. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 18 de noviembre de 2025
#-----------------------------------
#   Fichero: email_utils.py
#   Descripción: Funciones para el envío del código de verificación al usuario
#-----------------------------------

import os
import logging
import traceback
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from python_http_client.exceptions import HTTPError

# Configurar logging para systemd/journalctl
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SENDER_EMAIL = "ftikhom@upv.edu.es"

def send_confirmation_email(to_email: str, code: str) -> bool:
    """
    Envía un correo con un código de verificación al usuario.
    
    Args:
        to_email (str): Correo del destinatario
        code (str): Código de verificación
    
    Returns:
        bool: True si se envió correctamente, False si hubo error
    """
    # Leer la API key cada vez para asegurar que está disponible
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    if not SENDGRID_API_KEY:
        logger.error("No se encontró la variable de entorno SENDGRID_API_KEY")
        return False

    html_content = f"""
    <h2>Confirmación de correo electrónico</h2>
    <p>Gracias por registrarte.</p>
    <p>Tu código de verificación es:</p>

    <h1 style="letter-spacing: 4px; font-size: 32px; font-weight: bold;">
        {code}
    </h1>

    <p>Introduce este código en la aplicación para completar tu registro.</p>

    <p>Este código expira en 20 minutos.</p>
    """

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to_email,
        subject="Tu código de verificación",
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"Correo enviado a {to_email}, status code: {response.status_code}")
        return True

    except HTTPError as e:
        # Captura errores de HTTP de SendGrid
        logger.error(f"Error HTTP de SendGrid al enviar a {to_email}: {e.status_code} - {e.body}")
        logger.error(traceback.format_exc())
        return False

    except Exception as e:
        # Captura cualquier otro error
        logger.error(f"Error inesperado al enviar correo a {to_email}: {e}")
        logger.error(traceback.format_exc())
        return False


# Bloque de prueba opcional
if __name__ == "__main__":
    test_email = "tu_correo@gmail.com"
    test_code = "123456"
    if send_confirmation_email(test_email, test_code):
        print("Correo enviado correctamente")
    else:
        print("Fallo al enviar el correo")
