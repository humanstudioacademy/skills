# KIT PRESET — Clínica Estética

> **Preamble fixo injetado pelo engine em todo prompt deste kit.** Traduz o DNA (serif curvilinear romântica + paleta muted quente + retrato humano sempre + ornamentos orgânicos + ritmo respirado) em decisões técnicas pro Nano Banana e Seedance 2.0. Universo: wellness editorial, skincare luxury premium, beauty magazine contemporânea (AllureBurrow, Aēsop, Zitomer, Royal Clinic, Houston Aesthetic Lab).

**Régua mínima de qualidade:** nenhum asset deste kit pode cair abaixo do nível das refs visuais do usuário (editorial photography com controle de paleta e densidade técnica). Luz suave **não significa** prompt raso — ao contrário, luz suave exige descrição técnica mais cuidadosa pra não cair em genérico.

---

## CÂMERAS PREFERENCIAIS
- **Stills MF primária:** Hasselblad H6D-100c, Phase One XT — look editorial beauty signature.
- **Stills MF alternativa:** Mamiya RZ67 (analog feel quando briefing pede nostalgia contida), Fujifilm GFX100 II.
- **Cine opcional (pra vídeo ou frame cinético):** ARRI Alexa Mini LF, Sony VENICE 2.
- **Nunca:** câmeras consumer, action cameras, smartphone emulation.

## LENTES PREFERENCIAIS
- **Primary:** 80mm MF (equivalente ~50mm full-frame) Hasselblad HC ou XCD — beauty editorial classic.
- **Macro opcional:** 120mm Macro Hasselblad pra close-ups de pele, detalhes de textura.
- **Wide opcional:** 45mm MF (equivalente ~35mm full-frame) só pra cenas de espaço da clínica / lifestyle.
- **Abertura padrão:** f/2.8 — f/4 — shallow mas não extrema; a ideia é que o sujeito respire, não que flutue.
- **Vetos:** tele >150mm (compressão editorial não pertence), ultra-wide <28mm.

## ILUMINAÇÃO BASELINE
- **Esquema padrão:** **natural light or soft daylight-emulated**, large diffused source, wrapping suave.
  - **Janela grande north-facing** (5600K natural soft) é a referência visual.
  - Large soft source: octabox 7ft, book light amplo, ou real window com silk diffusion.
  - Fill: ambient bounce branco em superfícies do cenário (paredes cream, tecidos claros).
  - Key:fill típico **2:1 a 3:1** (baixo contraste, muito mais baixo que Portfolio).
  - **Sem rim light forte** — separação vem da paleta e do blur, não da luz.
- **Qualidade:** **soft wrapping em tudo** — pele, tecido, parede. Specular mínimo, mantido só nas maçãs do rosto e lábios quando relevante.
- **Contraste:** **low-key-suave**, zero crushed shadow, **lifted-but-controlled blacks** (pretos nunca totalmente crushados — leituras ficam mais atmosféricas).
- **Temperatura:** **5600K daylight** ou **4000K golden-hour balanced** — nunca tungsten saturado.
- **Modificadores frequentes:** silk diffusion 1/4 ou 1/2, large octabox, scrims, negative fill branco (nunca preto).

## TRATAMENTO DE COR
- **Paleta sempre dessaturada / muted / warm neutral.** HEX e descritores vêm do briefing.
- **Dominância declarada em %** — ex: "50% cream off-white, 30% soft blush, 15% warm taupe, 5% muted gold accent".
- **Tons sempre harmônicos:** cream, ivory, beige, blush, rose-taupe, sand, warm grey, muted sage, dusty rose, champagne. Gold/bronze só em detalhes finos (ornamentos, jewelry).
- **Proibido:** saturação vibrante, primary colors (red puro, blue puro), neon, cool palette, black-as-ink dominance.
- **Color science:** editorial beauty soft — highlight roll-off generoso, shadow softly lifted, skin tone com warm undertone consistente.
- **Refs de color science:** Cass Bird, Zoey Grossman, Zoe Ghertner — beauty editorial pastel-muted premium.

## TEXTURA & GRAIN
- **Grain profile:** **Kodak Portra 400 minimal** (mesma base de Portfolio, mas menor densidade ainda) ou **Fujifilm Pro 400H** pra tons levemente mais frescos. Porém: **nunca grain visível** no close-up de pele — beauty pede pele limpa-mas-real.
- **Alternativa opcional:** **zero grain** quando briefing pede look digital clean luxury (Aēsop-like) — mas material de pele/tecido/superfície **ainda exige micro-textura descrita**, só que sem grão sobreposto.
- **Pele:** descrição sempre como `clean skin with visible pores, matte finish with natural specular on high points, zero airbrush, zero beauty filter, zero skin smoothing`. Real-but-luminous.
- **Tecidos:** linho natural, algodão orgânico, seda leve, cashmere. Sempre com trama visível.
- **Superfícies de cenário:** plaster pintado mate, travertine, limestone, light oak, unlacquered brass — sempre com micro-textura.

## COMPOSITIONAL BIAS
- **Retrato humano sempre presente** — este kit é sobre pessoas. Mesmo se asset é "detalhe" ou "ornamento", referência humana (mãos, colo, silhueta) é recomendada.
- **Formato vertical 4:5 ou 3:4** predominante — ritmo editorial beauty magazine.
- **Horizontal 3:2** em headers de serviço / galeria de espaço.
- **Split 2-col mental:** sujeito num lado, negative space no outro (espaço reservado pro serif display + small caps label).
- **Eixo de câmera:** eye-level ou slight high angle (nunca low-angle — rompe a intimidade).
- **Sujeito raramente faz eye contact direto** — olhar lateral, baixo, fechado, perdido. A distância contemplativa é signature.

## TIPOGRAFIA RENDERIZADA (quando `hasText: true`)
Serif expressiva predominante; grotesque apenas em small caps para labels.
- **Famílias canônicas descritas no prompt:** Recoleta, Canela, GT Sectra Display, Migra, PP Editorial New Display, Fraunces (opsz high), ITC Garamond Light Display, Tiempos Headline.
- **Italic como recurso narrativo:** intercalar roman + italic na mesma frase quando briefing pedir (ex: `"Skin — "clean""` com "clean" em italic).
- **Escala:** `large editorial display occupying 15-30% of frame height`. Menor que Portfolio (que é massiva); aqui é elegante, não monumental.
- **Peso:** light, regular ou medium. **Nunca bold/black** (rompe a sensibilidade).
- **Tracking:** levemente aberto em display (+0.01em), muito aberto em small caps labels (+0.1em).
- **Cor do texto:** **deep-muted ink** (ex: dark brown #3E2A1F, dark sage #2E3A2E, dusty charcoal) — nunca preto puro. Ou **paleta deep da briefing** com warm undertone.
- **Tratamento:** `typography reads as editorial magazine cover layout, tasteful, unhurried, breath between words`. Nunca full-bleed knockout agressivo (isso é Portfolio).
- **Small caps labels** em sans humanista ou monospace serif — ex: `"BEAUTY"`, `"AESTHETICS"`, `"CONSULTATION"` em caixa alta pequena com tracking wide.

## MOTION BIAS (Seedance)
- **Câmera preferencial:** static with micro-breathing (quase imperceptível), very slow dolly-in, very gentle lateral drift.
- **Velocidade:** mais lenta que Portfolio — quase contemplativa.
- **Ritmo:** respirado — 5s é uma inspiração/expiração sustentada, 10s é uma cena meditativa (ex: sujeito abrindo olhos lentamente, luz deslizando no rosto).
- **Atmosfera dinâmica:** luz cambiante atravessando o frame (shaft of light drifting slowly), steam suave (tratamentos faciais), cortina de linho catching air subtle, cabelo soltando micro-movimento natural, pétalas caindo muito lentamente.
- **Vetos:** dolly-in agressivo, push-in rápido, orbital, qualquer movimento "ativo". Aqui cinema é **meditativo**.

## REJECTS (quando briefing viola o envelope)
- Paleta vibrante saturada → **Portfolio Editorial**
- Sans geométrica bold sem serif → **Tech Apple-ish**
- Produto-flutuante-clean-hero → **Tech Apple-ish**
- Tipografia monumental editorial aggressive → **Portfolio Editorial**
- Dark mode como default → **Tech Apple-ish**
- Narrativa declarativa minimal-bold → **Portfolio Editorial**

## PALAVRAS-ÂNCORA
`editorial beauty, soft, luminous, contemplative, tactile, natural, unhurried, intimate, premium-restraint, warm-muted, breath`

## PALAVRAS-VETO
`vibrant, bold, aggressive, saturated, graphic, declarative, neon, cool, minimal-tech, angular, rigid, product-showcase`

---

## PREAMBLE FORMAL — usado pelo engine

> Editorial beauty premium com registro de wellness/skincare luxury. Retrato humano dominante quando aplicável, paleta restrita a tons muted warm declarada em HEX — nunca vibrante, nunca cool. Captura em Hasselblad H6D-100c ou Phase One XT com lente 80mm MF a f/2.8-f/4, shallow DOF contemplativa, eye-level ou slight high angle. Iluminação natural ou daylight-emulated via large diffused source com soft wrapping universal, key:fill 2:1 a 3:1, low-key-suave sem crushed blacks, 5600K daylight ou 4000K golden-hour balanced. Pele clean com poros visíveis e zero airbrush, micro-textura preservada em tecidos naturais (linho, algodão, seda) e superfícies cream (plaster, travertine, light oak, unlacquered brass). Grain Kodak Portra 400 minimal ou zero grain digital-luxury. Composição vertical 4:5 com retrato em split mental, olhar raramente direto, negative space reservado pra tipografia serif expressiva (Recoleta, Canela, GT Sectra, Fraunces). Narrativa intimista, unhurried, breath. Zero airbrush, zero beauty filter, zero skin smoothing, zero saturação vibrante, zero cool cast.

O engine concatena este preamble + decupação das refs visuais do briefing + preenchimento dos 11 eixos da taxonomy.
