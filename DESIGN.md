# DESIGN.md — eloo.digital

> Sistema visual da v2 do site (home publicada em 2026-10-05). Fonte: `src/pages/index.astro`.

## Color

| Token | Valor | Uso |
|---|---|---|
| `--bg` | `#f4f2ed` | Fundo claro padrão |
| `--bg-alt` | `#e6e4dd` | Faixas claras alternadas, chips |
| `--card` | `#fbfaf7` | Superfícies sobre o fundo claro |
| `--ink` | `#1f1f1d` | Texto e faixas escuras |
| `--ink-soft` | `#55554f` | Texto de apoio (≥4.5:1 sobre `--bg`) |
| `--line` | `#d8d6ce` | Bordas |
| `--accent` | `#e0201a` | Único acento: CTAs, destaques, faixa vermelha |
| `--accent-deep` | `#b8160f` | Hover do acento |
| `--accent-ink` | `#fff3f2` | Texto sobre o vermelho |
| destaque escuro | `#ff8a84` | Palavra em destaque sobre fundo escuro |

## Type

- Títulos: **Bricolage Grotesque** 500–800, `letter-spacing: -0.01em`, `text-wrap: balance`.
- Corpo: **IBM Plex Sans** 400–600, 16px, `line-height: 1.6`.
- Escala de títulos com `clamp()`; h1 até ~3.6rem na home.

## Layout

- `.wrap` de 1120px com 1.4rem de margem lateral.
- Seções **full-bleed** (`.bleed`): foto ocupando metade da largura total, texto alinhado à grade do conteúdo; `.bleed-reverso` inverte o lado.
- Faixas de cor de largura total: escura (`.escuro`), vermelha (`.vermelho`), clara alternada.
- Hero com foto em tela cheia, scrim escuro de baixo para cima e texto ancorado embaixo.

## Components

Botões em pílula (`.btn-primario`, `.btn-ghost`, `.btn-claro`), cards com foto e cantos de 16px (usar com parcimônia), pílulas de tag, topo fixo com fundo translúcido.

## Motion

Transições curtas com `cubic-bezier(.16,1,.3,1)`; hover sobe 1–5px. Sem bounce. `prefers-reduced-motion` desliga entradas e zoom.
