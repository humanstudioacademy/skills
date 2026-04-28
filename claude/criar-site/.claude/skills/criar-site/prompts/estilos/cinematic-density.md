# DNA 01 — CINEMATIC DENSITY

> *Controlled chaos. Calm authority within disorder. Tactile materials under sculpted light.*

Extraído e expandido do prompt de referência (retrato cinematográfico com faíscas, ARRI + teal-warm). Este DNA deve se aplicar a **imagem, vídeo e layout** de qualquer site gerado sob este estilo, mantendo coerência visual entre os três domínios.

---

## 1. IDENTIDADE CENTRAL

- **Tensão como princípio**: energia volátil ao redor de elementos ultra-compostos.
- **Densidade material**: nada é plano — tudo tem micro-textura, peso, presença.
- **Luz como personagem**: temperatura, direção e intensidade narram antes do conteúdo.
- **Silêncio visual**: negative space deliberado, não decorativo.

Palavras-âncora: **tack-sharp, microcontrast, filmic, sculpted, controlled, weighted**.
Palavras-veto: *vibrant, playful, flat, cute, bubbly, glossy (a menos que intencionalmente subvertido).*

---

## 2. DNA IMAGEM (Nano Banana / Nano Banana Pro)

### Captura
- **Câmera preferencial**: ARRI Alexa Mini LF, Sony VENICE 2, RED KOMODO (alternativas)
- **Lente**: Zeiss Supreme Prime ou Cooke S7/i — 35mm / 40mm / 50mm
- **Abertura**: T2.0-T2.8 (shallow DOF com sujeito tack-sharp)
- **Foco**: preciso no olho/ponto focal, falloff suave para background

### Iluminação
- **Key**: warm practical ~2800K, direcional (45° preferencial), hard edge
- **Fill**: mínimo, camera-right baixa intensidade (preserva densidade de sombra)
- **Back/rim**: cool ambient ~5600K pra separar silhueta
- **Contraste**: médio-alto, clean blacks (sem esmagar), roll-off controlado nos highlights

### Cor
- **Paleta estrita**: deep cyan (#0E2A3E range), warm amber (#E89B2C range), neutral charcoal (#2B2B2E range)
- **Color science**: teal-warm cinematic contrast
- **Saturação**: moderada; nunca pop/vibrante

### Textura
- **Grão**: refined filmic, minimal, estruturado (nunca digital noise)
- **Sharpness**: extrema no sujeito, falloff natural no resto
- **Micro-contrast**: alto — pele mostra poros, tecido mostra trama, metal mostra risco

### Composição
- Broken rule-of-thirds, framing off-center
- Negative space intencional (acima/ao lado)
- Low-angle pra presença, high-angle pra vulnerabilidade, neutro pra observação
- Camadas: foreground dinâmico, midground sujeito, background atmosférico

---

## 3. DNA VÍDEO (Seedance 2.0)

### Movimento de câmera
- **Preferencial**: slow dolly-in, parallax lateral, crane sutil
- **Aceito**: static com micro-oscilação
- **Vetado**: handheld shake, whip-pan, dutch tilt (a menos que narrativo)

### Ritmo
- Shots de **5-8 segundos** (nunca <3s, raramente >10s)
- Slow reveal > hard cut
- Action/reaction pace: respirado, nunca acelerado

### Motion
- **Shutter drag leve** em elementos cinéticos (faíscas, partículas, chuva)
- **Sujeito sempre sharp** — motion blur só em foreground/background dinâmico
- **Frame rate feel**: 24fps cinematic (motion cadence)

### Áudio (quando disponível)
- Diegético preferencial
- Score: minimal, ambiente, tensão controlada
- Silêncio é ferramenta

### Prompt template (Seedance)
```
[DNA camera specs] slow dolly-in toward [subject],
[DNA lighting specs], [DNA color palette],
tack-sharp focus on [focal point], subtle motion blur on [kinetic element],
24fps cinematic cadence, [duration]s, [aspect ratio]
```

---

## 4. DNA LAYOUT (Astro + Tailwind)

### Tipografia
- **Display/Headings**: grotesque sans — `Neue Haas Grotesk`, `Söhne`, `ABC Diatype` (ou `Inter Tight` como fallback web)
- **Body**: mesma família, weight 400-500, tracking ligeiramente apertado
- **Meta/Caption**: monospace — `JetBrains Mono`, `IBM Plex Mono` (pra timestamps, labels, código)
- **Accent (raro)**: serif de alto contraste — `GT Sectra`, `Tiempos` — apenas para citações/quotes especiais

### Grid & Espaçamento
- 12 colunas, mas com **alinhamentos intencionalmente quebrados** (asymmetric)
- **Vertical rhythm generoso** (12-20vh entre seções)
- **Horizontal density** em componentes (tight inline spacing)
- Gutters grandes (~24-32px mínimo)

### Paleta web
- `--bg`: `#0A0B0D` (near-black)
- `--bg-alt`: `#12141A`
- `--surface`: `#1A1D25`
- `--accent-cool`: `#0E2A3E` (deep cyan)
- `--accent-warm`: `#E89B2C` (amber — uso parcimonioso)
- `--text`: `#E8E6E1` (off-white, nunca puro)
- `--text-dim`: `#8B8A87`

### Movimento / Scroll
- **Reveals**: `translateY(24px) → 0` + `opacity 0 → 1`, easing `cubic-bezier(0.22, 1, 0.36, 1)`
- **Durações**: 600-900ms, stagger de 80-120ms entre elementos próximos
- **Parallax sutil** em backgrounds de imagem/vídeo (0.3-0.6 speed)
- **Hover states**: underline animado, opacity shift sutil — nunca pulos/bounces

### Hierarquia
- **Uma afirmação hero** por fold — clareza absoluta
- Suporte abaixo com densidade (tech specs, métricas, detalhes)
- **Asset dominante** por seção (imagem OU vídeo, raramente ambos competindo)

### Componentes de assinatura
- **Caption overmark** — label monospace acima do heading principal (ex: `/ 01 — CHAPTER NAME`)
- **Metadata strips** — linhas inline de key:value em monospace
- **Full-bleed media** com overlay gradient bottom-up
- **Off-grid text blocks** quebrando alinhamento em pontos narrativos

---

## 5. COMO USAR ESTE DNA NO GERADOR DE PROMPTS

Quando a Skill gerar um prompt para um asset, deve:

1. **Identificar o asset**: hero image / section background / accent video / etc.
2. **Extrair specs técnicos deste DNA** (câmera, luz, cor, textura)
3. **Injetar contexto do site** (tema, sujeito, ação)
4. **Respeitar o limite de 3000 chars** do endpoint

Exemplo de prompt gerado automaticamente:

```
Ultra-sharp cinematic [wide shot / portrait / medium] of [contextual subject],
shot on ARRI Alexa Mini LF with Zeiss Supreme Prime 40mm at T2.8,
[contextual action/pose], tack-sharp focus on [focal point];
warm practical key light at 2800K from [direction], cool ambient 5600K backlight,
high microcontrast with clean blacks and controlled highlight roll-off;
palette: deep cyan, warm amber, neutral charcoal; teal-warm color science;
refined filmic grain, minimal, micro-structured;
composition: broken rule-of-thirds with intentional negative space [position];
24fps cinematic capture, shallow DOF with crisp subject sharpness.
```

Este stub é **expansível** (adicionar detalhes contextuais) e **comprimível** (remover camadas menos críticas) conforme necessário pra caber no limite de tokens.
