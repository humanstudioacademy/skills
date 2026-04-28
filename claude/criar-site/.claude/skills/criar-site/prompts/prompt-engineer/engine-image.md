# ENGINE — IMAGE (Nano Banana / Nano Banana Pro)

> **Invocado antes de toda chamada à Freepik API de imagem.** Recebe inputs estruturados, aplica a taxonomia, cospe um prompt único em inglês técnico + negative directives. Nenhuma imagem é gerada sem passar por aqui.

---

## CONTRATO DE ENTRADA

O engine recebe 5 inputs estruturados:

```yaml
asset:
  role: hero | gallery-still | texture | pattern-tile | ornament | badge
  aspectRatio: "4:5" | "3:2" | "1:1" | "16:9" | "9:16" | "2.39:1"
  hasText: boolean          # se true, o prompt deve renderizar texto na imagem
  textContent: string       # conteúdo literal (obrigatório quando hasText)

kit:
  # Nova estrutura híbrida (modelo canônico):
  primary:
    id: portfolio-editorial | clinica-estetica | tech-apple
    weight: 60 | 70 | 80 | 100   # %, default 100 se não há secondary
  secondary:
    id: portfolio-editorial | clinica-estetica | tech-apple
    weight: 40 | 30 | 20 | 0     # %, opcional (0 = kit puro)
  # Retrocompatibilidade: se chegar "preset: X" sem primary/secondary,
  # trata como primary=X weight=100.

brief:
  paletteHex: [string]      # até 3 HEX, ordenados por dominância
  paletteDescriptors: [string]  # ex: "cadmium red", "off-white linen", "polished black"
  moodOneLiner: string      # 1 frase declarativa do briefing
  subjectContext: string    # quem/o que é o sujeito no frame
  narrativeBeat: string     # 1 frase — qual a tensão/intenção do frame

visualRefs: [path]          # 0 a 6 imagens de referência (locais ou URLs)
  # se > 0, são anexadas como image reference na chamada API
  # o prompt textual deve reforçar (nunca contradizer) o que as refs mostram

editorialPolish:
  density: "editorial-premium"  # fixo — régua mínima, não ajustável pra baixo
```

---

## PIPELINE DE GERAÇÃO (ordem rígida)

### STEP 1 — Carregar kit preset (ou compor preamble híbrido)

**Caso A — projeto puro (weight primary = 100):**
Lê `kit-presets/{kit.primary.id}.md` e extrai o **preamble formal**. Aplica literal.

**Caso B — projeto híbrido (weight secondary > 0):**
Lê os dois presets. Compõe preamble híbrido seguindo a regra de `taxonomy.md > HIBRIDIZAÇÃO DE KITS > tolerância à hibridização nos 11 eixos`:
- Puxa **registro, estrutura, composição, motion biases, tipografia** do **primary**.
- Puxa **paleta, color science, luz baseline, grain profile, materialidade, tratamento de modelo, cenário warm/cool** do **secondary** na proporção declarada.
- Quando há conflito direto entre primary e secondary num eixo, resolve pela proporção:
  - 80/20: domina primary em quase tudo, secondary só em cor + luz + materialidade.
  - 70/30: primary estrutura, secondary paleta/mood **e** um elemento de materialidade notável.
  - 60/40: híbrido forte — primary ainda é reconhecível mas secondary "invade" ritmo/composição parcialmente.
- Redige **1 parágrafo formal de preamble híbrido próprio do projeto** (não concatena os dois textos) que carrega a mistura em linguagem coerente.

**Garantia:** o preamble híbrido **não deixa** o asset sair parecendo nenhum dos kits puros canônicos — ele é *dessa marca específica*, com DNA próprio derivado da proporção.

### STEP 2 — Decupar refs visuais (se houver)

**As refs visuais têm papel duplo:**
1. **Durante o briefing (Fase 2/2.5):** são o **norte estético** pra construção da ficha — decupadas em paleta HEX, mood, kit-fit, luz, composição, materialidade. Guiam a escolha de kit e o preenchimento do briefing **antes** de qualquer chamada à API.
2. **Na geração (esta step):** são anexadas como `reference_images` no payload da Freepik **E** o texto do prompt é reforçado com descritores técnicos do que elas mostram.

**Pra esta step:** para cada imagem em `visualRefs`:
- Extrair 3-5 descritores técnicos observáveis (`tungsten warm 3200K key`, `crushed blacks`, `matte dry plaster wall`, `cadmium red dominance 70%`).
- Incluir esses descritores como **reinforcement layer** no prompt textual — mesmo com a imagem anexada, o texto descreve o que a IA já vê, pra travar a geração naquele território.

Nano Banana lê melhor quando prompt + image reference dizem a mesma coisa em dialetos diferentes.

### STEP 3 — Preencher os 11 eixos (taxonomy.md)
Para cada eixo, aplicar esta hierarquia de decisão:
1. **Briefing explicita?** → usar direto.
2. **Ref visual mostra?** → descrever o que a ref carrega.
3. **Kit preset define?** → usar default do preset.
4. **Nada do acima?** → engine escolhe decisão **plausível dentro do registro publicitário premium**. Nunca deixa em branco. Nunca escolhe "genérico".

Nenhum eixo sai vazio. Se o eixo sair fraco, o checkpoint 11 (coerência) reforça.

### STEP 4 — Tratamento especial: texto renderizado
Se `asset.hasText === true`:
- Ler conteúdo literal em `asset.textContent`.
- Nano Banana renderiza texto com fidelidade quando o prompt trata a tipografia como **elemento cinematográfico**, não como metadata.
- Descrever: fonte de inspiração (`Anton grotesque condensed` / `Druk-like display` / `Bodoni didone high contrast`), tamanho relativo (`dominant massive display, 70% of frame height`), posição, tratamento (`solid ink, zero kerning drift, clean edge`), relação com a foto (`full-bleed overlap`, `bottom quarter only`, `negative knockout against subject`).
- Proibir: `warped letters`, `distorted typography`, `illegible character drift`.
- Sempre declarar o conteúdo exato entre aspas no prompt: `...displaying the word "RUTHLESSLY" in massive condensed grotesque typography...`.

### STEP 5 — Montar bloco corrido

**Prefixo obrigatório quando há image refs** (`visualRefs.length > 0`):
O prompt **sempre** começa com a linha literal:

> `Use the reference images only as aesthetic, compositional, and visual-aspect references to generate the following image:`

Sem essa frase, Nano Banana trata as refs como target de imitação e retorna algo quase idêntico à referência — bug confirmado empiricamente. Com a frase, ele extrai paleta/luz/composição/mood das refs mas compõe a cena nova a partir do texto.

Quando não há refs visuais (`visualRefs.length === 0`), o prefixo **não é incluído** — abre direto no bloco corrido.

**Bloco corrido:** concatenar os 11 eixos em **1 parágrafo único denso**, sem listas, sem headers, sem marcações. Ordem preferencial:
1. Linguagem visual + tipo de shot + sujeito
2. Câmera e lente
3. Iluminação
4. Cor e paleta
5. Textura e materialidade
6. Figurino (se pessoa)
7. Cenário
8. Composição + formato
9. Modelo (se pessoa)
10. Narrativa
11. (Texto renderizado, se aplicável)

Tamanho alvo: **400-900 palavras** (sem contar o prefixo). Abaixo de 400 = raso. Acima de 900 = Nano começa a ignorar partes.

### STEP 6 — Montar NEGATIVE
Montar uma string única separada por vírgulas, puxando do bloco `NEGATIVE DIRECTIVES` da taxonomy, escolhendo apenas as proibições relevantes pro asset em questão. Não jogar todas — jogar as pertinentes.

### STEP 7 — Checkpoint de coerência
Antes de emitir, verificar eixo 11 da taxonomy. Se encontrar contradição, corrigir e re-emitir — nunca entregar com falha conhecida.

### STEP 8 — Emitir
Output literal:
```
{bloco corrido de 400-900 palavras em inglês técnico}

NEGATIVE: {lista por vírgula}
```

Nada mais. Zero preâmbulo.

---

## EXEMPLO COMPLETO DE EXECUÇÃO

### Inputs
```yaml
asset:
  role: hero
  aspectRatio: "4:5"
  hasText: true
  textContent: "RUTHLESSLY FAST."

kit:
  preset: portfolio-editorial

brief:
  paletteHex: ["#C2261A", "#F5F4F0", "#0A0A0A"]
  paletteDescriptors: ["cadmium red wall", "off-white linen", "deep black ink"]
  moodOneLiner: "editorial running campaign with declarative typography over athletic portrait"
  subjectContext: "female long-distance runner mid-stride crossing finish banner, arms raised"
  narrativeBeat: "victory sustained as controlled composure, not celebration"

visualRefs: ["./refs/marathon_runner_editorial.jpg"]

editorialPolish:
  density: editorial-premium
```

### Output esperado

```
Use the reference images only as aesthetic, compositional, and visual-aspect references to generate the following image: Editorial fashion-sport photography with single-subject dominance and declarative typographic overlay. Full-body vertical 4:5 framing of a female long-distance runner in her late 20s, deep brown skin with warm red undertone, high cheekbones and strong jawline, tightly bound dark braids pulled back, captured mid-stride crossing a branded race banner with both arms raised at roughly 110° — weight committed forward, torso squared to camera, breath caught between exhalation and the next gesture. Shot on ARRI Alexa Mini LF with Cooke S7/i 50mm at T2.0, tack-sharp focus held on the subject's eyes, shallow DOF compressing the banner behind into a soft graphic plane, natural perspective compression with high microcontrast and filmic falloff. Lighting driven by a single large overhead soft source balanced with ambient bounce from the ground, key-to-fill ratio 4:1, soft wrapping quality across the skin with specular highlights only on the cheekbones and collarbones, medium-high contrast with clean blacks under the arms and jawline, controlled highlight roll-off on the white top, 5600K daylight temperature evenly held. Palette locked to three tones — 60% cadmium red dominant through background banner and branded elements (#C2261A range), 30% off-white linen jersey and race bib (#F5F4F0 range), 10% deep black ink through typographic overlay and braided hair (#0A0A0A); clean blacks, no lifted shadow, saturation moderate never vibrant. Athletic jersey in matte cotton blend catching light with subtle diffusion and visible weave texture across the shoulder, race bib in flat uncoated paper finish, slight kinetic sweat beading on forehead and temples reading as specular points, faint chalk dust and fine particles hanging in the air behind the subject catching warm rim from ambient bounce. Background a full-bleed cadmium red race banner repeating sponsor type in small scale across the plane, compressed by telephoto rendering into near-flat graphic field, no deep spatial recession, shallow enough to remain abstract. Composition built on broken rule-of-thirds with subject placed at vertical center-line filling the middle 40% of frame, 25% negative space above head reserved for dominant display typography, slight low angle emphasizing physical authority and forward commitment. The image carries massive condensed grotesque display typography inspired by Anton and Druk Wide rendered in solid deep black ink, the word "RUTHLESSLY" occupying the top 20% of frame edge-to-edge with zero kerning drift and crisp clean edges, the word "FAST." anchored in the bottom 20% at equivalent scale, both blocks treated as full-bleed knockout against the photograph with no drop-shadow and no outline, typography reads as cinematic element integrated into the image rather than metadata overlay. Refined Kodak Portra 400 grain across the entire frame at minimal density, zero digital noise, zero HDR crunch, no over-sharpening halos. Narrative tension of victory held as composed momentum — the moment before celebration breaks into release, carried in the set of the shoulders and the direct unbroken eye contact with the lens.

NEGATIVE: no plastic skin, no airbrush effect, no beauty filter, no HDR crunchy look, no over-sharpening halos, no digital noise, no banding, no cartoon stylization, no 3D render look, no stock photography cliché, no generic studio glossy, no broken anatomy, no warped letters, no distorted typography, no illegible character drift, no watermarks, no logos
```

**Observe:**
- Os 11 eixos estão todos presentes e densos.
- A paleta está em HEX com dominância % declarada.
- Tipografia é tratada como elemento cinematográfico integrado, não metadata.
- Nenhum adjetivo vazio ("beautiful", "stunning").
- Nenhum parâmetro MidJourney.
- Negative directives escolhidas pro asset (incluindo as de tipografia).

---

## INTEGRAÇÃO COM hub.py

O engine é invocado em `hub.py` antes de `call_freepik_nano_banana()`:

```python
# pseudocode
prompt, negative = prompt_engineer.render_image(
    asset=asset_spec,
    kit=active_kit,
    brief=brief_data,
    visualRefs=user_uploaded_refs,
)

response = call_freepik_nano_banana(
    prompt=prompt,
    negative_prompt=negative,
    reference_images=visualRefs,  # enviadas junto
    aspect_ratio=asset.aspectRatio,
    model="nano-banana-pro",
)
```

O contrato de saída do engine (`prompt`, `negative`) é exatamente o que a API espera — zero tradução intermediária necessária.

---

## QUANDO O ENGINE DEVE PARAR E PERGUNTAR AO USUÁRIO

Em vez de inventar quando falta dado crítico, o engine **pausa** nestes casos:
- `brief.paletteHex` está vazio E não há refs visuais.
- `asset.hasText === true` mas `asset.textContent` está vazio.
- `kit.preset` é desconhecido.
- O briefing pede algo que está no `rejects` do kit (ex: pedir pastel warm em Portfolio Editorial).

Nesses casos, o engine não inventa — volta pro usuário com a pergunta específica. "Inventar quando falta dado do briefing" (STEP 3) vale só pra detalhes técnicos (lente, Kelvin, shutter), nunca pra decisões estruturais do projeto.
