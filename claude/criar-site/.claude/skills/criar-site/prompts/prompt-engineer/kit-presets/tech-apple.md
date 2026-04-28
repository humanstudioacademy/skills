# KIT PRESET — Tech Apple-ish

> **Preamble fixo injetado pelo engine em todo prompt deste kit.** Traduz o DNA (produto flutuante clean + sans geométrica bold com periods + paleta fria neutra + light/dark variant + accent trocável via briefing + precisão cinematic) em decisões técnicas pro Nano Banana e Seedance 2.0. Universo: Apple product pages, premium hardware launches (Teenage Engineering, Nothing, Opal Camera, Rabbit, Humane), AI-product showcases (Perplexity, Vercel, Linear).

**Régua mínima de qualidade:** mesmo que o registro seja "clean digital" (não editorial filmic), o prompt deve ter densidade técnica equivalente às refs. "Clean" não é ausência de descrição — é descrição **precisa** de luz controlada, reflexos calibrados, materialidade exata de alumínio/vidro/alumínio anodizado, profundidade atmosférica medida.

---

## CÂMERAS PREFERENCIAIS
- **Product photography primária:** Phase One XT IQ4 150MP, Hasselblad H6D-100c.
- **Commercial alternative:** Fujifilm GFX100 II, Sony A1 II (para lifestyle).
- **Cine (pra vídeo product hero):** ARRI Alexa 35, Sony VENICE 2 (6K Alexa para reveal shots).
- **Nunca:** câmeras com look "analog warm" — rompe a precisão digital do kit.

## LENTES PREFERENCIAIS
- **Product shots:** 120mm Macro Hasselblad HC, 150mm Macro Phase One Schneider Kreuznach — renderização plana perfeita, zero distorção.
- **Alternative:** 80mm MF para product em 3/4.
- **Wide para lifestyle/contextual:** 45mm MF (35mm equiv FF).
- **Cine lens:** Zeiss Supreme Prime 50mm T1.5 para product hero motion; Cooke S7/i só quando briefing explicitar "cinematic warm" (raro em Tech).
- **Abertura padrão:** **f/8 a f/11** em product shots (deep focus universal), **f/1.8-f/2.8** em lifestyle ou dark-mode dramatic.
- **Vetos:** vintage character lenses (Leica R, Helios, Petzval) — quebra limpeza digital.

## ILUMINAÇÃO BASELINE
- **Esquema padrão — LIGHT MODE:** multi-source controlled, **clean studio infinity** ou **softbox environment seamless**.
  - Top light large softbox (overhead soft key).
  - Side fills de ambos os lados pra eliminar sombra dramática.
  - Subtle rim opcional nas bordas do produto pra destacar contra fundo claro.
  - Key:fill **2:1 a 1.5:1** — quase flat, mas com modelagem mínima.
  - **Objetivo:** produto lido como silhueta gráfica com specular precisos, zero sombra pesada.
- **Esquema padrão — DARK MODE:** **cinematic single-source dramatic**.
  - Key single hard source (fresnel focado ou spotlight), lateral a 45°-60°.
  - Zero fill (ou fill negativo), deixando metade do produto em shadow profunda.
  - Rim forte no contorno pra separar da escuridão total.
  - Key:fill **10:1 ou maior** — contraste cinematográfico.
  - **Objetivo:** produto como escultura dramática, shadow e highlight em igual peso visual.
- **Temperatura:** **5600K daylight clean** (light mode) ou **3200K mixed tungsten** (dark mode cinematic).
- **Qualidade:** light mode = soft universal; dark mode = hard specular + diffused shadow.
- **Modificadores frequentes:** large softbox grids, blackwrap flags pra controle absoluto, cookie patterns (só em dark mode para sombra gráfica).

## TRATAMENTO DE COR
- **Paleta fria neutra sempre** — light grey Apple #F5F5F7 ou deep black Apple #0A0A0A dominante.
- **Accent trocável via briefing** (Apple blue #0071E3, roxo #6C5CE7, verde #30D158, etc.) — usada em pontos específicos: tipografia CTA, elemento do produto, ambient lighting (raramente).
- **Material do produto em HEX:** aluminum space grey #4A4A4A, titanium #6D6B6D, gold #D4B896, silver #C0C0C0 — sempre declarado.
- **Dominância em %:** ex: "65% near-white studio #F5F5F7, 25% titanium grey product surface #6D6B6D, 10% accent blue #0071E3 on illuminated screen".
- **Color science:** **clean digital clinical** — zero warm cast, zero grain teinture, highlight specular branco puro, shadow neutral grey.
- **Proibido:** qualquer warm cast, qualquer saturação exceto accent declarada, qualquer "mood color wash".
- **Refs de color science:** Apple marketing (product pages oficiais), Teenage Engineering catalog, Nothing product imagery.

## TEXTURA & GRAIN
- **Grain profile:** **ZERO grain em light mode** — digital-clean absoluto. Permitido **microscopic dither** em dark mode cinematic pra evitar banding (quase imperceptível).
- **Materialidade obrigatória em descrição:**
  - Alumínio: `brushed aluminum with fine linear grain texture, satin anodized finish, specular roll-off diagonal across surface`.
  - Vidro: `optically flat glass with precise edge refraction, sub-surface scatter at edges, controlled reflections`.
  - Polímero: `soft-touch matte polymer with subtle microstructure, diffuse light absorption`.
  - Metal polido: `high-specular polished metal with controlled environmental reflection, clean horizon line reflection`.
  - OLED/screen: `deep inky OLED blacks with pixel-level sharpness, accent color radiating slight bloom, anti-reflective coating pattern subtle`.
- **Proibido:** grain filmico, texture overlay, paper-like surface, warm analog patina.

## COMPOSITIONAL BIAS
- **Produto centralizado absoluto** — simétrico, hierárquico, flutuante.
- **Negative space **enorme** em todas as direções** — produto ocupa tipicamente 30-50% do frame, resto é ar.
- **Formato horizontal 16:9, 3:2 ou cinemascope 2.39:1** predominante (Apple hero pages).
- **Vertical 9:16 ou 4:5** em hero mobile-first ou feature highlights.
- **Eixo de câmera:** perfectly level ou slight isometric 3/4 (`camera height exactly aligned with product center-line, 15°-30° offset isometric angle for 3/4 view`).
- **Product floating** — sombra de chão sutil ou ausente, como se o objeto estivesse flutuando em vazio.
- **Bordas limpas do produto** sempre renderizadas nítidas (edge sharpness máxima).

## TIPOGRAFIA RENDERIZADA (quando `hasText: true`)
Sans geométrica bold com periods — signature Apple.
- **Famílias canônicas:** SF Pro Display Bold, Inter Display Bold, Geist Variable Bold, Neue Haas Unica Black, Helvetica Now Display Black.
- **Monospace opt-in** (pra specs/stats): JetBrains Mono, Berkeley Mono, Geist Mono — usado em small labels, benchmarks, stats.
- **Escala:** `dominant bold display 15-25% of frame height, paired with small specs/caption beneath`.
- **Peso:** bold ou black — nunca regular, nunca light. Apple não usa light.
- **Periods nos títulos:** `text content always ends with period — "Hello." "Pro." "Unreal." "Unbelievable."` (signature Apple tipográfico).
- **Tracking:** tight negative em display (-0.02em a -0.03em).
- **Cor do texto:** **Apple ink #1D1D1F** em light mode, **off-white #F5F5F7** em dark mode, ou **accent da briefing** direto em CTAs.
- **Tratamento:** `title-case, crisp anti-aliased edges, pixel-perfect rendering, no drop-shadow, no glow, no outline unless accent highlight`.
- **Proibido:** serif, handwritten, italic, warped, condensed grotesque heavy (isso é Portfolio), casings caóticos.

## MOTION BIAS (Seedance)
- **Câmera preferencial:**
  - **Product hero:** orbital 3/4 smooth, slow reveal rotation (180° em 5s ou 360° em 10s), subtle push-in com depth acceleration.
  - **Interface/screen focus:** static locked + UI animation no screen do produto.
  - **Lifestyle:** steady handheld gimbal smooth (não shake).
- **Velocidade:** **precisa, mechanical, robotic-smooth** — nunca orgânica.
- **Ritmo:** preciso — 5s tende a ser "um reveal único" (ex: close-up detalhando um botão, screen iluminando-se, caixa abrindo); 10s tende a ser "mini-arco de product showcase" (beat de reveal + beat de rotation + beat de feature highlight).
- **Atmosfera dinâmica:** luz deslizando em metal brushed, UI screen animation sutil, ambient particles tecnológicos (só quando briefing justifica — ex: "AI vibe"), zero partícula orgânica (dust, pollen, fumaça).
- **Vetos:** handheld shake, grain de movimento filmico, warm motion blur artístico, qualquer coisa "humana" no movimento.

## REJECTS (quando briefing viola o envelope)
- Warm palette (cream/sage/rose) → **Clínica Estética**
- Serif display expressivo → **Clínica Estética** ou **Portfolio Editorial**
- Accent vibrante saturada como dominante (não só CTA) → **Portfolio Editorial**
- Grain filmico / analog look → **Portfolio Editorial**
- Retrato humano como elemento dominante → **Clínica Estética**
- Ornamento alfanumérico signature → **Portfolio Editorial**

## PALAVRAS-ÂNCORA
`precise, clean, minimal, geometric, engineered, luminous, crystalline, floating, calibrated, clinical-premium, seamless, pixel-perfect, optical`

## PALAVRAS-VETO
`organic, warm, natural-light, filmic, grainy, rustic, handcrafted, imperfect, analog, dusty, moody-warm, editorial-magazine, vintage`

---

## PREAMBLE FORMAL — usado pelo engine

> Apple-like product showcase premium com registro de tech hardware launch / AI product page. Produto centralizado flutuante como herói, paleta fria neutra (#F5F5F7 light ou #0A0A0A dark) + accent declarado via briefing. Captura em Phase One XT IQ4 ou Hasselblad H6D-100c com 120mm Macro Schneider a f/8-f/11 para product shots, ou ARRI Alexa 35 com Zeiss Supreme Prime 50mm para motion. Iluminação clean studio infinity em light mode (multi-source key:fill 2:1 soft, top softbox + bilateral fills, rim subtle) OU cinematic single-source dramatic em dark mode (hard fresnel 45°-60°, zero fill, key:fill 10:1, strong rim separation). Temperatura 5600K clean light ou 3200K cinematic dark. Zero grain digital-clean absoluto. Materialidade precisa: brushed aluminum satin anodized, optically flat glass with controlled reflections, soft-touch matte polymer, high-specular polished metal, deep OLED blacks com pixel sharpness. Composição simétrica centralizada com produto ocupando 30-50% do frame, negative space universal, formato horizontal 16:9 ou cinemascope 2.39:1, eye-level locked ou slight isometric 3/4. Tipografia SF Pro Display Bold ou Inter Display Bold title-case com periods, crisp anti-aliased. Zero warm cast, zero saturação exceto accent, zero organic texture, zero handcrafted imperfection, zero filmic grain.

O engine concatena este preamble + decupação das refs visuais do briefing + preenchimento dos 11 eixos da taxonomy, com atenção especial ao campo `light | dark` do briefing (variante nativa deste kit).
