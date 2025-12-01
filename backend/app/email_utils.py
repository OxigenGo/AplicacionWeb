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
import requests
from fastapi import HTTPException

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SENDER_EMAIL = "ftikhom@upv.edu.es"
SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"


def send_confirmation_email(to_email: str, code: str) -> bool:
    """
    Envía un código de verificación al correo del usuario usando SendGrid vía requests.
    
    Args:
        to_email (str): Correo destino
        code (str): Código de verificación
    
    Returns:
        bool: True si es enviado correctamente, False si ocurre un error
    """

    # Cargar API key de entorno
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

    payload = {
        "personalizations": [
            {
                "to": [{"email": to_email}],
                "subject": "Tu código de verificación"
            }
        ],
        "from": {"email": SENDER_EMAIL},
        "content": [
            {"type": "text/html", "value": html_content}
        ]
    }

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(SENDGRID_URL, json=payload, headers=headers)

        # SendGrid devuelve 202 cuando el correo se acepta correctamente
        if response.status_code == 202:
            logger.info(f"Correo enviado a {to_email}, status code: 202")
            return True

        # Si hay error de SendGrid
        logger.error(f"Error de SendGrid al enviar a {to_email}: {response.status_code} - {response.text}")
        return False

    except Exception as e:
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
