# 03 — COR

> Consultar ao montar paleta do site, escolher cor de acento, definir estados (hover/focus/disabled) e aplicar overlays.

---

## 1. Paleta radicalmente reduzida: máximo 3-4 cores ativas
- Base **near-black** (ex: `#0A0B0D`) — nunca `#000` puro
- Contraponto **off-white** (ex: `#F5F3EE`) — nunca `#FFF` puro
- **UMA** cor de acento funcional
- Uma secundária opcional (estados / feedback)

## 2. Cor serve função — jamais decora
- Acento sinaliza ação, status ou foco — nunca "porque fica bonito"
- Decoração vem de estrutura, não de cor

## 3. Neutros com temperatura intencional
- Preto tende sutilmente a azul / verde / cinza-quente
- Branco tende a cream / bege / cool-gray
- Zero neutros "literais" puros

## 4. Contraste carrega hierarquia
- **Body**: AA mínimo (4.5:1), alvo AAA (7:1)
- **Meta / caption**: contraste reduzido intencional (≥ 3:1)
- **Headings**: contraste máximo

## 5. Gradientes são exceção
- **Permitido**: overlays sutis em mídia (fade bottom-up em imagem/vídeo full-bleed)
- **Proibido**: gradientes decorativos em cards, backgrounds de seção, botões
- Cor chapada > cor degradê por padrão

## 6. Paleta com disciplina print-first
- Cada cor precisa sobreviver em P&B (teste brutal de contraste)
- CMYK-friendly — evita fluorescentes digitais-only
- **Menos cores é mais**
