"""
Formulário de contato público da landing page (eloo.digital/assessment) —
grava leads numa planilha própria, separada da(s) planilha(s) de coleta de
clientes ativos (ver `clientes.py`). Não é secret (mesma lógica de
`clientes.py`: o ID por si só não dá acesso a nada — quem protege é a
credencial da conta de serviço, que só o servidor tem).
"""
import logging
from datetime import datetime, timezone

import gspread
from google.oauth2.service_account import Credentials

from config import settings

logger = logging.getLogger(__name__)

LEADS_SPREADSHEET_ID = "1GYZIKoAxpveCCWUv2QnyGBMdSUqvRtTLjzPKXIC5VTk"
LEADS_ABA = "Leads"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

COLUNAS = ["Data/Hora", "Nome", "Empresa", "E-mail", "Telefone", "Mensagem"]


def _cliente_gspread():
    creds = Credentials.from_service_account_file(
        settings.google_credentials_file, scopes=SCOPES
    )
    return gspread.authorize(creds)


def _worksheet():
    sh = _cliente_gspread().open_by_key(LEADS_SPREADSHEET_ID)
    try:
        return sh.worksheet(LEADS_ABA)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(LEADS_ABA, rows=200, cols=len(COLUNAS))
        ws.append_row(COLUNAS)
        return ws


def salvar_lead(nome: str, empresa: str, email: str, telefone: str, mensagem: str) -> None:
    ws = _worksheet()
    agora = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([agora, nome, empresa, email, telefone, mensagem])
    logger.info(f"Novo lead salvo: {nome} ({empresa})")
