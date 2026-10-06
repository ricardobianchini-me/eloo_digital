"""
Prospecção ativa (outbound) no CRM de leads (/assessment/leads/crm, aba
"Prospecção"). Lê e grava a aba "Prospecção Clínicas Holísticas" da mesma
planilha do CRM (`leads.LEADS_SPREADSHEET_ID`).

As colunas são localizadas pelo nome do cabeçalho (a aba tem 31 colunas e
pode ganhar outras), nunca pela posição. Cada linha é identificada pelo
número real dela na planilha e conferida pelo nome da empresa antes de
gravar, para não escrever na linha errada se alguém ordenar a aba.
"""
import logging
import re

import gspread
from google.oauth2.service_account import Credentials

from config import settings
from leads import LEADS_SPREADSHEET_ID

logger = logging.getLogger(__name__)

ABA = "Prospecção Clínicas Holísticas"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

COL_EMPRESA = "Empresa / Clínica"

# Campos que a equipe comercial edita pela página.
CAMPOS_EDITAVEIS = {
    "Contato validado?", "Responsável/decisor", "Etapa do funil", "Último contato",
    "Próximo contato", "Resultado último contato", "Opt-out", "Observações comerciais",
}

OPCOES_VALIDACAO = ["Não — validar antes do envio", "Sim — validado", "Inválido — não usar"]
OPCOES_ETAPA = [
    "Novo", "Em contato", "Respondeu", "Diagnóstico enviado", "Conversa marcada",
    "Proposta enviada", "Ganho", "Em espera", "Perdido / Opt-out",
]
OPCOES_OPTOUT = ["", "Sim"]

_MAX_TEXTO = 2000
_DATA_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _worksheet():
    creds = Credentials.from_service_account_file(settings.google_credentials_file, scopes=SCOPES)
    return gspread.authorize(creds).open_by_key(LEADS_SPREADSHEET_ID).worksheet(ABA)


def _texto_seguro(valor: str) -> str:
    valor = (valor or "").strip()[:_MAX_TEXTO]
    if valor[:1] in ("=", "+", "-", "@"):
        valor = "'" + valor
    return valor


def _whatsapp(telefone: str) -> str:
    """Link wa.me a partir de um telefone brasileiro em qualquer formato."""
    digitos = re.sub(r"\D", "", telefone or "")
    if len(digitos) in (10, 11):
        digitos = "55" + digitos
    return f"https://wa.me/{digitos}" if len(digitos) >= 12 else ""


def _url(valor: str) -> str:
    valor = (valor or "").strip()
    if not valor:
        return ""
    if valor.startswith(("http://", "https://")):
        return valor
    return "https://" + valor.lstrip("/")


def _instagram(valor: str) -> str:
    valor = (valor or "").strip()
    if not valor:
        return ""
    if valor.startswith(("http://", "https://")):
        return valor
    return "https://www.instagram.com/" + valor.lstrip("@").strip("/") + "/"


def _data_iso(valor: str) -> str:
    """Data da planilha (dd/mm/aaaa ou aaaa-mm-dd) no formato do <input type=date>."""
    valor = (valor or "").strip()
    m = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", valor)
    if m:
        return f"{m[3]}-{m[2]}-{m[1]}"
    return valor if _DATA_ISO.match(valor) else ""


def listar() -> dict:
    """Prospects com os campos da planilha e os links prontos para a tela."""
    valores = _worksheet().get_all_values()
    if not valores:
        return {"prospects": [], "colunas": []}
    cab = valores[0]
    prospects = []
    for numero, row in enumerate(valores[1:], start=2):
        row = row + [""] * (len(cab) - len(row))
        item = {cab[j]: row[j] for j in range(len(cab))}
        if not item.get(COL_EMPRESA, "").strip():
            continue
        item["_row"] = numero
        item["_whatsapp"] = _whatsapp(item.get("Telefone comercial", ""))
        item["_site"] = _url(item.get("Site", ""))
        item["_instagram"] = _instagram(item.get("Instagram", ""))
        item["_email"] = (item.get("E-mail público", "") or "").strip()
        item["_busca_instagram"] = (item.get("Link de busca Instagram", "") or "").strip()
        item["_ultimo_iso"] = _data_iso(item.get("Último contato", ""))
        item["_proximo_iso"] = _data_iso(item.get("Próximo contato", ""))
        try:
            item["_score"] = int(float(item.get("Score comercial", "") or 0))
        except ValueError:
            item["_score"] = 0
        prospects.append(item)
    prospects.sort(key=lambda p: -p["_score"])
    return {"prospects": prospects, "colunas": cab}


def _validar(campo: str, valor: str) -> str:
    if campo not in CAMPOS_EDITAVEIS:
        raise ValueError(f"Campo não editável: {campo}")
    if campo in ("Último contato", "Próximo contato"):
        valor = (valor or "").strip()
        if valor and not _DATA_ISO.match(valor):
            raise ValueError("Data inválida")
        return valor
    return _texto_seguro(valor)


def atualizar(numero_linha: int, empresa: str, campo: str, valor: str) -> None:
    valor = _validar(campo, valor)
    if numero_linha < 2:
        raise ValueError("Linha inválida")
    ws = _worksheet()
    cab = ws.row_values(1)
    if campo not in cab or COL_EMPRESA not in cab:
        raise ValueError(f"Coluna não encontrada na planilha: {campo}")
    atual = ws.cell(numero_linha, cab.index(COL_EMPRESA) + 1).value or ""
    if atual.strip() != (empresa or "").strip():
        raise KeyError("A planilha mudou de ordem — atualize a página antes de editar")
    a1 = gspread.utils.rowcol_to_a1(numero_linha, cab.index(campo) + 1)
    ws.spreadsheet.values_update(f"'{ABA}'!{a1}", params={"valueInputOption": "USER_ENTERED"}, body={"values": [[valor]]})
    logger.info(f"Prospect linha {numero_linha} ({empresa}): {campo} = {valor!r}")
