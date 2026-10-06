"""
Gate de PIN da página de gestão da empresa (/gestao) —
mesmo padrão de `leads_crm_auth.py` (tela própria, cookie assinado), mas
cookie e PIN separados: é a visão administrativa dos sócios (roadmap, metas,
decisões), não o CRM comercial.

Diferente do CRM de leads, não existe PIN padrão: sem GESTAO_PIN no .env a
página fica fechada para todo mundo (o repositório é público, um padrão
versionado aqui seria um PIN conhecido por qualquer um).
"""
import hashlib
import hmac

from config import settings

COOKIE_NOME = "eloo_gestao"
_MENSAGEM = b"acesso-gestao-ok"


def _assinatura_esperada() -> str:
    chave = settings.secret_key.encode()
    # O PIN entra na assinatura: trocar o GESTAO_PIN derruba as sessões abertas.
    return hmac.new(chave, _MENSAGEM + settings.gestao_pin.encode(), hashlib.sha256).hexdigest()


def pin_correto(pin: str) -> bool:
    if not settings.gestao_pin:
        return False
    return hmac.compare_digest(pin or "", settings.gestao_pin)


def valor_cookie() -> str:
    return _assinatura_esperada()


def cookie_valido(valor: str | None) -> bool:
    if not valor or not settings.gestao_pin:
        return False
    return hmac.compare_digest(valor, _assinatura_esperada())
