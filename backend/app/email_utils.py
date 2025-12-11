#-----------------------------------
#   © 2025 OxiGo. Todos los derechos reservados.
#-----------------------------------
#   Autor: Fédor Tikhomirov
#   Fecha: 18 de noviembre de 2025
#-----------------------------------
#   Fichero: email_utils.py
#   Descripción: Funciones modulares para envío de correos
#                automatizados con SendGrid (versión corporativa)
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

# ============================================================
#   CONFIGURACIÓN CORPORATIVA
# ============================================================

PRIMARY_COLOR = "#0086FB"

LOGO_URL = ""
USE_LOGO = False


# ============================================================
#   PLANTILLA CORPORATIVA HTML (REUTILIZABLE)
# ============================================================

def build_corporate_email(title: str, content_html: str) -> str:
    """
    @brief Construye una plantilla HTML corporativa con estilo unificado.
    @param title Título principal del correo.
    @param content_html Contenido específico del correo (HTML).
    @return HTML final renderizado listo para enviar.
    """

    logo_html = f"""
        <div style="text-align:center; margin-bottom:20px;">
            <img src="{LOGO_URL}" alt="OxiGo" width="120">
        </div>
    """ if USE_LOGO else ""

    return f"""
    <div style="
        background:#f5f7fa;
        padding:40px 0;
        font-family:Arial, Helvetica, sans-serif;
        ">
        <div style="
            max-width:600px;
            margin:auto;
            background:white;
            border-radius:10px;
            border:1px solid #e5e5e5;
            padding:30px 40px;
            box-shadow:0 2px 6px rgba(0,0,0,0.05);
        ">
        
            {logo_html}

            <h2 style="
                color:{PRIMARY_COLOR};
                text-align:center;
                margin-top:0;
                margin-bottom:25px;
                font-size:26px;
            ">{title}</h2>

            <div style="font-size:15px; color:#333;">
                {content_html}
            </div>

            <hr style="margin:30px 0; border:none; border-top:1px solid #ddd;">

            <p style="font-size:12px; color:#777; text-align:center;">
                © 2025 OxiGo — Correo generado automáticamente.
            </p>
        </div>
    </div>
    """


# ============================================================
#   FUNCIONES BASE SENDGRID
# ============================================================

def build_sendgrid_payload(to_email: str, subject: str, html_body: str) -> dict:
    return {
        "personalizations": [{"to": [{"email": to_email}], "subject": subject}],
        "from": {"email": SENDER_EMAIL},
        "content": [{"type": "text/html", "value": html_body}]
    }


def send_email_via_sendgrid(payload: dict) -> bool:
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

    if not SENDGRID_API_KEY:
        logger.error("No se encontró la variable SENDGRID_API_KEY")
        return False

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(SENDGRID_URL, json=payload, headers=headers)

        if response.status_code == 202:
            logger.info("Correo enviado correctamente (202).")
            return True

        logger.error(f"Error de SendGrid: {response.status_code} - {response.text}")
        return False

    except Exception as e:
        logger.error(f"Error inesperado al enviar correo: {e}")
        logger.error(traceback.format_exc())
        return False


# ============================================================
#   CORREOS
# ============================================================

def send_confirmation_email(to_email: str, code: str) -> bool:
    content = f"""
        <p>Gracias por registrarte en OxiGo.</p>
        <p>Tu código de verificación es:</p>

        <div style="
            text-align:center;
            font-size:36px;
            letter-spacing:6px;
            margin:25px 0;
            color:{PRIMARY_COLOR};
            font-weight:bold;
        ">{code}</div>

        <p>Introduce este código en la aplicación para confirmar tu cuenta.</p>
        <p>El código expira en 20 minutos.</p>
    """

    html = build_corporate_email(
        title="Confirmación de correo",
        content_html=content
    )

    payload = build_sendgrid_payload(
        to_email=to_email,
        subject="Tu código de verificación",
        html_body=html
    )

    return send_email_via_sendgrid(payload)


def send_incident_created_email(to_email: str, incident_id: int, subject: str):
    content = f"""
        <p>Se ha registrado correctamente tu incidencia en el sistema.</p>

        <p><b>ID de incidencia:</b> {incident_id}</p>
        <p><b>Asunto:</b> {subject}</p>

        <p>Un administrador revisará tu caso lo antes posible.</p>
    """

    html = build_corporate_email(
        title="Incidencia creada",
        content_html=content
    )

    payload = build_sendgrid_payload(
        to_email=to_email,
        subject="Tu incidencia ha sido creada",
        html_body=html
    )

    return send_email_via_sendgrid(payload)


def send_incident_updated_email(to_email: str, incident_id: int, changes: dict):
    if changes:
        changes_html = "<ul>"
        for field, (old, new) in changes.items():
            changes_html += f"""
                <li style="margin-bottom:10px;">
                    <b>{field.capitalize()}</b><br>
                    <span style="color:#a00;">Antes:</span> {old}<br>
                    <span style="color:#0a0;">Ahora:</span> {new}
                </li>
            """
        changes_html += "</ul>"
    else:
        changes_html = "<p>No se especificaron detalles del cambio.</p>"

    content = f"""
        <p>Se han realizado cambios en tu incidencia.</p>

        <p><b>ID de incidencia:</b> {incident_id}</p>

        <h3 style="color:{PRIMARY_COLOR}; margin-top:25px;">Cambios realizados:</h3>
        {changes_html}

        <p style="margin-top:20px;">Si no reconoces esta modificación, contacta con soporte.</p>
    """

    html = build_corporate_email(
        title="Incidencia actualizada",
        content_html=content
    )

    payload = build_sendgrid_payload(
        to_email=to_email,
        subject="Tu incidencia ha sido actualizada",
        html_body=html
    )

    return send_email_via_sendgrid(payload)