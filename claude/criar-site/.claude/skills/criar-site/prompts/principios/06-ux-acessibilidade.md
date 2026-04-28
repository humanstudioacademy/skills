# 06 — UX / ACESSIBILIDADE

> Consultar ao definir breakpoints, cores de estado, semântica HTML, budgets de performance e, obrigatoriamente, como **checklist final** antes da entrega de qualquer site.

---

## 1. Mobile-first sempre
- Design começa em **375px**, escala pra cima
- Touch targets **≥ 44×44px**
- Zero ações críticas em hover-only

## 2. Contraste WCAG AA como piso, AAA como alvo
- Body **4.5:1** mínimo (alvo 7:1)
- Large text **3:1** mínimo
- Non-text elements (ícones, bordas de input) **3:1** mínimo

## 3. Foco visível sempre — `outline:none` sem substituto é proibido
- Custom focus rings respeitam DNA, mas nunca invisíveis
- `:focus-visible` preferido pra separar teclado de mouse

## 4. Semântica HTML correta
- **UM** `h1` por página
- Landmarks explícitos (`header` / `nav` / `main` / `aside` / `footer`)
- `alt=""` em imagem decorativa, descritivo em imagem informativa
- ARIA **só** quando HTML semântico não cobre

## 5. Performance budgets não-negociáveis
- **LCP** < 2.5s (alvo 1.5s)
- **INP** < 200ms (alvo 100ms)
- **CLS** < 0.1
- JS bundle < **200KB** sem lazy

## 6. Mídia otimizada por padrão
- **AVIF / WebP** com fallback
- `srcset` + `sizes` em imagens responsive
- Vídeos em **H.265 / WebM** com poster frame
- Lazy-load abaixo da dobra

## 7. Honestidade de estados
- **Loading states reais** (skeleton ou spinner) — nunca tela congelada
- **Error states** com mensagem específica + caminho de recuperação
- **Empty states** informativos
- **404** é oportunidade narrativa

## 8. Linguagem honesta em UI
- "Delete" ≠ "Remove" quando destrói
- Verbos de ação em botões (nunca só "OK")
- Confirmação dupla pra ações irreversíveis
