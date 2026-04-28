# /criar-site — skill Claude Code para sites generativos

> Sistema que gera sites estáticos completos (Astro + Tailwind) com imagens/vídeos cunhados por IA, partindo de um briefing conversado. Cada site nasce de uma síntese única de **3 matrizes estéticas** — Portfolio Editorial / Clínica Estética / Tech Apple-ish — combinadas em proporção pelo briefing.

## O que é

Uma skill do [Claude Code](https://docs.claude.com/claude-code) que orquestra:

- **Briefing em 3 fases conversadas** — identidade da marca → estrutura/refs/DNA → modo de geração + orçamento
- **Composer Python** que sintetiza um template-instância único do site (não clone-de-template)
- **Prompt-engineer interno** que destila prompts cinematográficos pro Nano Banana / Seedance 2.0 (taxonomy de 11 eixos + 4 extras pra motion, herdada do KinoImage Generator)
- **Geração via API** (Freepik integrada) **ou modo Manual** (skill entrega prompts, você gera externamente em qualquer plataforma — MidJourney, DALL-E, Flux, Imagen — e devolve as imagens)
- **Build Astro + deploy** (preview local, Netlify Drop, Vercel, ou tunnel Cloudflare)

## O que entrega

- 1 site completo por projeto: HTML + CSS + JS + assets de IA
- ~5-7 imagens/vídeos sob régua técnica editorial (paleta restrita, materialidade tátil, luz cinematográfica)
- Tokens compostos misturando 5 módulos (palette/typography/spacing/motion/radius) das 3 matrizes
- Slots signature opt-in (marquee, testimonials, specs, ornament) ativados pelo briefing

## Status

**Fase 2 da skill — completa.** Pronta pra teste e stress por terceiros.

- ✅ Skill end-to-end funcional
- ✅ Composer testado (validação de matrizes + cópia + mix de tokens + signatures cross-matrix)
- ✅ 24 lições consolidadas em `.claude/skills/criar-site/LESSONS.md` (constituição operacional)
- ⚠️ Validação visual com `npm run build` requer espaço em disco (lembrar de checar antes do primeiro uso)

## Estrutura do repo

```
.
├── .claude/skills/criar-site/         ← a skill em si
│   ├── SKILL.md                         ← workflow das 9 etapas
│   ├── LESSONS.md                       ← constituição operacional (regras universais)
│   ├── composer.py                      ← sintetizador de templates
│   ├── hub.py                           ← wrapper API Freepik (lazy key)
│   ├── prompt_engineer.py               ← helpers + validador
│   ├── prompts/
│   │   ├── principios/                  ← Camada 1 (universais inviolaveis)
│   │   └── prompt-engineer/             ← taxonomy + engines + kit-presets
│   ├── templates/
│   │   ├── _shared/                     ← briefing-schema + 15 token modules
│   │   ├── portfolio-editorial/         ← matriz 1
│   │   ├── clinica-estetica/            ← matriz 2
│   │   └── tech-apple/                  ← matriz 3
│   └── archive/                         ← runners e testes históricos
├── ref-prompt-engeneer/                 ← calibração interna (NUNCA é input de API)
├── sites/                               ← outputs gerados
└── INSTALL.md                           ← setup
```

## Quick start

### Opção A — Instalação via plugin (recomendado)

Dentro do Claude Code (CLI ou Desktop):

```
/plugin marketplace add SEU-USER/SEU-REPO
/plugin install criar-site@human-studio
```

Depois, no projeto onde for usar:

```bash
# Deps Python
pip install requests python-dotenv

# (Opcional) API key da Freepik
echo "FREEPIK_API_KEY=sua-chave" > .env
```

Invocar no Claude Code:

```
/criar-site
```

### Opção B — Instalação manual

Veja **[INSTALL.md](INSTALL.md)** pra clone direto da pasta `.claude/skills/criar-site/`.

## Filosofia da skill

1. **Matrizes, não templates.** Os 3 kits são DNAs abstratos. Cada briefing **cunha** seu próprio template-instância sintetizando matrizes.
2. **Maquinaria invisível.** Usuário conversa em linguagem de marca. Vocabulário interno (preset, envelope, schema, taxonomy) nunca vaza pra conversa.
3. **Templates moldam ao conteúdo real.** 1 projeto real = single-feature, não 6 cards fake. Nada inventado.
4. **Tipografia hero via CSS, sempre.** Pattern tipográfico via SVG/CSS, sempre. IA não renderiza letterform editorial confiável.
5. **Régua técnica inviolavel.** 11 eixos da taxonomy preenchidos em todo prompt. Zero adjetivo vazio. Inglês técnico cinematográfico.
6. **Modo agnóstico.** Freepik é engine preferido, não obrigatório. Modo manual entrega prompts pra qualquer plataforma de geração.

Detalhes completos em `.claude/skills/criar-site/LESSONS.md`.

## Licença / uso

Uso livre pra projetos pessoais e comerciais. Sem garantias.

A skill foi destilada de várias sessões reais de desenvolvimento de sites — agradeço feedback (issues, PRs, mensagens) com casos onde quebra ou onde poderia ser melhor.
