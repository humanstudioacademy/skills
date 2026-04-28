# 04 — MOVIMENTO

> Consultar ao adicionar qualquer transição, reveal, hover, scroll-trigger ou orquestração de animação.

---

## 1. Motion serve o conteúdo — jamais distrai
- Toda animação carrega significado ou não existe
- Zero "wow factor" gratuito
- Sutileza > espetáculo

## 2. Easing sempre curvado — linear é proibido
- Movimento natural usa curvas (aceleração + desaceleração)
- **Conjunto padrão**:
  - Reveals: `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out-expo)
  - Transitions: `cubic-bezier(0.65, 0, 0.35, 1)` (ease-in-out-cubic)
- Linear parece robótico — nunca usado

## 3. Sistema modular de timing
- Base **200ms** → múltiplos (150 / 300 / 450 / 600 / 900 / 1200ms)
- Micro-interações: **150-200ms**
- Transições de UI: **300-450ms**
- Reveals narrativos: **600-900ms**
- Orquestrações completas: **1200ms** (raro)
- **Nunca valores arbitrários entre os múltiplos**

## 4. Stagger como ritmo
- Grupos de elementos animam com stagger consistente (**60-120ms**)
- Cria fluxo narrativo, não caos

## 5. `prefers-reduced-motion` respeitado sempre
- Fallback completo para estado estático
- Zero animações vestigiais pra users com motion reduzido

## 6. 60fps como mínimo inegociável
- Só `transform` + `opacity` em animações (GPU-accel)
- Nunca animar `width`, `margin`, `top/left` — jank garantido
- `will-change` com precisão cirúrgica, nunca blanket

## 7. Scroll-triggered reveals com disciplina
- Entrada: offset **16-32px** + opacity fade
- **UMA** propriedade por elemento (zero combos sliding + scaling + rotating)
- `IntersectionObserver` threshold `0.15-0.25` (trigger natural)
