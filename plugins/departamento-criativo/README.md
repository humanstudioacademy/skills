# Departamento Criativo

Plugin para Claude Code — revisão criativa adversarial de conteúdo para redes sociais.

**Versão:** 1.0.0  
**Comando:** `/criativos`  
**Linguagem:** Português brasileiro  
**Requer:** Claude Code + Python 3.10+

---

## O que é

O Departamento Criativo é um painel de revisão criativa com 7 agentes especializados que avaliam conteúdo de redes sociais (copy, carrossel, Reel, arte) por cinco lentes: Atenção, Clareza, Originalidade, Coerência e Execução.

A revisão é adversarial por design: cada agente opera dentro do seu mandato e ponto cego, discute as questões reais do material e o Showrunner decide — sem tirar média, sem aprovar por inércia.

## Estrutura do painel

| Agente | Lente | Mandato |
|---|---|---|
| Roteirista | Atenção | Gancho e abertura — o primeiro beat prende? |
| Editor | Clareza | Mensagem e compreensão — o leitor entende? |
| Diretor Criativo | Originalidade | Ângulo e diferenciação — é genérico ou tem voz? |
| Diretor de Marca | Coerência | Fidelidade à marca — respeita os limites? |
| Diretor de Arte | Execução | Craft visual — a execução sustenta a ideia? |
| Showrunner | Síntese | Integra os pareceres e decide o veredito |
| Finalizador / Diretor de Arte | Reforma | Reescreve o que foi confirmado como problema |

## Instalação

```bash
# Instalar o plugin (a partir do diretório que contém a pasta departamento-criativo/)
claude plugin install ./departamento-criativo

# Verificar instalação
claude plugin list
```

O plugin requer Python 3.10+ disponível no `$PATH` para execução do engine interno.

## Uso

```
/criativos
```

Ao acionar o comando, o Departamento Criativo solicita o material para revisão e inicia o painel. Não há modos ou configurações expostas — o sistema calibra a profundidade internamente.

**Tipos de entrada aceitos:**
- Copy (legenda, texto de feed, CTA, headline)
- Carrossel (slide a slide ou descrição estruturada)
- Reel (roteiro, conceito, arte de capa)
- Conceito criativo (ideia, angle, proposta)
- Duas versões para comparação

**Configuração de marca (opcional):**  
Para ancorar a revisão no tom e limites da sua marca, use o onboarding em `criterios/04-briefing.md`. O arquivo `brand/brand-active.md` gerado é lido automaticamente nas revisões seguintes.

## O que o painel entrega

1. **Veredito** — aprovado / aprovado com ressalvas / precisa de revisão / precisa ser refeito
2. **O que já está funcionando** — o que preservar
3. **O que pegou** — problemas confirmados, com local + impacto + como corrigir
4. **A discussão do departamento** — falas reais dos agentes que acrescentam algo
5. **Direção final** — prioridade de correção
6. **Como ficaria melhor** — copy revisada ou briefing de arte concreto

## Arquitetura técnica

O plugin usa uma arquitetura de dois tiers de evidência:

- **T1 (canônico):** critérios atemporais, niche-agnósticos, derivados de princípios de comunicação. Produz o parecer cego — sem influência de dados de performance.
- **T2 (contextual):** banco empírico de padrões observados em conteúdo de alto e baixo desempenho. Contextualiza, nunca derruba o T1.

O engine (`runtime/sala.py`) orquestra: normalização → leitura cega por lente → congelamento T1 → roteamento de evidência T2 → discussão por questão → decisão do Showrunner → reforma.

## Conteúdo incluído

```
.claude-plugin/
  plugin.json
skills/criativos/
  SKILL.md                          # instruções de orquestração
  agents/                           # 7 agentes (roteirista, editor, ...)
  criterios/                        # 18 documentos de critério canônico
  evidencias/social-instagram-v1/   # banco T2 (padrões, balizas, assets)
  runtime/                          # sala.py, evidence_router.py, art_direction_handoff.py
  schemas/                          # JSON Schema do roteador
```

## Verificação de integridade

```bash
# A partir do diretório do plugin instalado:
sha256sum -c CHECKSUMS.sha256
```

---

Departamento Criativo v1.0.0
