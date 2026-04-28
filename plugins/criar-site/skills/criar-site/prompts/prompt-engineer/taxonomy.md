# TAXONOMY — Prompt Engineering System

> **Régua operacional.** Todo prompt gerado pela skill `/criar-site` passa por esta taxonomia. Nenhum asset sai com densidade técnica menor do que a descrita aqui. Se faltar dado, o engine completa com soluções plausíveis dentro do realismo publicitário premium — nunca gera "genérico".

Herança direta do system prompt do **KinoImage Generator** (GPT custom construído pro MidJourney, traduzido aqui pra Nano Banana + Seedance 2.0), com 4 eixos extras pra vídeo.

---

## HIBRIDIZAÇÃO DE KITS (regra de composição)

Os 3 kits são **territórios cardinais**, não modelos fechados. Cada marca real nasce de uma **mistura proporcional** de 2 (às vezes 3) DNAs.

### Como declarar a mistura

O briefing traz — **internamente, nunca exposto ao usuário em vocabulário de kit**:
- **DNA principal** (estrutura, tipografia, layout, ritmo) — 1 kit.
- **DNA secundário** (paleta, mood, tratamento de imagem/vídeo) — 1 kit diferente (opcional).
- **Proporção estimada** (ex: 80/20, 70/30, 100/0).

Exemplos:
- `primary: portfolio-editorial (80) + secondary: clinica-estetica (20)` — studio de arquitetura boutique com estrutura editorial e paleta warm muted.
- `primary: tech-apple (70) + secondary: portfolio-editorial (30)` — lançamento AI/hardware com precisão Apple mas acento editorial assimétrico.
- `primary: clinica-estetica (100)` — projeto puro, sem mistura.

### Como o engine compõe preamble híbrido

1. Puxa **estrutura, tipografia, composição, motion biases** do primary preset.
2. Puxa **paleta, color science, luz baseline, grain profile, materialidade, tratamento de modelo** do secondary preset (na proporção declarada).
3. Quando primary e secondary divergem num eixo (ex: primary Portfolio pede accent saturada vibrante; secondary Clínica pede muted warm), o engine **resolve pela proporção** — 80/20 significa usar o accent do secondary como paleta base, mas manter um ponto saturado no espírito do primary (ex: accent terracotta saturada = middle ground).
4. O preamble final concatenado diz ao Nano/Seedance: "estrutura editorial + paleta warm muted + materialidade natural + tipografia grotesque condensada massiva" — tudo coerente, sem contradição.

### O `rejects` de cada kit vira sinal, não bloqueio

Antes (modelo fechado): "briefing pede warm-palette → kit Portfolio rejeita → redireciona pra Clínica."

Agora (modelo híbrido): "briefing pede warm-palette com estrutura editorial → isso é Portfolio primary + Clínica secondary. Mistura intencional → registrar proporção e prosseguir."

O `rejects` só bloqueia quando a mistura **não faz sentido coerente** — ex: 100% Clínica puro (serif romântica contemplativa) pedindo tipografia SF Pro Bold com periods não respira; aí o engine pausa e alinha.

### Tolerância à hibridização nos 11 eixos

Eixos que vêm do **primary**: 1 (linguagem visual registro), 5 (composição), 9 (cenário escala), 11 (coerência total).

Eixos que vêm do **secondary** na proporção declarada: 2 (cor e paleta), 3 (luz baseline), 6 (textura/grain), 7 (modelo tratamento), 8 (figurino registro).

Eixos técnicos comuns aos dois: 4 (câmera/lente), 10 (narrativa).

A proporção % influencia principalmente os eixos 2 (cor) e 3 (luz) — que são os mais visíveis no asset gerado. 80% Editorial + 20% Clínica significa cor/luz **dominantemente** Clínica (warm muted), mas com intensidade/saturação trazidas um pouco do Editorial (um ponto quente saturado pra não morrer em pastel).

---

## DOIS NÍVEIS DE REFERÊNCIA (distinção crítica)

Há **dois** tipos de "referência visual" no sistema. Nunca confundir.

### Nível A — REFS DE CALIBRAÇÃO INTERNA (régua do sistema)
Localização: `ref-prompt-engeneer/IMAGENS/` + `ref-prompt-engeneer/design/`.

- **Função:** servem pra **mim (Claude, operando a skill)** calibrar internamente o que significa "qualidade editorial publicitária premium" em termos de **iluminação, nitidez, composição, casting, densidade técnica, materialidade, paleta disciplinada**. São o **parâmetro estético geral** do módulo — a régua invisível que meus prompts precisam **descrever com equivalente densidade técnica**.
- **Como uso:** leio essas imagens quando preciso entender o patamar mínimo de descrição; não como template de estilo, mas como benchmark de rigor. Se meu prompt descreve luz menos detalhadamente do que essas refs mostram, o prompt está raso.
- **O que elas NUNCA fazem:**
  - ❌ Nunca viram `reference_images` em chamada de API.
  - ❌ Nunca são mencionadas pelo nome, tipo, ou sujeito em prompts gerados.
  - ❌ Nunca servem como referência de estilo direto pra nenhum asset de nenhum projeto.
  - ❌ Nunca são anexadas a nada que vai pro Nano ou Seedance.
- **Resumo mental:** essas imagens ensinam o sistema a **pensar como um diretor de fotografia editorial**, não ensinam o sistema a **gerar cópias delas**.

### Nível B — `visualRefs` DO BRIEFING (refs por projeto)
Localização: campo `visualRefs` do `briefing.json` de cada projeto, alimentado pelo usuário na Fase 2.

- **Função dupla:**
  - (a) Informar a destilação do briefing (paleta HEX extraída, mood, kit-fit).
  - (b) Anexadas como `reference_images` na chamada Freepik, **com prefixo obrigatório** — ver regra global abaixo.
- **Essas sim podem virar input de API.** Nível A nunca.

---

## REGRAS OPERACIONAIS GLOBAIS

1. **Saída sempre em inglês técnico.** Nano e Seedance respondem com mais fidelidade em inglês — português trava a qualidade.
2. **Nunca usar sintaxe MidJourney** (`--ar`, `--v`, `--style`, `--no`, `--stylize`). Dois traços consecutivos são proibidos em qualquer output.
3. **Nunca explicar o prompt.** O engine cospe o prompt e nada mais; não há preâmbulo, não há comentário, não há "aqui está".
4. **Densidade mínima:** todo prompt obrigatoriamente preenche os 11 eixos (imagem) ou 15 eixos (vídeo). Nenhum eixo pode sair vazio — se faltar dado do briefing, o engine faz escolha tecnicamente plausível.
5. **Paleta restrita** — máximo 3 tons dominantes, especificados em HEX quando possível, com dominância declarada (ex: "80% deep oxblood, 15% cream, 5% black accents").
6. **Coerência total** — todos os 11/15 eixos pertencem ao mesmo universo visual. Nenhuma contradição de escala, material, luz ou tom.
7. **Refs visuais do briefing têm papel duplo:**
   - **(a) Norte estético do briefing** — durante a Fase 2/2.5, as refs guiam a destilação da ficha (paleta HEX extraída, mood, luz decupada, kit-fit). Elas **informam o briefing**, não só a chamada da API.
   - **(b) Image reference na API** — anexadas no payload Freepik, reforçadas no texto do prompt com descritores técnicos do que elas mostram.
   - O texto do prompt deve descrever o que as refs já mostram, reforçando (nunca contradizendo) o que o sistema já vai ver visualmente.
8. **Prefixo obrigatório quando há image refs no prompt do Nano:** o prompt **sempre** começa com *"Use the reference images only as aesthetic, compositional, and visual-aspect references to generate the following image:"*. Sem esse prefixo, Nano copia demais a referência em vez de compor cena nova. Prefixo omitido apenas quando `visualRefs.length === 0` ou em modo `image-to-video` do Seedance (que trata sourceImage como frame literal, comportamento desejado).
9. **Proibições linguísticas** — banir absolutamente: "beautiful", "stunning", "amazing", "high quality", "4K", "8K", "hyperrealistic", "masterpiece", "award-winning". Essas palavras são ruído — o rigor técnico entrega qualidade, não adjetivos.

---

## OS 11 EIXOS — IMAGEM (Nano Banana)

Todo prompt de imagem preenche estes 11 eixos, nesta ordem. Cada eixo é obrigatório; nenhum é ornamento.

### 1. LINGUAGEM VISUAL
Tom declarativo de 1 frase. Não é "vibe" genérica — é posicionamento estético específico.
- **Registro obrigatório:** realismo contemporâneo com refinamento publicitário; sofisticação editorial; teatralidade contida; presença dominante do sujeito; atmosfera controlada.
- **Exemplo:** *"editorial fashion photography with controlled theatricality, single-subject dominance against graphic backdrop"*

### 2. COR E CIÊNCIA DE COR
- **Paleta restrita** — até 3 tons dominantes, nomeados e idealmente em HEX.
- **Dominância cromática** — qual tom ocupa quanto do frame.
- **Relação figura-fundo** — contraste de saturação explícito.
- **Qualidade dos pretos** — `crushed blacks`, `lifted blacks`, `clean blacks`, `milky blacks`.
- **Highlight roll-off** — `controlled`, `hard clip`, `smooth falloff`.
- **Temperatura de cor em Kelvin** — `3200K tungsten`, `5600K daylight`, `2800K warm practical`, `mixed color temperature (balance specified)`.
- **Exemplo:** *"palette locked to three tones — 75% deep cadmium red wall (#C2261A range), 20% olive khaki linen, 5% polished black leather; clean blacks, controlled highlight roll-off; 2800K warm practical key balanced against 5600K ambient fill"*

### 3. ILUMINAÇÃO CINEMATOGRÁFICA
- **Esquema:** key, fill, rim, backlight, practicals — sempre explícito.
- **Qualidade:** `hard`, `soft`, `diffused`, `specular`, `wrapping`.
- **Direção:** `45° camera-left`, `top light`, `Rembrandt`, `butterfly`, `split lighting`, `loop lighting`.
- **Intensidade relativa:** razão key:fill (`4:1`, `8:1`) quando pertinente.
- **Contraste:** `low key`, `mid contrast`, `medium-high contrast`, `high contrast with deep shadow`.
- **Textura da luz sobre pele e materiais** — como a luz se comporta em cada superfície.
- **Modificadores plausíveis:** `softbox`, `fresnel`, `parabolic reflector`, `diffusion silk`, `grid`, `snoot`, `book light`.
- **Exemplo:** *"single 5ft parabolic softbox camera-left at 45°, key-to-fill ratio 6:1, no rim; medium-high contrast with clean shadow under jaw; specular rolloff on leather boot, diffused wrap across linen fabric"*

### 4. CÂMERA E LENTE
- **Câmera plausível** — cinema ou médio formato.
  - Cine: `ARRI Alexa Mini LF`, `Sony VENICE 2`, `RED V-Raptor`, `RED KOMODO`.
  - Stills: `Hasselblad H6D-100c`, `Phase One XT`, `Leica S3`, `Mamiya RZ67` (analog feel).
- **Lente** — 35-50mm predominante, com desvio justificado.
  - Tipos: `Zeiss Supreme Prime`, `Cooke S7/i`, `Cooke S4`, `ARRI Signature Prime`, `anamorphic`, `spherical`, `vintage Leica R`.
- **Abertura** — `f/1.8`, `T2.0`, `f/2.8`, `f/4`, `f/8`.
- **Profundidade de campo** — `shallow DOF with tack-sharp subject`, `deep focus`, `selective focus plane`.
- **Compressão de perspectiva** — `flat compression (telephoto feel)`, `natural 50mm render`, `mild wide distortion`.
- **Microcontraste e falloff** — tem que estar descrito.
- **Exemplo:** *"shot on ARRI Alexa Mini LF with Cooke S7/i 40mm at T2.0; tack-sharp focus on eye, shallow DOF, natural perspective, high microcontrast with filmic falloff into shadow"*

### 5. COMPOSIÇÃO
- **Hierarquia visual clara** — um único sujeito dominante por frame (regra editorial).
- **Espaço negativo intencional** — quantidade e posição.
- **Regra dos terços** — seguida ou **quebrada intencionalmente** (declarar qual).
- **Blocking** — em caso de múltiplos sujeitos, posições relativas explícitas.
- **Eixo de câmera** — `eye-level`, `low angle for dominance`, `slight high angle for vulnerability`, `neutral observer height`.
- **Formato declarado** — `vertical 4:5`, `horizontal 3:2`, `square 1:1`, `cinemascope 2.39:1`.
- **Exemplo:** *"central single-subject composition with broken rule-of-thirds, subject placed on vertical center-line, 30% negative space above head, slight low angle emphasizing dominance, vertical 4:5 framing"*

### 6. TEXTURAS E MATERIALIDADE
- **Descrição minuciosa das superfícies** — granulação, porosidade, brilho especular, reflexividade, absorção de luz, desgaste, fibras têxteis, densidade do couro, trama do denim, escovação do metal.
- **Interação da luz com cada material.**
- **Contraste entre superfícies matte e gloss.**
- **Grão/grain** — `refined filmic grain, minimal and structured`, `Kodak Portra grain`, `no digital noise`.
- **Exemplo:** *"matte dry-plaster wall showing micro-cracks and pigment granulation, absorbing light without specular; against polished leather with high specular roll-off and visible grain; linen fabric with coarse open weave diffusing light across folds; subtle Kodak Portra 400 grain across the frame, zero digital noise"*

### 7. MODELOS / PERSONAGENS
Descrever com riqueza técnica e respeito. Nunca estereotipar; tratar diversidade com precisão e naturalidade.
- **Etnia aparente** (quando relevante pro frame).
- **Tonalidade e subtom de pele** — `deep brown with warm red undertone`, `medium olive with cool undertone`, `fair porcelain with pink undertone`.
- **Estrutura óssea** — `high cheekbones`, `strong jawline`, `soft oval structure`.
- **Traços faciais** — descrição precisa sem adjetivos vazios.
- **Textura da pele** — `clean skin with visible pores`, `matte finish`, `dewy specular on high points`.
- **Cabelo** — tipo, densidade, acabamento (`tight coils, densely packed`, `straight silky shoulder-length`, `loose waves with natural sheen`).
- **Postura e microexpressão** — `weight on right leg, shoulders squared to camera, chin slightly lowered, neutral mouth, direct eye contact`.
- **Idade aproximada** — `early 20s`, `late 30s`, `mid-50s`.
- **Singularidades físicas** — freckles, scars, tattoos, piercings, etc. (opcional mas bem-vindo).

### 8. FIGURINO
- **Construção e corte** — `tailored shoulder`, `boxy oversized cut`, `bias-cut drape`.
- **Caimento e peso do tecido** — `heavy wool falling in sharp fold`, `lightweight silk catching air`, `stiff canvas holding structure`.
- **Costura e acabamento** — `raw edge`, `topstitched`, `French seam`, `visible construction`.
- **Resposta à luz** — `matte absorbing`, `specular catching highlight edge`, `translucent with backlight`.
- **Coerência com cenário e narrativa** — roupa tem que pertencer ao mesmo universo.
- **Silhueta gráfica** — contorno contra fundo, figura-fundo.

### 9. CENÁRIO
- **Minimalista ou simbólico** — cenário amplifica o sujeito, nunca compete.
- **Escala** — `intimate close-range space`, `vast architectural void`, `mid-range studio setup`.
- **Profundidade atmosférica** — `compressed flat backdrop`, `deep atmospheric perspective`, `controlled haze for separation`.
- **Textura de superfície e acabamento** — `raw concrete with visible aggregate`, `painted matte plaster wall`, `brushed steel`, `polished marble`, `controlled mist`, `softbox white infinity`.
- **Coerência cromática** — cenário pertence à paleta declarada.

### 10. NARRATIVA
- **1 frase** — qual a tensão do frame?
- **Personagem com intenção clara** — o que está acontecendo emocionalmente?
- **Atmosfera emocional** sustentada pela fotografia, não pela descrição explícita.
- **Simbólica, concisa, sofisticada** — nunca literal, nunca brega.
- **Exemplo:** *"subject holds composed stillness before a decisive movement, weight of anticipation carried in the set of the shoulders"*

### 11. COERÊNCIA TOTAL (checkpoint final)
Antes de emitir o prompt, o engine verifica:
- Nenhum material contradiz a luz declarada?
- Nenhum elemento quebra a paleta?
- A escala do cenário bate com a lente escolhida?
- O figurino pertence ao mesmo universo do cenário?
- A narrativa é coerente com a pose e luz?

Se alguma falha, o engine **corrige com decisão mais sofisticada e tecnicamente plausível** — nunca emite com contradição.

---

## OS 4 EIXOS EXTRA — VÍDEO (Seedance 2.0)

Vídeo herda todos os 11 eixos de imagem, e adiciona 4. Lembrete: Seedance 2.0 aceita **apenas 5s ou 10s** de duração (API constraint, ver `feedback_seedance_duration.md`).

### 12. MOVIMENTO DE CÂMERA
Nunca "handheld shake" genérico. Sempre declarar tipo + velocidade + trajetória.
- **Tipos primários:**
  - `slow dolly-in` — aproximação constante.
  - `slow dolly-out` — afastamento revelador.
  - `lateral tracking` — paralelo ao sujeito.
  - `subtle push-in` — micro-aproximação durante a cena.
  - `crane-up` / `crane-down` — movimento vertical.
  - `static with micro-oscillation` — câmera "respirando".
  - `orbital` — giro em torno do sujeito.
- **Velocidade:** `slow`, `moderate`, `deliberate`. Nunca "fast" (quebra o registro editorial).
- **Trajetória:** linear / arco / composto.
- **Vetos:** `whip-pan`, `handheld shake`, `dutch tilt dinâmico`, `snap-zoom` — a menos que o DNA do kit justifique.
- **Exemplo:** *"slow dolly-in toward subject across 10 seconds, linear trajectory, deliberate pace, camera height remaining at subject's eye level"*

### 13. RITMO DRAMÁTICO
Duração como decisão narrativa.
- **5s** = um único gesto, um batimento, um micro-momento. Não cabe arco; cabe *um instante sustentado*.
- **10s** = mini-arco — começo, desenvolvimento, resolução. Um shot tem que respirar.
- **Beat descrito** — quando o "momento-chave" acontece dentro do tempo (`beat at 0:03`, `reveal at 0:07`).
- **Exemplo (5s):** *"single sustained gesture — subject slowly exhales and closes eyes, full duration"*
- **Exemplo (10s):** *"subject begins in stillness (0:00-0:03), lifts chin with deliberate intent (0:03-0:06), settles into held gaze (0:06-0:10)"*

### 14. MOTION BLUR & SHUTTER
Seedance respeita shutter angle.
- **Cine standard** — `180° shutter angle, 24fps cinematic cadence`.
- **Double shutter** — `90° shutter for crisper motion` (uso raro, estilizado).
- **Motion blur nos elementos certos** — sujeito sempre sharp; motion blur em foreground cinético (partículas, chuva, faíscas, tecido esvoaçando) ou background passante.
- **Frame rate feel** — `24fps cinematic cadence` por padrão; `48fps slight slow-motion feel` só com justificativa.

### 15. ATMOSFERA DINÂMICA
O que se move além do sujeito principal — o que dá vida à cena sem competir.
- **Partículas:** `fine dust motes catching key light`, `soft falling snow`, `drifting steam`, `particles hanging in atmospheric haze`.
- **Tecido:** `linen catching subtle air movement`, `hair lifting slightly in ambient breeze`.
- **Luz cambiante:** `shaft of light drifting slowly across face as cloud passes`, `candlelight flicker on surrounding surfaces`.
- **Backgrounds passantes:** `silhouettes crossing behind subject out of focus`, `traffic motion blur in deep background`.
- **Regra:** atmosfera dinâmica **sustenta** o sujeito; nunca rouba atenção.
- **Silêncio como ferramenta** — se a cena pede stillness, o campo 15 pode declarar `atmosphere held in near-stillness, only breath and subtle fabric movement`.

---

## NEGATIVE DIRECTIVES (aplicável a todos os prompts)

Linguagem que o engine **inclui explicitamente** quando pertinente, pra cortar drift do modelo:

- `no plastic skin, no airbrush effect, no beauty filter`
- `no HDR crunchy look, no over-sharpening halos`
- `no digital noise, no banding, no compression artifacts`
- `no cartoon stylization, no illustration feel, no 3D render look`
- `no stock photography cliché, no generic studio glossy`
- `no floating objects without physics, no broken anatomy`
- `no text artifacts, no watermarks, no logos` (a menos que o briefing explicitamente peça texto renderizado)

Pra Seedance adicionar:
- `no frame stutter, no warping, no morphing between frames`
- `no identity drift on subject face across duration`
- `no background pumping or gaining sharpness inconsistently`

---

## FORMATO DE ENTREGA (contrato de saída)

O engine **sempre** cospe:

```
{prompt em inglês, 1 bloco corrido, 400-900 palavras, 11 ou 15 eixos presentes, zero adjetivos vazios}

NEGATIVE: {string única de proibições relevantes pro asset, separadas por vírgula}
```

Nada antes, nada depois. Zero comentário, zero explicação, zero parâmetro MidJourney.

Esse é o payload que entra literal na chamada HTTP da API Freepik.
