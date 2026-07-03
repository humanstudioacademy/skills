# Princípios de Aplicação — Backstage vs Frontstage

> Governa COMO os critérios canônicos (`00`, `02`) são usados. Resumo: o canon afia o agente; **nunca** aparece na avaliação. A saída é prática, concreta e calibrada ao nicho/contexto do usuário.

---

## As três camadas (e quem vê o quê)

| Camada | O que é | Onde vive | Usuário vê? |
|---|---|---|---|
| **1. Núcleo canônico (atemporal)** | princípios + exemplares históricos (Loewenstein, Caravaggio, etc.) | docs `00`/`02` | **NÃO** — backstage |
| **2. Contexto/nicho** | atualidade: nicho, público, plataforma, objetivo, vida útil, o que funciona/satura *agora* ali | `briefing.md` (gerado no onboarding) | parcialmente (é o input dele) |
| **3. Saída** | o veredito + as correções concretas | a "ata" | **SIM** — frontstage |

O agente raciocina com a camada 1 (**o critério**), **modula pela camada 2** (só a atualidade/contexto), e entrega só a camada 3.

> ⚠️ A camada 2 toca **apenas a dimensão de atualidade** de cada análise — não o critério. O critério essencial vem todo da camada 1.

---

## Regra 1 — O canon nunca vaza pra saída
- ❌ "O slide 1 viola a Information Gap Theory (Loewenstein, 1994)."
- ❌ "Isso era radical em 1917, hoje é banal."
- ✅ "O slide 1 entrega a solução antes de criar o problema — não para o scroll."

A teoria está **dentro** do julgamento, não na linguagem. Se uma frase da avaliação só faz sentido pra quem leu Aristóteles, ela está errada de registro.

## Regra 2 — A saída fala a língua do artefato
O uso comum é **copy, corpo de carrossel, arte de 48h** — não ensaio. Então a saída é:
- Curta, concreta, acionável. Aponta o elemento exato e entrega a correção/alternativa.
- Sem jargão de design/retórica/cinema. Vocabulário de quem produz conteúdo, não de quem dá aula.
- Proporcional à vida útil: peça de 48h não merece tratado — merece "muda isso, posta".

## Regra 3 — O nicho manda (camada 2 pondera a camada 1)
O princípio é universal; **o limiar e a expressão são do nicho.** O mesmo "abrir lacuna de atenção":
- Nicho **estética/clínica** → nomear a dor primeiro ("por que seu hidratante não funciona").
- Nicho **finanças/B2B** → stakes de custo ("o erro de R$X que sua empresa comete").
- Nicho **humor/entretenimento** → quebra de expectativa/timing.

Mesma mecânica canônica, três saídas diferentes. **O agente nunca aplica o canon cru — instancia ele no nicho.**

## Regra 4 — Cases recorrentes do nicho são parâmetro
Além do canon, a camada 2 carrega **padrões já testados naquele nicho** (ex: antes/depois, "X erros", listicle, prova social) — o que recorrentemente funciona ali e o que satura. Isso vem do briefing + curadoria. O agente checa: *a peça usa um padrão que funciona neste nicho, ou ignora?*

## Regra 5 — A fronteira: o briefing modula a atualidade, nunca redefine o critério
O **critério** de cada lente (o que ela essencialmente mede) é canônico e **invariável** — vem da camada 1. O briefing (camada 2) **não cria critério**; ele só atua na **dimensão de atualidade/contexto**:
- se a peça conversa com o que funciona *agora* naquele nicho;
- as convenções e o que já saturou *ali*;
- a **prioridade relativa** entre as lentes (pesos), dado o objetivo.

O briefing responde *"isso encaixa no contexto atual?"* — nunca *"o que é boa atenção/clareza/execução?"*. A segunda pergunta é exclusiva do núcleo essencial.

### Regra do piso (o peso não perdoa o essencial)
Peso baixo ≠ licença pra violar o essencial. Uma **falha essencial** (ex: luz incoerente em Execução; peça incompreensível em Clareza; clichê puro sem assinatura em Originalidade) é **sempre sinalizada**, independente do peso do nicho. O peso só re-hierarquiza entre peças que **já passam no essencial** — ele prioriza, nunca absolve.

---

## O briefing inicial (onboarding da skill) captura
1. **Nicho** e sub-nicho.
2. **Público** (quem é, dor principal, nível de consciência).
3. **Plataforma + formato** (Reel, carrossel, copy de feed, anúncio).
4. **Objetivo** da peça (salvar, comentar, compartilhar, vender, autoridade).
5. **Vida útil** (48h efêmero vs evergreen) → calibra profundidade da revisão.
6. **O que funciona no nicho** (referências, cases recorrentes) e **o que nunca fazer**.
7. **Marca/tom** (vira o slot de Coerência).

→ Gera `briefing.md`. É a camada 2. Sem ele, o agente roda só no canon (genérico) — funcional, mas cego ao nicho.

---

## Schema de achado (corrigido: âncora é interna)

```json
{
  "lente": "atencao",
  "nota": 1,
  "local": "slide 1 / título",
  "problema": "entrega a solução antes de criar o problema — não para o scroll",
  "correcao": "começar pela dor do público, não pela oferta",
  "alternativas": ["Por que seu protocolo não está fixando", "Você está perdendo cliente nisso aqui"],
  "severidade": "alta",
  "encaixe_nicho": "no nicho estético, nomear a dor primeiro é o que retém",
  "_ancora_interna": "lacuna de atenção",   // NÃO renderizar ao usuário — só rastreabilidade
  "confianca": 0.8
}
```

- `_ancora_interna` força o agente a fundamentar (anti-perspectivismo), mas **não é exibida**. Fica pra auditar/depurar o raciocínio do agente, não pra erudir o usuário.
- `encaixe_nicho` é o que conecta o julgamento ao contexto — esse SIM aparece.

---

## Campos opcionais T2 (retrocompatíveis)
> Adicionados pela integração do banco empírico. São **opcionais e backstage**: o schema antigo (sem eles) continua válido; nenhum consumidor existente quebra.

```json
{
  "t1_assessment": {},      // parecer T1 CONGELADO (imutável; recuperável após T2)
  "t2_context": {},         // modulação empírica (review_prompts, guidance, warnings) — NÃO pontua
  "evidence_refs": [        // rastro dos itens T2 usados
    {"id": "RP-...", "layer": "T2", "role": "review_prompt | contextual_guidance | example | counterexample | confounding_warning", "scope": "string", "confidence": "baixa | baixa-media"}
  ],
  "evaluation_status": "complete | partial | insufficient_information | not_applicable"
}
```

Regras:
- **Opcionais:** ausentes → schema válido (comportamento idêntico ao pré-integração).
- `t1_assessment` **não é sobrescrito** por `t2_context`; o T2 nunca apaga piso, nunca muda `nota`/`veredito`.
- **Informação ausente** → `evaluation_status: not_applicable | insufficient_information`; nunca nota zero, nunca reprovação automática; sem imagem → sem nota visual; sem copy → sem nota de copy; sem briefing → confiança menor, não defeito.
- `evidence_refs` é só rastreabilidade; não renderiza no frontstage.
