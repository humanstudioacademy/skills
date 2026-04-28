"""
Composer — sintetiza um site único a partir de um briefing.

Os 3 kits viram MATRIZES ESTÉTICAS. Cada briefing cunha um template-instância próprio
combinando: anatomia da matriz primary + token modules mixados das 3 matrizes + slots
signature opt-in. Não há mais clone-de-template — há síntese.

Uso típico:
    from composer import compose_site
    compose_site(briefing_path="sites/mezzanine/briefing.json")

O briefing segue o schema em `templates/_shared/briefing-schema.ts`.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

BASE = Path(__file__).parent
TEMPLATES = BASE / "templates"
SHARED = TEMPLATES / "_shared"
TOKEN_MODULES = SHARED / "token-modules"

VALID_MATRICES = ("portfolio-editorial", "clinica-estetica", "tech-apple")
VALID_TOKEN_MODULES = ("palette", "typography", "spacing", "motion", "radius")

# Variantes de Hero permitidas por matriz primary (refletem variant prop dos componentes Astro reais)
HERO_STYLES_BY_MATRIX = {
    "portfolio-editorial": {"monumental-word", "editorial-phrase"},
    "clinica-estetica":    {"split-portrait", "fullbleed-blur", "collage-polaroid"},
    "tech-apple":          {"product-floating", "product-isometric", "product-hero", "product-detail"},
}

# Mapping: slot principal → componente Astro da matriz
COMPONENT_MAPPING = {
    "portfolio-editorial": {
        "header":   "Header.astro",
        "hero":     "Hero.astro",
        "pitch":    "EditorialPitch.astro",
        "grid":     "WorkGrid.astro",
        "cta":      "ContactCTA.astro",
        "footer":   "Footer.astro",
        "marquee":  "Marquee.astro",          # signature
    },
    "clinica-estetica": {
        "header":        "Header.astro",
        "hero":          "Hero.astro",
        "pitch":         "Mission.astro",
        "grid":          "ServicesGrid.astro",
        "gallery":       "SpaceGallery.astro",
        "cta":           "BookingCTA.astro",
        "footer":        "Footer.astro",
        "testimonials":  "Testimonials.astro",   # signature
    },
    "tech-apple": {
        "header":      "Header.astro",
        "hero":        "Hero.astro",
        "grid":        "FeatureCards.astro",
        "gallery":     "CloseUp.astro",
        "cta":         "BuyCTA.astro",
        "footer":      "Footer.astro",
        "specs":       "Specs.astro",            # signature
        "highlights":  "Highlights.astro",
    },
}


# ───────────────────────── carregamento + validação ─────────────────────────

def load_briefing(path: str | Path) -> dict[str, Any]:
    """Lê briefing.json e valida campos obrigatórios."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))

    # Validações duras
    matrix = data.get("matrix", {})
    primary = matrix.get("primary")
    if primary not in VALID_MATRICES:
        raise ValueError(f"matrix.primary inválido: {primary}. Opções: {VALID_MATRICES}")

    secondary = matrix.get("secondary")
    if secondary and secondary not in VALID_MATRICES:
        raise ValueError(f"matrix.secondary inválido: {secondary}")
    if secondary == primary:
        raise ValueError("matrix.secondary não pode ser igual à primary")

    tokens = data.get("tokens", {})
    for module in VALID_TOKEN_MODULES:
        m = tokens.get(module)
        if m not in VALID_MATRICES:
            raise ValueError(
                f"tokens.{module} = {m!r} inválido. Cada token module precisa apontar pra "
                f"uma das matrizes: {VALID_MATRICES}"
            )

    # Validação Hero style ∈ variantes da matriz primary
    hero = data.get("slots", {}).get("hero")
    if hero:
        style = hero.get("style")
        allowed = HERO_STYLES_BY_MATRIX[primary]
        if style not in allowed:
            raise ValueError(
                f"hero.style = {style!r} não pertence à matriz primary {primary!r}. "
                f"Permitidos: {sorted(allowed)}"
            )

    return data


# ───────────────────────── composição de tokens.css ─────────────────────────

def compose_tokens_css(token_assignment: dict[str, str]) -> str:
    """
    Lê os 5 token modules das matrizes escolhidas e concatena num único @theme {}.
    Cada @import e cada bloco é só os custom properties — sem wrapper duplicado.
    """
    parts = ["@import \"tailwindcss\";", ""]
    parts.append("/*")
    parts.append("  Tokens compostos pela skill /criar-site")
    parts.append("  Cada bloco abaixo vem da matriz declarada no briefing.tokens")
    parts.append("*/")
    parts.append("")
    parts.append("@theme {")

    for module in VALID_TOKEN_MODULES:
        matrix = token_assignment[module]
        module_path = TOKEN_MODULES / matrix / f"{module}.css"
        if not module_path.exists():
            raise FileNotFoundError(f"Token module não encontrado: {module_path}")

        content = module_path.read_text(encoding="utf-8")
        parts.append(f"  /* ── {module.upper()} (do {matrix}) ── */")
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            # Pula comentários iniciais do arquivo (block /* ... */)
            if stripped.startswith("/*") or stripped.startswith("*/") or stripped.startswith("*"):
                continue
            # Indenta dentro do @theme
            if stripped.startswith("--"):
                parts.append(f"  {stripped}")
        parts.append("")

    parts.append("}")
    parts.append("")
    return "\n".join(parts)


# ───────────────────────── materialização do site ─────────────────────────

def compose_site(briefing_path: str | Path, force: bool = False) -> Path:
    """
    Lê o briefing, monta o site em sites/<slug>/. Retorna o path do site criado.

    Etapas:
        1. Validar briefing
        2. Criar estrutura de pastas
        3. Compor tokens.css (mix de 5 módulos)
        4. Copiar componentes da matriz primary (anatomia)
        5. Adicionar componentes signature opt-in das matrizes que os ofereceram
        6. (Etapa E vai gerar o index.astro a partir do briefing)
    """
    briefing = load_briefing(briefing_path)
    primary = briefing["matrix"]["primary"]
    slug = briefing["meta"]["slug"]

    out_dir = Path.cwd() / "sites" / slug
    if out_dir.exists() and not force:
        raise FileExistsError(f"sites/{slug} já existe. Use force=True pra sobrescrever.")
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copiar package.json + astro.config + tsconfig + .gitignore + public/favicon do primary
    primary_dir = TEMPLATES / primary
    for fname in ("package.json", "astro.config.mjs", "tsconfig.json", ".gitignore"):
        src = primary_dir / fname
        if src.exists():
            shutil.copy(src, out_dir / fname)
    if (primary_dir / "public").exists():
        shutil.copytree(primary_dir / "public", out_dir / "public", dirs_exist_ok=True)

    # 2. Copiar src/ inteiro do primary (BaseLayout, components, scripts, styles base)
    if (primary_dir / "src").exists():
        shutil.copytree(primary_dir / "src", out_dir / "src", dirs_exist_ok=True)

    # 3. Sobrescrever tokens.css com a composição
    tokens_dir = out_dir / "src" / "styles"
    tokens_dir.mkdir(parents=True, exist_ok=True)
    composed_tokens = compose_tokens_css(briefing["tokens"])
    (tokens_dir / "tokens.css").write_text(composed_tokens, encoding="utf-8")

    # 4. Adicionar componentes signature opt-in de outras matrizes (que não a primary)
    sig_slots = briefing.get("signatureSlots") or {}
    for slot_name in sig_slots.keys():
        if not sig_slots[slot_name]:
            continue
        # Descobrir qual matriz oferece esse signature
        for matrix_id, components in COMPONENT_MAPPING.items():
            if matrix_id == primary:
                continue  # já copiado
            if slot_name in components:
                comp_filename = components[slot_name]
                src = TEMPLATES / matrix_id / "src" / "components" / "sections" / comp_filename
                dst = out_dir / "src" / "components" / "sections" / comp_filename
                if src.exists() and not dst.exists():
                    shutil.copy(src, dst)
                break

    # 5. Persistir o briefing + meta-info no projeto
    (out_dir / "briefing.json").write_text(
        json.dumps(briefing, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (out_dir / ".composer-meta.json").write_text(
        json.dumps({
            "primary": primary,
            "secondary": briefing["matrix"].get("secondary"),
            "tertiary": briefing["matrix"].get("tertiary"),
            "intent": briefing["matrix"].get("intent"),
            "tokens": briefing["tokens"],
        }, indent=2), encoding="utf-8"
    )

    return out_dir


def report_composition(briefing: dict) -> str:
    """Imprime resumo da composição pro usuário ver antes/depois."""
    matrix = briefing["matrix"]
    tokens = briefing["tokens"]
    sigs = briefing.get("signatureSlots") or {}
    active_sigs = [k for k, v in sigs.items() if v]

    lines = [
        f"┌─── Composição do site ───",
        f"│ Nome:      {briefing['meta']['name']}",
        f"│ Slug:      {briefing['meta']['slug']}",
        f"├─ Matrizes ─",
        f"│ Primary:    {matrix['primary']}  (define anatomia)",
    ]
    if matrix.get("secondary"):
        lines.append(f"│ Secondary:  {matrix['secondary']}")
    if matrix.get("tertiary"):
        lines.append(f"│ Tertiary:   {matrix['tertiary']}")
    lines.append(f"│ Intent:     {matrix.get('intent', '—')}")
    lines.append(f"├─ Token modules ─")
    for module in VALID_TOKEN_MODULES:
        lines.append(f"│ {module:11} → {tokens[module]}")
    if active_sigs:
        lines.append(f"├─ Signature slots opt-in ─")
        for s in active_sigs:
            lines.append(f"│ ✓ {s}")
    lines.append(f"└──────────────────────────")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    # Smoke test — composição híbrida exemplo (primary=Editorial + secondary=Clínica em mistura 60/40)
    example = {
        "meta": {
            "name": "Example Studio",
            "slug": "example-studio",
            "language": "pt-BR",
            "description": "Briefing de exemplo pra smoke-test do composer.",
        },
        "matrix": {
            "primary":   "portfolio-editorial",
            "secondary": "clinica-estetica",
            "tertiary":  None,
            "intent":    "60% Editorial estrutural + 40% Clínica em paleta/luz",
        },
        "tokens": {
            "palette":    "clinica-estetica",
            "typography": "portfolio-editorial",
            "spacing":    "portfolio-editorial",
            "motion":     "portfolio-editorial",
            "radius":     "clinica-estetica",
        },
        "sectionOrder": ["header", "hero", "marquee", "pitch", "grid", "cta", "footer"],
        "slots": {
            "hero": {"style": "monumental-word", "word": "EXAMPLE."},
        },
        "signatureSlots": {
            "marquee": [{"items": ["Residential", "Hospitality"], "tone": "ink"}],
        },
    }

    print("─── Smoke test: composição híbrida exemplo ───")
    print(report_composition(example))
    print()
    print("─── Smoke test: tokens compostos (preview) ───")
    print(compose_tokens_css(example["tokens"])[:1200] + "\n... [truncated]")
