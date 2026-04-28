# SHARING — distribuir e coletar feedback

Guia operacional de como entregar essa skill pra outras pessoas testarem e o que pedir como retorno.

---

## 1. O que entregar

**Pacote completo** = `criar-site-skill-v1.zip`. Tem dentro:

- `.claude/skills/criar-site/` — a skill em si (workflow + composer + prompt-engineer + 3 matrizes + LESSONS.md)
- `ref-prompt-engeneer/` — pasta de calibração interna (vazia + README orientando o usuário a popular)
- `sites/` — vazia, será preenchida pelo uso
- `README.md` — visão geral
- `INSTALL.md` — setup passo a passo
- `SHARING.md` — este arquivo
- `.env` — template comentado (sem chave)

**Tamanho:** ~500KB zipado, ~630KB descompactado.

---

## 2. Quem testar

Perfil ideal de tester:
- Tem Claude Code instalado e familiaridade básica
- Tem Node.js 18+ e Python 3.10+ instalados
- Já criou pelo menos 1 site/landing antes (pra ter referencial de qualidade)
- Disponível pra ~2-3h de teste end-to-end (briefing → site no ar)
- Pode dar feedback estruturado (não só "ficou bom")

Bons casos de teste:
- Designer freelancer que monta landing pages de cliente
- Studio criativo pequeno
- Dev front-end que faz sites pessoais/portfolio
- Profissional de marketing que precisa de microsite por campanha

---

## 3. Briefing pra mandar junto com o ZIP

Cole/adapte o texto abaixo no canal de envio (WhatsApp, email, Telegram):

> **Olá!** Esta é uma skill do Claude Code que gera sites estáticos completos a partir de um briefing conversado. Você invoca `/criar-site` no Claude Code e ela conduz: identidade da marca → estrutura+refs → modo de geração+orçamento → produz o site.
>
> **Pra rodar:** descompacta o ZIP num projeto novo (ou move `.claude/skills/criar-site/` pra `~/.claude/skills/` pra deixar global), segue o `INSTALL.md`, abre o Claude Code dentro do projeto e digita `/criar-site`.
>
> **O que eu queria que você testasse:**
> 1. Faça **um site real seu** (projeto pessoal, freelancer, conceito) — não site fictício.
> 2. Use **modo Manual** no começo (sem precisar de API Freepik) — a skill entrega prompts e você gera as imagens onde preferir (MidJourney, DALL-E, Flux, web Freepik). Se tiver chave Freepik, pode testar modo API depois.
> 3. **Cronometre tempo total** (do `/criar-site` ao site no ar) — queria comparar com tua estimativa de fazer manual.
> 4. Anote **onde travou** ou ficou confuso — esses são os pontos mais valiosos.
>
> **Feedback que mais quero:**
> - O briefing conversado fez sentido? Onde foi vago/confuso?
> - A síntese visual do site bateu com o que você imaginava do briefing? Onde ficou off?
> - Os prompts gerados (modo Manual) deram resultados editoriais bons na ferramenta que você usou? Ou saíram genéricos?
> - **Diagramação** — alinhamentos, spacing, hierarquia visual: tava ok ou precisou muitos ajustes?
> - O que você esperava que rolaria diferente?
>
> Sem pressa. Pode mandar feedback por mensagem mesmo, ou abrir um doc compartilhado se quiser estruturar.

---

## 4. Canais de distribuição (escolha o que serve)

**Pessoal e direto:**
- WhatsApp / Telegram com o ZIP anexado + briefing acima
- Drive/Dropbox compartilhado com link

**Estruturado pra grupo:**
- GitHub privado com convite pra testers (eles clonam, leem README, abrem issues com feedback)
- Notion/Linear board onde testers reportam achados

**Público (depois de validado com 3-5 testers):**
- Repo GitHub público com README comprehensive
- Post em X/Twitter / LinkedIn / Reddit r/ClaudeAI mostrando 1-2 sites gerados como showcase
- Anthropic Discord channel `#skills` (se existir)

---

## 5. Template de feedback estruturado

Mande junto pra cada tester preencher:

```
**Tester:** [nome]
**Projeto que tentou fazer:** [tipo de site]
**Modo usado:** API / Manual

### Tempo total
- Briefing: __min
- Composição de prompts: __min
- Geração de assets: __min
- Composição do site: __min
- Iterações: __ ajustes
- TOTAL: ~__h

### Onde travou ou ficou confuso
- [pontos]

### Resultado final
- Site URL: [link Netlify Drop / Cloudflare tunnel / Vercel]
- Qualidade percebida vs imaginado: [escala 1-5 + comentário]

### Diagramação
- Alinhamentos / spacing / hierarquia: [comentário específico]

### Prompts gerados (modo Manual)
- Plataforma usada: [MidJourney / DALL-E / Flux / Freepik web / etc]
- Resultados: [editorial bom / genérico / inconsistente]

### O que faltou ou faria diferente
- [pontos]

### Você usaria isso de novo? Em que cenário?
- [resposta]
```

---

## 6. Como categorizar o feedback que volta

- **Bugs reais (skill quebra)** — prioridade máxima, fix imediato
- **Confusão de fluxo** — refinar perguntas/explicações na skill
- **Régua de qualidade caindo** — popular `ref-prompt-engeneer/` com mais refs ou refinar `taxonomy.md`
- **Variantes/casos não cobertos** — adicionar suporte na próxima versão
- **Pedidos cosméticos** — backlog

Versionar:
- `v1.0.0` — release inicial
- `v1.1.0` — patches de bug + refinamentos pequenos pós-feedback
- `v2.0.0` — novas matrizes / novas variantes / composer mais sofisticado

---

## 7. Expectativa honesta — comunique aos testers

**O que essa versão entrega bem:**
- Briefing conversado claro e estruturado
- 3 matrizes estéticas com identidades distintas
- Composição híbrida funcional (matriz primary + tokens mixados + signatures opt-in)
- Prompts cinematográficos com régua técnica clara
- Site Astro estático buildável + deployable

**Onde provavelmente vai aparecer fricção:**
- **Diagramação** — Claude faz pass visual mas pode escapar detalhes (alinhamento de uma seção, proporção de card)
- **Casos limite de mistura 3-way** — testes empíricos foram principalmente 2-way
- **Modo Manual** depende muito da plataforma de geração externa que o tester usar — se a ferramenta dele não respeita prompts cinematográficos longos, qualidade cai
- **Composer e Astro em Windows** com paths complicados (espaços, acentos) — pode dar `npm install` quirks; recomendar Git Bash ou WSL

**Onde NÃO entrega ainda (ser honesto upfront):**
- Sites multi-página (só single-page por enquanto)
- E-commerce / forms reais (CTAs são `mailto:` ou links externos)
- CMS / conteúdo dinâmico
- Internacionalização
- Vídeos (suporte existe mas validação visual ainda é leve)

Comunique essas limitações no convite — economiza frustração.

---

## 8. Privacidade dos testers

- Nenhum tester precisa compartilhar conteúdo proprietário com você. Os sites que ele gerar ficam **na máquina dele**.
- Logs de custo (`custos.log`) ficam locais — você não tem acesso.
- Quando ele te mandar feedback ou link de demo, é decisão dele compartilhar URL pública.
- Se ele rodar em modo API, a chave Freepik dele fica no `.env` local — nada vaza.
