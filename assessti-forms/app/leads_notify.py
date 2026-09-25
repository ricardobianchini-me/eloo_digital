"""
Notificação por e-mail de novo lead — Gmail SMTP com senha de app.

Best-effort de propósito: a planilha (leads.py) é a fonte de verdade do
lead — se o e-mail falhar (credencial errada, Gmail fora do ar, etc.), o
lead já está salvo mesmo assim. Este módulo só loga a falha, nunca levanta
exceção pro chamador.
"""
import logging
import smtplib
from email.mime.text import MIMEText

from config import settings

logger = logging.getLogger(__name__)

_CAMPOS_VISIVEIS = [
    "Nome", "Instituição", "Cargo", "E-mail", "WhatsApp",
    "Interesse", "Origem", "Urgência", "Mensagem",
]


def notificar_novo_lead(lead: dict[str, str]) -> None:
    if not settings.gmail_user or not settings.gmail_app_password:
        logger.warning(
            "Notificação de lead pulada — GMAIL_USER/GMAIL_APP_PASSWORD não configurados"
        )
        return

    destino = settings.leads_notify_email or settings.gmail_user
    corpo = "\n".join(f"{campo}: {lead.get(campo, '')}" for campo in _CAMPOS_VISIVEIS)
    corpo += "\n\nGerenciar: https://eloo.digital/assessment/leads/crm"

    msg = MIMEText(corpo)
    msg["Subject"] = f"Novo lead eloo.digital — {lead.get('Nome', '')} ({lead.get('Instituição', '')})"
    msg["From"] = settings.gmail_user
    msg["To"] = destino

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as smtp:
            smtp.login(settings.gmail_user, settings.gmail_app_password)
            smtp.send_message(msg)
        logger.info(f"Notificação de lead enviada para {destino}")
    except Exception:
        logger.exception("Falha ao enviar notificação de lead por e-mail")
