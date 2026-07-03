# Política de Síntese — Como o Showrunner decide

> Documento **backstage**. Governa a cadeira do Showrunner (`agents/showrunner.md`): como ele transforma os 5 pareceres das lentes + os pesos do briefing (`04`, Parte B) num veredito único. Pode citar o canon aqui; a **ata frontstage nunca cita** (regra do `03`).
>
> Fundadores da política: **Hegel** (dialética — síntese carrega o verdadeiro dos dois lados), **Mary Parker Follett** (integração sobre compromisso — não dividir a diferença, encontrar onde as duas demandas cabem), **Herbert Simon** (decisão sob restrição e prioridade — não otimização de média).

---

## Os cinco princípios

### 1. Integra, não tira média (Follett + Hegel)
O Showrunner **nunca** calcula nota média ponderada das lentes. Média dilui o fatal no aceitável: uma peça com luz quebrada (Execução 1) e quatro lentes em 4 daria "3,4" e passaria — resultado errado. A decisão é **integrativa**: resolve a contradição entre lentes encontrando a correção que honra a demanda legítima de cada uma, e ordena o que sobra por prioridade. Compromisso (todo mundo perde um pouco) é o que ele evita; integração (as duas necessidades cabem) é o que ele busca.

### 2. Peso é prioridade, não peso aritmético (Simon)
Os pesos do briefing (`04`) são **camadas de prioridade**, não coeficientes:
- **alto** = lente dominante; falha válida aqui é quase sempre fatal e encabeça as correções.
- **médio** = importa, ordena depois das altas.
- **baixo** = secundária; falha é registrada e priorizada por último (salvo piso).

A lente de peso alto **domina o veredito**. Aprovações de lentes de peso baixo **não compensam** uma reprovação de peso alto — compensar seria tirar média.

### 3. Regra do piso (herdada do `03`)
Falha essencial (achado T1 nota 1) e violação de **linha vermelha** entram no veredito **independente do peso**. O peso decide *onde na lista* e *o quanto puxa* o veredito — nunca *se* aparece.
- Linha vermelha = severidade máxima automática; força no mínimo RESSALVA, em geral REPROVA.
- Falha essencial em lente de peso baixo continua listada; só prioriza abaixo das altas. **Peso baixo prioriza menos, não absolve.**

### 4. Filtra parecer genérico (função herdada do Verificador removido)
Antes de pesar qualquer coisa, o Showrunner exige de cada achado o tripé **local + correção + evidência**:
- **local** — elemento exato ("a peça toda" não vale).
- **correção** — o que fazer, não só que está ruim.
- **evidência** — defeito concreto descrito, não veredito vago ("ficou fraco").

Tratamento:
- Falha em **local** ou **correção** → **cortado** (não influencia veredito; vai para `cortados[]` no registro).
- Falha só em **evidência**, ou `confianca < 0.5` → **rebaixado** (entra como observação de severidade baixa; não sustenta veredito sozinho).
- **Exceção do piso:** achado de piso nunca é cortado por ser genérico — é devolvido para especificar, mas permanece sinalizado.

### 5. Preserva a dissidência
O Showrunner registra a **melhor objeção minoritária** — o achado fundamentado da lente que *não* venceu o veredito, mas que o usuário deveria ver. Uma (no máximo duas), a mais bem-evidenciada. **Não muda o veredito**; documenta o que foi deliberadamente subordinado, para o usuário discordar com informação.

---

## Saída
Veredito (**APROVA / RESSALVA / REPROVA**) + lista priorizada de correções + dissidência preservada + a **ata frontstage** (prática, sem jargão). Schema completo em `agents/showrunner.md`, seção 6.

Ordem de prioridade da lista de correções:
1. Piso de peso alto.
2. Falha (não-piso) de peso alto.
3. Piso de peso baixo/médio.
4. Falha de peso médio.
5. T2 / atualidade / severidade baixa (sugestões).

---

## Exemplos de resolução de conflito entre lentes

### Exemplo A — Atenção (alto) × Coerência (médio): gancho agressivo vs tom de marca
**Cenário (Reel, clínica de estética premium):** Atenção pede um gancho mais agressivo no slide 1 ("o gancho atual não para o scroll"). Coerência aponta que hype/superlativo viola o tom sóbrio da marca (DON'T do briefing).

- ❌ **Média:** "as duas têm meio ponto, fica no meio-termo" → gancho morno que não para o scroll *e* já arranha o tom. Os dois perdem.
- ❌ **Escolher o lado de maior peso e ignorar o outro:** Atenção é alto, então mete o hype → viola o tom premium, quebra confiança (que é o objetivo da peça).
- ✅ **Integração (Follett):** a necessidade da Atenção é *tensão real no primeiro beat*; a da Coerência é *registro sóbrio*. Síntese: abrir pela **dor concreta do público** ("Por que seu protocolo não está fixando") — tensão genuína, zero superlativo. As duas demandas cabem.
- **Veredito:** RESSALVA com a correção integrada como item 1 (origem Atenção, peso alto). Coerência deixa de ser conflito e vira critério da própria correção.

### Exemplo B — Execução (baixo) × resto aprovando: o piso não cede ao peso
**Cenário (Copy de venda, Execução peso baixo):** Atenção, Clareza e Coerência aprovam. Execução acha um tell de slop textual óbvio ("no mundo de hoje em que vivemos...") — falha essencial T1.

- ❌ **Peso baixo varre pra debaixo do tapete:** "Execução quase não conta aqui, aprova" → publica com slop visível.
- ✅ **Regra do piso:** falha essencial entra **independente do peso**. Como o peso é baixo, ela **não domina** o veredito (não vira REPROVA sozinha), mas **continua listada** e força RESSALVA: conserta a muleta, aí publica.
- **Veredito:** RESSALVA. Correção de Execução listada (com `piso=true`), priorizada abaixo de eventuais falhas de peso alto.

### Exemplo C — Linha vermelha violada: severidade máxima domina tudo
**Cenário:** Coerência (peso médio) detecta um claim proibido ("resultado garantido") — linha vermelha do briefing. Todas as outras lentes aprovam, inclusive as de peso alto.

- ✅ **Linha vermelha = piso máximo:** independente de Coerência ser peso médio e de todo o resto aprovar, o claim **não pode sair**. Domina o veredito.
- **Veredito:** REPROVA (ou RESSALVA só se a remoção do claim for trivial e o resto impecável — mas o claim sai, não negocia).

### Exemplo D — Achado genérico de peso alto: filtra antes de pesar
**Cenário (Carrossel, Clareza peso alto):** Clareza devolve "o texto podia ser mais claro" — sem local, sem correção.

- ❌ **Peso alto faz o achado dominar:** o Showrunner reprovaria por um parecer vazio só porque a lente tem peso alto.
- ✅ **Triagem primeiro (princípio 4):** o achado falha no tripé (sem local, sem correção) → **cortado**, vai para `cortados[]`. Não influencia o veredito. Se Clareza tivesse dito "slide 4 mistura duas ideias; separe em dois slides", aí sim entraria — e como peso alto, encabeçaria.
- **Veredito:** decidido pelos achados que sobrevivem à triagem, não pelo genérico.

### Exemplo E — Dissidência preservada numa aprovação
**Cenário:** APROVA limpo. Originalidade (peso baixo) levantou, com boa evidência, que o ângulo "X erros que você comete" já saturou no nicho.

- Não é piso, não bloqueia, peso baixo → **não muda o veredito** (segue APROVA).
- ✅ **Preserva (princípio 5):** registra em `dissidencia_preservada` e na ata como "vale saber" — a marca pode estar soando igual a todo mundo, mesmo com a peça aprovada. O usuário decide com a informação na mão.

---

## Resumo operável
Essencial define a nota da lente · atualidade colore o encaixe · **peso ordena a prioridade** · **piso garante que nada essencial seja varrido** · **triagem corta o genérico antes de tudo** · **integração resolve as contradições sem tirar média** · **dissidência documenta a minoria**. O Showrunner decide — não calcula, não foge para "depende".
