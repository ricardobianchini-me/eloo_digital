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


# Metadados do módulo (quem respondeu, quem apoiou) — vivem fora da tabela
# de perguntas, nas colunas K/L (a tabela usa só A-I), pra não interferir
# com `ler_linhas`/`COLUNAS`. K1/K2 são os rótulos (escritos na primeira
# gravação), L1/L2 os valores.
_META_CAMPOS = {
    "responsavel": {"linha": 1, "rotulo": "Responsável pelo módulo"},
    "apoio": {"linha": 2, "rotulo": "Quem apoiou nas respostas"},
}


def ler_metadados(spreadsheet_id: str, aba: str) -> dict[str, str]:
    ws = worksheet(spreadsheet_id, aba)
    valores = ws.get("K1:L2")
    resultado = {}
    for campo, info in _META_CAMPOS.items():
        i = info["linha"] - 1
        linha = valores[i] if i < len(valores) else []
        resultado[campo] = linha[1] if len(linha) > 1 else ""
    return resultado


def salvar_metadado(spreadsheet_id: str, aba: str, campo: str, valor: str) -> None:
    if campo not in _META_CAMPOS:
        raise ValueError(f"Metadado desconhecido: {campo}")
    info = _META_CAMPOS[campo]
    ws = worksheet(spreadsheet_id, aba)
    ws.update(f"K{info['linha']}:L{info['linha']}", [[info["rotulo"], valor]])
    logger.info(f"Atualizado {aba}!L{info['linha']} metadado={campo}")
