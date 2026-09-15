"""
Google Sheets — leitura e escrita das respostas de levantamento.
Uma aba por módulo (ver `modulos.py`), colunas fixas em `COLUNAS`.
"""
import logging
from typing import Any

import gspread
from google.oauth2.service_account import Credentials

from config import settings
from modulos import COLUNAS

logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

_COL_INDEX = {nome: i + 1 for i, nome in enumerate(COLUNAS)}  # 1-based, para gspread


def _cliente():
    creds = Credentials.from_service_account_file(
        settings.google_credentials_file, scopes=SCOPES
    )
    return gspread.authorize(creds)


def _planilha(spreadsheet_id: str):
    return _cliente().open_by_key(spreadsheet_id)


def worksheet(spreadsheet_id: str, aba: str):
    return _planilha(spreadsheet_id).worksheet(aba)


def ler_linhas(spreadsheet_id: str, aba: str) -> list[dict[str, Any]]:
    """Lê todas as linhas da aba (exceto cabeçalho), incluindo separadores de
    subtema (linhas cujo Ref começa com "## ") — o chamador decide como
    exibi-las. Cada linha ganha o campo interno "_row" com o número real da
    linha na planilha (1-based), necessário para updates pontuais.
    """
    ws = worksheet(spreadsheet_id, aba)
    valores = ws.get_all_values()
    if not valores:
        return []
    linhas = []
    for i, row in enumerate(valores[1:], start=2):  # pula cabeçalho
        row = row + [""] * (len(COLUNAS) - len(row))  # preenche colunas faltantes
        item = {COLUNAS[j]: row[j] for j in range(len(COLUNAS))}
        item["_row"] = i
        linhas.append(item)
    return linhas


def atualizar_campo(spreadsheet_id: str, aba: str, numero_linha: int, campo: str, valor: str) -> None:
    """Atualiza uma única célula (linha real da planilha, coluna pelo nome)."""
    if campo not in _COL_INDEX:
        raise ValueError(f"Campo desconhecido: {campo}")
    ws = worksheet(spreadsheet_id, aba)
    ws.update_cell(numero_linha, _COL_INDEX[campo], valor)
    logger.info(f"Atualizado {aba}!L{numero_linha} campo={campo}")
