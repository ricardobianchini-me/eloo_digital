"""
Gate de PIN da página oculta de gestão de leads (/assessment/leads/crm) —
mesmo padrão de `pin_auth.py` (tela própria, cookie assinado — não HTTP
Basic Auth do nginx), mas cookie e PIN separados: público-alvo diferente
(equipe comercial, não quem preenche assessment) e não deve compartilhar
sessão com o PIN interno do Assessment.
"""
import hashlib
import hmac

from config import settings

COOKIE_NOME = "eloo_leads_crm"
_MENSAGEM = b"acesso-leads-crm-ok"


def _assinatura_esperada() -> str:
    chave = settings.secret_key.encode()
    return hmac.new(chave, _MENSAGEM, hashlib.sha256).hexdigest()


def pin_correto(pin: str) -> bool:
    if not settings.leads_crm_pin:
        return False
    return hmac.compare_digest(pin or "", settings.leads_crm_pin)


def valor_cookie() -> str:
    return _assinatura_esperada()


def cookie_valido(valor: str | None) -> bool:
    if not valor:
        return False
    return hmac.compare_digest(valor, _assinatura_esperada())
