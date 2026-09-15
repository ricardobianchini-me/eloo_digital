import logging
from pathlib import Path

from fastapi import APIRouter, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from auth import PAPEL_REVISOR, validar_token
from clientes import get_cliente
from modulos import CAMPOS_ENTREVISTADO, CAMPOS_REVISOR, COL_STATUS, MODULOS_POR_ID
import sheets as sheets_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent

# Rota fixa e compartilhada por todos os clientes, com "responder/" no meio
# pra bater com o mesmo location regex do nginx do host que já cobre
# /assessment/{cliente}/responder/ — assim nenhum client novo exige editar
# o nginx de novo, e estáticos/saúde também não precisam de location à parte.
STATIC_PATH = "/assessment/_shared/responder/static"

app = FastAPI(title="eloo Assessment")
app.mount(STATIC_PATH, StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
templates.env.globals["static_path"] = STATIC_PATH

router = APIRouter(prefix="/assessment/{cliente}/responder")


def _campos_permitidos(papel: str) -> set[str]:
    return CAMPOS_REVISOR if papel == PAPEL_REVISOR else CAMPOS_ENTREVISTADO


def _agrupar_por_subtema(linhas: list[dict]) -> list[dict]:
    """Transforma a lista plana de linhas em [{titulo, perguntas: [...]}, ...],
    usando as linhas separadoras ("## Subtema") como fronteira.
    """
    grupos: list[dict] = []
    atual = {"titulo": "Geral", "perguntas": []}
    for linha in linhas:
        ref = linha.get("Ref", "")
        if ref.startswith("## "):
            if atual["perguntas"]:
                grupos.append(atual)
            atual = {"titulo": ref[3:], "perguntas": []}
            continue
        if not ref:
            continue
        atual["perguntas"].append(linha)
    if atual["perguntas"]:
        grupos.append(atual)
    return grupos


def _cliente_ou_404(cliente: str) -> dict:
    dados = get_cliente(cliente)
    if not dados:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return dados


@router.get("/m/{modulo_id}", response_class=HTMLResponse)
def formulario(request: Request, cliente: str, modulo_id: str, token: str = ""):
    dados_cliente = _cliente_ou_404(cliente)
    modulo = MODULOS_POR_ID.get(modulo_id)
    if not modulo:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")

    papel = validar_token(cliente, modulo_id, token)
    if not papel:
        return templates.TemplateResponse(
            "sem_acesso.html", {"request": request}, status_code=403
        )

    try:
        linhas = sheets_client.ler_linhas(dados_cliente["spreadsheet_id"], modulo["aba"])
    except Exception:
        logger.exception("Falha ao ler a planilha")
        return templates.TemplateResponse(
            "erro.html",
            {"request": request, "mensagem": "Não foi possível carregar as perguntas agora. Tente novamente em instantes."},
            status_code=502,
        )

    grupos = _agrupar_por_subtema(linhas)
    total = sum(len(g["perguntas"]) for g in grupos)
    respondidas = sum(
        1 for g in grupos for p in g["perguntas"] if p.get("Resposta do Entrevistado", "").strip()
    )

    return templates.TemplateResponse(
        "modulo.html",
        {
            "request": request,
            "cliente": cliente,
            "cliente_nome": dados_cliente["nome"],
            "modulo": modulo,
            "token": token,
            "papel": papel,
            "pode_revisar": papel == PAPEL_REVISOR,
            "grupos": grupos,
            "total": total,
            "respondidas": respondidas,
        },
    )


@router.post("/m/{modulo_id}/salvar")
async def salvar_campo(
    cliente: str,
    modulo_id: str,
    token: str = Form(...),
    linha: int = Form(...),
    campo: str = Form(...),
    valor: str = Form(""),
):
    dados_cliente = _cliente_ou_404(cliente)
    modulo = MODULOS_POR_ID.get(modulo_id)
    if not modulo:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")

    papel = validar_token(cliente, modulo_id, token)
    if not papel:
        raise HTTPException(status_code=403, detail="Token inválido para este módulo")

    if campo not in _campos_permitidos(papel):
        raise HTTPException(status_code=403, detail="Seu link não permite editar este campo")

    try:
        sheets_client.atualizar_campo(dados_cliente["spreadsheet_id"], modulo["aba"], linha, campo, valor)
    except Exception:
        logger.exception("Falha ao salvar campo")
        raise HTTPException(status_code=502, detail="Não foi possível salvar agora — tente novamente")

    return JSONResponse({"ok": True})


@router.post("/m/{modulo_id}/status")
async def marcar_status(cliente: str, modulo_id: str, token: str = Form(...), linha: int = Form(...), status: str = Form(...)):
    dados_cliente = _cliente_ou_404(cliente)
    modulo = MODULOS_POR_ID.get(modulo_id)
    if not modulo:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")

    papel = validar_token(cliente, modulo_id, token)
    if papel != PAPEL_REVISOR:
        raise HTTPException(status_code=403, detail="Só o link de revisor pode alterar o status")

    try:
        sheets_client.atualizar_campo(dados_cliente["spreadsheet_id"], modulo["aba"], linha, COL_STATUS, status)
    except Exception:
        logger.exception("Falha ao salvar status")
        raise HTTPException(status_code=502, detail="Não foi possível salvar agora — tente novamente")

    return JSONResponse({"ok": True})


@router.get("/", response_class=HTMLResponse)
def raiz(request: Request, cliente: str):
    _cliente_ou_404(cliente)
    return templates.TemplateResponse("sem_acesso.html", {"request": request}, status_code=200)


@app.get("/assessment/_shared/responder/saude")
def saude():
    return {"status": "ok"}


app.include_router(router)
