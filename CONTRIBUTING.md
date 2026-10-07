# Fluxo de trabalho — eloo_digital

> Combinado entre os sócios em 2026-10-06: **nada vai para produção sem passar
> pelo GitHub**. Toda mudança entra por branch e pull request, e o deploy só
> acontece depois do merge na `main`.

## Por quê

A `main` publica sozinha. Um push nela dispara o deploy na VM-1:

| Workflow | Quando roda | O que publica |
|---|---|---|
| `deploy.yml` | push na `main` fora de `assessti-forms/` | site estático (eloo.digital) |
| `deploy-assessment-forms.yml` | push na `main` em `assessti-forms/` | app FastAPI (CRM de leads, gestão, Assessment) |

Os dois sincronizam com `rsync --delete`: **o que estiver na VM e não estiver
no git é apagado no próximo deploy.** Por isso nenhuma alteração é feita direto
no servidor.

## Passo a passo

1. Atualize a `main` local: `git checkout main && git pull`.
2. Crie uma branch a partir dela, com prefixo pelo tipo de mudança:
   - `feat/` funcionalidade nova (ex.: `feat/crm-prospeccao`)
   - `fix/` correção (ex.: `fix/filtro-socio-gestao`)
   - `site/` texto ou visual do site (ex.: `site/pagina-pacce`)
   - `docs/` documentação
3. Faça commits pequenos e com mensagem que explique o porquê.
4. `git push -u origin <branch>` e abra o pull request para a `main`.
5. O workflow **CI** (`ci.yml`) roda no PR: build do site e checagem do app.
   PR com CI vermelho não entra.
6. Outro sócio revisa quando a mudança afetar o que ele usa (CRM, gestão,
   páginas de produto). Mudança só de texto pode ser aprovada por quem abriu.
7. Merge na `main` (preferir **Squash and merge** para manter o histórico
   limpo, um commit por PR). O deploy roda sozinho; confira em produção.

## O que nunca fazer

- Push direto na `main` (fica bloqueado pela regra de proteção da branch).
- `git push --force` na `main` ou reescrever histórico já publicado.
- Editar arquivos, `.env` ou containers direto na VM. Segredos vão em
  **Settings → Secrets and variables → Actions**; o workflow escreve o `.env`
  a cada deploy.
- Subir credenciais no repositório (ele é **público**).

## Infra fora deste repositório

A configuração do nginx da VM-1 vive no repositório `hlera-bot`
(`nginx/vm1-apps/eloo-digital`). Mudança de rota segue o mesmo fluxo lá:
branch, PR, merge e só então aplicar na VM, com backup e `nginx -t` antes de
recarregar.

## Versões e volta atrás

- Marcos importantes ganham tag (ex.: `site-v1`, backup da home anterior à v2).
- Para desfazer algo já publicado, abra um PR com `git revert <commit>` em vez
  de apagar commits.
