"""
Script de configuração inicial da planilha de coleta — execute UMA VEZ por
novo cliente/engajamento, depois que o squad `assessment-ti` já gerou os 7
questionários (Fase 3) em `output/{run_id}/v1/questionario-*.md`.

Uso:
    python seed.py --cliente super-logistica --squad-dir "/caminho/para/output/2026-09-14-135322/v1" --criar "Assessment TI - Nome do Cliente"
    python seed.py --cliente super-logistica --squad-dir "..." --planilha-id 1AbC...   # reaproveita planilha existente
    python seed.py --cliente super-logistica --links-only                              # só reimprime os links de cada módulo

Requer GOOGLE_CREDENTIALS_FILE no .env. Depois de rodar, adicionar/conferir
a entrada do cliente em `clientes.py` (slug -> nome + spreadsheet_id) —
esse script não edita `clientes.py` sozinho, só imprime o que colar lá.
"""
import argparse
import os
import sys
from pathlib import Path

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv(Path(__file__).parent.parent / ".env")

from auth import PAPEL_ENTREVISTADO, PAPEL_REVISOR, gerar_token  # noqa: E402
from modulos import MODULOS  # noqa: E402
from seed_parser import parse_questionario  # noqa: E402

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def _cliente_gspread():
    credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE", "../credentials/credentials.json")
    creds = Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
    return gspread.authorize(creds)


def criar_ou_abrir_planilha(gc, criar_titulo: str | None, planilha_id: str | None):
    if criar_titulo:
        print(f"📄 Criando planilha '{criar_titulo}'...")
        sh = gc.create(criar_titulo)
        print(f"   ✓ Criada. ID: {sh.id}")
        return sh
    if planilha_id:
        print(f"📄 Abrindo planilha existente {planilha_id}...")
        return gc.open_by_key(planilha_id)
    raise SystemExit("Informe --criar '<título>' ou --planilha-id <id>")


def popular_modulo(sh, modulo: dict, linhas: list[list[str]]):
    aba = modulo["aba"]
    try:
        ws = sh.worksheet(aba)
        ws.clear()
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(aba, rows=max(len(linhas) + 5, 50), cols=len(linhas[0]) + 1)

    n_linhas_necessarias = len(linhas)
    if ws.row_count < n_linhas_necessarias:
        ws.add_rows(n_linhas_necessarias - ws.row_count)

    ultima_col = chr(ord("A") + len(linhas[0]) - 1)
    ws.update(f"A1:{ultima_col}{len(linhas)}", linhas, value_input_option="USER_ENTERED")

    ws.format(f"A1:{ultima_col}1", {
        "backgroundColor": {"red": 0.12, "green": 0.24, "blue": 0.36},
        "textFormat": {"foregroundColor": {"red": 1, "green": 1, "blue": 1}, "bold": True},
    })

    # Linhas de separador de subtema ("## ...") em destaque visual
    for i, linha in enumerate(linhas, start=1):
        if linha[0].startswith("## "):
            ws.format(f"A{i}:{ultima_col}{i}", {
                "backgroundColor": {"red": 0.89, "green": 0.91, "blue": 0.94},
                "textFormat": {"bold": True},
            })

    print(f"   ✓ {aba}: {len(linhas) - 1} linhas (perguntas + separadores de subtema)")


def imprimir_links(base_url: str, cliente: str):
    prefixo = f"{base_url}/assessment/{cliente}/responder"
    print(f"\n🔗 Links por módulo — NUNCA compartilhar o de revisor com o cliente:\n")
    for m in MODULOS:
        tok_e = gerar_token(cliente, m["id"], PAPEL_ENTREVISTADO)
        tok_r = gerar_token(cliente, m["id"], PAPEL_REVISOR)
        print(f"  {m['nome']}")
        print(f"    Entrevistado : {prefixo}/m/{m['id']}?token={tok_e}")
        print(f"    Revisor      : {prefixo}/m/{m['id']}?token={tok_r}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cliente", required=True, help="Slug do cliente (bate com a entrada em clientes.py), ex.: super-logistica")
    ap.add_argument("--squad-dir", help="Diretório com os questionario-*.md gerados pelo squad (Fase 3)")
    ap.add_argument("--criar", help="Título da nova planilha a criar")
    ap.add_argument("--planilha-id", help="ID de planilha existente a reaproveitar")
    ap.add_argument("--base-url", default="https://eloo.digital", help="URL pública onde a app está hospedada")
    ap.add_argument("--links-only", action="store_true", help="Só reimprime os links, sem tocar na planilha")
    args = ap.parse_args()

    if args.links_only:
        imprimir_links(args.base_url, args.cliente)
        return

    if not args.squad_dir:
        raise SystemExit("--squad-dir é obrigatório (a menos que use --links-only)")

    squad_dir = Path(args.squad_dir)
    if not squad_dir.is_dir():
        raise SystemExit(f"Diretório não encontrado: {squad_dir}")

    gc = _cliente_gspread()
    sh = criar_ou_abrir_planilha(gc, args.criar, args.planilha_id)

    print("\n📋 Populando módulos a partir dos questionários do squad...\n")
    for modulo in MODULOS:
        caminho = squad_dir / modulo["arquivo"]
        if not caminho.exists():
            print(f"   ⚠ {modulo['arquivo']} não encontrado — pulando {modulo['nome']}")
            continue
        linhas = parse_questionario(caminho)
        popular_modulo(sh, modulo, linhas)

    # Remove abas padrão vazias, se existirem
    for nome_padrao in ("Página1", "Sheet1"):
        try:
            sh.del_worksheet(sh.worksheet(nome_padrao))
        except Exception:
            pass

    print(f"\n✅ Planilha pronta: https://docs.google.com/spreadsheets/d/{sh.id}")
    print(f"\n📝 Adicione (ou confira) em clientes.py:")
    print(f'    "{args.cliente}": {{"nome": "<Nome do Cliente>", "spreadsheet_id": "{sh.id}"}},')
    imprimir_links(args.base_url, args.cliente)


if __name__ == "__main__":
    main()
