# Human Studio — Marketplace de Skills do Claude Code

Coleção de skills opinionadas do Human Studio, distribuídas como **plugin marketplace** do Claude Code. Cada skill aqui dentro é instalável independentemente.

## Como instalar

Dentro do Claude Code:

```
/plugin marketplace add humanstudioacademy/skills
/plugin install criar-site@human-studio
```

> Substitua `humanstudioacademy/skills` pelo `owner/repo` real no GitHub.

Para listar skills disponíveis:

```
/plugin marketplace list human-studio
```

## Skills disponíveis

| Skill | O que faz |
|---|---|
| [`criar-site`](plugins/criar-site/) | Gera site responsivo end-to-end (Astro + Tailwind) com imagens/vídeos de IA via Freepik ou modo manual, em 3 matrizes estéticas hibridáveis. |

Mais skills serão adicionadas conforme amadurecemos. Cada uma vira um plugin separado em `plugins/`.

## Estrutura do repo

```
.
├── .claude-plugin/
│   └── marketplace.json          ← declara o marketplace e os plugins
├── plugins/
│   └── criar-site/               ← um plugin = uma skill instalável
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   └── criar-site/
│       │       ├── SKILL.md
│       │       └── ...
│       ├── README.md
│       ├── INSTALL.md
│       └── SHARING.md
└── README.md (este arquivo)
```

## Adicionar uma nova skill

1. Cria `plugins/<nome>/` seguindo o layout acima
2. Adiciona o plugin em `.claude-plugin/marketplace.json` no array `plugins`
3. Valida com `/plugin validate .` dentro do Claude Code
4. Commit e push

## Licença

MIT — ver cada plugin para detalhes.
