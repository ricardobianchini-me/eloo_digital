"""
Registro dos 7 módulos do Assessment TI — mantido em sincronia com o squad
Opensquad `assessment-ti` (pipeline/data/domain-framework.md, tabela
agente -> módulo). Cada módulo corresponde a uma aba na planilha de coleta.
"""

MODULOS = [
    {"id": "seguranca", "nome": "Segurança da Informação", "prefixo": "SEG", "aba": "Segurança da Informação",
     "arquivo": "questionario-sergio-seguranca.md"},
    {"id": "infraestrutura", "nome": "Infraestrutura e Redes", "prefixo": "INF", "aba": "Infraestrutura e Redes",
     "arquivo": "questionario-ivo-infraestrutura.md"},
    {"id": "cloud", "nome": "Cloud e Licenciamento", "prefixo": "CLD", "aba": "Cloud e Licenciamento",
     "arquivo": "questionario-caio-cloud.md"},
    {"id": "arquitetura", "nome": "Arquitetura Corporativa", "prefixo": "ARQ", "aba": "Arquitetura Corporativa",
     "arquivo": "questionario-adriana-arquitetura.md"},
    {"id": "endpoint", "nome": "Endpoint Management", "prefixo": "EPT", "aba": "Endpoint Management",
     "arquivo": "questionario-elisa-endpoint.md"},
    {"id": "backup", "nome": "Backup e Continuidade", "prefixo": "BKP", "aba": "Backup e Continuidade",
     "arquivo": "questionario-breno-backup.md"},
    {"id": "governanca", "nome": "Governança de TI", "prefixo": "GOV", "aba": "Governança de TI",
     "arquivo": "questionario-gustavo-governanca.md"},
]

MODULOS_POR_ID = {m["id"]: m for m in MODULOS}

# Colunas da planilha, na ordem — únicas para todos os módulos.
COLUNAS = [
    "Ref",
    "Pergunta",
    "Evidência Esperada",
    "Método de Verificação Exigido",
    "Resposta do Entrevistado",
    "Evidência Anexada (Sim/Não/Parcial)",
    "Referência da Evidência",
    "Complemento do Entrevistador",
    "Status",
]

COL_RESPOSTA = "Resposta do Entrevistado"
COL_EVIDENCIA_STATUS = "Evidência Anexada (Sim/Não/Parcial)"
COL_EVIDENCIA_REF = "Referência da Evidência"
COL_COMPLEMENTO = "Complemento do Entrevistador"
COL_STATUS = "Status"

# Campos que o papel "entrevistado" pode editar.
CAMPOS_ENTREVISTADO = {COL_RESPOSTA, COL_EVIDENCIA_STATUS, COL_EVIDENCIA_REF}
# Campos adicionais liberados para o papel "revisor".
CAMPOS_REVISOR = CAMPOS_ENTREVISTADO | {COL_COMPLEMENTO, COL_STATUS}
