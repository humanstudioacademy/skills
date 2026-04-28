# ref-prompt-engeneer/

> **Pasta de calibração interna do sistema.** Nada daqui vira input de API. Nada daqui é referência de estilo direto. Essas imagens existem apenas para formar o **padrão estético mínimo** que o módulo `prompt-engineer` deve respeitar ao compor prompts pro Nano Banana e Seedance 2.0.

## O que tem aqui

| Arquivo/Pasta | Conteúdo |
|---|---|
| `Descrição técnica.txt` | System prompt original do **KinoImage Generator** (GPT custom construído pro MidJourney pelo usuário). É a base que traduzimos em `prompts/prompt-engineer/taxonomy.md`. |
| `IMAGENS/` | Refs fotográficas editoriais selecionadas pelo usuário que representam a **régua mínima de qualidade** — iluminação, nitidez, composição, casting, materialidade, disciplina de paleta. |
| `design/` | Refs gráficas (magazines, design editorial com tipografia integrada) que definem o registro de linguagem visual esperado. |

## Como essa pasta é usada

1. **Quando o Claude compõe um prompt novo** (pra um site real), ele já sabe internamente que o resultado precisa ter densidade técnica equivalente à dessas refs — luz direcional controlada, grão filmico mínimo, paleta restrita, materialidade descrita em detalhe.
2. **Se um prompt compõe menos denso que essas refs**, o checkpoint de coerência rejeita e regenera com mais specs.
3. **Essas imagens nunca são citadas por nome, sujeito, ou enviadas como `reference_images` pra Nano.** Elas são o "olho interno" do módulo.

## Regra fundamental

Ver em memory (`feedback_dois_niveis_refs.md`):

- **Nível A — refs de calibração interna** (esta pasta): invisível, formatiza o rigor do Claude.
- **Nível B — `visualRefs` do briefing** (pasta do projeto em `sites/<projeto>/refs/`): input real de API, anexadas ao Nano com o prefixo obrigatório.

Confundir os dois quebra o sistema. Esta pasta **nunca** é `visualRefs`.

## Se quiser expandir a calibração

Adicionar mais imagens aqui tem 1 efeito: amplia o repertório interno de "o que é qualidade editorial premium". O Claude vai absorver e a régua fica mais alta. Mas nenhuma dessas imagens vai aparecer em site algum.
