"""
Registro dos clientes ativos do eloo Assessment. Cada cliente é uma
planilha de coleta própria — adicionar um cliente novo é só uma entrada
aqui (mais o compartilhamento da planilha com a conta de serviço); não
precisa de novo deploy de infraestrutura, novo container nem novo secret.

O slug (chave do dicionário) vira parte da URL:
eloo.digital/assessment/{slug}/responder/...
"""

CLIENTES = {
    "super-logistica": {
        "nome": "Super Logística",
        "spreadsheet_id": "1MkV9WrqeAIrHkP9ndTcaAOuvJSnKbOgveJWzQD0VVRU",
    },
}


def get_cliente(slug: str) -> dict | None:
    return CLIENTES.get(slug)
