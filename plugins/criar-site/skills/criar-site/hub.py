"""
HUB Freepik API — wrapper unificado para Nano Banana (imagem) e Seedance 2.0 (vídeo).

Princípio obrigatório: SEMPRE mostra custo estimado antes de enviar request.
Log real de custos escrito em custos.log (gitignored).
"""
import os
import sys
import time
import json
import base64
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# Garante import absoluto do prompt_engineer mesmo quando hub.py é chamado como script.
sys.path.insert(0, str(Path(__file__).parent))
import prompt_engineer  # noqa: E402

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


load_dotenv(Path.cwd() / ".env")

API_KEY = os.getenv("FREEPIK_API_KEY")
BASE_URL = "https://api.freepik.com/v1/ai"

# Skill opera em dois modos:
#   - API: API_KEY configurada no .env → gera automaticamente via endpoints
#   - MANUAL: API_KEY ausente → skill só compõe prompts e mostra custos estimados;
#             usuário gera externamente (web UI, MidJourney, etc) e sobe as imagens.
# Por isso o check da key é preguiçoso (só quando alguém tenta chamar API), não no import.


def _require_api_key() -> str:
    if not API_KEY:
        raise RuntimeError(
            "Sem chave de API configurada. Configura `FREEPIK_API_KEY` no `.env` na raiz "
            "do projeto, ou opera em modo manual (skill gera os prompts e você produz "
            "externamente)."
        )
    return API_KEY


def has_api_key() -> bool:
    """Usado pela skill pra descobrir o modo de operação no começo da Fase 3."""
    return bool(API_KEY)


# Tabela oficial de preços (USD) — fonte: freepik.com/api/pricing (23/04/2026)
PRECOS = {
    # Imagens — preço por imagem
    "gemini-2-5-flash-image-preview":   {"imagem": 0.042},
    "nano-banana-pro-1k":                {"imagem": 0.10},
    "nano-banana-pro-2k":                {"imagem": 0.15},
    "nano-banana-pro-4k":                {"imagem": 0.30},
    "nano-banana-pro-flash-1k":          {"imagem": 0.095},
    "nano-banana-pro-flash-2k":          {"imagem": 0.143},
    "nano-banana-pro-flash-4k":          {"imagem": 0.19},
    # Vídeos Seedance 2.0 — preço por segundo
    "seedance-pro-480p":                 {"segundo": 0.026},
    "seedance-pro-720p":                 {"segundo": 0.07},
    "seedance-pro-1080p":                {"segundo": 0.155},
    "seedance-lite-480p":                {"segundo": 0.024},
    "seedance-lite-720p":                {"segundo": 0.051},
    "seedance-lite-1080p":                {"segundo": 0.113},
}

# Mapeamento modelo → endpoint REST (imagem)
ENDPOINTS_IMAGEM = {
    "gemini-2-5-flash-image-preview": "/text-to-image/gemini-2-5-flash-image-preview",
    "nano-banana-pro-1k":             "/text-to-image/nano-banana-pro",
    "nano-banana-pro-2k":             "/text-to-image/nano-banana-pro",
    "nano-banana-pro-4k":             "/text-to-image/nano-banana-pro",
    "nano-banana-pro-flash-1k":       "/text-to-image/nano-banana-pro-flash",
    "nano-banana-pro-flash-2k":       "/text-to-image/nano-banana-pro-flash",
    "nano-banana-pro-flash-4k":       "/text-to-image/nano-banana-pro-flash",
}

LOG_FILE = Path(__file__).parent / "custos.log"
THRESHOLD_CONFIRMACAO_USD = 1.00   # pede confirmação acima disso
DEFAULT_TIMEOUT_IMG = 180          # s
DEFAULT_TIMEOUT_VID = 600          # s


# ──────────────────────────── Orçamento ────────────────────────────

def estimar_custo(modelo: str, duration: int = 5, **_) -> float:
    if modelo not in PRECOS:
        raise ValueError(f"Modelo desconhecido: {modelo}. Opções: {list(PRECOS)}")
    p = PRECOS[modelo]
    return p["imagem"] if "imagem" in p else p["segundo"] * duration


def orcamento_lote(items: list[dict]) -> tuple[float, list[dict]]:
    """
    items = [{"tipo": "imagem|video", "modelo": str, "params": {...}}, ...]
    Retorna (total_usd, breakdown) sem chamar a API.
    """
    breakdown = []
    total = 0.0
    for it in items:
        custo = estimar_custo(it["modelo"], **it.get("params", {}))
        total += custo
        breakdown.append({**it, "custo_usd": round(custo, 4)})
    return round(total, 4), breakdown


def imprimir_orcamento_lote(total: float, breakdown: list[dict]):
    print("\n┌─────────── ORÇAMENTO DO LOTE ───────────")
    for b in breakdown:
        params = b.get("params", {})
        dur = f" {params['duration']}s" if b["tipo"] == "video" else ""
        print(f"│ {b['tipo']:6} │ {b['modelo']:32}{dur} │ ${b['custo_usd']:.4f}")
    print(f"├──────────────────────────────────────────")
    print(f"│ TOTAL ESTIMADO: ${total:.4f}")
    print(f"└──────────────────────────────────────────\n")


def _pedir_confirmacao(custo: float, forcar: bool = False) -> bool:
    if forcar or custo > THRESHOLD_CONFIRMACAO_USD:
        resp = input(f"[HUB] Custo estimado: ${custo:.4f}. Confirma? [s/N]: ")
        return resp.strip().lower() == "s"
    return True


# ──────────────────────────── Log de custos ────────────────────────────

def _registrar(modelo: str, custo: float, sucesso: bool, task_id: str | None = None):
    linha = json.dumps({
        "ts": datetime.now().isoformat(timespec="seconds"),
        "modelo": modelo,
        "custo_estimado_usd": round(custo, 4),
        "sucesso": sucesso,
        "task_id": task_id,
    }, ensure_ascii=False)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(linha + "\n")


def gasto_acumulado() -> float:
    if not LOG_FILE.exists():
        return 0.0
    total = 0.0
    with open(LOG_FILE, encoding="utf-8") as f:
        for linha in f:
            try:
                reg = json.loads(linha)
                if reg.get("sucesso"):
                    total += reg.get("custo_estimado_usd", 0)
            except json.JSONDecodeError:
                continue
    return round(total, 4)


# ──────────────────────────── HTTP helpers ────────────────────────────

def _headers() -> dict:
    return {"x-freepik-api-key": _require_api_key(), "Content-Type": "application/json"}


def _post(endpoint: str, payload: dict) -> dict:
    r = requests.post(f"{BASE_URL}{endpoint}", json=payload, headers=_headers(), timeout=30)
    if not r.ok:
        # Mensagens amigáveis pros erros mais comuns
        if r.status_code == 429:
            raise RuntimeError(
                f"Freepik free tier esgotado (429). Configure billing em:\n"
                f"https://www.freepik.com/developers/dashboard/billing"
            )
        if r.status_code in (402, 403):
            raise RuntimeError(
                f"Freepik billing ({r.status_code}). Verifique limites/pagamento: {r.text[:200]}"
            )
        if r.status_code == 400:
            raise RuntimeError(f"Bad request em {endpoint}: {r.text[:500]}")
        raise RuntimeError(f"POST {endpoint} falhou ({r.status_code}): {r.text[:500]}")
    return r.json()


def _aguardar(endpoint: str, task_id: str, timeout: int, intervalo: int = 3) -> dict:
    url = f"{BASE_URL}{endpoint}/{task_id}"
    inicio = time.time()
    while time.time() - inicio < timeout:
        r = requests.get(url, headers={"x-freepik-api-key": _require_api_key()}, timeout=30)
        r.raise_for_status()
        data = r.json()
        payload = data.get("data", data)
        status = (payload.get("status") or "").upper()
        if status in ("COMPLETED", "SUCCESS"):
            return payload
        if status in ("FAILED", "ERROR"):
            raise RuntimeError(f"Task {task_id} falhou: {payload}")
        time.sleep(intervalo)
    raise TimeoutError(f"Task {task_id} não completou em {timeout}s")


def _extrair_task_id(resposta: dict) -> str:
    payload = resposta.get("data", resposta)
    tid = payload.get("task_id") or payload.get("id")
    if not tid:
        raise RuntimeError(f"Resposta sem task_id: {resposta}")
    return tid


def _resolucao_do_modelo(modelo: str) -> str | None:
    for suf in ("1k", "2k", "4k"):
        if modelo.endswith(f"-{suf}"):
            return suf.upper()
    return None


def _ref_to_api_format(ref: str) -> str:
    """Converte path local em data URI base64. URLs/data URIs passam direto."""
    if ref.startswith(("http://", "https://", "data:")):
        return ref
    path = Path(ref)
    if not path.exists():
        raise FileNotFoundError(f"Reference image not found: {ref}")
    ext = path.suffix.lower()
    mime_map = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".webp": "image/webp",
        ".gif": "image/gif",
    }
    mime = mime_map.get(ext)
    if mime is None:
        with open(path, "rb") as f:
            header = f.read(4)
        if header.startswith(b"\xff\xd8"):
            mime = "image/jpeg"
        elif header.startswith(b"\x89PNG"):
            mime = "image/png"
        elif header.startswith(b"RIFF"):
            mime = "image/webp"
        else:
            mime = "image/jpeg"
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


# ──────────────────────────── API pública ────────────────────────────

def gerar_imagem(
    prompt: str,
    modelo: str = "gemini-2-5-flash-image-preview",
    pular_confirmacao: bool = False,
    reference_images: list[str] | None = None,
    negative_prompt: str | None = None,
    validar_densidade: bool = True,
    **params,
) -> dict | None:
    """Gera imagem. Mostra custo antes. Retorna dict com URL(s) geradas ou None se cancelado.

    Args:
        reference_images: URLs ou caminhos de imagens de referência (Nano Banana).
            Quando passadas, o módulo prompt_engineer garante que o prompt comece
            com o prefixo obrigatório pra evitar que Nano copie demais a ref.
        negative_prompt: string de proibições (taxonomy NEGATIVE).
        validar_densidade: se True, valida régua mínima antes de chamar API.
    """
    has_refs = bool(reference_images)
    prompt = prompt_engineer.apply_ref_prefix(prompt, has_refs)

    if validar_densidade:
        prompt_engineer.ensure_density(prompt, is_motion=False)

    custo = estimar_custo(modelo, **params)
    print(f"[HUB] {modelo} → imagem → custo: ${custo:.4f}" + (f" (+{len(reference_images)} refs)" if has_refs else ""))
    if not pular_confirmacao and not _pedir_confirmacao(custo):
        print("[HUB] Cancelado.")
        return None

    endpoint = ENDPOINTS_IMAGEM.get(modelo, f"/text-to-image/{modelo}")
    res = _resolucao_do_modelo(modelo)
    payload = {"prompt": prompt, **params}
    if res and "resolution" not in payload:
        payload["resolution"] = res
    if has_refs:
        payload["reference_images"] = [_ref_to_api_format(r) for r in reference_images]
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt

    task_id = None
    try:
        resposta = _post(endpoint, payload)
        task_id = _extrair_task_id(resposta)
        resultado = _aguardar(endpoint, task_id, timeout=DEFAULT_TIMEOUT_IMG)
        _registrar(modelo, custo, True, task_id)
        return resultado
    except Exception:
        _registrar(modelo, custo, False, task_id)
        raise


def gerar_video(
    prompt: str,
    modelo: str = "seedance-lite-720p",
    duration: int = 5,
    imagem_url: str | None = None,
    pular_confirmacao: bool = False,
    negative_prompt: str | None = None,
    validar_densidade: bool = True,
    **params,
) -> dict | None:
    """Gera vídeo. Se imagem_url passada → image-to-video, senão text-to-video.

    Seedance 2.0 só aceita duration ∈ {5, 10}. Valida antes de chamar API.

    Observação: o prefixo de "use as refs only as aesthetic references" é
    exclusivo do Nano Banana. Em image-to-video do Seedance, a sourceImage é
    tratada como frame literal (comportamento desejado) — nenhum prefixo é
    aplicado aqui.
    """
    if modelo.startswith("seedance-") and duration not in (5, 10):
        raise ValueError(
            f"Seedance duration={duration} inválido. Só aceita 5 ou 10 "
            f"(API retorna 400). Escolha 5 (loop curto) ou 10 (narrativa)."
        )
    if validar_densidade:
        prompt_engineer.ensure_density(prompt, is_motion=True)

    custo = estimar_custo(modelo, duration=duration)
    tipo = "image-to-video" if imagem_url else "text-to-video"
    print(f"[HUB] {modelo} → {tipo} → {duration}s → custo: ${custo:.4f}")
    if not pular_confirmacao and not _pedir_confirmacao(custo):
        print("[HUB] Cancelado.")
        return None

    endpoint = f"/{tipo}/{modelo}"
    payload = {"prompt": prompt, "duration": str(duration), **params}
    if imagem_url:
        payload["image"] = imagem_url
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt

    task_id = None
    try:
        resposta = _post(endpoint, payload)
        task_id = _extrair_task_id(resposta)
        resultado = _aguardar(endpoint, task_id, timeout=DEFAULT_TIMEOUT_VID)
        _registrar(modelo, custo, True, task_id)
        return resultado
    except Exception:
        _registrar(modelo, custo, False, task_id)
        raise


if __name__ == "__main__":
    # Smoke test — não chama API, só valida estimativas
    exemplo = [
        {"tipo": "imagem", "modelo": "gemini-2-5-flash-image-preview"},
        {"tipo": "imagem", "modelo": "nano-banana-pro-2k"},
        {"tipo": "video",  "modelo": "seedance-lite-720p", "params": {"duration": 5}},
        {"tipo": "video",  "modelo": "seedance-pro-720p",  "params": {"duration": 8}},
    ]
    total, bd = orcamento_lote(exemplo)
    imprimir_orcamento_lote(total, bd)
    print(f"Gasto acumulado registrado em log: ${gasto_acumulado():.4f}")
