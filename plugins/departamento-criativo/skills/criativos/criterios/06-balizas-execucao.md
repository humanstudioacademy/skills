# Balizas — Diretor de Arte (obras que gabaritam cada conceito)
> Catálogo curado de obras-baliza por conceito de `05-conceitos-execucao.md`. Função: few-shot **por ponto de avaliação** — o padrão-ouro contra o qual o agente compara. Cross-domínio e cross-época de propósito (pintura, foto, cinema, design gráfico, tipografia).
>
> **Polo +** = gabarita o conceito · **Polo −** = anti-exemplo (falha didática). Obras nomeadas (verificáveis); para os itens marcados 📌 vale anexar imagem real como âncora literal de vision na calibração.
>
> **ÂNCORAS OFICIAIS (imagens reais):** `evidencias/balizas/` — imagens da base padrão-ouro, organizadas por conceito: `01-luz-chiaroscuro`, `02-cor-como-sistema`, `03-composicao-minimal`, `04-composicao-tableau`, `05-styling-art-direction`, `06-material-textura`, `07-narrativa-mood`, `08-acting-gesto`. Ver `07-padroes-ouro-execucao.md`.

## 1. Luz e estrutura tonal
- **Coerência da fonte de luz / chiaroscuro** 📌 — **+** Caravaggio, *A Vocação de São Mateus*; Rembrandt, *Ronda Noturna*; Georges de La Tour (luz de vela, fonte única); Deakins, *Blade Runner 2049*. **−** composite com sombra do sujeito contra a do fundo.
- **Amplitude/leitura tonal** 📌 — **+** Ansel Adams, *Moonrise, Hernandez*; Gordon Willis, *O Poderoso Chefão* (sombras profundas legíveis). **−** imagem "lavada" (sem preto) ou "esmagada" (sem detalhe na sombra).
- **Oclusão de contato / aterramento** — **+** Chardin (naturezas-mortas, objetos assentados); Vermeer. **−** sujeito recortado "flutuando" sem sombra de contato.
- **Realce especular x material** — **+** Willem Kalf (*pronkstilleven*: metal/vidro/cetim); Vermeer, *Moça com Brinco de Pérola* (a pérola).

## 2. Forma, anatomia e perspectiva
- **Anatomia/proporção** 📌 — **+** Michelangelo, *Davi* e teto Sistino; Leonardo, *Homem Vitruviano*; pranchas Bridgman/Loomis. **−** mãos/dedos de IA, simetria facial perfeita demais.
- **Perspectiva** — **+** Masaccio, *A Trindade* (1ª perspectiva linear rigorosa); Piero della Francesca, *A Flagelação*. **−** linhas de fuga inconsistentes / horizontes múltiplos.
- **Leitura volumétrica** — **+** Zurbarán; Ingres (desenho); a luz revelando forma.

## 3. Composição e organização visual
- **Figura-fundo** — **+** Toulouse-Lautrec (cartazes); Saul Bass (pôsteres). **−** sujeito que se funde no fundo.
- **Ponto focal / hierarquia** — **+** Leonardo, *A Última Ceia* (convergência em Cristo); cartazes do Design Suíço. **−** focos competindo.
- **Leis de agrupamento (Gestalt)** — **+** logos WWF e FedEx (fechamento); IBM (Paul Rand).
- **Grid e alinhamento** 📌 — **+** Müller-Brockmann (cartazes Tonhalle Zürich); revista *Neue Grafik*. **−** elementos sem ancoragem, desalinho acidental.
- **Espaço negativo ativo** — **+** seta no negativo do FedEx; sumi-e japonês (*ma*); cartaz suíço. **−** *horror vacui* (tudo cheio).
- **Equilíbrio de peso visual** — **+** Mondrian, *Composição com Vermelho, Azul e Amarelo* (assimetria equilibrada).

## 4. Cor
- **Cor é relacional** 📌 — **+** Josef Albers, série *Homage to the Square*.
- **Contraste de valor (legibilidade)** — **+** xilogravura / cartaz alto-contraste. **−** texto matiz-sobre-matiz sem diferença de valor.
- **Disciplina de paleta** — **+** cartazes Bauhaus; Rothko (paleta restrita). **−** poluição cromática.
- **Tipos de contraste de cor (Itten)** [estilo] — **+** Matisse / Fauvismo (contraste de matiz).

## 5. Material, textura e acabamento
- **Plausibilidade de material** 📌 — **+** Kalf (natureza-morta holandesa); Irving Penn (still de produto). **−** material "plástico" genérico de IA.
- **Qualidade de borda** — **+** Sargent (bordas duras/suaves intencionais). **−** halo/serrilhado de recorte.
- **Acabamento/resolução** — **+** Vermeer; foto de grande formato (Adams). **−** "borrado" ou over-sharpen.

## 6. Veracidade / anti-slop
- **Ausência de artefato / vale da estranheza** 📌 — **+** integração VFX crível (ILM, *Jurassic Park*); retrato fotográfico real. **−** *The Polar Express* (2004) — olhar morto; tells de IA (mãos, dentes/joias fundidos).
- **Plausibilidade física** — **+** *Gravity* (luz/física coerentes). **−** reflexo/sombra que desobedece a física.
- **Continuidade (sequência)** — **+** *1917* (continuidade de plano-sequência); decupagem clássica. **−** salto de luz/props/eyeline entre frames.

## 7. Tipografia (quando há texto)
- **Hierarquia / grid** 📌 — **+** Müller-Brockmann (grid); Tschichold (*Die neue Typographie*, capas Penguin). **−** hierarquia plana, tudo no mesmo peso.
- **Legibilidade** — **+** sinalização do metrô de NY (Vignelli); tipo Johnston (metrô de Londres). **−** corpo pequeno / contraste insuficiente.

## Como usar na calibração
- Cada obra-baliza é uma **âncora de comparação** para o ponto específico, não um estilo a imitar — "essa luz tem a coerência de um Caravaggio?" mede o *princípio*, não pede chiaroscuro.
- 📌 = candidatos a virar **âncora de imagem real** (arquivo anexado) se a vision precisar de referência literal.
- Mesmo método se repete para os agentes de texto (Roteirista, Editor): lá as balizas serão roteiros, leads e peças de copy que gabaritam cada conceito — feito quando construirmos cada um.
