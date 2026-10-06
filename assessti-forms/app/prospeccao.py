"""
Leads de prospecção comercial outbound (cold leads carregados manualmente ou
por base externa) — aba separada "Prospecção Clínicas Holísticas" na mesma
planilha de `leads.py` (inbound do site), mas com schema próprio de 31
colunas (ver pacce-co/Base_Prospecção_Comercial_Clinicas_Holisticas_SP_v3.xlsx).
Só um subconjunto das colunas é editável pelo painel /assessment/leads/crm/prospeccao
— o resto é dado de pesquisa/qualificação, preenchido fora daqui.
"""
import logging

import gspread
from google.oauth2.service_account import Credentials

from config import settings
import historico

logger = logging.getLogger(__name__)

PROSPECCAO_SPREADSHEET_ID = "1GYZIKoAxpveCCWUv2QnyGBMdSUqvRtTLjzPKXIC5VTk"
PROSPECCAO_ABA = "Prospecção Clínicas Holísticas"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

COLUNAS = [
    "Empresa / Clínica", "Cidade", "Região", "Categoria", "Endereço",
    "Telefone comercial", "E-mail público", "Site", "Instagram",
    "Status CRM", "Prioridade comercial", "Fonte", "Observação / validação",
    "Tipo de Prospect", "Público-alvo provável", "Potencial para software",
    "Motivo do potencial", "Canal primário", "Canal secundário",
    "Contato validado?", "Data da validação", "Responsável/decisor",
    "Etapa do funil", "Último contato", "Próximo contato",
    "Resultado último contato", "Opt-out", "Score comercial",
    "Mensagem personalizada", "Link de busca Instagram", "Observações comerciais",
    "Canal de origem", "Pontuação", "Último sinal",
]

CAMPOS_CRM_EDITAVEIS = {
    "Etapa do funil", "Próximo contato", "Resultado último contato",
    "Responsável/decisor", "Observações comerciais",
    "Canal de origem", "Pontuação", "Último sinal",
}

CANAIS_ORIGEM = [
    "Instagram DM", "WhatsApp", "E-mail", "LinkedIn",
    "Indicação", "Google / Maps", "Site / Diagnóstico", "Evento", "Outro",
]

# (nome exibido/gravado na planilha, slug usado nas classes CSS .status-*)
ETAPAS = [
    ("Novo", "novo"),
    ("Contato validado", "contato-validado"),
    ("Abordagem enviada", "abordagem-enviada"),
    ("Em conversa", "em-conversa"),
    ("Diagnóstico agendado", "diagnostico-agendado"),
    ("Proposta enviada", "proposta-enviada"),
    ("Fechado — Ganho", "fechado-ganho"),
    ("Perdido / Opt-out", "perdido-opt-out"),
]
ETAPA_SLUG = {nome: slug for nome, slug in ETAPAS}

# Descrição curta de cada etapa, usada só na aba Leia-me do painel.
ETAPA_DESCRICOES = {
    "Novo": " — ainda não foi contatado.",
    "Contato validado": " — telefone/e-mail/Instagram conferidos, pronto pra abordagem.",
    "Abordagem enviada": " — primeira mensagem/ligação feita, aguardando resposta.",
    "Em conversa": " — respondeu e o diálogo está rolando.",
    "Diagnóstico agendado": " — marcou o Diagnóstico LUMEN ou uma conversa mais a fundo.",
    "Proposta enviada": " — já recebeu uma proposta formal.",
    "Fechado — Ganho": " — virou cliente.",
    "Perdido / Opt-out": " — não seguiu, ou pediu pra não ser mais contatado.",
}

# Campos oferecidos no formulário de "+ Novo lead" e aceitos na importação
# CSV (o resto das 31 colunas é dado de pesquisa/qualificação, preenchido
# fora daqui). "Empresa / Clínica" é o único obrigatório.
CAMPOS_CRIACAO = [
    "Empresa / Clínica", "Categoria", "Cidade", "Região", "Telefone comercial",
    "E-mail público", "Site", "Instagram", "Prioridade comercial", "Fonte",
    "Tipo de Prospect", "Responsável/decisor", "Etapa do funil",
    "Próximo contato", "Mensagem personalizada", "Observações comerciais",
    "Canal de origem", "Pontuação",
]

_COL_INDEX = {nome: i + 1 for i, nome in enumerate(COLUNAS)}  # 1-based, para gspread


def _cliente_gspread():
    creds = Credentials.from_service_account_file(
        settings.google_credentials_file, scopes=SCOPES
    )
    return gspread.authorize(creds)


def _worksheet():
    sh = _cliente_gspread().open_by_key(PROSPECCAO_SPREADSHEET_ID)
    return sh.worksheet(PROSPECCAO_ABA)


def listar_leads() -> list[dict[str, str]]:
    """Ordenado por Score comercial (maior primeiro), igual ao painel que já
    existia pra esses dados. Cada item ganha "_row" (linha real na planilha,
    1-based) pra viabilizar updates."""
    ws = _worksheet()
    valores = ws.get_all_values()
    if not valores:
        return []
    linhas = []
    for i, row in enumerate(valores[1:], start=2):  # pula cabeçalho
        row = row + [""] * (len(COLUNAS) - len(row))
        item = {COLUNAS[j]: row[j] for j in range(len(COLUNAS))}
        item["_row"] = i
        linhas.append(item)

    def _score(item):
        try:
            return int(item.get("Score comercial") or 0)
        except ValueError:
            return 0

    linhas.sort(key=_score, reverse=True)
    return linhas


def atualizar_campo_lead(numero_linha: int, campo: str, valor: str) -> None:
    if campo not in CAMPOS_CRM_EDITAVEIS:
        raise ValueError(f"Campo não editável pelo CRM: {campo}")
    ws = _worksheet()
    valor_anterior = ws.cell(numero_linha, _COL_INDEX[campo]).value or ""
    empresa = ws.cell(numero_linha, _COL_INDEX["Empresa / Clínica"]).value or ""
    ws.update_cell(numero_linha, _COL_INDEX[campo], valor)
    logger.info(f"Prospecção linha {numero_linha}: {campo} = {valor!r}")
    if valor_anterior != valor:
        historico.registrar("Prospecção", empresa, "Campo alterado", campo, valor_anterior, valor)


def _linha_de(dados: dict[str, str]) -> list[str]:
    linha = [str(dados.get(c, "") or "").strip() for c in COLUNAS]
    if not linha[_COL_INDEX["Status CRM"] - 1]:
        linha[_COL_INDEX["Status CRM"] - 1] = "Novo"
    if not linha[_COL_INDEX["Etapa do funil"] - 1]:
        linha[_COL_INDEX["Etapa do funil"] - 1] = "Novo"
    return linha


def criar_lead_manual(dados: dict[str, str]) -> dict[str, str]:
    """`dados` usa as mesmas chaves de COLUNAS (normalmente só as de
    CAMPOS_CRIACAO vêm preenchidas) — "Empresa / Clínica" obrigatório,
    validado na rota antes de chamar isto."""
    ws = _worksheet()
    linha = _linha_de(dados)
    ws.append_row(linha)
    empresa = linha[_COL_INDEX["Empresa / Clínica"] - 1]
    logger.info(f"Novo lead de prospecção: {empresa}")
    historico.registrar("Prospecção", empresa, "Criado")
    return dict(zip(COLUNAS, linha))


def importar_csv(linhas: list[dict[str, str]]) -> int:
    """`linhas`: dicts já mapeados pras chaves de COLUNAS pela rota (de-para
    do cabeçalho do CSV). Ignora silenciosamente qualquer linha sem
    "Empresa / Clínica". Retorna quantas linhas foram gravadas."""
    ws = _worksheet()
    gravadas = []
    for dados in linhas:
        if not (dados.get("Empresa / Clínica") or "").strip():
            continue
        gravadas.append(_linha_de(dados))
    if gravadas:
        ws.append_rows(gravadas)
        for linha in gravadas:
            historico.registrar("Prospecção", linha[_COL_INDEX["Empresa / Clínica"] - 1], "Criado (CSV)")
    logger.info(f"Importação CSV de prospecção: {len(gravadas)} lead(s) gravados")
    return len(gravadas)
