"""
Formulário de contato público da landing page (eloo.digital) — grava leads
numa planilha própria (Google Sheets), separada da(s) planilha(s) de coleta
de clientes ativos (ver `clientes.py`). Não é secret (mesma lógica de
`clientes.py`: o ID por si só não dá acesso a nada — quem protege é a
credencial da conta de serviço, que só o servidor tem).

Além dos campos preenchidos pelo visitante, a planilha tem 3 colunas de
CRM básico (Status, Próximo Retorno, Notas Internas), editadas só pela
página oculta /assessment/leads/crm (ver leads_crm_auth.py) — nunca pelo
formulário público.
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

# Colunas preenchidas pelo visitante no formulário público, seguidas das
# colunas de gestão interna (CRM), preenchidas só pela equipe.
COLUNAS = [
    "Data/Hora", "Nome", "Instituição", "Cargo", "E-mail", "WhatsApp",
    "Interesse", "Origem", "Urgência", "Mensagem",
    "Status", "Próximo Retorno", "Notas Internas",
]

STATUS_PADRAO = "Novo"
CAMPOS_CRM_EDITAVEIS = {"Status", "Próximo Retorno", "Notas Internas"}

_COL_INDEX = {nome: i + 1 for i, nome in enumerate(COLUNAS)}  # 1-based, para gspread


def _cliente_gspread():
    creds = Credentials.from_service_account_file(
        settings.google_credentials_file, scopes=SCOPES
    )
    return gspread.authorize(creds)


def _worksheet():
    sh = _cliente_gspread().open_by_key(LEADS_SPREADSHEET_ID)
    try:
        ws = sh.worksheet(LEADS_ABA)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(LEADS_ABA, rows=200, cols=len(COLUNAS))
        ws.append_row(COLUNAS)
        return ws

    # A aba já existia antes das colunas de CRM serem adicionadas — conserta
    # só o cabeçalho (linha 1) pro nome novo de colunas, sem tocar em
    # nenhuma linha de dado já gravada (não sabemos o suficiente pra
    # remapear dado antigo com segurança; melhor deixar visível/manual).
    cabecalho_atual = ws.row_values(1)
    if cabecalho_atual != COLUNAS:
        ws.update("A1", [COLUNAS])
        logger.warning(
            "Cabeçalho da aba 'Leads' estava desatualizado — corrigido para o novo "
            "conjunto de colunas. Linhas gravadas antes desta mudança não foram "
            "remapeadas automaticamente."
        )
    return ws


def salvar_lead(
    nome: str, instituicao: str, cargo: str, email: str, whatsapp: str,
    interesse: str, origem: str, urgencia: str, mensagem: str,
) -> dict[str, str]:
    ws = _worksheet()
    agora = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")
    linha = [
        agora, nome, instituicao, cargo, email, whatsapp,
        interesse, origem, urgencia, mensagem,
        STATUS_PADRAO, "", "",
    ]
    ws.append_row(linha)
    logger.info(f"Novo lead salvo: {nome} ({instituicao})")
    return dict(zip(COLUNAS, linha))


def listar_leads() -> list[dict[str, str]]:
    """Mais recente primeiro. Cada item ganha o campo interno "_row" com o
    número real da linha na planilha (1-based), necessário para updates."""
    ws = _worksheet()
    valores = ws.get_all_values()
    if not valores:
        return []
    linhas = []
    for i, row in enumerate(valores[1:], start=2):  # pula cabeçalho
        row = row + [""] * (len(COLUNAS) - len(row))  # preenche colunas faltantes
        item = {COLUNAS[j]: row[j] for j in range(len(COLUNAS))}
        item["_row"] = i
        linhas.append(item)
    linhas.reverse()
    return linhas


def atualizar_campo_lead(numero_linha: int, campo: str, valor: str) -> None:
    if campo not in CAMPOS_CRM_EDITAVEIS:
        raise ValueError(f"Campo não editável pelo CRM: {campo}")
    ws = _worksheet()
    ws.update_cell(numero_linha, _COL_INDEX[campo], valor)
    logger.info(f"Lead linha {numero_linha}: {campo} = {valor!r}")
