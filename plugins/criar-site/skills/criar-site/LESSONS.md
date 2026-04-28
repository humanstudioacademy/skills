# LESSONS — constituição operacional da skill `/criar-site`

> **Este documento viaja com a skill.** Toda decisão importante de design/processo/UX que essa skill aprendeu (testando, errando, corrigindo) está aqui consolidada. Quando rodar a skill em outra máquina, Claude lê este arquivo + SKILL.md como fonte primária de regras.

> Origem: as memories pessoais de quem desenvolveu a skill (`~/.claude/projects/.../memory/`) registram contexto histórico. Aqui estão **só as regras universais**, válidas pra qualquer projeto que use `/criar-site`.

---

## 1. ARQUITETURA — Matrizes vs Templates

**Os 3 kits NÃO são templates clonáveis. São matrizes estéticas abstratas.** Cada briefing **cunha** seu próprio template-instância sintetizando essas matrizes na proporção declarada.

- **`matrix.primary`** define ANATOMIA (quais componentes principais — Header, Hero, Grid, CTA, Pitch, Gallery, Footer — vêm dessa matriz).
- **`matrix.secondary` / `tertiary`** contribuem com **ingredientes** (token modules específicos, signature slots opt-in).
- **Token modules** (`palette`, `typography`, `spacing`, `motion`, `radius`) — cada uma das 5 vagas escolhe livremente uma das 3 matrizes. Mix livre.
- **Slots signature** (`marquee`, `testimonials`, `specs`, `ornament`, `marker`, `placeholderEditorial`, `carouselControls`) são **opt-in** independente da primary — qualquer briefing pode ativar qualquer signature.
- **Proporção é descritiva, não fórmula**. Briefing declara intenção (ex: "60% Editorial + 30% Clínica + 10% Tech") que **orienta** a escolha de tokens e signatures. Claude decide, usuário aprova.
- `kit.config.ts.rejects` viraram **sinais advisory**, não bloqueios. Se mistura faz sentido coerente, prossegue. Só bloqueia em contradição (ex: tipografia SF Pro Bold com periods + serif romântica contemplativa simultaneamente).

**Sintetizador:** o `composer.py` lê o `briefing.json`, valida, copia componentes da primary, mixa tokens, injeta signatures opt-in. Cada projeto vira um template **único** — não há mais "site Portfolio puro".

---

## 2. LINGUAGEM COM USUÁRIO — Maquinaria invisível

**Presets, `kit.config.ts`, envelope, rejects, taxonomy, preamble, 11 eixos, schema, composer — tudo isso é vocabulário do sistema, não da conversa.** O sujeito que está criando vê **narrativa de marca**, não arquitetura do módulo.

**O que o usuário vê:**
- Análise das refs em linguagem de direção de arte (luz, paleta, materialidade, registro, mood).
- Direção da marca (quem ela é, o que declara).
- Descrição do hero/asset em linguagem de creative director.
- Orçamento limpo.

**O que NÃO aparece na conversa:**
- "O kit Portfolio rejeita warm-palette" — em vez disso: "a marca tem identidade warm editorial".
- "Display font do preset = Big Shoulders Display Black" — em vez disso: "tipografia grotesque condensada massiva".
- Tabelas comparativas de "Kit canônico vs refs".
- Menção a `briefing.json`, `composer.compose_site()`, `tokens.css`, `kit.config.ts`.

Internamente Claude opera com `primary=portfolio-editorial + secondary=clinica-estetica + tokens.palette=clinica`. Externamente diz "studio de arquitetura editorial com paleta autoral warm".

---

## 3. MODOS DE GERAÇÃO — Pergunta na Fase 3.0

**Antes de mensurar orçamento, perguntar literalmente:**

> "Como você prefere gerar as imagens/vídeos do site?
>
> **(A) Modo API** — você linka sua API de geração (Freepik, etc) e eu gero automaticamente em paralelo. Mais rápido, precisa de chave configurada no `.env`.
>
> **(B) Modo Manual** — eu entrego os prompts técnicos finalizados + specs (aspect, modelo sugerido, refs, negative); você gera externamente na plataforma que preferir e me devolve as imagens. Continuo o fluxo a partir daí."

- **Modo A** verifica `hub.has_api_key()`. Se não, orienta colar no `.env`.
- **Modo B** entrega pacote de `.txt` por asset + tabela-guia. Aguarda usuário voltar com arquivos nomeados pelo `id` do asset. Continua pra Etapa 8.
- **Modo Manual NÃO é fallback** — é opção legítima. Skill é agnóstica de engine. Nano Banana é **engine preferido**, não obrigatório (MidJourney/DALL-E/Flux/Imagen funcionam igual no modo manual).
- `hub.py` não exige `FREEPIK_API_KEY` no import (lazy check). Só falha quando alguém tenta chamar API.

---

## 4. PROMPTS TÉCNICOS — 11 eixos da `taxonomy.md`

Todo prompt de imagem/vídeo passa pelo **prompt-engineer** (`prompts/prompt-engineer/`). Régua mínima inviolavel:

- **Inglês técnico sempre.** Português trava qualidade.
- **Zero sintaxe MidJourney.** Nenhum `--ar`, `--v`, `--style`, `--no`, `--stylize`. Nenhum duplo traço.
- **Zero adjetivos vazios.** Banidos: "beautiful", "stunning", "amazing", "high quality", "4K", "8K", "hyperrealistic", "masterpiece", "award-winning". Rigor técnico entrega qualidade — adjetivo não.
- **Paleta restrita** — máximo 3 tons dominantes em HEX, com dominância % declarada.
- **Câmera + lente plausível nomeada** — ARRI Alexa, Hasselblad, Cooke, Zeiss. Stocks (Sony A7) quebram registro premium.
- **Iluminação descrita em termos cine** — key/fill/rim, qualidade (hard/soft/wrapping), Kelvin, modificadores.
- **11 eixos preenchidos sempre** (linguagem visual, cor, luz, câmera, composição, textura, modelo, figurino, cenário, narrativa, coerência). Nenhum vazio. Se faltar dado, engine escolhe plausível.
- **400-900 palavras pra imagem** / **300-700 pra motion**. Curto demais = raso. Longo demais = Nano ignora partes.
- **Vídeo só após imagem-base aprovada.** Engine de motion **herda** ficha da imagem aprovada. Em modo manual = 2 rodadas separadas.
- **Seedance 2.0 duration ∈ {5, 10}.** API constraint. `hub.py` valida.

---

## 5. REFERÊNCIAS VISUAIS — Dois níveis distintos

**Nível A — Calibração interna (`ref-prompt-engeneer/IMAGENS/`):**
- Régua invisível de qualidade que Claude usa pra mensurar densidade técnica dos prompts compostos.
- **NUNCA** vira `reference_images` em chamada de API.
- **NUNCA** é ref de estilo direto pra nenhum projeto.
- **NUNCA** é mencionada por nome/sujeito em prompts gerados.

**Nível B — `visualRefs` do briefing:**
- Refs uploadadas pelo usuário **por projeto**.
- Têm papel duplo:
  - (a) **Norte do briefing** — alimentam destilação de paleta HEX, mood, kit-fit.
  - (b) **Image reference na API** — anexadas como `reference_images` no payload Freepik.
- **Prefixo obrigatório** quando usadas com Nano: prompt começa com `Use the reference images only as aesthetic, compositional, and visual-aspect references to generate the following image:` — senão Nano copia demais. Bug confirmado empiricamente.

Confundir os dois quebra o sistema. Nível A é formação estética interna; Nível B é input real de API.

---

## 6. TIPOGRAFIA E PATTERN GRÁFICO — Sempre via CSS, nunca Nano

**Regra absoluta confirmada empiricamente:**

- **Tipografia massiva no hero** (palavra/frase grande sobreposta à fotografia) → **CSS absolute no Astro**, NÃO embutida no prompt do Nano. Hero gera **sem título**, e `<h1>` em CSS posiciona sobre a imagem com mix-blend-mode opcional.
  - Por que: Nano em 2K **ignora** instrução de tipografia quando frame é fotograficamente complexo. Insistir desperdiça créditos.
  - Exceção: asset **tipográfico puro** (frame inteiro É tipografia, ex: ornament editorial divisor) — Nano renderiza bem.

- **Pattern tiles tipográficos** (monograma `M` repeat, watermark de letra, logo lockup repetido) → **SVG/CSS em código**, NÃO via Nano.
  - Por que: Nano **deforma letterform** (M sai como triângulo desbalanceado) e **erra opacidade** (renderiza full opacity quando se pede 12% watermark).
  - Caminho certo: `background-image: url("data:image/svg+xml,<svg>...<text font-family='X'>M</text></svg>")` com `background-size: 120px` repeat + `opacity: 0.08`.

---

## 7. TEMPLATES MOLDÁVEIS AO CONTEÚDO REAL

**Estrutura do site se adapta ao inventário de assets/conteúdo real disponível.** Nunca preencher seção com placeholder fake pra inflar template.

| Inventário | Layout adequado |
|---|---|
| 1 projeto real | `single-feature` (hero card grande + copy editorial + linha de fechamento "Archive on request") |
| 2-3 projetos reais | `2-col` ou `stacked` |
| 4-6 projetos reais | `3-col` (default) |
| 7+ projetos reais | `3-col` com filtragem por categoria |

- **Nada inventado:** nomes de projetos, clientes, depoimentos, stats — devem ser reais ou seções **somem** / **viram copy editorial** ("More projects in the archive — contact for full portfolio").
- Marcadores alfanuméricos (`(01)`, `(A/05)`) **são signature**, não placeholder fake.
- Antes de escolher variant de componente (`WorkGrid layout`), **verificar inventário real** declarado em `briefing.assetInventory`.

**Componente `PlaceholderEditorial.astro`** existe pra slots quando falta mídia REAL e a estrutura honesta exige aquela posição (ex: hero sem foto disponível ainda) — vira tipografia signature, não "imagem genérica".

---

## 8. CUSTO E COMUNICAÇÃO

- **Sempre mostrar custo estimado antes de chamar API** — zero exceções, mesmo em lotes pré-autorizados.
- **Sempre perguntar aspect ratio + resolução + duração antes de gerar** — zero defaults silenciosos.
- **Mostrar descrição curta do asset em linguagem de DA**, NUNCA o prompt técnico bruto antes da aprovação. Ex: "Vertical 4:5. Retrato 3/4 frontal de diretora criativa em espaço em obra, segurando travertino. Linho cru + wool escuro. Cadeira accent burnt orange ao fundo." — não despejar 800 palavras de inglês técnico.
- **Briefing em 3 fases progressivas:** Identidade (nome/propósito/tom) → Estrutura+Refs+DNA+Ancoragem → Modo+Orçamento+Assets.
- **Registrar custo real pós-execução** em `custos.log` (JSONL).
- **Checkpoint de qualidade pós-geração** — rejeitar genérico e regenerar (máx 2 retries automáticos antes de pedir ajuste ao usuário).

---

## 8.5 DIAGRAMAÇÃO — Pass visual antes de declarar pronto

Após compor `index.astro`, **antes** de declarar o site pronto pro usuário:

- Subir dev server, fazer scroll completo da página, anotar tudo que parece off em diagramação.
- **Spacing entre seções**: cada seção tem respiro coerente, sem esmagar nem deixar vácuo desproporcional.
- **Alinhamento vertical**: rules, headings, conteúdo seguem o mesmo grid em todas as seções.
- **Hierarquia visual por seção**: 1 elemento dominante, suporte secundário em proporção; não deixar elementos competirem.
- **Quebras de linha em headings monumentais**: forçar `<br/>` quando a quebra natural cortar palavras de forma desconfortável.
- **Aspect de cards no grid**: se asset é horizontal (3:2) e card é 4/5 vertical, vai cortar feio — adaptar `cardAspect` em vez de cropar.
- **Footer densidade**: colunas equilibradas, espaço suficiente entre seções de info.
- **Hero proporção**: `min-h-[88vh]` é OK, mas garantir que foto + tipografia respiram nesse height; descontar header se necessário.
- **Grid com órfãos**: 4 cards em `3-col` deixa 1 órfão na 4ª linha — preferir `2-col` ou ajustar inventário.

Ao apresentar o site ao usuário, **antecipar essa preocupação**: "qualquer ajuste de spacing/proporção/alinhamento, me diz que afino". Diagramação é o ponto frágil que usuário detecta primeiro.

---

## 9. PRINCÍPIOS UNIVERSAIS — Camada 1 sempre vence

`prompts/principios/` (8 arquivos) é **Camada 1** — princípios não-negociáveis (composição, tipografia, cor, movimento, qualidade IA, UX/A11y, estrutura site).

**Camada 1 veta Camada 2 (matrizes) e Camada 3 (briefing).** Se um briefing pede algo que viola contraste WCAG, touch targets <44px, ou outro princípio-tótem, **skill recusa ou adapta** — nunca entrega quebrado.

**Validação anti-drift** (rodar ao final da Etapa 8):
- `tokens.css` final só tem propriedades dos 5 módulos selecionados (sem custom properties órfãs).
- `index.astro` só importa de `@components/` da matriz primary OU de signatures explicitamente opt-in.
- `kit.config.ts` da matriz primary não foi violado em decisão dura (advisory ok).
- Contraste WCAG AA validado entre `--color-ink` × `--color-bg` e accent × bg.

---

## 10. SUBAGENTS PARA PARALELISMO

Quando **assets são independentes** (ex: gerar 6 imagens em lote), **spawnar subagent por asset**:
- Cada subagent recebe: prompt + modelo + aspect + caminho de output.
- Chama `hub.gerar_imagem` com `pular_confirmacao=True` (já autorizado no orçamento consolidado).
- Retorna `{path, seed, task_id, custo_real}`.
- Subagents **isolam ruído de logs da API** do contexto principal.

---

## 11. ERROS CONHECIDOS — Tratamentos

| Erro | Ação |
|---|---|
| `400 prompt >3000 chars` | Composer comprime (drops Narrative tone, depois trim de cláusulas redundantes) |
| `400 aspect_ratio inválido` | Usar formato `X:Y` (ex: `16:9`), não `widescreen_16_9` |
| `429 / 402 / 403 free tier` | Pausar, link de billing claro pro usuário, sem retry automático |
| Seedance `duration` rejeitado | `hub.py` valida ∈ {5, 10} antes do POST |
| Geração genérica | Regenerar com mais specs (câmera, lente, luz, HEX); máx 2 retries |
| Tipografia hero malformada | Gerar hero sem tipo embutido, aplicar via CSS (regra 6) |
| Pattern tile tipográfico deformado | Gerar via SVG/CSS, não via Nano (regra 6) |
| Ref visual copiada (Nano) | Faltou prefixo obrigatório (regra 5) |
| Placeholder vazio em work grid | Trocar layout pra `single-feature` ou `2-col` (regra 7) |
| Vite bloqueia tunnel host (`Blocked request`) | Adicionar em `astro.config.mjs` → `vite.server.allowedHosts: ['.trycloudflare.com', '.ngrok.io']` |
| Mix-blend-difference no hero | É override de projeto específico (paleta dark-saturated em fotografia editorial), NÃO default do kit. Hero do kit usa tipo em `var(--color-ink)` com gradient cream sutil opcional |

---

## 12. DEPLOY E COMPARTILHAMENTO

Após `npm run build`:
- **Netlify Drop** (`https://app.netlify.com/drop`) — arrastar pasta `dist/` → URL pública permanente, sem login obrigatório. Recomendado pra demo.
- **Vercel CLI** — `npm i -g vercel && vercel` → URL `*.vercel.app`. Bom pra dominio próprio depois.
- **Cloudflared tunnel** (temporário) — `cloudflared tunnel --url http://localhost:4321`. Expira ao fechar terminal. Bom pra demo de 1-2h. **Lembrar de adicionar `.trycloudflare.com` em `vite.server.allowedHosts`.**

---

## REFERÊNCIA RÁPIDA

- `SKILL.md` — workflow das 9 etapas
- `composer.py` — sintetizador de templates
- `prompt_engineer.py` — helpers de prompt + validador
- `hub.py` — wrapper Freepik (lazy API key)
- `prompts/principios/` — Camada 1
- `prompts/prompt-engineer/` — taxonomy + engines + kit-presets
- `templates/_shared/` — schema + token modules
- `templates/<kit>/` — matrizes (Portfolio Editorial / Clínica Estética / Tech Apple-ish)
- `archive/tests-legacy/` — runners e testes anteriores arquivados

Em caso de dúvida operacional, consultar este `LESSONS.md` antes de inventar comportamento.
