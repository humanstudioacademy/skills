# /criativos — Departamento Criativo

Painel de revisão criativa adversarial com 7 agentes especializados.

## Estrutura da skill

```
criativos/
  SKILL.md                    # orquestração principal (leia primeiro)
  agents/
    roteirista.md             # lente Atenção
    editor.md                 # lente Clareza
    diretor-criativo.md       # lente Originalidade
    diretor-de-marca.md       # lente Coerência
    diretor-de-arte.md        # lente Execução
    showrunner.md             # síntese e veredito
    finalizador.md            # reforma pós-decisão
  criterios/
    00-fundacao-canonica.md   # princípios atemporais
    01-rubricas.md            # escalas de avaliação
    02-corpus-canonico.md     # exemplares de referência
    03-principios-de-aplicacao.md  # backstage vs frontstage
    04-briefing.md            # onboarding de marca
    05-conceitos-execucao.md  # conceitos da lente Execução
    06-balizas-execucao.md    # balizas da lente Execução
    07-padroes-ouro-execucao.md    # padrões-ouro de Execução
    balizas-{atencao,clareza,coerencia,originalidade}.md
    conceitos-{atencao,clareza,coerencia,originalidade}.md
    politica-revisao.md       # regras de revisão
    politica-sintese.md       # como o Showrunner decide
  evidencias/
    social-instagram-v1/      # banco T2 (padrões de performance)
  runtime/
    sala.py                   # engine principal
    evidence_router.py        # roteamento de evidência T2
    art_direction_handoff.py  # handoff para Diretor de Arte
  schemas/
    evidence_router.schema.json
```

## Fluxo de execução

1. Claude lê `SKILL.md` e interpreta o pedido
2. Monta `input.json` com o material e contexto
3. Produz pareceres cegos (T1) por lente, sem evidência empírica
4. Engine (`sala.py`) recebe os pareceres e orquestra a discussão por questão
5. Showrunner decide questão a questão (integração, não média)
6. Finalizador/Diretor de Arte reforma o que foi confirmado
7. Claude traduz o `output.json` em resposta coloquial

## Configuração de marca

O arquivo `brand/brand-active.md` (opcional) ancora a revisão no tom e limites da marca. Gere-o rodando o onboarding de `criterios/04-briefing.md` (Parte A).

## Banco de evidências T2

O módulo `evidencias/social-instagram-v1` contém padrões contextuais observados em conteúdo de redes sociais. É lido pelo `evidence_router.py` com base em (lente, escopo, nicho, tipo de conta). O T2 contextualiza a análise — nunca derruba critérios T1, nunca pontua.

## Invariantes

- T1 sempre cego: o parecer inicial de cada lente não tem acesso a dados de performance
- T2 contextualiza, nunca derruba T1
- Frontstage coloquial: o usuário nunca vê IDs internos, jargão técnico ou métricas brutas
- Showrunner integra (Follett): resolve contradições entre lentes sem tirar média
- Regra do piso: falha essencial nunca é varrida pelo peso baixo da lente
