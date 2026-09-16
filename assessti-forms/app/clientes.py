"""
Registro dos clientes ativos do eloo Assessment. Cada cliente é uma
planilha de coleta própria — adicionar um cliente novo é só uma entrada
aqui (mais o compartilhamento da planilha com a conta de serviço); não
precisa de novo deploy de infraestrutura, novo container nem novo secret.

O slug (chave do dicionário) vira parte da URL:
eloo.digital/assessment/{slug}/responder/...

Primeiro deploy real: 2026-09-16, depois que os secrets ASSESSMENT_SECRET_KEY
e ASSESSMENT_GOOGLE_CREDENTIALS_B64 foram cadastrados no GitHub.
"""

CLIENTES = {
    "super-logistica": {
        "nome": "Super Logística",
        "spreadsheet_id": "1MkV9WrqeAIrHkP9ndTcaAOuvJSnKbOgveJWzQD0VVRU",
        # PIN de acesso ao portal publicado (proposta, status, questionários).
        # Substitui o Basic Auth do navegador — mesmo padrão de UX do PIN
        # interno (ver portal_auth.py). Entregue ao cliente por canal
        # separado (nunca por e-mail junto com o link).
        "portal_pin": "131313",
    },
    "jc-gestao-de-risco": {
        "nome": "JC Gestão de Risco",
        # Proposta apresentada em 2026-09-16, ainda não aceita — sem planilha
        # real ainda. Placeholder até o aceite: NÃO habilitar "Responder ao
        # vivo" nem qualquer rota /responder/ para este cliente enquanto
        # este valor não for trocado por um spreadsheet_id real.
        "spreadsheet_id": "PENDENTE_ATE_ACEITE",
        "portal_pin": "160926",
    },
}


def get_cliente(slug: str) -> dict | None:
    return CLIENTES.get(slug)
