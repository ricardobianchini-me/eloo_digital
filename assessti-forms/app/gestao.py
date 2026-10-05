"""
Página de gestão da empresa (/assessment/leads/gestao) — roadmap, metas,
funil, visão e decisões dos sócios, lidos e gravados na mesma planilha do
CRM de leads ("eloo.digital — CRM e Plano", ver `leads.LEADS_SPREADSHEET_ID`).

A planilha continua sendo a fonte de verdade: a aba "Painel" dela calcula as
mesmas métricas por fórmula, e quem preferir pode editar direto por lá. Esta
página só oferece uma visão de gestão mais rápida e edição sem abrir o Sheets.

Abas usadas (cabeçalho na linha 1):
- "Roadmap Q4": ID | Área | Item | Dono | Mês | Prazo | Status | Nota | Atualizado em | Atualizado por
- "Metas Q4":   Objetivo | Resultado-chave | Meta | Atual | Dono | Prazo
- "Visão":      Bloco | Conteúdo | Detalhe
- "Nichos":     Nicho | Exemplos | Dor principal | Entrada | Oferta núcleo | Canal | Status
- "Decisões":   Data | Decisão | Quem decidiu | Impacto
- "Leads" e "Prospecção Clínicas Holísticas": só leitura, para o funil.

Linhas do roadmap são localizadas pelo ID (coluna A), nunca pelo número de
linha vindo do navegador — alguém pode ter ordenado ou inserido linhas na
planilha entre o carregamento da página e o salvamento.
"""
import logging
import re
import secrets
from datetime import date, datetime, timedelta, timezone

import gspread
from google.oauth2.service_account import Credentials

from config import settings
from leads import LEADS_SPREADSHEET_ID

logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

ABA_ROADMAP = "Roadmap Q4"
ABA_METAS = "Metas Q4"
ABA_VISAO = "Visão"
ABA_NICHOS = "Nichos"
ABA_DECISOES = "Decisões"
ABA_LEADS = "Leads"
ABA_PROSPECCAO = "Prospecção Clínicas Holísticas"

COLUNAS_ROADMAP = ["ID", "Área", "Item", "Dono", "Mês", "Prazo", "Status", "Nota", "Atualizado em", "Atualizado por"]
COLUNAS_METAS = ["Objetivo", "Resultado-chave", "Meta", "Atual", "Dono", "Prazo"]
COLUNAS_DECISOES = ["Data", "Decisão", "Quem decidiu", "Impacto"]

AREAS = [
    "Vendas em andamento", "Estratégia de mkt e vendas", "Site", "Redes sociais",
    "Leads e funil", "Apresentações", "Produtos por nicho", "Segurança e DevSecOps",
    "Contratos", "Gestão",
]
DONOS = ["Ricardo", "Alessandro", "Rafael", "Todos"]
MESES = ["Out", "Nov", "Dez"]
STATUS = ["A fazer", "Em andamento", "Bloqueado", "Feito"]

# Campos do roadmap que a página pode alterar, com a regra de cada um.
CAMPOS_ROADMAP_EDITAVEIS = {"Item", "Dono", "Mês", "Prazo", "Status", "Nota", "Área"}
_LISTAS = {"Dono": DONOS, "Mês": MESES, "Status": STATUS, "Área": AREAS}
_MAX_TEXTO = 2000

_COL_ROADMAP = {nome: i + 1 for i, nome in enumerate(COLUNAS_ROADMAP)}  # 1-based
_DATA_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ---------------------------------------------------------------- acesso

def _planilha():
    creds = Credentials.from_service_account_file(settings.google_credentials_file, scopes=SCOPES)
    return gspread.authorize(creds).open_by_key(LEADS_SPREADSHEET_ID)


def _como_linhas(valores: list[list[str]], colunas: list[str]) -> list[dict]:
    """Converte valores brutos (com cabeçalho) em dicts pelas colunas
    esperadas, ignorando linhas totalmente vazias."""
    linhas = []
    for row in valores[1:]:
        row = row + [""] * (len(colunas) - len(row))
        if not any(c.strip() for c in row[: len(colunas)]):
            continue
        linhas.append({colunas[j]: row[j] for j in range(len(colunas))})
    return linhas


def _texto_seguro(valor: str) -> str:
    """Evita que texto digitado vire fórmula na planilha (gravação é
    USER_ENTERED para datas virarem data de verdade)."""
    valor = (valor or "").strip()[:_MAX_TEXTO]
    if valor[:1] in ("=", "+", "-", "@"):
        valor = "'" + valor
    return valor


def _gravar(sh, aba: str, a1: str, valores: list[list[str]]) -> None:
    sh.values_update(
        f"'{aba}'!{a1}",
        params={"valueInputOption": "USER_ENTERED"},
        body={"values": valores},
    )


def _hoje() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")


def _parse_data(valor: str) -> date | None:
    valor = (valor or "").strip()
    for formato in ("%d/%m/%Y", "%Y-%m-%d", "%d/%m/%y"):
        try:
            return datetime.strptime(valor, formato).date()
        except ValueError:
            continue
    return None


# ---------------------------------------------------------------- leitura

def carregar() -> dict:
    """Lê todas as abas de uma vez (uma chamada à API) e devolve os dados
    prontos para a página, já com as métricas calculadas."""
    sh = _planilha()
    abas = [ABA_ROADMAP, ABA_METAS, ABA_VISAO, ABA_NICHOS, ABA_DECISOES, ABA_LEADS, ABA_PROSPECCAO]
    resposta = sh.values_batch_get([f"'{a}'" for a in abas])
    brutos = {a: r.get("values", []) for a, r in zip(abas, resposta.get("valueRanges", []))}

    roadmap = _como_linhas(brutos[ABA_ROADMAP], COLUNAS_ROADMAP)
    hoje = datetime.now(timezone.utc).astimezone().date()
    for item in roadmap:
        prazo = _parse_data(item["Prazo"])
        item["_prazo_iso"] = prazo.isoformat() if prazo else ""
        item["_prazo_curto"] = prazo.strftime("%d/%m") if prazo else item["Prazo"]
        # Ordem na tela: feitos por último, depois por prazo (sem prazo no fim).
        item["_ordem"] = ("1" if item["Status"] == "Feito" else "0") + (item["_prazo_iso"] or "9999")
        aberto = item["Status"] != "Feito"
        item["_atrasado"] = bool(prazo and aberto and prazo < hoje)
        item["_vence_7d"] = bool(prazo and aberto and hoje <= prazo <= hoje + timedelta(days=7))

    valores_visao = _como_linhas(brutos[ABA_VISAO], ["Bloco", "Conteúdo", "Detalhe"])
    nichos = _como_linhas(
        brutos[ABA_NICHOS],
        ["Nicho", "Exemplos", "Dor principal", "Entrada", "Oferta núcleo", "Canal", "Status"],
    )
    decisoes = _como_linhas(brutos[ABA_DECISOES], COLUNAS_DECISOES)
    decisoes.sort(key=lambda d: _parse_data(d["Data"]) or date.min, reverse=True)

    metas = []
    for i, row in enumerate(brutos[ABA_METAS][1:], start=2):
        row = row + [""] * (len(COLUNAS_METAS) - len(row))
        if not any(c.strip() for c in row[: len(COLUNAS_METAS)]):
            continue
        meta = {COLUNAS_METAS[j]: row[j] for j in range(len(COLUNAS_METAS))}
        meta["_row"] = i
        metas.append(meta)

    return {
        "roadmap": roadmap,
        "metas": metas,
        "visao": valores_visao,
        "nichos": nichos,
        "decisoes": decisoes,
        "metricas": _metricas(roadmap),
        "funil": _funil(brutos[ABA_LEADS], brutos[ABA_PROSPECCAO], hoje),
        "hoje": hoje.strftime("%d/%m/%Y"),
        "areas": AREAS, "donos": DONOS, "meses": MESES, "status": STATUS,
    }


def _contagem(itens: list[dict]) -> dict:
    total = len(itens)
    feitos = sum(1 for i in itens if i["Status"] == "Feito")
    return {
        "total": total,
        "feito": feitos,
        "andamento": sum(1 for i in itens if i["Status"] == "Em andamento"),
        "bloqueado": sum(1 for i in itens if i["Status"] == "Bloqueado"),
        "afazer": sum(1 for i in itens if i["Status"] == "A fazer"),
        "atrasados": sum(1 for i in itens if i["_atrasado"]),
        "pct": round(100 * feitos / total) if total else 0,
    }


def _metricas(roadmap: list[dict]) -> dict:
    return {
        "geral": {**_contagem(roadmap), "vence_7d": sum(1 for i in roadmap if i["_vence_7d"])},
        "por_dono": [{"nome": d, **_contagem([i for i in roadmap if i["Dono"] == d])} for d in DONOS],
        "por_area": [{"nome": a, **_contagem([i for i in roadmap if i["Área"] == a])} for a in AREAS],
        "por_mes": [{"nome": m, **_contagem([i for i in roadmap if i["Mês"] == m])} for m in MESES],
        "atrasados": sorted([i for i in roadmap if i["_atrasado"]], key=lambda i: i["_prazo_iso"]),
        "vence_7d": sorted([i for i in roadmap if i["_vence_7d"]], key=lambda i: i["_prazo_iso"]),
        "bloqueados": [i for i in roadmap if i["Status"] == "Bloqueado"],
    }


def _funil(leads: list[list[str]], prospeccao: list[list[str]], hoje: date) -> dict:
    """Números do topo de funil. Na aba de prospecção, as colunas usadas
    são localizadas pelo nome do cabeçalho (a aba tem 31 colunas)."""
    cab = prospeccao[0] if prospeccao else []
    linhas = [r for r in prospeccao[1:] if r and r[0].strip()]

    def col(nome: str) -> int | None:
        return cab.index(nome) if nome in cab else None

    def valor(r: list[str], idx: int | None) -> str:
        return r[idx].strip() if idx is not None and idx < len(r) else ""

    c_valid, c_etapa = col("Contato validado?"), col("Etapa do funil")
    c_ultimo, c_prox, c_opt = col("Último contato"), col("Próximo contato"), col("Opt-out")

    etapas: dict[str, int] = {}
    for r in linhas:
        etapa = valor(r, c_etapa) or "Sem etapa"
        etapas[etapa] = etapas.get(etapa, 0) + 1

    vencidos = 0
    for r in linhas:
        prox = _parse_data(valor(r, c_prox))
        if prox and prox < hoje:
            vencidos += 1

    leads_linhas = [r for r in leads[1:] if r and r[0].strip()]
    return {
        "prospects": len(linhas),
        "validados": sum(1 for r in linhas if valor(r, c_valid).lower().startswith("sim")),
        "contatados": sum(1 for r in linhas if valor(r, c_ultimo)),
        "proximo_vencido": vencidos,
        "optout": sum(1 for r in linhas if valor(r, c_opt).lower().startswith("sim")),
        "leads_site": len(leads_linhas),
        "diagnosticos": sum(1 for r in leads_linhas if len(r) > 10 and r[10].strip()),
        "etapas": sorted(etapas.items(), key=lambda kv: -kv[1]),
    }


# ---------------------------------------------------------------- escrita

def _linha_do_item(ws, item_id: str) -> int:
    ids = ws.col_values(1)
    for i, valor in enumerate(ids, start=1):
        if i > 1 and valor == item_id:
            return i
    raise KeyError(item_id)


def _validar(campo: str, valor: str) -> str:
    if campo not in CAMPOS_ROADMAP_EDITAVEIS:
        raise ValueError(f"Campo não editável: {campo}")
    if campo in _LISTAS:
        if valor not in _LISTAS[campo]:
            raise ValueError(f"Valor inválido para {campo}")
        return valor
    if campo == "Prazo":
        valor = (valor or "").strip()
        if valor and not _DATA_ISO.match(valor):
            raise ValueError("Prazo deve ser uma data (AAAA-MM-DD) ou vazio")
        return valor
    if campo == "Item" and not (valor or "").strip():
        raise ValueError("O item precisa de um título")
    return _texto_seguro(valor)


def atualizar_item(item_id: str, campo: str, valor: str, quem: str) -> None:
    valor = _validar(campo, valor)
    sh = _planilha()
    ws = sh.worksheet(ABA_ROADMAP)
    linha = _linha_do_item(ws, item_id)
    col = _COL_ROADMAP[campo]
    _gravar(sh, ABA_ROADMAP, gspread.utils.rowcol_to_a1(linha, col), [[valor]])
    _gravar(sh, ABA_ROADMAP, f"I{linha}:J{linha}", [[_hoje(), _quem(quem)]])
    logger.info(f"Roadmap {item_id}: {campo} = {valor!r} ({quem})")


def novo_item(area: str, item: str, dono: str, mes: str, prazo: str, quem: str) -> str:
    area, dono, mes = _validar("Área", area), _validar("Dono", dono), _validar("Mês", mes)
    item, prazo = _validar("Item", item), _validar("Prazo", prazo)
    item_id = "nv-" + secrets.token_hex(3)
    sh = _planilha()
    ws = sh.worksheet(ABA_ROADMAP)
    ws.append_row(
        [item_id, area, item, dono, mes, prazo, "A fazer", "", _hoje(), _quem(quem)],
        value_input_option="USER_ENTERED",
        table_range="A1",
    )
    logger.info(f"Roadmap novo item {item_id}: {item!r} ({quem})")
    return item_id


def atualizar_meta_atual(numero_linha: int, valor: str) -> None:
    if numero_linha < 2:
        raise ValueError("Linha inválida")
    sh = _planilha()
    _gravar(sh, ABA_METAS, f"D{numero_linha}", [[_texto_seguro(valor)]])
    logger.info(f"Meta linha {numero_linha}: Atual = {valor!r}")


def nova_decisao(decisao: str, quem_decidiu: str, impacto: str) -> None:
    decisao = _texto_seguro(decisao)
    if not decisao:
        raise ValueError("Descreva a decisão")
    sh = _planilha()
    sh.worksheet(ABA_DECISOES).append_row(
        [_hoje(), decisao, _texto_seguro(quem_decidiu), _texto_seguro(impacto)],
        value_input_option="USER_ENTERED",
        table_range="A1",
    )
    logger.info(f"Nova decisão registrada por {quem_decidiu!r}")


def _quem(quem: str) -> str:
    return quem if quem in DONOS else ""
