# 05 — QUALIDADE TÉCNICA DE IA

> Consultar ao gerar qualquer prompt para Nano Banana (imagem) ou Seedance 2.0 (vídeo). Este é o documento mais carregado durante execução em lote de assets.

---

## 1. Todo prompt de imagem exige obrigatoriamente:
- **Tipo de shot** (wide / medium / close / portrait)
- **Câmera + lente específica + abertura** (ex: `ARRI Alexa Mini LF + Zeiss Supreme Prime 40mm T2.8`)
- **Iluminação** (fonte, direção, temperatura Kelvin)
- **Paleta com cores específicas nomeadas**
- **Textura e grão explícitos**
- **Composição** (framing + regra + negative space)

## 2. Todo prompt de vídeo exige obrigatoriamente:
- **Movimento de câmera declarado** (`slow dolly-in`, `static`, `parallax left`)
- **Duração-alvo** (5-8s padrão)
- **Ritmo** (`24fps cinematic cadence`, `slow reveal`)
- **Motion blur diretiva** (onde sim, onde não)
- **Aspect ratio**

## 3. Negative prompts padrão (implícitos em todo request)
- `no plastic skin`
- `no vibrant saturation`
- `no generic stock aesthetic`
- `no glossy digital look`
- `no cluttered composition`
- `no harsh digital sharpening`
- `no motion blur on subject` · `no shaky handheld` (vídeo)

## 4. Especificidade técnica > adjetivos emocionais
- `2800K warm practical` **>** `warm lighting`
- `40mm at T2.8` **>** `cinematic`
- `Zeiss Supreme Prime` **>** `prime lens`
- Concretude técnica vence vocabulário subjetivo

## 5. Respeita limite de 3000 chars
- Compressor automático no wrapper (`hub.py`)
- Ao comprimir, preserva specs técnicos (câmera/luz/cor) e sacrifica narrativa conceitual

## 6. Checkpoint de qualidade pós-geração
- Claude analisa output antes de aceitar
- **Rejeição + regeneração** se:
  - Composição genérica
  - Cores escapando da paleta declarada
  - Texturas plásticas / digitais
  - Motion blur aplicado ao sujeito errado
  - Iluminação ignorando a diretiva

## 7. Controle de seed para consistência
- Série de assets relacionados (mesma personagem, mesmo ambiente, mesma hora do dia) usa **seed fixo**
- Seeds de assets-chave **documentados** pra regeneração futura
