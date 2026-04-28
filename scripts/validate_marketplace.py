#!/usr/bin/env python3
"""
Validador estrutural do marketplace.

Roda no CI a cada push pra main. Falha se:
- marketplace.json ausente, malformado, ou sem campos obrigatórios
- Algum plugin listado tem source apontando pra dir inexistente
- Plugin não tem .claude-plugin/plugin.json válido
- Plugin não tem ao menos uma skill em skills/<nome>/SKILL.md
- SKILL.md não tem frontmatter com `name` e `description`
- Algum .env é tracked
- Algum .py não compila

Uso:
    python3 scripts/validate_marketplace.py
"""
from __future__ import annotations

import json
import py_compile
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        err(f"arquivo ausente: {path.relative_to(ROOT)}")
        return {}
    except json.JSONDecodeError as e:
        err(f"JSON inválido em {path.relative_to(ROOT)}: {e}")
        return {}


def parse_frontmatter(skill_md: Path) -> dict | None:
    """Extrai frontmatter YAML simples (apenas chaves de 1 nível) do SKILL.md."""
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    frontmatter: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            frontmatter[k.strip()] = v.strip()
    return frontmatter


def validate_marketplace() -> tuple[dict, Path]:
    print(f"[1/5] marketplace.json em {MARKETPLACE.relative_to(ROOT)}")
    if not MARKETPLACE.exists():
        err(".claude-plugin/marketplace.json não existe na raiz")
        return {}, ROOT
    data = load_json(MARKETPLACE)
    for field in ("name", "owner", "plugins"):
        if field not in data:
            err(f"marketplace.json: campo obrigatório '{field}' ausente")
    if "owner" in data and "name" not in data["owner"]:
        err("marketplace.json: owner.name ausente")
    if "plugins" in data and not isinstance(data["plugins"], list):
        err("marketplace.json: plugins deve ser array")
    plugin_root_str = data.get("metadata", {}).get("pluginRoot", ".")
    plugin_root = (ROOT / plugin_root_str).resolve()
    if not plugin_root.exists():
        err(f"marketplace.json: pluginRoot '{plugin_root_str}' não existe")
    return data, plugin_root


def validate_plugin(entry: dict, plugin_root: Path) -> None:
    name = entry.get("name", "<sem-nome>")
    print(f"[2/5] plugin '{name}'")
    if "name" not in entry:
        err("plugin sem 'name' em marketplace.json")
        return
    if "source" not in entry:
        err(f"plugin '{name}' sem 'source'")
        return

    plugin_dir = (plugin_root / entry["source"]).resolve()
    if not plugin_dir.exists():
        err(f"plugin '{name}' source aponta pra dir inexistente: {plugin_dir.relative_to(ROOT)}")
        return

    plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
    if not plugin_json_path.exists():
        err(f"plugin '{name}': falta {plugin_json_path.relative_to(ROOT)}")
        return
    plugin_json = load_json(plugin_json_path)
    for field in ("name", "description"):
        if field not in plugin_json:
            err(f"plugin '{name}' plugin.json sem campo '{field}'")
    if plugin_json.get("name") and plugin_json["name"] != name:
        err(f"plugin '{name}': nome no marketplace.json ({name}) "
            f"diverge do plugin.json ({plugin_json['name']})")

    skills_dir = plugin_dir / "skills"
    if not skills_dir.exists():
        err(f"plugin '{name}' sem pasta skills/")
        return
    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
    if not skill_dirs:
        err(f"plugin '{name}' não tem nenhuma skill em skills/")
        return

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            err(f"skill '{skill_dir.name}' sem SKILL.md")
            continue
        fm = parse_frontmatter(skill_md)
        if fm is None:
            err(f"skill '{skill_dir.name}' SKILL.md sem frontmatter YAML")
            continue
        for k in ("name", "description"):
            if not fm.get(k):
                err(f"skill '{skill_dir.name}' SKILL.md sem '{k}' no frontmatter")
        if fm.get("name") and fm["name"] != skill_dir.name:
            err(f"skill '{skill_dir.name}' frontmatter.name='{fm['name']}' "
                f"diverge do nome da pasta")


def check_no_secrets() -> None:
    print("[3/5] checando secrets tracked")
    try:
        out = subprocess.check_output(
            ["git", "ls-files"], cwd=ROOT, text=True
        )
    except subprocess.CalledProcessError:
        warn("git ls-files falhou — pulei check de secrets tracked")
        return
    suspect_patterns = (".env", "credentials.json", "secrets.json", "id_rsa", "id_ed25519")
    bad = [
        line for line in out.splitlines()
        if any(line.endswith(p) or line.endswith("/" + p) for p in suspect_patterns)
    ]
    if bad:
        for f in bad:
            err(f"arquivo suspeito tracked: {f}")


def check_python_compiles() -> None:
    print("[4/5] py_compile em todos os .py")
    py_files = list(ROOT.rglob("*.py"))
    py_files = [p for p in py_files if ".git" not in p.parts]
    if not py_files:
        warn("nenhum .py encontrado")
        return
    for p in py_files:
        try:
            py_compile.compile(str(p), doraise=True)
        except py_compile.PyCompileError as e:
            err(f"{p.relative_to(ROOT)}: não compila — {e}")


def check_gitignore() -> None:
    print("[5/5] checando .gitignore")
    gi = ROOT / ".gitignore"
    if not gi.exists():
        err(".gitignore ausente na raiz")
        return
    content = gi.read_text(encoding="utf-8")
    required = (".env",)
    for p in required:
        if p not in content:
            err(f".gitignore não bloqueia padrão obrigatório: {p}")


def main() -> int:
    data, plugin_root = validate_marketplace()
    if data and "plugins" in data and isinstance(data["plugins"], list):
        for entry in data["plugins"]:
            validate_plugin(entry, plugin_root)
    check_no_secrets()
    check_python_compiles()
    check_gitignore()

    print()
    if warnings:
        print(f"⚠️  {len(warnings)} warning(s):")
        for w in warnings:
            print(f"   - {w}")
    if errors:
        print(f"❌ {len(errors)} erro(s):")
        for e in errors:
            print(f"   - {e}")
        return 1
    print(f"✅ marketplace válido — {len(data.get('plugins', []))} plugin(s) verificado(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
