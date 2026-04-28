---
name: criar-site
description: Gera site responsivo completo com imagens e vídeos de IA (Nano Banana + Seedance 2.0 via Freepik API), aplicando princípios universais de design e um dos 3 kits opinionados (Portfolio Editorial / Clínica Estética / Tech Apple-ish). Usuário invoca para criar um site end-to-end com briefing, assets generativos e preview local.
---

# /criar-site — Orquestrador end-to-end

## Propósito

Esta Skill cria um site completo (HTML + CSS + JS + assets de IA) a partir de um briefing do usuário, aplicando:

- **Camada 1** — Princípios universais não-negociáveis (`prompts/principios/`)
- **Camada 2** — 1 dos 3 **kits opinionados** em `templates/` — cada kit é um projeto Astro próprio com `kit.config.ts` definindo editáveis, variants e envelope de rejects. Os kits são: Portfolio Editorial, Clínica Estética, Tech Apple-ish
- **Camada 3** — Personalização por briefing (este workflow — preenche os `editableTokens` do kit escolhido)

---

## Quando ativar

Usuário:
- Digita explicitamente `/criar-site`
- Pede "gerar site com IA", "criar landing page completa", "montar site com imagens/vídeos generativos"

**Não ativar automaticamente** em pedidos parciais (ex: "gera só uma imagem"). Nesses casos, usar `hub.py` diretamente.

---

## Pré-requisitos (verificar antes de iniciar)

1. `.env` na raiz do projeto contém `FREEPIK_API_KEY` válida
2. Dependências Python instaladas (`pip install -r requirements.txt` a partir da raiz da skill)
3. Todos os 8 arquivos de `prompts/principios/` existem (index + 01-07)
4. Os 3 kits existem em `templates/`:
   - `templates/portfolio-editorial/` (kit 1 — grotesque condensada + 1 accent saturada + ritmo declarativo)
   - `templates/clinica-estetica/` (kit 2 — serif expressiva + muted quente + retratos + ornamentos orgânicos)
   - `templates/tech-apple/` (kit 3 — sans geométrica bold + produto flutuante + light/dark variant)
   - Cada kit contém `kit.config.ts` com `editableTokens`, `componentVariants` e `rejects`
5. Node.js ≥ 18 instalado (`node --version`)

Se algum pré-requisito falhar, abortar com mensagem clara e orientação.

---

## Workflow em 9 etapas

### Etapa 1 — Briefing faseado em 3 fases (progressive disclosure)

**Fase 1 — Identidade do projeto** (as 3 perguntas juntas):
1. **Nome do projeto** (real ou codinome)
2. **Propósito** (landing / portfolio / institucional / produto / evento)
3. **Público & tom de voz** (pra quem + como se comunica — corporate / punk / luxury / editorial / próprio)

**Fase 2 — Estrutura e estética** (após resposta da Fase 1):
4. **Seções desejadas** (propor set padrão baseado no propósito; usuário ajusta) — OU usuário pede "sugira"
5. **Referências visuais (`visualRefs`)** — pedir ao usuário que cole caminhos locais ou URLs de **2 a 6 imagens** que representam o território estético desejado. **Papel duplo dessas refs:**
   - **(a) Norte do briefing** — a skill **lê** cada ref e decupa em descritores técnicos observáveis (paleta HEX, luz, composição, materialidade, mood, tipo de grão). Esses descritores alimentam a Fase 2.5 e a escolha de kit — não é só "moodboard ornamental".
   - **(b) Image reference na API** — as mesmas imagens são anexadas como `reference_images` no payload Freepik durante a geração (Etapa 5). Nano Banana aceita image refs nativamente.
   - Opcional (mas fortemente recomendado) — sem refs, a skill opera só no texto e a precisão estética cai.
   - Salvar paths/URLs em `briefing.json` no campo `visualRefs`.
6. **Classificação interna do DNA** (NÃO exposta ao usuário em vocabulário de kit):
   - **Lê as refs visuais + resposta Fase 1** e identifica **silenciosamente**:
     - **DNA principal** (estrutura, tipografia, layout, ritmo) — 1 dos 3 territórios cardinais
     - **DNA secundário** (paleta, mood, tratamento de imagem) — 1 diferente, opcional
     - **Proporção estimada** (ex: 80/20, 70/30, 100/0)
   - Os 3 territórios cardinais (vocabulário interno):
     - **Portfolio Editorial** — estrutura editorial, grotesque condensada, ritmo declarativo
     - **Clínica Estética** — wellness editorial, serif expressiva, muted quente, ritmo respirado
     - **Tech Apple-ish** — product showcase, sans geométrica bold, paleta fria, precisão cinematic
   - **Regras de hibridização:**
     - Se refs/briefing apontam para um território dominante forte, registra weight=100 (projeto puro).
     - Se refs/briefing mostram tensão entre dois territórios (ex: estrutura editorial + paleta warm muted), registra mistura com proporção — isso é regra, não exceção.
     - `rejects` de cada preset vira **sinal advisory, não bloqueio**: se o conflito pode ser resolvido por mistura consciente, prossegue.
     - Só **redireciona/pausa** quando a mistura resulta em contradição coerente (ex: pedir serif romântica contemplativa com tagline declarativa bold com periods).

7. **Traduzir a classificação pra linguagem de marca** (exposta ao usuário):
   - Em vez de "seu projeto é Portfolio Editorial 80% + Clínica 20%", dizer:
     > "Pelas refs e o briefing, vejo um studio editorial com paleta autoral warm — estrutura gráfica bold dialoga com fotografia de materialidade natural. Tipografia grotesque condensada + paleta cream/wood/terracotta + retratos humanos em contexto de material."
   - **Toda narrativa usa linguagem criativa** (direção de arte, mood, registro), nunca vocabulário do módulo.
   - O usuário confirma, ajusta ou redireciona **pela lente criativa**. Internamente, ajustes viram updates na proporção ou troca de DNA primary/secondary.

8. **Parâmetros específicos do projeto** (expostos como escolhas criativas, não tokens de kit):
   - Paleta final em HEX (3 tons dominantes com proporção) — proposta com base nas refs, confirmada pelo usuário.
   - Tipografia display + body — proposta com famílias nomeadas, nunca "opção 3 do preset".
   - Accent específico do projeto quando pertinente.
   - Tudo apresentado como "a marca usa X", não "o kit expõe token Y".

**Fase 2.5 — Ancoragem conceitual** (sub-perguntas específicas ao tipo de projeto):
- 4-6 perguntas direcionadas extraem referências concretas (período, obras-âncora, locações, figuras humanas, palette override)
- Formato múltipla escolha curta quando possível pra reduzir fadiga
- Evita descrições genéricas no Fase 3
- Ver `feedback_ancoragem_conceitual.md` em memory pra templates por tipo de projeto

**Fase 3 — Modo de geração + Orçamento + Assets** (eu proponho, usuário aprova):

**Fase 3.0 — Modo de geração** (PERGUNTA ANTES DE QUALQUER ESTIMATIVA DE CUSTO):

> "Como você prefere gerar as imagens/vídeos do site?
>
> **(A) Modo API** — você linka sua API de geração (Freepik, etc) e eu gero automaticamente em paralelo. Mais rápido, mas precisa de chave configurada.
>
> **(B) Modo Manual** — eu te entrego os prompts técnicos já finalizados + specs (aspect ratio, modelo sugerido, negative prompt); você gera externamente na plataforma que preferir (web UI Freepik, MidJourney, DALL-E, etc) e me devolve as imagens. Continuo o fluxo a partir daí."

- Se **A**: verificar se há chave configurada (`hub.has_api_key()`). Se sim, prosseguir. Se não, orientar a colar no `.env` na raiz do projeto.
- Se **B**: skill pula a geração automatizada. Após a Fase 3, em vez da Etapa 7 (geração via subagents), entrega o pacote de prompts compostos e aguarda usuário voltar com os arquivos. Ver **Etapa 7-Manual** abaixo.

**Fase 3.1 — Proposta de assets:**
7. **Com base em TUDO coletado (incluindo ancoragem)**, proponho lista concreta de assets: quantidade + tipos + modelos **sugeridos** + aspect ratios + descrições **específicas**. Em modo manual, sugerir o modelo ainda é útil — orienta o usuário na plataforma externa.

**Fase 3.2 — Orçamento estimado:**
8. **Apresento custo estimado consolidado** (`hub.orcamento_lote`). Em modo manual, o custo é **referência** — usuário paga diretamente na plataforma dele, não pela nossa API. Mesmo assim mostrar pra ele saber o tamanho do comprometimento.

**Fase 3.3 — Aprovação:**
9. Usuário aprova, ajusta (adicionar/cortar, trocar modelo), ou cancela.

**Importante sobre vídeos:** quantidade decidida aqui, mas **vídeos só são gerados APÓS aprovação das imagens-base** (ver Etapa 7). Cf. `feedback_video_apos_imagem.md`.

Salvar briefing completo em `sites/{slug-do-projeto}/briefing.json` ao fim da Fase 3.

### Etapa 2 — Carregar princípios + kit escolhido

Ler **apenas** os arquivos necessários pra economizar contexto:

- `prompts/principios/index.md` (sempre — traz princípios-tótem)
- `prompts/principios/01-composicao.md`
- `prompts/principios/07-estrutura-site.md`
- `prompts/principios/05-qualidade-ia.md`
- `templates/{kit-escolhido}/kit.config.ts` (editableTokens + componentVariants + rejects + structuralDefaults)
- Listar `templates/{kit-escolhido}/src/components/sections/` — inventário de seções disponíveis no kit

Princípios de tipografia, cor, movimento e UX serão carregados **sob demanda** durante etapas específicas (ex: tipografia na Etapa 8 ao gerar tokens).

### Etapa 3 — Planejar arquitetura do site

Com base em briefing + princípios + **vocabulário do kit escolhido**, produzir plano estrutural:

- Lista ordenada de seções — **mapeadas para componentes reais** de `templates/{kit}/src/components/sections/` (não inventar seções fora do inventário do kit)
- Para cada seção: componente + variant (quando o componente expõe prop de variação — ex: `Hero variant="monumental-word"` no Portfolio)
- Para cada seção: tipo de asset (imagem / vídeo / só tipografia)
- Hierarquia de CTAs (UM dominante por fold, secundários subordinados)
- Estrutura de navegação (5-7 itens máx)
- Footer editorial com metadata real

**Default sensato**: seguir `kit.config.ts.structuralDefaults.sectionOrder` como ponto de partida. O briefing customiza — não reinventa.

**Gate de confirmação**: mostrar plano ao usuário em tabela clara (coluna "Componente" ao lado de "Seção"). Aguardar aprovação ou ajuste antes de seguir.

### Etapa 4 — Planejar assets (perguntar parâmetros)

Para cada asset identificado no plano, **perguntar ao usuário** (obrigatório, sem defaults silenciosos):

- **Aspect ratio** (opções válidas Freepik: `1:1`, `2:3`, `3:2`, `4:3`, `3:4`, `5:4`, `4:5`, `16:9`, `9:16`, `21:9`)
- **Modelo/resolução**:
  - Imagem: `gemini-2-5-flash-image-preview` / `nano-banana-pro-1k|2k|4k` / `nano-banana-pro-flash-1k|2k|4k`
  - Vídeo: `seedance-lite-720p|1080p` / `seedance-pro-720p|1080p`
- **Duração** (só vídeo, 5-8s padrão)
- **Briefing contextual específico** (sujeito, ação, ambiente)

Sugerir padrão sensato por tipo de asset, mas sempre confirmar com usuário.

### Etapa 5 — Gerar prompts técnicos via módulo `prompt-engineer`

Prompts **não** são mais montados inline nesta etapa. Toda geração passa pelo módulo `prompts/prompt-engineer/` (relativo à raiz da skill) — ver `prompts/prompt-engineer/README.md`.

**Pipeline obrigatório por asset:**

1. **Carregar kit preset** — ler `prompts/prompt-engineer/kit-presets/{kit-escolhido}.md` e extrair o preamble formal + specs técnicas (câmeras, lentes, luz baseline, grain profile, palavras-âncora, rejects).

2. **Destilar ficha estética** a partir do briefing:
   - Paleta HEX + descritores nomeados
   - Mood one-liner (da Fase 1)
   - Sujeito/contexto do asset
   - Beat narrativo (1 frase)
   - `visualRefs` paths (da Fase 2)

3. **Invocar engine correspondente**:
   - Imagem (Nano Banana) → `hub.render_image(asset, kit, brief, visualRefs)`
   - Vídeo (Seedance) → `hub.render_motion(asset, kit, brief, motion, sourceImage)` — vídeo **só depois da imagem-base aprovada** (regra de ouro)
   - O engine aplica os **11 eixos** da taxonomy (+ 4 extras pra motion), inclui prefixo obrigatório `"Use the reference images only as aesthetic, compositional, and visual-aspect references to generate the following image:"` quando `visualRefs.length > 0`, e cospe `(prompt, negative)` prontos pra API.

4. **Salvar** prompts gerados em `sites/{projeto}/prompts-gerados/{asset-name}.txt` pra rastreabilidade.

5. **Validar densidade técnica** — se o engine retornar prompt abaixo da régua (sem os 11 eixos preenchidos, sem HEX na paleta, sem câmera/lente declarada, com adjetivo banido), regenerar. Máx 2 retries antes de pedir ajuste ao usuário.

**Validação de limite:** cada prompt deve caber em 3000 chars antes do `hub.py` comprimir. Tamanho alvo do engine: 400-900 palavras pra imagem, 300-700 pra motion.

**Régua mínima:** nenhum prompt cai abaixo da densidade das refs visuais em `ref-prompt-engeneer/IMAGENS/`. Se cair, o engine falha visivelmente — não mascarar com retry genérico.

### Etapa 6 — Consolidar orçamento e confirmar

Chamar `hub.orcamento_lote()` com lista completa. Apresentar:

```
┌─────────── ORÇAMENTO DO SITE ───────────
│ {Nome do projeto}
├──────────────────────────────────────────
│ [breakdown detalhado por asset]
├──────────────────────────────────────────
│ TOTAL ESTIMADO: $X.XXXX
│ Gasto acumulado histórico: $Y.YYYY
│ Saldo free tier restante: ~$Z.ZZZZ
└──────────────────────────────────────────

Confirma gerar? [s/N]
```

Se usuário recusar:
- Oferecer opções: downgrade de modelo, cortar asset opcional, reduzir duração de vídeo
- Recalcular e reapresentar

### Etapa 7 — Gerar assets

Ramifica conforme o **modo declarado na Fase 3.0**:

#### Etapa 7-API (modo automatizado)

- **Spawnar um subagent por asset** usando Agent tool.
- Cada subagent recebe: prompt + modelo + aspect_ratio + duration (se vídeo) + caminho de output.
- Subagent chama `hub.gerar_imagem()` ou `hub.gerar_video()` com `pular_confirmacao=True` (já autorizado no orçamento consolidado).
- Subagent baixa o arquivo e retorna apenas `{path, seed, task_id, custo_real}`.
- Subagents isolam ruído de logs da API do contexto principal.
- Fallback: se geração de 1 asset falhar após 2 retries, notificar usuário sem abortar lote inteiro.

#### Etapa 7-Manual (modo externo)

1. **Gravar pacote de prompts** em `sites/{projeto}/prompts-gerados/` — um `.txt` por asset, cada arquivo contém:
   - `id` do asset
   - `aspect_ratio` final
   - `modelo` sugerido (apenas referência, usuário pode usar outro)
   - `PROMPT` (bloco corrido em inglês técnico, com prefixo obrigatório se há `visualRefs`)
   - `NEGATIVE` (string de proibições)
   - Lista de `visualRefs` (paths relativos pra `sites/{projeto}/refs/`) que devem ser anexadas externamente, se a ferramenta suportar.

2. **Entregar ao usuário uma tabela-guia** com: id · aspect · modelo sugerido · refs a anexar · caminho do `.txt` pra copiar-e-colar.

3. **Aguardar o usuário subir os arquivos gerados** — pedir que ele crie uma pasta, gere externamente (Freepik web, MidJourney, DALL-E, etc), e coloque as imagens com **nome idêntico ao id do asset** (ex: `01-hero.png`, `02-still.png`).

4. **Ao receber os arquivos**: validar que todos os ids esperados estão presentes. Mover pra `sites/{projeto}/public/assets/` com nomes limpos. Registrar no `seeds.json` com `source: manual` (não tem `task_id` nem `seed` da nossa API — anotar a ferramenta usada se o usuário quiser rastrear).

5. **Validar densidade técnica visualmente** (o Claude lê as imagens recebidas e checa: paleta bate com briefing? composição editorial? materialidade densa? Se qualquer asset cai abaixo da régua, pedir regeneração externa com ajuste no prompt).

6. Seguir pra Etapa 8 (assembly) igual ao modo API.

**Importante — vídeo em modo manual:** o briefing pode incluir vídeos, mas só entregamos prompt de vídeo **depois** da imagem-base ser aprovada (regra inviolável). Em modo manual, isso significa: fluxo de 2 rodadas — primeiro recebe as imagens, aprova, depois entrega prompts de vídeo, usuário gera externamente, sobe os arquivos.

### Etapa 8 — Composição do site via Composer (matrizes → template único)

**Princípio-tótem (Fase 2 da skill):** cada kit é uma **matriz estética** abstrata. Cada briefing **cunha** um template-instância único combinando matrizes em proporção. **Não há mais clone-de-template** — há síntese pelo `composer.py`.

O briefing produz um JSON conforme `templates/_shared/briefing-schema.ts` declarando:
- `matrix.primary` — define ANATOMIA (componentes principais)
- `matrix.secondary` / `tertiary` — opcionais, contribuem com ingredientes
- `tokens.{palette, typography, spacing, motion, radius}` — cada um vem de uma das 3 matrizes (mix livre)
- `slots` — dados pra cada seção principal (header, hero, pitch, grid, cta, footer, gallery)
- `signatureSlots` — opt-in de elementos signature (marquee, testimonials, specs, ornament) de qualquer matriz
- `assetInventory` — quantidade real de projetos/assets pra ajustar layout (single-feature vs grid)

**Composer orquestra:**

```python
from composer import compose_site, report_composition
print(report_composition(briefing))    # mostra ao usuário a síntese
out = compose_site("sites/<slug>/briefing.json")
```

O composer:
1. Valida o briefing (matriz primary válida, hero.style ∈ variantes da primary, tokens apontam pra matrizes válidas)
2. Cria `sites/<slug>/`
3. Copia `package.json`, `astro.config.mjs`, `tsconfig.json`, `public/` da matriz primary
4. Copia `src/` da primary (BaseLayout + components + scripts + styles base)
5. **Sobrescreve `src/styles/tokens.css`** com a composição mixada (5 token modules das matrizes escolhidas, dentro de um único `@theme {}`)
6. Adiciona componentes signature opt-in das outras matrizes (ex: Marquee do Portfolio mesmo se primary é Clínica)
7. Persiste `briefing.json` + `.composer-meta.json` no projeto pra rastreabilidade

**Após o composer:**

8. Compor `src/pages/index.astro` referenciando os componentes copiados, ordem definida em `briefing.sectionOrder`, props vindas dos `briefing.slots`. Cada seção é um componente da matriz primary (ou signature opt-in) com props traduzidas.
9. Aplicar tipografia hero **via CSS** sobre a foto (regra inviolavel — Nano nunca renderiza tipo embutido em hero fotográfico).
10. Gerar metadata SEO (`<title>`, `<meta description>`, OG tags, sitemap, robots).
11. Executar checklist de acessibilidade (`06-ux-acessibilidade.md`): WCAG AA, touch ≥ 44px, focus-visible, alt text.

**Validação anti-drift:**
- Verificar que `tokens.css` final só tem propriedades dos 5 módulos selecionados (sem custom properties órfãs).
- Verificar que `index.astro` só importa de `@components/` da matriz primary OU de signatures explicitamente opt-in.
- Verificar que o `kit.config.ts` da matriz primary não foi violado (rejects continuam advisory, mas se algum bloqueio duro aparecer, parar).
- Se qualquer falhar, parar e corrigir antes da Etapa 9.

Com todos os assets baixados:

1. **Copiar kit escolhido** de `templates/{kit}/` → `sites/{projeto}/`
   - Inclui: `kit.config.ts`, `src/**/*`, `public/**/*`, `package.json`, `astro.config.mjs`, `tsconfig.json`, `.gitignore`
   - NÃO incluir: `node_modules/`, `dist/`, `.astro/`

2. **Sobrescrever `src/styles/tokens.css`** com overrides do briefing:
   - **Apenas** os tokens listados em `kit.config.ts.editableTokens` podem ser sobrescritos
   - Resolver referência → valor: se briefing disse `accent: 'cadmium-red'`, pegar hex de `editableTokens.accent.presets[name='cadmium-red'].value`
   - Para fonts: resolver `editableTokens.displayFont.options[choice].stack` e substituir `--font-display`
   - Respeitar `03-cor.md` (máx 4 cores ativas, contraste WCAG AA), `02-tipografia.md` (base 16, razão modular do kit), `04-movimento.md` (múltiplos de 200ms)
   - NUNCA sobrescrever tokens fora do envelope — se briefing pediu algo fora, já redirecionamos na Etapa 1 Fase 2

3. **Atualizar `BaseLayout.astro`** se briefing trocou fonts:
   - O kit já declara `<link href="https://fonts.googleapis.com/css2?family=...">` com TODAS as options do kit pré-carregadas. Normalmente não precisa trocar.
   - Se briefing pediu mono opt-in no Tech Apple-ish, confirmar que a família mono do briefing está na URL de fonts (já está por default).

4. **Compor `src/pages/index.astro`** com as seções do plano:
   - Para cada seção do plano, importar o componente correspondente de `@components/sections/`
   - Passar as props definidas no plano — incluindo `variant` quando o componente aceita (ex: `<Hero variant="monumental-word" word="BRAND" ... />`)
   - Injetar copy + paths de assets gerados em `public/assets/`
   - NÃO usar componentes fora do inventário do kit. Se uma seção do plano não tem componente correspondente no kit, voltar à Etapa 3 e replanejar — nunca criar componente ad-hoc que quebra o arquétipo

5. **Gerar metadata**:
   - `<title>` + `<meta description>` únicos derivados do briefing
   - Open Graph tags
   - `sitemap.xml` + `robots.txt`

6. **Executar checklist final** (de `06-ux-acessibilidade.md`):
   - Contraste WCAG AA validado (usar `--color-ink` vs `--color-bg` do kit + accent vs bg quando accent é CTA)
   - Touch targets ≥ 44px
   - Focus visível em todos elementos interativos (o `global.css` do kit já tem `:focus-visible` com accent)
   - Imagens com alt text
   - Performance estimada dentro dos budgets

**Validação anti-drift** (executar ao final da Etapa 8):
- Verificar que o `tokens.css` final não tem cor fora de `editableTokens.*.presets` nem fonts fora de `editableTokens.*.options`
- Verificar que `index.astro` só importa de `@components/sections/` e `@components/base/` do kit
- Verificar que nenhuma prop passada a um componente usa valor fora do enum de `componentVariants`
- Se qualquer uma falhar, parar e corrigir antes da Etapa 9

### Etapa 8.5 — Matriz de variação garantida

Dois sites com o **mesmo kit** precisam parecer **distintos visualmente**. Garantir ao menos 2 destes dimensões diferentes entre dois briefings do mesmo kit:

- Accent color (Portfolio, Tech)
- Display font (todos os kits)
- Paleta (Clínica)
- Hero variant (todos)
- Mode light/dark (Tech)
- Section order (todos — `structuralDefaults.sectionOrder` é sugestão, não camisa)
- Copy tone (briefing)
- Assets gerados (sempre únicos por seed)

Se um novo briefing coincide com um site anterior em mais de 3 dimensões, forçar divergência no briefing.

### Etapa 9 — Preview e entrega

1. `cd sites/{projeto}/ && npm install && npm run dev`
2. Abrir browser em `http://localhost:4321`
3. Apresentar relatório ao usuário:
   - Total de assets gerados
   - Custo real (lendo `custos.log`)
   - Arquivos principais + paths
   - Seeds documentados em `sites/{projeto}/seeds.json`
4. Oferecer próximos passos:
   - Regenerar asset específico (com mesmo seed ou seed novo)
   - Ajustar copy
   - Build de produção (`npm run build`)
   - Orientação de deploy (Vercel, Netlify, static)

---

## Estrutura de arquivos que esta Skill produz

```
sites/{slug-projeto}/
├── briefing.json                    (Etapa 1)
├── plano-arquitetura.json           (Etapa 3)
├── prompts-gerados/                 (Etapa 5)
│   └── {asset-name}.txt
├── seeds.json                       (Etapa 7)
├── public/assets/                   (Etapa 7 — mídia gerada)
│   ├── hero.png
│   ├── bg-loop.mp4
│   └── ...
├── src/                             (Etapa 8 — Astro)
│   ├── pages/index.astro
│   ├── components/
│   ├── layouts/
│   └── styles/tokens.css
├── package.json
└── astro.config.mjs
```

---

## Regras de ouro (inviolaveis)

Consolidadas das memórias de feedback do projeto. Todas inviolaveis — quando em conflito, vence a regra mais alta.

### Operacionais (API + briefing)
1. **Custo estimado antes de toda chamada API** — zero exceções, mesmo em lotes autorizados.
2. **Perguntar aspect ratio + resolução + duração antes de gerar** — zero defaults silenciosos.
3. **Mostrar descrição curta do asset em linguagem de DA**, nunca o prompt técnico bruto antes da aprovação.
4. **Briefing em 3 fases** — Identidade → Estrutura+Refs → Assets+Orçamento.
5. **Video só após imagem-base aprovada** — sem exceções, mesmo se o orçamento já incluir vídeos.
6. **Registrar custo real pós-execução** em `custos.log` (JSONL).
7. **Checkpoint de qualidade pós-geração** — rejeitar genérico e regenerar (máx 2 retries auto; depois pede ajuste ao usuário).

### Linguagem com o usuário (narrativa vs maquinaria)
8. **Maquinaria interna nunca vaza na conversa.** Presets, `kit.config.ts`, envelope, rejects, taxonomy, preamble, 11 eixos — tudo isso é vocabulário do sistema, não da conversa. Usuário vê **narrativa de marca**, nunca arquitetura do módulo.
9. **Explicar decisões pela lente criativa**, nunca arquitetural. "A marca tem identidade warm editorial" ≠ "o kit Portfolio rejeita warm-palette".

### Kits e hibridização
10. **Kits são territórios cardinais hibridáveis, não modelos fechados.** Cada briefing declara `primary + secondary + proporção` (ex: 80% Editorial + 20% Clínica). `rejects` viram sinais advisory, não bloqueios.
11. **Templates se moldam ao conteúdo real.** 1 projeto real = single-project showcase, não 6 cards fake. Placeholder fake é proibido.
12. **Nenhum dado inventado** — nomes de projetos, clientes, depoimentos, stats devem ser reais ou seções inteiras desaparecem. "More in archive / on request" é aceitável; "Cliente Tal, 500 projetos entregues" fictício não é.

### Tipografia e assets gráficos
13. **Tipografia massiva no hero sempre via CSS**, nunca via Nano. Hero gera sem tipo embutido; `<h1>` em CSS absolute sobre a imagem.
14. **Pattern tiles tipográficos (monograma, letter-repeat, watermark) via SVG/CSS**, nunca via Nano — Nano deforma letterform e erra opacidade.

### Refs visuais
15. **Dois níveis de ref, nunca confundir:**
    - **Nível A — calibração interna do Claude** (`ref-prompt-engeneer/IMAGENS/`). Régua invisível de qualidade técnica. **Nunca** vira input de API. **Nunca** é referência de estilo.
    - **Nível B — `visualRefs` do briefing**. Uploadadas pelo usuário por projeto. Entram como `reference_images` na API Freepik + alimentam destilação do briefing.
16. **Prefixo obrigatório quando há image refs no Nano:** prompt começa com `Use the reference images only as aesthetic, compositional, and visual-aspect references to generate the following image:` — senão Nano copia demais a ref.

### Princípios universais (Camada 1)
17. **Camada 1 (princípios universais) veta Camada 2 (kits) e Camada 3 (briefing).** Se briefing viola princípio-tótem (contraste WCAG, touch targets, etc), skill recusa ou adapta — nunca entrega quebrado.
18. **Subagents em paralelo** quando assets são independentes — ganho de tempo real.

---

## Tratamento de erros conhecidos

| Erro | Causa provável | Ação |
|---|---|---|
| `400 prompt >3000 chars` | Prompt ultrapassou limite | Wrapper comprime automaticamente (drops Narrative tone, depois trim de clausulas redundantes) |
| `400 aspect_ratio inválido` | Formato errado (ex: `widescreen_16_9`) | Usar formato `X:Y` (ex: `16:9`) |
| `402 / 403 / 429 free tier` | Free tier esgotado | Pausar execução, reportar link do billing, não retry automático |
| Seedance `duration` rejeitado | Só aceita 5 ou 10 | `hub.py` valida antes do POST |
| Geração genérica | Prompt insuficientemente técnico | Regenerar com mais specs (câmera, lente, luz, HEX); máx 2 retries |
| Tipografia hero malformada | Nano ignora texto em fotografia densa | Gerar hero sem tipo embutido, aplicar via CSS absolute no Astro |
| Pattern tile tipográfico deformado | Nano erra letterform + opacity | Gerar via SVG/CSS, não via Nano |
| Ref visual copiada (Nano) | Faltou prefixo obrigatório | Sempre iniciar prompt com "Use the reference images only as aesthetic..." |
| Placeholder vazio em work grid | Briefing tem menos projetos reais que o grid | Trocar layout pra `single-feature` ou `2-col`, adaptar ao inventário |
| Download do asset falha | Rede / URL expirada | Retry 3x com backoff exponencial, depois reportar |
| Modelo rejeita conteúdo | Violação de política Freepik | Reportar ao usuário + pedir ajuste de prompt |
| Vite bloqueia tunnel host | `server.allowedHosts` restritivo | Adicionar em `astro.config.mjs` → `vite.server.allowedHosts: ['.trycloudflare.com']` |

---

## Referências rápidas

- **Wrapper HTTP**: `hub.py`
- **Custos em tempo real**: `custos.log` (JSONL)
- **Constituição**: `prompts/principios/index.md`
- **Kits disponíveis**:
  - `templates/portfolio-editorial/` + `kit.config.ts`
  - `templates/clinica-estetica/` + `kit.config.ts`
  - `templates/tech-apple/` + `kit.config.ts`
