#-----------------------------------
#   © 2025 OxiGo. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 18 de noviembre de 2025
#-----------------------------------
#   Fichero: email_utils.py
#   Descripción: Funciones para el envio del código de verificacion al usuario
#-----------------------------------

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = "OxiGo@mail.com"

def send_confirmation_email(to_email: str, code: str):
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

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)
