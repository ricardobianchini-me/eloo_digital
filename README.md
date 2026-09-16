# eloo.digital

Site institucional da Eloo, feito em [Astro](https://astro.build), construído em `pacce-co` (playbook estratégico da empresa) e migrado pra esse repositório próprio em 13/08/2026.

**No ar:** https://eloo.digital

## Páginas

| Rota | Arquivo | O quê |
|---|---|---|
| `/` | `src/pages/index.astro` | Landing institucional — funil PACCE (Diagnóstico Digital → Site/CMS → PACCE), público espiritualista/terceiro setor |
| `/assessment` | `src/pages/assessment.astro` | Landing pública do **eloo Assessment** — vertical B2B separada (Assessment de Governança/Infraestrutura/Sistemas de TI, COBIT 2019 + ITIL 4), adicionada 15/09/2026 |
| `/assessment/{cliente}/` | `src/pages/assessment/{cliente}/` | **Portal privado** de um cliente do eloo Assessment (proposta + questionários) — protegido por senha, não indexado. Ver seção abaixo. |

Todas as páginas importam o mesmo `src/styles/global.css` (paleta e tokens
únicos da marca).

## Portais de cliente (eloo Assessment)

Cada cliente do eloo Assessment que teve proposta e questionários publicados
tem uma pasta própria em `src/pages/assessment/{slug-do-cliente}/`, com:

- `index.astro` — painel do projeto (resumo, status RAG, links para proposta e questionários);
- `questionario-{modulo}.md` — um arquivo por módulo técnico, renderizado via
  o layout `src/layouts/ClientDoc.astro` (mesma paleta, tabela estilizada,
  banner de confidencialidade);
- a proposta visual fica em `public/assessment/{cliente}/proposta.html`
  (HTML já pronto, servido como arquivo estático, sem passar pelo layout).

**Fonte de verdade do conteúdo** continua sendo `pacce-co/assessment/{cliente}/`
(ver `pacce-co/assessment/CLIENTES.md`) — as páginas aqui são uma **cópia
publicada** desse conteúdo, gerada manualmente quando o material está pronto
para o cliente acessar. Ao atualizar proposta/questionário depois de
publicado, editar os dois lugares (fonte em `pacce-co`, cópia aqui) ou, no
mínimo, atualizar aqui e replicar depois na fonte.

**Proteção de acesso (2026-09-16 — PIN, não mais Basic Auth):** essas páginas
ficam atrás de um PIN por cliente, com a mesma UX da ferramenta interna de
resposta ao vivo (tela própria, só um campo de PIN — nunca o popup nativo
de usuário+senha do navegador do HTTP Basic Auth, que era confuso). O gate
roda no **nginx do host** (`hlera-bot/nginx/vm2-apps/eloo-digital`), via
`auth_request` contra `GET /assessment/{cliente}/portal/check` no app
`assessti-forms` (`app/portal_auth.py` + `app/clientes.py`, campo
`portal_pin`) — o nginx *deste* repositório (`nginx.conf`, dentro do
container do site estático) não faz mais nenhum auth_basic, pra não conflitar
com esse fluxo. Pra adicionar um cliente novo:

1. Adicionar `"portal_pin": "<pin>"` na entrada do cliente em
   `assessti-forms/app/clientes.py` e fazer deploy do app (dispara sozinho
   com `paths: ['assessti-forms/**']`).
2. Criar a pasta `src/pages/assessment/{slug}/` seguindo o padrão acima —
   nenhum location block novo é necessário no nginx do host nem aqui, o
   gate já cobre `/assessment/{qualquer-slug}/` genericamente.
3. O PIN é entregue ao cliente por canal separado (nunca por e-mail junto
   com o link do portal).

Todas essas páginas têm `<meta name="robots" content="noindex, nofollow">`
e o path `/assessment/*/` está bloqueado em `public/robots.txt` — não
aparecem em busca nem em sitemap, e não há link de navegação apontando pra
elas a partir de `/` ou `/assessment`.

---

## Arquitetura

```
push em main
      │
      ▼
GitHub Actions (.github/workflows/deploy.yml)
      │
      ├─ 1. rsync do repo inteiro pra VM-2 (~/eloo-digital)
      ├─ 2. docker compose build   (Astro build -> nginx:alpine servindo /dist)
      └─ 3. docker compose up -d  (recria o container eloo_digital)
      │
      ▼
VM-2 (OCI, 163.176.228.252) — infra do hlera-bot
      │
      container eloo_digital, porta 8082 (interna, não exposta direto)
      │
      ▼
NGINX do host (não containerizado) — termina TLS, faz proxy_reverse
pra localhost:8082, config em /etc/nginx/sites-enabled/eloo-digital
(espelhada em hlera-bot/nginx/vm2-apps/eloo-digital)
```

Não tem servidor de aplicação — é um site 100% estático (`astro build` gera HTML/CSS/JS puro), o container só serve os arquivos via nginx interno. Sem banco de dados, sem backend.

## Por que essa arquitetura (e não GitHub Pages)

O site começou no GitHub Pages (deploy automático, zero infra própria). Foi migrado pra rodar na mesma VM que já hospeda o bot do HLERA_doBEM porque:
- domínio próprio (`eloo.digital`) já registrado, precisava de hosting real de qualquer forma;
- a VM-2 já está paga e operada pela equipe, com NGINX+Certbot já configurados pra outros domínios (`moocamor.duckdns.org`, `superacao-apps.duckdns.org`) — reaproveitar em vez de criar infra nova;
- deploy automático via GitHub Actions preserva a mesma ergonomia do Pages (`git push` e pronto), só troca o destino.

Contrapartida assumida conscientemente: depende da VM-2 ficar de pé (sem redundância/CDN como o Pages tinha).

## Infraestrutura — detalhes de acesso

Isso é **infra do hlera-bot**, não deste repositório. Documentação completa (IPs das VMs, como conectar por SSH, bugs conhecidos de NSG/iptables, etc) está em `hlera-bot/CLAUDE.md` e `hlera-bot/nginx/README.md`. Resumo do que é específico do eloo.digital:

| Item | Valor |
|---|---|
| VM | VM-2 apps (OCI), IP `163.176.228.252` |
| Container | `eloo_digital`, porta publicada `8082:80` |
| Diretório na VM | `~/eloo-digital` (sincronizado via rsync a cada deploy — **não editar direto na VM**, qualquer mudança lá é sobrescrita no próximo push) |
| NGINX (host, fora do Docker) | `/etc/nginx/sites-enabled/eloo-digital` — reverse proxy `eloo.digital`/`www.eloo.digital` → `localhost:8082`, TLS via Certbot |
| Certificado TLS | Let's Encrypt, emitido 15/09/2026, expira 14/12/2026, renovação automática (mesmo cron/systemd timer do Certbot que já cuida dos outros domínios da VM) |
| DNS | GoDaddy, registro `A @ → 163.176.228.252` e `CNAME www → eloo.digital` (painel: account.godaddy.com, domínio `eloo.digital`) |

## Secrets do GitHub Actions (Settings → Secrets and variables → Actions)

| Secret | Valor | Pra quê |
|---|---|---|
| `OCI_HOST` | `163.176.228.252` | IP da VM-2 |
| `OCI_USER` | `ubuntu` | usuário SSH |
| `OCI_SSH_KEY` | conteúdo de `~/.ssh/oci_hlera_key` (chave privada) | autenticação SSH do workflow — **a chave em si só existe no computador de quem tem acesso à VM**, nunca commitada em lugar nenhum |

Se o deploy começar a falhar por causa de SSH, o primeiro suspeito é um desses três secrets (expirado, apagado, ou a chave privada rotacionada sem atualizar aqui).

## Desenvolvimento local

```sh
npm install
npm run dev       # localhost:4321
npm run build     # gera ./dist
npm run preview   # serve ./dist localmente, simula produção
```

Estrutura:
```
src/pages/index.astro                    — landing institucional (funil PACCE)
src/pages/assessment.astro               — landing pública do eloo Assessment (vertical B2B)
src/pages/assessment/{cliente}/          — portal privado de um cliente (ver seção "Portais de cliente" acima)
src/layouts/ClientDoc.astro              — layout dos documentos de cliente (questionários em markdown)
src/styles/global.css                    — tokens de design (cores, tipografia) + wordmark, compartilhado por todas as páginas
public/                                  — favicon, assets estáticos, robots.txt, proposta.html de cada cliente
Dockerfile                               — build Astro + serve via nginx:alpine
docker-compose.yml                       — como o container roda na VM
nginx.conf                               — config do nginx *dentro* do container (não confundir com o nginx do host) — só serve estático, o gate de PIN dos portais de cliente vive no nginx do host + assessti-forms
```

Cada página em `src/pages/` vira uma rota automaticamente (Astro file-based
routing) — para adicionar uma nova página/vertical, criar um novo arquivo
`.astro` ali, importando `../styles/global.css` para herdar a paleta.

## Paleta e tipografia

Ver `pacce-co/DESIGN.md` (fonte da verdade) — resumo:
- `--deep` `#1A2421`, `--mint` `#C2E7D9`, `--salvia` `#6B8E81`, `--dourado` `#D4AF37`, `--parchment` `#F4F2EA`, `--ink` `#23261F`
- Wordmark do logo em Montserrat (embutida via `@font-face`, só nessa peça); título/corpo em pilha de fonte de sistema.

## Como mudar algo

Qualquer alteração de conteúdo/estilo: editar a página relevante em `src/pages/` (ou `src/styles/global.css` para mudar tokens globais), `git push` pra `main`. O deploy é automático — normalmente leva 20-40s do push até o ar (o `docker compose build` reaproveita cache de camadas quando só o conteúdo muda, então é rápido). Acompanhar em [Actions](https://github.com/ricardobianchini-me/eloo_digital/actions).

## Troubleshooting

- **Site fora do ar / 502 Bad Gateway**: o container provavelmente não está rodando. `ssh -i ~/.ssh/oci_hlera_key ubuntu@163.176.228.252 'sudo docker ps | grep eloo'` — se não aparecer nada, `cd ~/eloo-digital && sudo docker compose up -d` resolve na maioria dos casos.
- **Deploy falha no GitHub Actions**: ver o log do step que falhou em Actions. Já aconteceu uma vez (run #5, 15/09/2026) da conexão SSH cair bem na transição entre build e start, deixando o container criado mas nunca iniciado — o workflow atual já tem keepalive (`ServerAliveInterval`) pra isso não se repetir, mas se acontecer de novo, `docker compose up -d` manual na VM resolve na hora enquanto se investiga.
- **Certificado TLS expirando**: não deveria acontecer (renovação automática), mas se acontecer, `sudo certbot renew` na VM-2 resolve.
