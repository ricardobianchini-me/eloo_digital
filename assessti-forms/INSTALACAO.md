# Guia de Instalação — Assessti Forms

## 1. Pré-requisitos

- Docker Desktop (ou Docker Engine + Compose no OCI)
- Uma conta de serviço do Google Cloud com acesso à Google Sheets API e Google Drive API

## 2. Configurar a conta de serviço do Google

1. No [Google Cloud Console](https://console.cloud.google.com), crie um projeto (ou reaproveite um existente — pode ser o mesmo do hlera-bot, ou um novo, dedicado a esta app).
2. Ative as APIs **Google Sheets API** e **Google Drive API**.
3. Crie uma conta de serviço (Service Account) e gere uma chave JSON.
4. Salve o arquivo como `credentials/credentials.json` nesta pasta (`assessti-forms/credentials/`).
5. Anote o e-mail da conta de serviço (formato `nome@projeto.iam.gserviceaccount.com`) — você vai precisar dele no próximo passo.

## 3. Criar e popular a planilha do cliente

Isso é feito pelo script `seed.py`, que lê os `questionario-{modulo}.md` já gerados pelo squad `assessment-ti` (Fase 3) e cria as 7 abas com as perguntas — uma vez por cliente, não por deploy.

```bash
cd assessti-forms
python -m venv .venv
.venv/Scripts/activate   # Windows; no Linux/Mac: source .venv/bin/activate
pip install -r app/requirements.txt

# Copie o .env.example para .env e preencha GOOGLE_CREDENTIALS_FILE e SECRET_KEY
cp .env.example .env

cd app
python seed.py --cliente super-logistica --squad-dir "G:/My Drive/ClaudeCode/Agentes/squads/assessment-ti/output/{run_id}/v1" --criar "Assessment TI - Nome do Cliente"
```

O script imprime o `SPREADSHEET_ID` da planilha criada e a entrada pronta pra colar em `clientes.py`.

**Se a criação falhar por cota do Google Drive esgotada:** libere espaço (esvazie a Lixeira do Drive, ou veja `one.google.com/storage` para checar Gmail/Fotos) e rode de novo. Alternativamente, crie a planilha manualmente pelo Google Sheets, compartilhe com o e-mail da conta de serviço como Editor, e rode `seed.py --cliente ... --planilha-id <ID> --squad-dir ...` para só popular as abas.

## 4. Registrar o cliente em `clientes.py`

```python
CLIENTES = {
    "super-logistica": {"nome": "Super Logística", "spreadsheet_id": "<id impresso pelo seed.py>"},
}
```

`SECRET_KEY` (no `.env`) é única por ambiente, não por cliente — todos os clientes compartilham a mesma; o token já embute o slug do cliente, então não colide entre engajamentos.

## 5. Subir a aplicação

```bash
cd assessti-forms
docker-compose up -d --build
```

Acesse `http://localhost:8000/assessment/_shared/responder/saude` — deve responder `{"status": "ok"}`.

## 6. Obter os links de cada módulo

```bash
cd app
python seed.py --cliente super-logistica --links-only --base-url "https://eloo.digital"
```

Copie os links de **entrevistado** (opcional, pra quem for preencher sozinho antes da entrevista) e **revisor** (uso interno, pra preencher junto na chamada) de cada módulo e guarde em `pacce-co/assessment/{cliente}/projeto/links-internos.md` — nunca neste repositório.

## 7. Hospedar (produção real: VM-2 compartilhada, via GitHub Actions)

Em produção este app roda multi-cliente num único container na VM-2 que já
hospeda `eloo_digital` e `hlera-bot`, atrás do NGINX do host. Vive **dentro
do repositório do site institucional** (`eloo_digital`, pasta
`assessti-forms/`), com um workflow próprio
(`.github/workflows/deploy-assessment-forms.yml` na raiz do repo,
`paths: ['assessti-forms/**']`) — reaproveita os secrets `OCI_HOST`,
`OCI_USER`, `OCI_SSH_KEY` que já existem ali (usados pelo deploy do site),
só precisa cadastrar dois novos: `ASSESSMENT_SECRET_KEY` e
`ASSESSMENT_GOOGLE_CREDENTIALS_B64`. Um push em `main` que toque algo
dentro de `assessti-forms/` já dispara o deploy (rsync só dessa pasta,
`.env`, `credentials.json`, build, restart) sem rebuildar o site estático.
Ver a seção "Produção" do [README](README.md) para a tabela completa de
secrets e a explicação do `location` block extra necessário no NGINX do
host (regex genérico, cobre qualquer cliente futuro sem editar de novo).

Se preferir hospedar em outro lugar (VM própria, sem compartilhar com o
hlera-bot): suba uma instância com Docker + Compose, copie o repositório,
copie `credentials/credentials.json` manualmente (nunca via git), configure
HTTPS na frente do container e `docker-compose up -d --build`.

Veja o [Guia de Manutenção](MANUTENCAO.md) para operação do dia a dia.
