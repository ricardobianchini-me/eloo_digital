# 🕯️ eloo Assessment (eloo.digital)

App web de coleta das respostas dos 7 módulos do **Assessment TI** (squad Opensquad `assessment-ti`), no padrão *working paper* definido em `maturity-scales.md` Seção 5: cada pergunta tem Ref, Método de Verificação Exigido e campo de Evidência Anexada — sem coluna de Maturidade (isso é determinação do especialista na Fase 4, feita depois, fora desta app).

Produto sob a marca **eloo.digital**, chamado **eloo Assessment** — deliberadamente distinto da metodologia **Lumen** (`pacce-co/05_metodologia_lumen.md`), que é o diagnóstico gratuito de outro público-alvo (instituições espiritualistas) e não deve ser reaproveitado aqui para evitar confusão de marca. Identidade visual herdada de `pacce-co/DESIGN.md` (paleta deep/mint/sálvia/dourado/parchment).

Hospedagem própria, separada do `hlera-bot`, da Fraternidade do Amor e do site institucional da eloo.digital — projeto e `docker-compose` isolados, nada de infraestrutura compartilhada.

## O que faz

- **Multi-cliente num único deployment** — cada cliente é uma entrada em `app/clientes.py` (slug → nome + ID da planilha), não um container/deploy separado
- Publica um formulário web por módulo (Segurança, Infraestrutura, Cloud, Arquitetura, Endpoint, Backup, Governança), por cliente, em `/assessment/{cliente}/responder/m/{modulo}`
- Cada módulo/cliente tem dois links: um para o **entrevistado** (só responde) e um para o **entrevistador/revisor** (responde + complementa + marca "Revisado")
- Grava tudo direto na planilha Google Sheets daquele cliente — a mesma que os especialistas do squad leem na Fase 4 (diagnóstico)
- Sem cadastro de usuário: acesso é só pelo link com token (token amarra cliente + módulo + papel, nunca vale pra outro cliente)

## Stack

| Componente | Tecnologia |
|------------|-----------|
| Backend | Python 3.11 + FastAPI |
| Templates | Jinja2 (server-rendered, sem framework JS) |
| Banco de dados | Google Sheets |
| Infraestrutura | Docker + Docker Compose |

## Estrutura

```
assessti-forms/
├── docker-compose.yml
├── .env.example
├── credentials/              # credenciais Google (não vai ao GitHub)
├── app/
│   ├── main.py                # rotas FastAPI (prefixo /assessment/{cliente}/responder)
│   ├── clientes.py             # registro de clientes ativos (slug -> nome + spreadsheet_id)
│   ├── modulos.py              # registro dos 7 módulos e colunas da planilha (igual pra todo cliente)
│   ├── auth.py                 # tokens por cliente+módulo+papel (entrevistado, revisor)
│   ├── sheets.py                # leitura/escrita na planilha (recebe spreadsheet_id por chamada)
│   ├── seed.py                  # cria/popula a planilha de um cliente a partir dos questionario-*.md do squad
│   ├── seed_parser.py            # parser dos arquivos markdown do squad
│   ├── templates/
│   └── static/style.css
├── INSTALACAO.md
└── MANUTENCAO.md
```

## Fluxo de uso por cliente/engajamento

1. Rode o squad `assessment-ti` (Opensquad) até a Fase 3 — ele gera `questionario-{modulo}.md` para os 7 módulos.
2. Rode `python seed.py --cliente {slug} --squad-dir "..." --criar "Assessment TI - Nome do Cliente"` — ele cria/popula a planilha, imprime a entrada pra colar em `clientes.py` e os links de cada módulo.
3. Adicione a entrada em `clientes.py`, commit + push (deploy automático) — nenhum secret novo, nenhum container novo.
4. Compartilhe cada link só com o interlocutor daquele domínio (link de entrevistado) — o link de revisor é uso interno da equipe, nunca vai pro cliente.
5. Quando todos os módulos estiverem com as respostas revisadas, volte para o squad (Fase 4) — os especialistas leem a mesma planilha para diagnosticar.

Veja o [Guia de Instalação](INSTALACAO.md) para o passo a passo completo.

## Produção — um deployment, todos os clientes

A partir de 2026-09-16, este app roda em produção na mesma VM-2 (OCI) do
`eloo_digital` e do `hlera-bot`, como **container próprio** (porta `8001`),
exposto via NGINX do host sob o mesmo domínio do portal estático:
`https://eloo.digital/assessment/{cliente}/responder/...`. O `{cliente}`
é resolvido em tempo de execução via `app/clientes.py` — **cliente novo
não pede novo deploy de infraestrutura, novo container, nova porta nem
novo secret do GitHub**, só uma entrada nova nesse arquivo.

**Deploy:** GitHub Actions (`.github/workflows/deploy.yml`), disparado por
push em `main`. Diferente do `eloo_digital` (site estático sem segredos),
aqui `.env` e `credentials/credentials.json` **nunca vão pro repositório**
— o workflow escreve os dois na VM a cada deploy, a partir de secrets do
GitHub (fixos, não crescem por cliente):

| Secret do GitHub | Valor |
|---|---|
| `OCI_HOST`, `OCI_USER`, `OCI_SSH_KEY` | mesmos do repo `eloo_digital` (mesma VM) |
| `ASSESSMENT_SECRET_KEY` | chave dos tokens de todos os clientes/módulos (trocar invalida TODOS os links de TODOS os clientes de uma vez) |
| `ASSESSMENT_INTERNAL_PIN` | PIN da tela de login interna (`/responder/entrar`), compartilhado entre clientes |
| `ASSESSMENT_GOOGLE_CREDENTIALS_B64` | JSON da service account em base64 (`base64 -w0 credentials.json`) |

**Acesso interno da equipe:** tela de login própria do app, em
`/assessment/_shared/responder/entrar` — pede só o PIN (`INTERNAL_PIN`
no `.env`/secret `ASSESSMENT_INTERNAL_PIN`), não é HTTP Basic Auth do
nginx (esse era o design original, trocado em 2026-09-16 porque o popup
nativo do navegador pede usuário+senha, confuso pra quem só esperava
digitar um PIN — ver `pin_auth.py`). Login bem-sucedido grava um cookie
assinado (HMAC com `SECRET_KEY`), válido por 12h, compartilhado entre
todos os clientes. Mesmo passando por esse PIN, cada módulo só abre com
o token correto daquele cliente (`auth.py`) — duas camadas independentes.
O `location` no host NGINX (mirror em `hlera-bot/nginx/vm2-apps/eloo-digital`)
é hoje só um proxy_pass simples, regex genérico
`^/assessment/[^/]+/responder/` — já cobre qualquer cliente futuro sem
editar o nginx de novo.

**Links de acesso por módulo (revisor/entrevistado)** de cada engajamento
ativo ficam em `pacce-co/assessment/{cliente}/projeto/links-internos.md`
— nunca neste repositório, nunca versionados, nunca compartilhados com o
cliente. Gerar com `python seed.py --cliente {slug} --links-only`.
