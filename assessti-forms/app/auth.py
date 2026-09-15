"""
Autenticação por link — sem cadastro de usuário. Cada módulo, de cada
cliente, tem dois tokens determinísticos derivados de SECRET_KEY: um para
o entrevistado (só responde) e um para o entrevistador/revisor (responde +
complementa + fecha o status).

O cliente (slug) entra na mensagem assinada, então um token nunca vale
para outro cliente nem para outro módulo — vazar um token só dá acesso
àquele módulo específico daquele cliente. SECRET_KEY é compartilhada entre
todos os clientes (não precisa trocar por engajamento); trocá-la invalida
todos os tokens de todos os clientes de uma vez.
"""
import hashlib
import hmac

from config import settings

PAPEL_ENTREVISTADO = "entrevistado"
PAPEL_REVISOR = "revisor"


def gerar_token(cliente: str, modulo_id: str, papel: str) -> str:
    mensagem = f"{cliente}:{modulo_id}:{papel}".encode()
    chave = settings.secret_key.encode()
    return hmac.new(chave, mensagem, hashlib.sha256).hexdigest()[:16]


def validar_token(cliente: str, modulo_id: str, token: str) -> str | None:
    """Retorna o papel (entrevistado/revisor) se o token for válido, senão None."""
    for papel in (PAPEL_REVISOR, PAPEL_ENTREVISTADO):
        esperado = gerar_token(cliente, modulo_id, papel)
        if hmac.compare_digest(esperado, token or ""):
            return papel
    return None
