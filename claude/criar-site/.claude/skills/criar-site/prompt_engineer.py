"""
Prompt Engineer — módulo auxiliar da skill /criar-site.

A composição do prompt é feita pela skill lendo os docs em `prompts/prompt-engineer/`
(taxonomy.md, engine-image.md, engine-motion.md, kit-presets/*.md).

Este arquivo expõe helpers operacionais:
- load_kit_preamble() — carrega o preamble formal de um kit
- apply_ref_prefix() — injeta prefixo obrigatório quando há image refs
- validate_prompt() — checa régua mínima antes de enviar pra API
"""
from __future__ import annotations

import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
ENGINEER_DIR = BASE_DIR / "prompts" / "prompt-engineer"

REF_PREFIX = (
    "Use the reference images only as aesthetic, compositional, and visual-aspect "
    "references to generate the following image: "
)

# Adjetivos banidos (taxonomy regra 8).
BANNED_WORDS = [
    "beautiful", "stunning", "amazing", "gorgeous",
    "high quality", "4K", "8K", "ultra HD", "ultra-HD",
    "hyperrealistic", "photorealistic masterpiece",
    "masterpiece", "award-winning", "award winning",
    "breathtaking", "magical",
]

VALID_KITS = ("portfolio-editorial", "clinica-estetica", "tech-apple")


def load_kit_preamble(kit_id: str) -> str:
    """Lê o bloco 'PREAMBLE FORMAL' do kit preset correspondente.

    O preset tem formato:
        ## PREAMBLE FORMAL — usado pelo engine
        <texto explicativo opcional>
        > Texto do preamble linha 1
        > Texto do preamble linha 2
        <linha não-blockquote que fecha o bloco>

    Extrai o texto do blockquote e retorna como string única (linhas concatenadas).
    """
    if kit_id not in VALID_KITS:
        raise ValueError(f"kit_id desconhecido: {kit_id}. Opções: {VALID_KITS}")

    path = ENGINEER_DIR / "kit-presets" / f"{kit_id}.md"
    if not path.exists():
        raise FileNotFoundError(f"preset não encontrado: {path}")

    content = path.read_text(encoding="utf-8")

    # Extrai o primeiro blockquote após o header "## PREAMBLE FORMAL"
    match = re.search(
        r"##\s+PREAMBLE FORMAL.*?\n(>\s*.+?)(?:\n[^>\s]|\Z)",
        content,
        flags=re.DOTALL,
    )
    if not match:
        raise RuntimeError(f"PREAMBLE FORMAL não encontrado em {path}")

    # Remove o marcador ">" de cada linha do blockquote
    raw = match.group(1)
    cleaned = re.sub(r"^>\s?", "", raw, flags=re.MULTILINE)

    # Colapsa whitespace (blockquote tem \n entre linhas)
    return re.sub(r"\s+", " ", cleaned.strip())


def apply_ref_prefix(prompt: str, has_refs: bool) -> str:
    """Se há image refs, garante que o prompt comece com o prefixo obrigatório.

    Sem esse prefixo, Nano Banana copia demais a referência em vez de usá-la
    como inspiração estética (bug confirmado empiricamente).
    """
    if not has_refs:
        return prompt
    if prompt.startswith(REF_PREFIX):
        return prompt
    return REF_PREFIX + prompt.lstrip()


def validate_prompt(prompt: str, *, is_motion: bool = False) -> list[str]:
    """Checa régua mínima de qualidade. Retorna lista de violações (vazia = ok)."""
    violations: list[str] = []

    # 1. Adjetivos banidos
    lower = prompt.lower()
    for word in BANNED_WORDS:
        if word.lower() in lower:
            violations.append(f"adjetivo banido: '{word}'")

    # 2. Sintaxe MidJourney proibida (dois traços consecutivos)
    if "--" in prompt:
        violations.append("sintaxe MidJourney detectada (dois traços consecutivos)")

    # 3. Precisa ter ao menos 1 HEX de cor
    if not re.search(r"#[0-9A-Fa-f]{6}", prompt):
        violations.append("nenhuma cor em HEX declarada (taxonomy regra 5)")

    # 4. Precisa ter câmera/lente declarada
    camera_markers = [
        "ARRI", "Alexa", "VENICE", "RED V-Raptor", "RED KOMODO",
        "Hasselblad", "Phase One", "Leica", "Fujifilm GFX",
        "Cooke", "Zeiss", "Supreme Prime", "anamorphic",
    ]
    if not any(m in prompt for m in camera_markers):
        violations.append("câmera ou lente não declarada (eixo 4 da taxonomy)")

    # 5. Precisa ter iluminação descrita
    light_markers = ["key", "fill", "rim", "softbox", "daylight", "tungsten", "Kelvin",
                     "contrast", "shadow", "highlight", "K "]
    if not any(m.lower() in lower for m in light_markers):
        violations.append("iluminação não descrita (eixo 3 da taxonomy)")

    # 6. Tamanho alvo
    word_count = len(prompt.split())
    if is_motion:
        if word_count < 200:
            violations.append(f"prompt motion curto demais ({word_count}w, alvo 300-700)")
        elif word_count > 800:
            violations.append(f"prompt motion longo demais ({word_count}w, alvo 300-700)")
    else:
        if word_count < 300:
            violations.append(f"prompt imagem curto demais ({word_count}w, alvo 400-900)")
        elif word_count > 1000:
            violations.append(f"prompt imagem longo demais ({word_count}w, alvo 400-900)")

    return violations


def ensure_density(prompt: str, *, is_motion: bool = False) -> None:
    """Raises RuntimeError se o prompt violar a régua mínima. Uso em runtime."""
    violations = validate_prompt(prompt, is_motion=is_motion)
    if violations:
        raise RuntimeError(
            "Prompt abaixo da régua mínima de qualidade:\n  - "
            + "\n  - ".join(violations)
        )


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    for kit in VALID_KITS:
        print(f"\n------ {kit} ------")
        print(load_kit_preamble(kit)[:300] + "...")
        print()

    # Valida que validate_prompt pega adjetivo banido
    bad = "A beautiful sunset, 4K, award-winning --ar 16:9"
    issues = validate_prompt(bad)
    print(f"Smoke validate (bad prompt): {len(issues)} violations")
    for v in issues:
        print(f"  - {v}")

    # Valida prefixo
    assert apply_ref_prefix("hello", has_refs=False) == "hello"
    assert apply_ref_prefix("hello", has_refs=True).startswith(REF_PREFIX)
    print("\nSmoke apply_ref_prefix: OK")
