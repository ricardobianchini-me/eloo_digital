"""
Histórico de atividade do CRM de Leads — log plano de eventos (criação de
lead, mudança de campo) pros dois fluxos (`leads.py` e `prospeccao.py`),
numa aba própria ("Histórico") na mesma planilha. Só leitura/escrita de
append — nunca edita uma linha já gravada, então não tem risco de corromper
um evento passado.

Decisão de design: um log plano (sem relação formal com a linha de origem)
em vez de tentar manter um histórico por lead dentro da própria linha dele.
Mais simples de implementar e suficiente pro uso real (ver "o que mudou
recentemente", não "me dê o diff exato de um lead específico").
"""
import logging
from datetime import datetime, timezone

import gspread
from google.oauth2.service_account import Credentials

from config import settings

logger = logging.getLogger(__name__)

HISTORICO_SPREADSHEET_ID = "1GYZIKoAxpveCCWUv2QnyGBMdSUqvRtTLjzPKXIC5VTk"
HISTORICO_ABA = "Histórico"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

COLUNAS = ["Data/Hora", "Origem", "Lead", "Evento", "Campo", "De", "Para"]


def _cliente_gspread():
    creds = Credentials.from_service_account_file(
        settings.google_credentials_file, scopes=SCOPES
    )
    return gspread.authorize(creds)


def _worksheet():
    sh = _cliente_gspread().open_by_key(HISTORICO_SPREADSHEET_ID)
    try:
        return sh.worksheet(HISTORICO_ABA)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(HISTORICO_ABA, rows=500, cols=len(COLUNAS))
        ws.append_row(COLUNAS)
        return ws


def registrar(origem: str, lead: str, evento: str, campo: str = "", de: str = "", para: str = "") -> None:
    """Nunca deixa uma falha de log quebrar a operação principal (salvar um
    campo, criar um lead) — só registra o erro e segue."""
    try:
        ws = _worksheet()
        agora = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([agora, origem, lead, evento, campo, de, para])
    except Exception:
        logger.exception(f"Falha ao registrar histórico: {origem} / {lead} / {evento}")


def listar_recentes(limite: int = 200) -> list[dict[str, str]]:
    """Mais recente primeiro."""
    ws = _worksheet()
    valores = ws.get_all_values()
    if len(valores) <= 1:
        return []
    linhas = []
    for row in valores[1:]:
        row = row + [""] * (len(COLUNAS) - len(row))
        linhas.append({COLUNAS[j]: row[j] for j in range(len(COLUNAS))})
    linhas.reverse()
    return linhas[:limite]
