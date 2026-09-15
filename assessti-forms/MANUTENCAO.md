# Guia de Manutenção — Assessti Forms

## Rodar após editar código

```bash
docker-compose up -d --build app
```

## Ver logs em tempo real

```bash
docker logs assessti_forms -f
```

## Novo cliente / novo engajamento

Cada engajamento tem sua própria planilha, mas **compartilha** a mesma instância e a mesma `SECRET_KEY` — os links de um cliente nunca funcionam para outro porque o token já embute o slug do cliente na assinatura:

1. Rode `seed.py --cliente {slug-do-novo-cliente} --squad-dir <output do novo run> --criar "Assessment TI - Novo Cliente"`.
2. Adicione a entrada impressa em `clientes.py` (slug, nome, spreadsheet_id).
3. Commit + push em `main` — o deploy (GitHub Actions) já sobe a versão nova de `clientes.py`; não precisa mexer em `.env` nem em secrets.
4. Rode `seed.py --cliente {slug} --links-only` para pegar os links desse cliente.

Não precisa de container novo, porta nova, secret novo nem edição de NGINX — o `location` do host já é genérico para qualquer `{cliente}`.

## Perguntas mudaram no squad (nova versão do questionário)

Se o squad `assessment-ti` gerar uma nova versão dos questionários (ex.: depois de ajustar o rigor do formato), rode `seed.py` de novo apontando para a nova pasta de output — ele **limpa e repopula** as abas correspondentes. Respostas já salvas na planilha são perdidas nesse processo; se houver respostas em andamento, exporte-as antes (Arquivo > Fazer download, na própria planilha).

## Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| "Não foi possível carregar as perguntas agora" | `credentials.json` ausente/errado, ou planilha não compartilhada com a conta de serviço | Confira `GOOGLE_CREDENTIALS_FILE` e se a planilha foi compartilhada (Editor) com o e-mail da conta de serviço |
| Link retorna "Link inválido" | Token não bate com o `SECRET_KEY` atual, cliente/módulo errado na URL, ou slug do cliente não existe em `clientes.py` | Confirme o slug em `clientes.py`; gere os links de novo com `seed.py --cliente {slug} --links-only` após qualquer troca de `SECRET_KEY` (troca invalida os links de TODOS os clientes) |
| Erro ao criar planilha (`storageQuotaExceeded`) | Cota do Google Drive da conta esgotada | Esvaziar a Lixeira do Drive ou liberar espaço em `one.google.com/storage`, depois tentar de novo |
| Respostas não aparecem para o especialista do squad (Fase 4) | Aba com nome diferente do esperado, ou cliente apontando pra planilha errada em `clientes.py` | Confirme que o nome da aba bate exatamente com `modulos.py` (`aba`) e que `clientes.py` tem o `spreadsheet_id` certo pra esse cliente |
| 404 em `/assessment/{cliente}/responder/...` | Slug do cliente não existe (ou está grafado diferente) em `clientes.py` | Conferir o slug exato — é case-sensitive e precisa bater com a URL distribuída |
