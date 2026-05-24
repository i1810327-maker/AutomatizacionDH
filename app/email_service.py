import logging
import os
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"


def _get_gmail_service():
    if not os.path.exists(TOKEN_FILE):
        logging.warning("No token.json — correo no disponible. Ejecutá 'uv run python auth_gmail.py' para autorizar.")
        return None
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
        else:
            logging.warning("Token inválido — ejecutá 'uv run python auth_gmail.py' de nuevo.")
            return None
    return build("gmail", "v1", credentials=creds)


def send_rejection_email(
    destinatario: str,
    nombre_docente: str,
    titulo_reporte: str,
    comentarios: str,
) -> bool:
    service = _get_gmail_service()
    if service is None:
        logging.warning(
            "Gmail API no configurado (falta credentials.json). "
            "Correo no enviado."
        )
        return False

    asunto = f"Reporte rechazado: {titulo_reporte}"
    cuerpo = f"""
Hola {nombre_docente},

Tu reporte "{titulo_reporte}" ha sido revisado y no cumple con los requisitos establecidos.

Comentarios de la Directora:
{comentarios}

Por favor, realiza las correcciones necesarias y vuelve a enviar el reporte.

Saludos,
Sistema de Automatización DH
"""
    message_text = (
        f"From: me\r\n"
        f"To: {destinatario}\r\n"
        f"Subject: {asunto}\r\n\r\n"
        f"{cuerpo.strip()}"
    )
    try:
        message = service.users().messages().send(
            userId="me",
            body={"raw": __import__("base64").urlsafe_b64encode(
                message_text.encode("utf-8")
            ).decode("utf-8")},
        ).execute()
        logging.info(f"Correo enviado a {destinatario}: {message['id']}")
        return True
    except HttpError as error:
        logging.error(f"Error al enviar correo: {error}")
        return False
