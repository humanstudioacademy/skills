# INSTALL — `/criar-site` skill

Setup passo a passo. Funciona em macOS, Linux e Windows (Git Bash / WSL recomendados pra fluxo mais liso).

---

## Pré-requisitos

| Software | Versão mín. | Como verificar |
|---|---|---|
| **Claude Code CLI** | latest | `claude --version` |
| **Node.js** | 18+ | `node --version` |
| **Python** | 3.10+ | `python --version` |
| **Git** | qualquer recente | `git --version` |

Opcional (modo API):
- Conta Freepik com API ativa → https://www.freepik.com/developers
- Chave Freepik (free tier funciona pros primeiros testes)

Opcional (compartilhar preview pública):
- `cloudflared` pra tunnel temporário → `winget install Cloudflare.cloudflared` (Windows) / `brew install cloudflared` (macOS)
- ou conta Netlify gratuita pra Drop deploy

---

## 1. Clonar o repo

```bash
git clone <url-do-repo>
cd <pasta-do-repo>
```

Estrutura que você terá:

```
.
├── .claude/skills/criar-site/      ← a skill
├── ref-prompt-engeneer/            ← calibração interna do sistema
├── sites/                          ← outputs serão criados aqui
├── README.md
└── INSTALL.md  (este arquivo)
```

---

## 2. (Opcional) Instalar a skill globalmente

Se quiser usar `/criar-site` em qualquer projeto sem ter que clonar de novo:

```bash
# macOS / Linux
mkdir -p ~/.claude/skills
cp -r .claude/skills/criar-site ~/.claude/skills/

# Windows (PowerShell)
mkdir -Force "$env:USERPROFILE\.claude\skills"
Copy-Item -Recurse .claude\skills\criar-site "$env:USERPROFILE\.claude\skills\"
```

A skill também precisa da pasta `ref-prompt-engeneer/` no diretório onde for usada (calibração interna). Copie junto:

```bash
cp -r ref-prompt-engeneer ~/.claude/skills/criar-site/
# ou deixe na raiz do projeto onde vai rodar
```

---

## 3. Instalar deps Python

```bash
pip install -r .claude/skills/criar-site/requirements.txt
```

Isso instala `requests` + `python-dotenv` (deps mínimas do `hub.py` e `composer.py`).

---

## 4. Configurar `.env` (opcional — só se for usar modo API)

Crie `.env` na **raiz do projeto** (não dentro da skill):

```bash
# .env
FREEPIK_API_KEY=sua-chave-aqui
```

**Modo Manual não precisa do `.env`.** Skill detecta a ausência e oferece modo manual automaticamente na Fase 3.

---

## 5. Rodar a skill

Dentro do Claude Code, no projeto onde vai gerar o site:

```
/criar-site
```

A skill conduz a conversa em 3 fases:

1. **Identidade** — nome, propósito, tom
2. **Estrutura + Refs** — seções, refs visuais (paths/URLs), classificação interna de matriz
3. **Modo + Orçamento + Assets** — escolha API ou Manual, assets propostos, custo estimado

Após aprovação, gera os assets, monta o site Astro em `sites/<slug>/`, dá preview local em `localhost:43xx`.

---

## 6. Build de produção e deploy

Após o site rodar localmente:

```bash
cd sites/<slug>
npm run build
```

Output em `dist/`. Pra publicar:

- **Netlify Drop**: `https://app.netlify.com/drop` → arrastar pasta `dist/`. URL pública instantânea.
- **Vercel CLI**: `npm i -g vercel && vercel`. URL `*.vercel.app`.
- **Cloudflare tunnel** (preview ao vivo): `cloudflared tunnel --url http://localhost:4321`. Lembrar de adicionar `.trycloudflare.com` em `astro.config.mjs` → `vite.server.allowedHosts` antes de subir o tunnel.

---

## Troubleshooting

| Sintoma | Causa | Solução |
|---|---|---|
| `Sem chave de API configurada` ao gerar | `.env` ausente ou variável vazia | Configurar `FREEPIK_API_KEY` ou escolher modo Manual |
| `npm install` falha com `ENOSPC` | Disco cheio | Limpar `~/.npm/_cacache` e cache de outros builds |
| `npm install` falha com `parser.ps1 not found` | Quirk do npm em Windows com paths complicados | Tentar com `--no-bin-links` ou rodar dentro de WSL |
| Vite bloqueia `*.trycloudflare.com` ao abrir tunnel | `allowedHosts` restritivo | Adicionar em `astro.config.mjs`: `vite: { server: { allowedHosts: ['.trycloudflare.com'] } }` |
| `429 free tier` ao gerar via API | Free tier Freepik esgotado | Configurar billing no painel ou trocar pra modo Manual |
| Tipografia do hero saiu sem texto | Esperado — hero foto + título via CSS é regra | Tipografia é renderizada via `<h1>` em CSS absolute sobre a imagem, não via Nano. Ver `LESSONS.md` regra 6 |

---

## Onde aprender mais

- **`README.md`** — visão geral do projeto
- **`.claude/skills/criar-site/SKILL.md`** — workflow completo das 9 etapas
- **`.claude/skills/criar-site/LESSONS.md`** — constituição operacional (24 lições aprendidas)
- **`.claude/skills/criar-site/prompts/prompt-engineer/README.md`** — taxonomy de 11 eixos pra prompts cinematográficos
- **`.claude/skills/criar-site/prompts/principios/`** — Camada 1 (princípios universais inviolaveis)

---

## Suporte

Reporte issues / melhorias no repo. Casos especialmente úteis:
- Briefings que travaram a skill em algum ponto
- Sites onde a régua técnica caiu abaixo do esperado
- Combinações de matrizes que não foram testadas (ex: 100% Tech, 60/30/10 três-vias)
