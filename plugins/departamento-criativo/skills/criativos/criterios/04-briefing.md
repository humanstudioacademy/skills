# Briefing — Onboarding e Template (Camada 2: nicho/contexto)

> Roda uma vez por marca/nicho (`/criativos`), persiste, e é reusado em toda avaliação. É o que instancia o canon no nicho e **pondera os pesos das lentes**. Sem ele, o painel roda só no canon (genérico, cego ao nicho).

---

## Parte A — Onboarding (`/criativos`)

**Regra mestra de UX: a taxonomia é problema da skill, não do usuário.** Ele fala natural ("sempre faço X, nunca Y"); a skill é que classifica nos três blocos (nicho / DO-DON'T / linha vermelha). Nenhuma pergunta usa esses termos. Poucas perguntas, a skill propõe e classifica, o usuário confirma.

### Atalho de engenharia reversa (sempre oferecer primeiro)
> "Vou aprender sua marca uma vez (~3 min). Atalho: se tiver guia de marca, CLAUDE.md ou 2-3 posts que funcionaram, cola aqui que eu extraio o que der."

Se o usuário colar material, a skill **lê via vision + texto** e pré-preenche tom, DO's/DON'Ts e padrões — chega com o rascunho pronto pra ele só corrigir. Página em branco zero.

### As perguntas (curtas; a skill completa)
1. **Nicho** — "Qual seu nicho/sub-nicho?"
2. **Público + dor** — "Quem é seu público e a dor nº1 dele?" → skill infere nível de consciência e propõe.
3. **Formatos + objetivo** — "Que formatos você mais produz e o objetivo de cada um?" (parar scroll / salvar / comentar / vender / autoridade)
4. **Vida útil** — "Mais efêmero (≈48h) ou evergreen?" → calibra profundidade.
5. **O que funciona** — *skill PROPÕE:* "Nesse nicho costumam funcionar [X, Y, Z] e já saturaram [W]. Tira/adiciona?"
6. **Sempre/nunca da marca** — "2-3 coisas que sua marca **sempre** faz e 2-3 que **nunca** faz."
7. **Inegociáveis** (única classificação que o usuário faz) — "Dos seus 'nunca', quais são **inegociáveis** — a marca se contradiz se fizer?"
8. **Tom + referências** — "Tom em uma frase? 2-3 referências que admira + 1 anti-referência."

### A classificação (a skill faz sozinha, nos bastidores)
| O que o usuário diz | Bloco no `briefing.md` |
|---|---|
| padrões da pergunta 5 | **Nicho** (compartilhado) |
| "sempre faz" (pergunta 6) | **DO da marca** |
| "nunca faz" graduado (pergunta 6) | **DON'T da marca** |
| "nunca" marcado inegociável (pergunta 7) | **Linha vermelha** (hard stop) |
| tom + anti-referência (pergunta 8) | **Tom / Coerência** |

> Só a pergunta 7 pede julgamento de classificação do usuário (DON'T graduado vs hard stop). Todo o resto a skill deduz.

### Confirmação
A skill mostra o `briefing.md` montado (blocos preenchidos) e o usuário **edita inline**. Roda uma vez, persiste, reusa. Deriva os pesos (Parte B).

### Enriquecimento contínuo (não termina no setup)
A cada correção numa avaliação ("não, isso a gente *faz*"), a skill **propõe adicionar ao DO/DON'T**. O briefing fica mais afiado com o uso, sem nova entrevista — é a memória persistente aprendendo a marca ao longo do tempo.

---

## Parte B — Derivação dos pesos das lentes

Os pesos não são fixos: o **objetivo** e o **formato** os definem. Tabela-base (a skill parte daqui e ajusta):

| Objetivo / formato dominante | Atenção | Clareza | Originalidade | Coerência | Execução |
|---|---|---|---|---|---|
| Reel (parar o scroll) | **alto** | médio | alto | médio | médio |
| Carrossel salvável | médio | **alto** | alto | médio | médio |
| Copy de venda | alto | **alto** | médio | **alto** (oferta↔promessa) | baixo |
| Arte/estática (feed, anúncio) | alto (1º olhar) | alto | médio | médio | **alto** (vision) |
| Autoridade / institucional | médio | alto | médio | **alto** | alto |

> O peso **não** é média ponderada — é prioridade pro Sintetizador. Peso alto = uma falha nessa lente é quase sempre fatal pra peça; peso baixo = falha ali é secundária.

---

## Distinção importante (3 blocos, não confundir)
- **Nicho** — o que funciona pra qualquer um daquele nicho (compartilhado).
- **DO's/DON'Ts da marca** — particular desta marca (graduado, preferência).
- **Linhas vermelhas** — subconjunto inviolável dos DON'Ts (hard stop = severidade máxima).

Os três são **camada 2**: alimentam a lente **Coerência** + o check de nicho. Pela regra do piso (`03`), **nunca absolvem falha essencial** — um DO da marca não torna boa uma peça que viola o canon.

## Parte C — Template do `briefing.md` gerado

```markdown
# Briefing — [Marca/Nicho]
> Camada 2. Gerado em [data]. Editável a qualquer momento.

## Nicho
[nicho / sub-nicho]

## Público
- Perfil: [...]
- Dor nº1: [...]
- Nível de consciência: [inconsciente / consciente da dor / buscando solução / comparando]

## Formatos típicos
[Reel, carrossel, copy de feed, arte estática, anúncio...]

## Objetivo dominante
Principal: [...] · Secundário: [...]

## Vida útil
[efêmero ≈48h / evergreen] → profundidade de revisão: [enxuta / aprofundada]

## Conteúdos/ângulos que funcionam no nicho (compartilhado pelo nicho)
- [antes/depois, "X erros que você comete", prova social, listicle, mito vs verdade, ...]

## Saturado no nicho / evitar
- [o que já cansou o público deste nicho]

## DO's e DON'Ts da marca (particular desta marca)
**DO:** [o que esta marca sempre faz — tom, vocabulário, estética, tipo de gancho, formato preferido]
**DON'T:** [o que esta marca evita — graduado, não necessariamente inviolável]

## Linhas vermelhas (subconjunto INVIOLÁVEL dos DON'Ts — hard stop)
- Claims proibidos: [...]
- Temas/tom que a marca nunca usa: [...]

## Tom de marca + referências (slot de Coerência)
- Tom: [...]
- Referências admiradas: [...] · Anti-referência: [...]

## Pesos das lentes (derivados — editáveis)
- Atenção: [alto/médio/baixo] — [razão curta]
- Clareza: [...]
- Originalidade: [...]
- Coerência: [...]
- Execução: [...]
```

---

## Parte D — Exemplo preenchido

```markdown
# Briefing — Clínica de Estética "X"

## Nicho
Estética / harmonização facial — clínica premium.

## Público
- Perfil: mulheres 30–50, classe A/B, já fazem procedimentos.
- Dor nº1: medo de resultado artificial / "ficar com cara de feita".
- Nível de consciência: comparando ofertas (escolhendo clínica, não descobrindo o problema).

## Formatos típicos
Carrossel educativo, Reel de antes/depois, copy de feed.

## Objetivo dominante
Principal: autoridade/confiança · Secundário: salvar.

## Vida útil
Evergreen (educativo) → profundidade: aprofundada.

## Conteúdos/ângulos que funcionam no nicho
- "X erros que envelhecem", mito vs verdade, antes/depois sutil, explicação de processo.

## Saturado no nicho / evitar
- Promessa milagrosa, antes/depois exagerado (gera desconfiança neste público).

## DO's e DON'Ts da marca
**DO:** explicar o porquê fisiológico; mostrar processo; tom de médica acolhedora; antes/depois sutil e realista.
**DON'T:** superlativo de venda; pressão estética; comparar pacientes; emoji em excesso.

## Linhas vermelhas (inviolável)
- Claims proibidos: "garantido", "sem riscos", cura.
- Tom: nada sensacionalista ou de "pressão estética".

## Tom de marca + referências
- Tom: sóbrio, científico-acessível, acolhedora.
- Referências: [perfis de dermato sérios].

## Pesos das lentes
- Atenção: médio — objetivo é confiança, não viralizar a qualquer custo.
- Clareza: alto — explicação tem que ser cristalina.
- Originalidade: médio — fresh ajuda, mas não às custas de credibilidade.
- Coerência: alto — qualquer exagero quebra a confiança premium.
- Execução: alto — antes/depois precisa de craft impecável (vision).
```

> Esse exemplo serve depois como **referência de exemplo**: rodar o painel num carrossel deste nicho e checar se os vereditos batem com o que de fato funciona em estética.

---

## Parte E — `evidence_profile` (opcional)

Seção **opcional** do `brand.md`. Liga/desliga e contextualiza os módulos de evidência empírica (camada T2) por marca. **`brand.md` sem `evidence_profile` continua 100% válido** — a skill roda igual, só sem o tempero empírico.

```yaml
evidence_profile:
  primary_niche: unknown          # unknown é válido — não inferir nada de prescritivo do nicho
  secondary_niche: null
  account_type: unknown           # creator | brand | b2b | b2c | mixed | unknown
  business_model: unknown
  preferred_formats: []           # ex: [carousel, reel] — só se o usuário confirmar
  enabled_evidence_modules:       # os dois módulos coexistem e são selecionáveis por marca
    - social-instagram-v1         # evidência CRIATIVA (features de copy/arte)
    # - platform-mechanics-v1     # evidência de MECÂNICA/alcance (módulo markdown existente) — habilitar se auditado
  excluded_reference_groups: []   # ex: [apple, nike] — controles, nunca modelo
  evidence_confidence: low        # low por construção (corpus = associação, não causa)
```

Regras (invioláveis):
- **Valores sugeridos pela skill são confirmáveis pelo usuário** — nunca aplicados sozinhos.
- **`unknown` é válido** e é o default. Nicho `unknown` → o roteador devolve pacote seguro/vazio; nunca inventa contexto.
- **Nenhuma preferência estilística é inferida automaticamente do nicho** (a skill não decide "use fotografia", "use poucos emojis" etc.).
- **Briefing explícito prevalece** sobre qualquer taxonomia inferida.
- **Dois módulos separáveis:** `enabled_evidence_modules` seleciona quais entram; eles **não se fundem** — cada evidência carrega sua origem (criativa vs mecânica de plataforma).
