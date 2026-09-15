"""
Gate de PIN interno — substitui o HTTP Basic Auth do nginx (que sempre
mostra um popup de usuário+senha, mesmo quando a "senha" é só um número)
por uma tela de login própria do app que pede só o PIN, e guarda a sessão
num cookie assinado.

Não é por-cliente nem por-módulo (isso já é o `auth.py`) — é um gate único,
de uso interno da equipe, na frente de toda a ferramenta de preenchimento.

ASSESSMENT_INTERNAL_PIN cadastrado no GitHub Actions em 2026-09-16.
"""
import hashlib
import hmac

from config import settings

COOKIE_NOME = "eloo_interno"
_MENSAGEM = b"acesso-interno-ok"


def _assinatura_esperada() -> str:
    chave = settings.secret_key.encode()
    return hmac.new(chave, _MENSAGEM, hashlib.sha256).hexdigest()


def pin_correto(pin: str) -> bool:
    if not settings.internal_pin:
        return False
    return hmac.compare_digest(pin or "", settings.internal_pin)


def valor_cookie() -> str:
    return _assinatura_esperada()


def cookie_valido(valor: str | None) -> bool:
    if not valor:
        return False
    return hmac.compare_digest(valor, _assinatura_esperada())
