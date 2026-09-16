"""
Gate de PIN do portal do cliente — substitui o HTTP Basic Auth do nginx
(popup nativo de usuário+senha) por uma tela de login própria, só com PIN,
igual ao padrão já usado na ferramenta interna de resposta (`pin_auth.py`).

Diferença: aqui o PIN é POR CLIENTE (`clientes.py`, campo `portal_pin`), não
um PIN único compartilhado — o cookie é assinado incluindo o slug do
cliente na mensagem, então o cookie de um cliente nunca destranca o portal
de outro.
"""
import hashlib
import hmac

from config import settings

COOKIE_PREFIX = "eloo_portal_"


def cookie_nome(cliente: str) -> str:
    return f"{COOKIE_PREFIX}{cliente}"


def _assinatura_esperada(cliente: str) -> str:
    chave = settings.secret_key.encode()
    mensagem = f"portal-ok:{cliente}".encode()
    return hmac.new(chave, mensagem, hashlib.sha256).hexdigest()


def pin_correto(cliente_info: dict, pin: str) -> bool:
    pin_esperado = cliente_info.get("portal_pin")
    if not pin_esperado:
        return False
    return hmac.compare_digest(pin or "", pin_esperado)


def valor_cookie(cliente: str) -> str:
    return _assinatura_esperada(cliente)


def cookie_valido(cliente: str, valor: str | None) -> bool:
    if not valor:
        return False
    return hmac.compare_digest(valor, _assinatura_esperada(cliente))
