"""
Parser dos arquivos `questionario-{modulo}.md` gerados pelo squad Opensquad
`assessment-ti` (tabelas markdown de 7 colunas: Ref | Pergunta | Evidência
Esperada | Método de Verificação Exigido | Resposta do Entrevistado |
Evidência Anexada | Complemento do Entrevistador).

O arquivo `.md` do squad é a fonte única de verdade do banco de perguntas —
este parser nunca duplica conteúdo de pergunta manualmente, só traduz o
markdown já gerado para as linhas que a planilha de coleta espera.
"""
import re
from pathlib import Path

from modulos import COLUNAS

_SUBTEMA_RE = re.compile(r"^##\s+(.+)$")
_REF_ROW_RE = re.compile(r"^\|\s*([A-Z]{3}-\d+)\s*\|(.+)\|\s*$")


def parse_questionario(caminho: Path) -> list[list[str]]:
    """Retorna as linhas prontas para a planilha: cabeçalho + separadores de
    subtema + uma linha por pergunta, na ordem de `modulos.COLUNAS`.
    """
    texto = caminho.read_text(encoding="utf-8")
    linhas: list[list[str]] = [list(COLUNAS)]

    for linha_bruta in texto.splitlines():
        linha_bruta = linha_bruta.rstrip()

        m_sub = _SUBTEMA_RE.match(linha_bruta)
        if m_sub:
            titulo = m_sub.group(1).strip()
            linhas.append(["## " + titulo, "", "", "", "", "", "", "", ""])
            continue

        m_ref = _REF_ROW_RE.match(linha_bruta)
        if not m_ref:
            continue

        ref = m_ref.group(1)
        resto = m_ref.group(2)
        celulas = [c.strip() for c in resto.split("|")]
        # celulas esperadas (após o Ref): Pergunta, Evidência, Método, Resposta, Evidência Anexada, Complemento
        # (Resposta/Evidência/Complemento sempre vêm vazias do squad — a planilha é quem coleta)
        if len(celulas) < 3:
            continue
        pergunta = celulas[0]
        evidencia = celulas[1]
        metodo = celulas[2]

        linhas.append([ref, pergunta, evidencia, metodo, "", "", "", "", "Pendente"])

    return linhas
