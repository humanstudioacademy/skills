# 07 — ESTRUTURA DE SITE

> Consultar ao estruturar arquitetura de informação, desenhar seções, definir navegação e configurar SEO técnico.

---

## 1. UM CTA dominante por fold
- Hero tem **UM** primário — não três
- CTAs secundários visualmente subordinados (peso tipográfico menor, sem cor de destaque)

## 2. Densidade informacional crescente
- **Hero**: afirmação única e forte
- **Meio**: suporte com densidade (métricas, exemplos, detalhe técnico)
- **Fim**: CTA + metadata real

## 3. Hierarquia narrativa explícita entre seções
- Cada seção = **um capítulo** com premissa clara
- Transições marcadas (overmark captions, numbered markers tipo `/ 01 — CHAPTER`)
- "Onde estou, pra onde vou" sempre respondível

## 4. Footer como documento, não lixeira
- Metadata real (CNPJ, endereço, políticas, última atualização)
- Nav secundária estruturada tipograficamente
- Footer editorial > dump de links

## 5. Loading e 404 existem desde o MVP
- Nunca entregar site sem loading state
- **404 respeita o DNA** + oferece caminho útil (buscar, voltar, contato)

## 6. Navegação com intenção
- Menu horizontal com **5-7 itens máx**
- Mega-menu só quando inevitável
- Breadcrumbs em hierarquias profundas
- Estado "current" claro em toda navegação

## 7. Componentes sistemáticos — zero one-offs
- **Button system** com max 3 variantes (primary / secondary / ghost)
- **Card system** unificado (mesma estrutura, variações por contexto)
- **Section patterns** documentados
- Grid components antes de custom divs

## 8. SEO técnico baseline
- Meta `title` / `description` únicos por rota
- Open Graph tags presentes
- `sitemap.xml` + `robots.txt`
- Structured data (JSON-LD) quando aplicável
- Canonical tags
