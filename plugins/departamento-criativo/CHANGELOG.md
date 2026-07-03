# CHANGELOG — Departamento Criativo

## [1.0.0] — 2026-06-28

### Lançamento inicial

**Painel de agentes**
- 7 agentes especializados: Roteirista (Atenção), Editor (Clareza), Diretor Criativo (Originalidade), Diretor de Marca (Coerência), Diretor de Arte (Execução), Showrunner (síntese), Finalizador/Diretor de Arte (reforma)
- Cada agente com mandato e ponto cego explícitos — sem invasão de lente
- Discussão por questão: só quem tem relação real com o achado fala

**Critérios canônicos (T1)**
- Fundação canônica com princípios atemporais e corpus de exemplares históricos
- Rubricas de pontuação por lente (escala ancorada em 5/3/1)
- Balizas e padrões-ouro para as 5 lentes
- Políticas de revisão e de síntese

**Banco empírico (T2)**
- Módulo `social-instagram-v1`: padrões observados em 62 carrosseis completos e recorte de carousel cover-only
- Roteador de evidência determinístico: mapeia (lente, escopo, nicho, tipo de conta) → pacote de evidência
- 24 exemplos visuais de referência (balizas positivas, negativas, contraexemplos)
- Padrões contextuais FC-CP-001 a FC-CP-007 para carrosseis completos
- Confounds explicitados — nenhum padrão contextual é usado como regra de pontuação

**Engine**
- `sala.py`: orquestração completa do painel (554 linhas)
- `evidence_router.py`: roteamento determinístico de evidência T2
- `art_direction_handoff.py`: passagem de contexto para o Diretor de Arte na reforma
- Suporte a comparação de duas versões

**Arquitetura**
- T1 sempre cego (sem evidência empírica no parecer inicial)
- T2 contextualiza, nunca derruba T1
- Showrunner integra (não tira média), aplica regra do piso, preserva dissidência
- Frontstage coloquial — backstage técnico nunca vaza para o usuário
