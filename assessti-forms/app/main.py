import logging
from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from auth import PAPEL_REVISOR, gerar_token, validar_token
from clientes import get_cliente
import leads
import leads_crm_auth
import leads_notify
from modulos import CAMPOS_ENTREVISTADO, CAMPOS_REVISOR, COL_STATUS, MODULOS_POR_ID
import pin_auth
import portal_auth
import sheets as sheets_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent

# Rota fixa e compartilhada por todos os clientes, com "responder/" no meio
# pra bater com o mesmo location regex do nginx do host que já cobre
# /assessment/{cliente}/responder/ — assim nenhum client novo exige editar
# o nginx de novo, e estáticos/saúde também não precisam de location à parte.
STATIC_PATH = "/assessment/_shared/responder/static"
LOGIN_PATH = "/assessment/_shared/responder/entrar"
LEADS_CRM_LOGIN_PATH = "/assessment/leads/crm/entrar"

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


def _autenticado(request: Request) -> bool:
    return pin_auth.cookie_valido(request.cookies.get(pin_auth.COOKIE_NOME))


def _exigir_pin_ou_redirecionar(request: Request) -> RedirectResponse | None:
    """Pra rotas GET: se não estiver logado, manda pra tela de PIN, com
    ?next=<url original> pra voltar direto pra onde a pessoa queria ir."""
    if _autenticado(request):
        return None
    destino = quote(str(request.url.path) + (f"?{request.url.query}" if request.url.query else ""))
    return RedirectResponse(url=f"{LOGIN_PATH}?next={destino}")


@app.get("/assessment/_shared/responder/entrar", response_class=HTMLResponse)
def tela_login(request: Request, next: str = "/assessment/_shared/responder/saude", erro: bool = False):
    return templates.TemplateResponse("entrar.html", {"request": request, "next": next, "erro": erro})


@app.post("/assessment/_shared/responder/entrar")
def processar_login(pin: str = Form(...), next: str = Form("/assessment/_shared/responder/saude")):
    if not pin_auth.pin_correto(pin):
        return RedirectResponse(
            url=f"{LOGIN_PATH}?erro=1&next={quote(next)}", status_code=303
        )
    resposta = RedirectResponse(url=next, status_code=303)
    resposta.set_cookie(
        pin_auth.COOKIE_NOME,
        pin_auth.valor_cookie(),
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=60 * 60 * 12,  # 12h — dura uma sessão de trabalho, não precisa logar de novo entre módulos
    )
    return resposta


# Portal do cliente (proposta, status, questionários publicados em
# eloo.digital/assessment/{cliente}/) — PIN por cliente (clientes.py,
# campo portal_pin), mesmo padrão de UX do PIN interno acima, no lugar do
# HTTP Basic Auth do nginx. O gate em si roda no nginx via auth_request
# contra o endpoint /portal/check abaixo (ver hlera-bot/nginx/vm2-apps/eloo-digital).
@app.get("/assessment/{cliente}/portal/entrar", response_class=HTMLResponse)
def portal_tela_login(request: Request, cliente: str, next: str = "", erro: bool = False):
    dados = _cliente_ou_404(cliente)
    destino = next or f"/assessment/{cliente}/"
    return templates.TemplateResponse(
        "portal_entrar.html",
        {"request": request, "cliente": cliente, "nome_cliente": dados["nome"], "next": destino, "erro": erro},
    )


@app.post("/assessment/{cliente}/portal/entrar")
def portal_processar_login(cliente: str, pin: str = Form(...), next: str = Form("")):
    dados = _cliente_ou_404(cliente)
    destino = next or f"/assessment/{cliente}/"
    if not portal_auth.pin_correto(dados, pin):
        return RedirectResponse(
            url=f"/assessment/{cliente}/portal/entrar?erro=1&next={quote(destino)}", status_code=303
        )
    resposta = RedirectResponse(url=destino, status_code=303)
    resposta.set_cookie(
        portal_auth.cookie_nome(cliente),
        portal_auth.valor_cookie(cliente),
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=60 * 60 * 24 * 30,  # 30 dias — engajamento dura meses, não precisa logar toda visita
    )
    return resposta


@app.get("/assessment/{cliente}/portal/check")
def portal_check(request: Request, cliente: str):
    """Alvo do auth_request do nginx — 200 destranca, 401 manda pro login."""
    dados = get_cliente(cliente)
    if not dados:
        raise HTTPException(status_code=404)
    valor = request.cookies.get(portal_auth.cookie_nome(cliente))
    if not portal_auth.cookie_valido(cliente, valor):
        raise HTTPException(status_code=401)
    return {"ok": True}


@router.get("/m/{modulo_id}", response_class=HTMLResponse)
def formulario(request: Request, cliente: str, modulo_id: str, token: str = ""):
    redir = _exigir_pin_ou_redirecionar(request)
    if redir:
        return redir

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

    try:
        metadados = sheets_client.ler_metadados(dados_cliente["spreadsheet_id"], modulo["aba"])
    except Exception:
        logger.exception("Falha ao ler metadados do módulo")
        metadados = {"responsavel": "", "apoio": ""}

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
            "metadados": metadados,
        },
    )


@router.post("/m/{modulo_id}/salvar")
async def salvar_campo(
    request: Request,
    cliente: str,
    modulo_id: str,
    token: str = Form(...),
    linha: int = Form(...),
    campo: str = Form(...),
    valor: str = Form(""),
):
    if not _autenticado(request):
        raise HTTPException(status_code=401, detail="Sessão interna expirada — atualize a página e faça login de novo")

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


@router.post("/m/{modulo_id}/metadado")
async def salvar_metadado(
    request: Request,
    cliente: str,
    modulo_id: str,
    token: str = Form(...),
    campo: str = Form(...),
    valor: str = Form(""),
):
    """Quem respondeu (responsável) e quem apoiou nas respostas — identificação
    do lado do cliente por módulo, gravada direto na planilha (colunas K/L,
    fora da tabela de perguntas)."""
    if not _autenticado(request):
        raise HTTPException(status_code=401, detail="Sessão interna expirada — atualize a página e faça login de novo")

    dados_cliente = _cliente_ou_404(cliente)
    modulo = MODULOS_POR_ID.get(modulo_id)
    if not modulo:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")

    if not validar_token(cliente, modulo_id, token):
        raise HTTPException(status_code=403, detail="Token inválido para este módulo")

    if campo not in ("responsavel", "apoio"):
        raise HTTPException(status_code=400, detail="Campo inválido")

    try:
        sheets_client.salvar_metadado(dados_cliente["spreadsheet_id"], modulo["aba"], campo, valor)
    except Exception:
        logger.exception("Falha ao salvar metadado")
        raise HTTPException(status_code=502, detail="Não foi possível salvar agora — tente novamente")

    return JSONResponse({"ok": True})


@router.post("/m/{modulo_id}/status")
async def marcar_status(request: Request, cliente: str, modulo_id: str, token: str = Form(...), linha: int = Form(...), status: str = Form(...)):
    if not _autenticado(request):
        raise HTTPException(status_code=401, detail="Sessão interna expirada — atualize a página e faça login de novo")

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


@router.get("/quem-respondeu")
async def quem_respondeu(cliente: str):
    """Endpoint público (sem PIN, sem token) — devolve só o nome do
    responsável cadastrado por módulo, pro painel público do cliente
    mostrar sem duplicar/desincronizar esse dado do formulário. Nunca
    expõe token, resposta de pergunta nem qualquer outro campo."""
    dados_cliente = _cliente_ou_404(cliente)
    resultado: dict[str, str] = {}
    for modulo_id, modulo in MODULOS_POR_ID.items():
        try:
            meta = sheets_client.ler_metadados(dados_cliente["spreadsheet_id"], modulo["aba"])
            resultado[modulo_id] = meta.get("responsavel", "")
        except Exception:
            logger.exception(f"Falha ao ler responsável do módulo {modulo_id}")
            resultado[modulo_id] = ""
    return JSONResponse(resultado)


@router.get("/", response_class=HTMLResponse)
def raiz(request: Request, cliente: str):
    redir = _exigir_pin_ou_redirecionar(request)
    if redir:
        return redir
    _cliente_ou_404(cliente)
    return templates.TemplateResponse("sem_acesso.html", {"request": request}, status_code=200)


@router.get("/ir/{modulo_id}")
def ir_para_modulo(request: Request, cliente: str, modulo_id: str):
    """Atalho de uso interno: gera o token de revisor na hora e redireciona
    pro formulário — assim o link "Responder ao vivo" do painel do cliente
    nunca precisa ter um token gravado em nenhum arquivo/página estática
    (o token só existe em memória, gerado a partir do SECRET_KEY do
    ambiente, nunca commitado). Pede o PIN interno antes de gerar o token.
    """
    redir = _exigir_pin_ou_redirecionar(request)
    if redir:
        return redir
    _cliente_ou_404(cliente)
    if modulo_id not in MODULOS_POR_ID:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")
    token = gerar_token(cliente, modulo_id, PAPEL_REVISOR)
    return RedirectResponse(url=f"/assessment/{cliente}/responder/m/{modulo_id}?token={token}")


@app.get("/assessment/_shared/responder/saude")
def saude():
    return {"status": "ok"}


@app.post("/assessment/leads/enviar", response_class=HTMLResponse)
async def enviar_lead(
    request: Request,
    nome: str = Form(...),
    empresa: str = Form(...),
    cargo: str = Form(""),
    email: str = Form(...),
    telefone: str = Form(""),
    interesse: str = Form(""),
    origem: str = Form(""),
    urgencia: str = Form(""),
    mensagem: str = Form(""),
    site: str = Form(""),  # honeypot — campo escondido no form; bot preenche, humano não
):
    if site.strip():
        # Some it: finge sucesso pro bot, não grava nada.
        return templates.TemplateResponse("lead_obrigado.html", {"request": request})

    if not nome.strip() or not empresa.strip() or "@" not in email:
        return templates.TemplateResponse(
            "lead_erro.html", {"request": request}, status_code=400
        )

    try:
        lead_salvo = leads.salvar_lead(
            nome.strip(), empresa.strip(), cargo.strip(), email.strip(), telefone.strip(),
            interesse.strip(), origem.strip(), urgencia.strip(), mensagem.strip(),
        )
    except Exception:
        logger.exception("Falha ao salvar lead")
        return templates.TemplateResponse(
            "lead_erro.html", {"request": request}, status_code=502
        )

    leads_notify.notificar_novo_lead(lead_salvo)

    return templates.TemplateResponse("lead_obrigado.html", {"request": request})


def _leads_crm_autenticado(request: Request) -> bool:
    return leads_crm_auth.cookie_valido(request.cookies.get(leads_crm_auth.COOKIE_NOME))


@app.get("/assessment/leads/crm/entrar", response_class=HTMLResponse)
def leads_crm_tela_login(request: Request, next: str = "/assessment/leads/crm", erro: bool = False):
    return templates.TemplateResponse("leads_crm_entrar.html", {"request": request, "next": next, "erro": erro})


@app.post("/assessment/leads/crm/entrar")
def leads_crm_processar_login(pin: str = Form(...), next: str = Form("/assessment/leads/crm")):
    if not leads_crm_auth.pin_correto(pin):
        return RedirectResponse(
            url=f"{LEADS_CRM_LOGIN_PATH}?erro=1&next={quote(next)}", status_code=303
        )
    resposta = RedirectResponse(url=next, status_code=303)
    resposta.set_cookie(
        leads_crm_auth.COOKIE_NOME,
        leads_crm_auth.valor_cookie(),
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=60 * 60 * 24 * 7,  # 7 dias — uso comercial recorrente, não só uma sessão de trabalho
    )
    return resposta


@app.get("/assessment/leads/crm", response_class=HTMLResponse)
def leads_crm_painel(request: Request):
    if not _leads_crm_autenticado(request):
        return RedirectResponse(url=f"{LEADS_CRM_LOGIN_PATH}?next=/assessment/leads/crm")
    try:
        registros = leads.listar_leads()
    except Exception:
        logger.exception("Falha ao ler leads")
        return templates.TemplateResponse(
            "erro.html",
            {"request": request, "mensagem": "Não foi possível carregar os leads agora. Tente novamente em instantes."},
            status_code=502,
        )
    return templates.TemplateResponse("leads_crm.html", {"request": request, "leads": registros})


@app.post("/assessment/leads/crm/salvar")
async def leads_crm_salvar(
    request: Request, linha: int = Form(...), campo: str = Form(...), valor: str = Form("")
):
    if not _leads_crm_autenticado(request):
        raise HTTPException(status_code=401, detail="Sessão expirada — atualize a página e faça login de novo")

    if campo not in leads.CAMPOS_CRM_EDITAVEIS:
        raise HTTPException(status_code=403, detail="Campo não editável por aqui")

    try:
        leads.atualizar_campo_lead(linha, campo, valor)
    except Exception:
        logger.exception("Falha ao salvar campo do lead")
        raise HTTPException(status_code=502, detail="Não foi possível salvar agora — tente novamente")

    return JSONResponse({"ok": True})


app.include_router(router)
