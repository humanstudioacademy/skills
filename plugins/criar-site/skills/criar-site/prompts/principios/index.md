# PRINCÍPIOS UNIVERSAIS — CONSTITUIÇÃO DO SISTEMA

> Estes princípios aplicam-se a **todo site** gerado pela Skill `/criar-site`, independente do DNA estético escolhido ou do briefing do usuário. **São não-negociáveis.**

---

## Arquitetura de 3 camadas

```
CAMADA 1 — PRINCÍPIOS UNIVERSAIS  (este documento)
  └── Qualidade, hierarquia, performance, composição, acessibilidade

CAMADA 2 — DNAs DE ESTILO         (prompts/estilos/*.md)
  └── cinematic-density, minimal-product, editorial-soft, etc.
  └── Biblioteca — usuário escolhe UMA por site

CAMADA 3 — PERSONALIZAÇÃO         (briefing do /criar-site)
  └── Tema, seções, paleta contextual, copy, assets
```

Os princípios desta constituição **vetam** qualquer escolha de Camada 2 ou 3 que os violem.

---

## Como consultar estes documentos durante a execução da Skill

Carregar apenas o princípio relevante pra cada passo (economia de contexto):

| Fase do workflow | Princípio(s) a consultar |
|---|---|
| Escolher tipografia | `02-tipografia.md` |
| Montar paleta | `03-cor.md` |
| Compor layout de seção | `01-composicao.md` + `07-estrutura-site.md` |
| Gerar prompt pra Nano Banana / Seedance | `05-qualidade-ia.md` |
| Adicionar animações/transições | `04-movimento.md` |
| Antes de entregar (checklist final) | `06-ux-acessibilidade.md` |

---

## Índice

- **[01 — Composição visual](01-composicao.md)** — Grid, hierarquia, assimetria, alinhamento, ponto focal
- **[02 — Tipografia](02-tipografia.md)** — Parcimônia, escala modular, tracking, hierarquia por peso
- **[03 — Cor](03-cor.md)** — Paleta reduzida, função, temperatura intencional, contraste
- **[04 — Movimento](04-movimento.md)** — Easing curvado, timing modular, stagger, reduced-motion, 60fps
- **[05 — Qualidade técnica de IA](05-qualidade-ia.md)** — Specs obrigatórios, negative prompts, specificity, seeds
- **[06 — UX / Acessibilidade](06-ux-acessibilidade.md)** — Mobile-first, WCAG, semântica, performance, estados
- **[07 — Estrutura de site](07-estrutura-site.md)** — Um CTA por fold, densidade crescente, footer editorial, SEO

---

## Princípios-tótem (não-negociáveis absolutos)

Os 5 que, se violados, **invalidam qualquer output do sistema**:

1. **Grid matemático sempre** — nenhuma composição sai sem sistema de grid (cf. 01)
2. **Paleta máxima de 4 cores ativas** — reduzir é a regra (cf. 03)
3. **60fps em toda animação** — sem exceção (cf. 04)
4. **Especificidade técnica em prompts de IA** — câmera + lente + luz + paleta sempre (cf. 05)
5. **WCAG AA como piso absoluto** — contraste e foco nunca negociáveis (cf. 06)
