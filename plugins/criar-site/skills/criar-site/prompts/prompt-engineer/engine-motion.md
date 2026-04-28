# ENGINE — MOTION (Seedance 2.0)

> **Invocado antes de toda chamada à Freepik API de vídeo (Seedance 2.0 Pro / Lite, image-to-video ou text-to-video).** Recebe inputs estruturados, aplica a taxonomia (11 eixos de imagem + 4 de movimento), cospe prompt técnico único em inglês. Nenhum vídeo é gerado sem passar por aqui.

**Pré-requisito regra-de-ouro:** vídeo só é gerado **após a imagem-base aprovada** (ver `feedback_video_apos_imagem.md`). O engine de motion trabalha em cima de um asset de imagem já validado, não do zero.

---

## CONTRATO DE ENTRADA

```yaml
asset:
  role: hero-video | section-loop | detail-motion | transition-bridge
  aspectRatio: "16:9" | "9:16" | "1:1" | "4:5" | "2.39:1"
  duration: 5 | 10                # API constraint — apenas esses dois valores
  model: "seedance-2-pro-720p" | "seedance-2-pro-1080p" | "seedance-2-lite-720p"
  generationMode: "image-to-video" | "text-to-video"
  sourceImage: path               # obrigatório quando mode=image-to-video (frame inicial)

kit:
  preset: portfolio-editorial | clinica-estetica | tech-apple

brief:
  # herdado da imagem-base aprovada — mesmos campos do engine-image
  paletteHex: [string]
  paletteDescriptors: [string]
  moodOneLiner: string
  subjectContext: string
  narrativeBeat: string

motion:
  cameraMove: string              # descrito pelo usuário ou inferido do kit
  rhythmIntent: string            # "sustained single gesture" | "mini-arc with reveal"
  dynamicElement: string          # o que se move além do sujeito (opcional)

editorialPolish:
  density: "editorial-premium"
```

---

## PIPELINE DE GERAÇÃO

### STEP 1 — Validar API constraints
- `duration` ∈ {5, 10} — qualquer outro valor é rejeitado imediatamente (ver `hub.py` já valida).
- `aspectRatio` suportado pelo model escolhido.
- Se `generationMode === "image-to-video"`, `sourceImage` precisa existir e ter sido aprovada.

### STEP 2 — Carregar kit preset
Mesma lógica do engine-image. O preset carrega os defaults de movimento daquele kit (ex: Portfolio Editorial → slow dolly-in preferencial; Clínica → breathing static; Tech → product-tilt orbital).

### STEP 3 — Herdar ficha estética da imagem-base
Os 11 eixos de imagem **não são reinventados** — o engine lê a ficha usada pra gerar a imagem-base aprovada e herda:
- Paleta exata
- Iluminação declarada
- Câmera + lente
- Textura
- Figurino + cenário + modelo + narrativa

Isso garante que o vídeo **continua a cena da imagem**, não cria um universo paralelo.

### STEP 4 — Preencher os 4 eixos de motion (taxonomy 12-15)

**Eixo 12 — Movimento de câmera**
- Se `motion.cameraMove` vem do usuário, usar.
- Se vem do kit preset, usar default.
- Se nenhum, engine escolhe dentro dos tipos aceitos pelo kit.
- **Sempre declarar:** tipo + velocidade + trajetória + altura de câmera.
- Ex: `slow deliberate dolly-in along linear trajectory toward subject, camera height locked at eye-level, constant speed across full duration`

**Eixo 13 — Ritmo dramático**
- `duration: 5` → engine escreve como single sustained gesture. Descrever **um** micro-momento.
- `duration: 10` → engine escreve como mini-arc com beat declarado (momento-chave em timestamp específico).
- Ex (5s): `subject holds breath across 5 seconds, chest rising once subtly at 0:02, eyes remaining locked on lens`
- Ex (10s): `stillness at 0:00-0:03, subject lifts chin with deliberate intent at 0:04, settles into held gaze 0:06-0:10`

**Eixo 14 — Motion blur & shutter**
- Default: `180° shutter angle at 24fps cinematic cadence`.
- Sujeito sempre sharp; motion blur apenas em foreground/background cinético.
- Se o DNA do kit pede look específico, declarar (ex: `90° shutter for crisper athletic motion` em algum frame de Tech).

**Eixo 15 — Atmosfera dinâmica**
- Do briefing ou inferido.
- O que se move além do sujeito: partículas, tecido, luz cambiante, background passante.
- **Regra:** sustenta o sujeito, nunca compete.
- Se briefing/kit pedem stillness: declarar `atmosphere held in near-stillness, only breath and subtle fabric movement` — silêncio é ferramenta.

### STEP 5 — Montar bloco corrido
Concatenar em **1 parágrafo único** em inglês técnico. Ordem preferencial:
1. Tipo de shot herdado da imagem + sujeito + formato + duração
2. Câmera/lente herdada
3. Movimento de câmera (eixo 12) — declarado detalhadamente
4. Iluminação herdada
5. Cor e paleta herdadas
6. Textura + figurino + cenário herdados (compactados)
7. Ritmo dramático (eixo 13) — com timestamps
8. Motion blur / shutter (eixo 14)
9. Atmosfera dinâmica (eixo 15)
10. Narrativa herdada

Tamanho alvo: **300-700 palavras** (Seedance prefere prompts ligeiramente mais enxutos que Nano — mais gordura vira drift temporal).

### STEP 6 — Montar NEGATIVE específico pra vídeo
Sempre incluir:
- `no frame stutter, no warping, no morphing between frames`
- `no identity drift on subject face across duration`
- `no background pumping or gaining sharpness inconsistently`
- `no unnatural motion speedup or slowdown`
- `no camera shake not declared in prompt`

Somar com as negatives relevantes da imagem herdada.

### STEP 7 — Emitir
```
{bloco corrido 300-700 palavras em inglês técnico}

NEGATIVE: {lista por vírgula}
```

---

## EXEMPLO COMPLETO

### Inputs
```yaml
asset:
  role: hero-video
  aspectRatio: "4:5"
  duration: 5
  model: "seedance-2-pro-720p"
  generationMode: "image-to-video"
  sourceImage: "./generated/hero_frame_01.jpg"  # imagem aprovada do exemplo do engine-image

kit:
  preset: portfolio-editorial

brief:
  # herdado
  paletteHex: ["#C2261A", "#F5F4F0", "#0A0A0A"]
  paletteDescriptors: ["cadmium red wall", "off-white linen", "deep black ink"]
  moodOneLiner: "editorial running campaign with declarative typography over athletic portrait"
  subjectContext: "female long-distance runner mid-stride crossing finish banner, arms raised"
  narrativeBeat: "victory sustained as controlled composure, not celebration"

motion:
  cameraMove: "very slow push-in toward subject"
  rhythmIntent: "single sustained gesture — the moment before release"
  dynamicElement: "fine chalk dust hanging in air, gentle drift behind subject"
```

### Output

```
Editorial fashion-sport cinematic video of a female long-distance runner in her late 20s captured mid-stride crossing a branded race banner with both arms raised at roughly 110°, vertical 4:5 framing, 5 seconds duration at 24fps cinematic cadence. Shot on ARRI Alexa Mini LF with Cooke S7/i 50mm at T2.0, tack-sharp focus sustained on the subject's eyes across the full duration, shallow DOF compressing the banner behind into a soft graphic plane. Camera executes a very slow deliberate push-in along linear trajectory toward the subject, starting at mid-torso framing and closing roughly 8% across 5 seconds, camera height locked at eye-level, zero lateral drift, no handheld shake, no dutch tilt. Lighting held consistent with single large overhead soft source balanced with ambient bounce from ground, key-to-fill ratio 4:1, soft wrapping quality across skin with specular highlights only on cheekbones and collarbones, medium-high contrast with clean blacks, controlled highlight roll-off on white jersey, 5600K daylight temperature stable across duration. Palette locked to three tones — 60% cadmium red dominant through banner (#C2261A range), 30% off-white linen jersey (#F5F4F0 range), 10% deep black through braided hair and subtle typographic plane (#0A0A0A); saturation moderate held constant, no color drift. Matte cotton jersey catching subtle air movement along the shoulder, race bib paper remaining still, sweat beading on forehead reading as sustained specular points without popping, braided hair showing micro-lift from forward momentum carried into the held frame. Background a full-bleed cadmium red race banner compressed by telephoto into near-flat graphic plane, holding its abstract field with no parallax shift beyond the camera push-in. The duration carries a single sustained gesture — subject holds a caught-breath stillness from 0:00 to 0:03 with eyes locked on lens and chest barely lifting, a micro-exhalation releases at 0:03 with chin settling one degree lower by 0:04, the final beat from 0:04 to 0:05 holds in composed steady presence before cut. 180° shutter angle producing natural filmic motion blur, sujeito consistently sharp with crisp edge on the jawline across every frame, subtle motion blur only on the finest elements — drifting chalk dust particles hanging in air behind the subject catching warm ambient bounce, slow gentle drift rightward across the full duration, never crossing in front of the subject. Refined Kodak Portra 400 grain held at minimal density uniformly across duration. Narrative of victory held as composed momentum, the moment before celebration breaks into release — carried by the unchanged set of the shoulders and the unbroken direct eye contact with the lens.

NEGATIVE: no frame stutter, no warping, no morphing between frames, no identity drift on subject face, no background pumping, no unnatural motion speedup, no handheld shake, no dutch tilt, no whip-pan, no color drift across duration, no plastic skin, no beauty filter, no digital noise, no 3D render look, no broken anatomy, no watermarks
```

**Observe:**
- Os 11 eixos de imagem vêm herdados e compactados (não reinventados).
- Os 4 eixos de motion estão todos explícitos.
- Ritmo com timestamps precisos (0:00, 0:03, 0:04, 0:05).
- Câmera declarada em detalhe (tipo + trajetória + velocidade + altura + constância).
- Atmosfera dinâmica pertence ao mesmo universo (chalk dust que a imagem já sugere).
- Negative cobre os riscos específicos de Seedance.

---

## INTEGRAÇÃO COM hub.py

```python
# pseudocode
prompt, negative = prompt_engineer.render_motion(
    asset=video_spec,
    kit=active_kit,
    brief=brief_data_from_approved_image,
    motion=motion_spec,
    sourceImage=approved_image_path,
)

response = call_freepik_seedance(
    prompt=prompt,
    negative_prompt=negative,
    reference_image=approved_image_path,  # para image-to-video
    duration=asset.duration,  # 5 ou 10, validado no STEP 1
    aspect_ratio=asset.aspectRatio,
    model=asset.model,
)
```

---

## QUANDO O ENGINE PAUSA

Mesma regra do engine-image. Adicionar:
- `generationMode: "image-to-video"` mas `sourceImage` não foi aprovada pelo usuário → pausa até aprovação.
- `duration` fora de {5, 10} → rejeita e pede correção.
- Briefing pede movimento que o kit `rejects` (ex: Portfolio Editorial rejeitando snap-zoom frenético) → pausa e sugere alternativa dentro do envelope.
