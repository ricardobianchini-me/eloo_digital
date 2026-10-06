"""
Dashboard combinado do CRM de Leads — visão agregada dos dois fluxos (leads
inbound do site em `leads.py` e prospecção outbound em `prospeccao.py`).
Só leitura/agregação; nenhuma escrita acontece aqui.
"""
from collections import Counter
from datetime import datetime, timedelta

import prospeccao

DIAS_EVOLUCAO = 30

STATUS_SITE_OPCOES = ["Novo", "Em contato", "Qualificado", "Proposta enviada", "Ganho", "Perdido"]
STATUS_SITE_SLUG = {
    "Novo": "novo", "Em contato": "em-contato", "Qualificado": "qualificado",
    "Proposta enviada": "proposta-enviada", "Ganho": "ganho", "Perdido": "perdido",
}


def _parse_data_hora(valor: str):
    try:
        return datetime.strptime(valor, "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return None


def _leads_site_por_dia(registros: list[dict], dias: int = DIAS_EVOLUCAO) -> list[dict]:
    hoje = datetime.now().date()
    inicio = hoje - timedelta(days=dias - 1)
    contagem: Counter = Counter()
    for r in registros:
        dt = _parse_data_hora(r.get("Data/Hora", ""))
        if dt and dt.date() >= inicio:
            contagem[dt.date()] += 1
    serie = []
    for i in range(dias):
        dia = inicio + timedelta(days=i)
        serie.append({
            "data_curta": dia.strftime("%d/%m"),
            "data_completa": dia.strftime("%d/%m/%Y"),
            "total": contagem.get(dia, 0),
        })
    return serie


def construir_dashboard(leads_site: list[dict], leads_prospeccao: list[dict]) -> dict:
    """Agrega as duas listas já carregadas pela rota (evita ler as planilhas
    de novo — a rota unificada /assessment/leads/crm já busca as duas pra
    montar as abas de tabela)."""

    hoje = datetime.now().date()
    sete_dias_atras = hoje - timedelta(days=6)
    leads_site_7d = 0
    for r in leads_site:
        dt = _parse_data_hora(r.get("Data/Hora", ""))
        if dt and dt.date() >= sete_dias_atras:
            leads_site_7d += 1

    status_site = Counter(r.get("Status") or "Novo" for r in leads_site)
    status_site_lista = [(nome, status_site.get(nome, 0)) for nome in STATUS_SITE_OPCOES]
    max_status_site = max((c for _, c in status_site_lista), default=0) or 1

    etapa_prospeccao = Counter(r.get("Etapa do funil") or "Novo" for r in leads_prospeccao)
    etapas_prospeccao = [
        (nome, etapa_prospeccao.get(nome, 0), slug) for nome, slug in prospeccao.ETAPAS
    ]
    max_etapa_prospeccao = max((c for _, c, _ in etapas_prospeccao), default=0) or 1

    ganhos = etapa_prospeccao.get("Fechado — Ganho", 0)
    perdidos = etapa_prospeccao.get("Perdido / Opt-out", 0)
    novos = etapa_prospeccao.get("Novo", 0)
    em_andamento = len(leads_prospeccao) - novos - ganhos - perdidos

    prioridade_prospeccao = Counter(r.get("Prioridade comercial") or "—" for r in leads_prospeccao)
    prioridade_lista = [
        (nome, prioridade_prospeccao.get(nome, 0)) for nome in ["Alta", "Média", "Baixa"]
    ]

    categorias = Counter(r.get("Categoria") or "—" for r in leads_prospeccao)
    top_categorias = categorias.most_common(6)

    cidades = Counter(r.get("Cidade") or "—" for r in leads_prospeccao)
    top_cidades = cidades.most_common(6)

    serie_site = _leads_site_por_dia(leads_site)
    max_serie_site = max((d["total"] for d in serie_site), default=0) or 1

    return {
        "total_leads_site": len(leads_site),
        "leads_site_7d": leads_site_7d,
        "total_prospeccao": len(leads_prospeccao),
        "prospeccao_novos": novos,
        "prospeccao_em_andamento": em_andamento,
        "prospeccao_ganhos": ganhos,
        "prospeccao_perdidos": perdidos,
        "serie_site": serie_site,
        "max_serie_site": max_serie_site,
        "status_site_lista": status_site_lista,
        "status_site_slug": STATUS_SITE_SLUG,
        "max_status_site": max_status_site,
        "etapas_prospeccao": etapas_prospeccao,
        "max_etapa_prospeccao": max_etapa_prospeccao,
        "prioridade_prospeccao": prioridade_lista,
        "top_categorias": top_categorias,
        "top_cidades": top_cidades,
    }
