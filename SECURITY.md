# Política de Segurança

## Princípios

Este marketplace distribui código que é executado dentro do Claude Code do usuário final. Por isso operamos sob três princípios:

1. **Zero segredos no repo.** Nenhum `.env`, chave de API, token ou credencial é jamais commitado. CI bloqueia push que contenha segredo (gitleaks).
2. **Permissões mínimas.** Skills declaram explicitamente quais ferramentas usam. Plugins não pedem permissões além do necessário.
3. **Auditoria pública.** Toda skill é open-source MIT. Qualquer pessoa pode ler exatamente o que executa antes de instalar.

## O que cada skill PODE fazer

Quando uma skill é invocada, ela roda no Claude Code do usuário com as permissões que o usuário concedeu (Read, Bash, Edit, etc). Cada `SKILL.md` documenta:

- Quais arquivos a skill lê/escreve
- Quais comandos shell ela executa
- Quais APIs externas ela chama
- Quais variáveis de ambiente ela consome

Se algo estiver faltando dessa lista, é um bug — abra issue.

## O que cada skill NÃO pode fazer

- ❌ Enviar dados do projeto do usuário pra qualquer servidor sem aviso explícito
- ❌ Modificar arquivos fora do diretório de trabalho declarado
- ❌ Persistir credenciais em qualquer lugar acessível ao repo
- ❌ Executar binários baixados de fontes não-verificadas

## Reportar vulnerabilidade

Se você encontrar uma falha de segurança (skill que vaza dados, prompt injection que escapa do escopo, dependência com CVE conhecido):

- **Não abra issue público.** 
- Mande email pra `humanstudio.ai@gmail.com` com subject `[SECURITY] <skill> — <resumo>`.
- Inclua: passos pra reproduzir, impacto, versão da skill (commit SHA).

Resposta esperada em até 72h. Patch em até 7 dias para vulnerabilidades de alta severidade.

## Scans automatizados

Cada push pra `main` dispara:

- **gitleaks** — scan de segredos no diff e no histórico
- **validate_marketplace.py** — validação estrutural (manifestos, frontmatter, paths)
- **py_compile** — todos os `.py` compilam sem erro

Os badges no README refletem o estado real de cada check.

## Dependências de terceiros

Skills que dependem de pacotes externos (pip, npm) declaram em arquivos versionados (`requirements.txt`, `package.json`). Ao instalar, você roda esses pacotes na sua máquina. Audite antes em projetos sensíveis.

A skill `criar-site` depende de:
- Python: `requests`, `python-dotenv` (ambos amplamente auditados)
- Node: dependências do template Astro (instaladas só dentro de `sites/<slug>/`)
- API externa opcional: Freepik (apenas em modo API, com chave do usuário)
