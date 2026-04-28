# Prompt Engineer — módulo da skill `/criar-site`

> **Sistema que transforma inputs estruturados (kit + briefing + refs visuais) em prompts técnicos cinematográficos pra Nano Banana e Seedance 2.0.** Invocado obrigatoriamente antes de toda chamada à Freepik API. Nenhum asset é gerado sem passar por aqui.

Herança direta do **KinoImage Generator** (GPT custom construído pro MidJourney), traduzido pro stack Freepik e costurado ao DNA dos 3 kits da skill.

---

## ARQUIVOS

| Arquivo | Propósito |
|---|---|
| `taxonomy.md` | Régua operacional: 11 eixos pra imagem + 4 extra pra vídeo, regras globais, proibições. |
| `engine-image.md` | Pipeline Nano Banana — contrato de entrada/saída, pipeline de 8 steps, exemplo completo. |
| `engine-motion.md` | Pipeline Seedance 2.0 — herda da imagem aprovada, adiciona movimento/ritmo/shutter/atmosfera. |
| `kit-presets/portfolio-editorial.md` | Preamble fixo + specs técnicas pro kit 1. |
| `kit-presets/clinica-estetica.md` | Preamble fixo + specs técnicas pro kit 2. |
| `kit-presets/tech-apple.md` | Preamble fixo + specs técnicas pro kit 3. |

---

## FLUXO COMPLETO

```
[Fase 2 do briefing]
  ├─ Coleta refs visuais (visualRefs) do usuário
  └─ Classifica (internamente, sem expor): primary + secondary + proporção
           ↓
[Engine monta preamble híbrido]
  puxa estrutura/tipo/composição do primary
  puxa paleta/luz/materialidade do secondary na proporção declarada
           ↓
[Engine decupa visualRefs em descritores técnicos]
           ↓
[Engine preenche 11 eixos da taxonomy]
           ↓
[Engine emite prompt bloco corrido + NEGATIVE]
  aplica prefixo obrigatório se visualRefs.length > 0
  exclui texto renderizado de hero (vai via CSS no Astro)
           ↓
[hub.py chama Freepik API com prompt + reference_images (base64) + negative_prompt]
           ↓
[Imagem retorna → usuário aprova]
           ↓ (só depois disso)
[Engine de motion herda ficha + adiciona 4 eixos (câmera/ritmo/shutter/atmosfera)]
           ↓
[hub.py chama Seedance image-to-video]
```

---

## REGRAS DE OURO (ler antes de qualquer ajuste)

1. **Régua mínima, não teto.** As imagens em `ref-prompt-engeneer/IMAGENS/` (+ `design/`) são **calibração interna** — parâmetro de qualidades essenciais (luz, nitidez, composição, casting, materialidade, disciplina de paleta). **⚠️ NUNCA viram input de API. NUNCA referência de estilo direto.** Ver `taxonomy.md` → "DOIS NÍVEIS DE REFERÊNCIA".
2. **Inglês técnico sempre.** Nano/Seedance respondem melhor em inglês.
3. **Zero sintaxe MidJourney.** Nenhum `--ar`, `--v`, `--style`, `--no`, `--stylize`. Nenhum duplo traço em output.
4. **Zero adjetivos vazios.** Banidos: "beautiful", "stunning", "4K", "hyperrealistic", "masterpiece", "award-winning". Rigor técnico entrega qualidade.
5. **Vídeo só após imagem aprovada.** Engine de motion herda ficha — nunca inventa universo paralelo.
6. **Duração Seedance apenas 5 ou 10s.** API constraint.
7. **Kits hibridáveis, rejects advisory.** Briefing declara `primary + secondary + proporção` (ex: 80/20). Rejects do kit **não bloqueiam** — sinalizam que o item pode vir do secondary. Só bloqueia se mistura resulta em contradição coerente. Ver `feedback_kits_hibridizaveis` em memory.
8. **Refs visuais reforçam, não contradizem.** Prompt descreve o que a ref mostra em dialeto diferente. Prefixo obrigatório: `"Use the reference images only as aesthetic, compositional, and visual-aspect references to generate the following image:"`.
9. **Tipografia massiva no hero sempre via CSS**, nunca embutida no prompt. Pattern tiles tipográficos (monograma, letter-repeat) via SVG/CSS. Ver `feedback_tipografia_hero_via_css` e `feedback_pattern_tipografico_via_codigo` em memory.
10. **Templates moldáveis ao conteúdo real.** Briefing com 1 projeto real = single-project showcase, não 6 cards fake. Ver `feedback_templates_moldaveis_ao_conteudo` em memory.
11. **Maquinaria interna nunca vaza na narrativa com o usuário.** Presets/envelope/rejects são vocabulário do sistema; usuário conversa em linguagem de marca.

---

## INTEGRAÇÃO COM `hub.py`

O módulo expõe 2 funções principais:

```python
# pseudocode
from prompt_engineer import render_image, render_motion

prompt, negative = render_image(asset, kit, brief, visualRefs)
prompt, negative = render_motion(asset, kit, brief, motion, sourceImage)
```

Ambas cospem `(str, str)` — prontas pra entrar literal na chamada HTTP da API Freepik. Zero tradução intermediária.

---

## INTEGRAÇÃO COM `SKILL.md` (Etapa 8)

A etapa 8 do SKILL.md ("compor index.astro + validação anti-drift") precisa adicionar substep 8.2:

> **8.2 — Pipeline de geração de assets.** Antes de cada chamada à Freepik API:
> 1. Carregar kit preset de `.claude/skills/criar-site/prompts/prompt-engineer/kit-presets/{kit.id}.md`.
> 2. Destilar ficha estética da Fase 2.5 do briefing (paleta HEX + mood + refs visuais).
> 3. Invocar `render_image()` ou `render_motion()` do módulo prompt-engineer.
> 4. Passar output direto pra `hub.py` → Freepik API.
> 5. Após resposta, validar densidade técnica do asset — se cair abaixo da régua das refs canônicas, regenerar (até 2 retries).

---

## STATUS DE IMPLEMENTAÇÃO

- [x] `visualRefs` no briefing Fase 2 (ver `SKILL.md` Fase 2 item 5 — papel duplo).
- [x] `hub.py::gerar_imagem` aceita `reference_images` + aplica prefixo + valida densidade.
- [x] `hub.py::gerar_video` aceita `negative_prompt` + valida densidade.
- [x] `prompt_engineer.py` com `load_kit_preamble`, `apply_ref_prefix`, `validate_prompt`, `ensure_density`.
- [x] `SKILL.md` Etapa 5 reescrita pra referenciar o módulo.

## PRÓXIMO TESTE DE VALIDAÇÃO

Pra validar divergência entre os 3 kits, o teste correto é:

- **Criar 3 briefings ficcionais distintos**, um natural pra cada kit (ex: studio criativo → Portfolio, clínica de harmonização → Clínica, lançamento de produto AI → Tech).
- Cada briefing pode ter suas **próprias `visualRefs` coerentes com o projeto** (fornecidas pelo usuário ou buscadas).
- Gerar 1 hero por kit + comparar outputs.
- **Nunca** usar as imagens de `ref-prompt-engeneer/IMAGENS/` como `visualRefs` de teste — elas são calibração interna, não input válido.
