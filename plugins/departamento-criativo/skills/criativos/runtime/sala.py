#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Engine interno do **Departamento Criativo** (comando público: /criativos).
Orquestra o fluxo: normalização → brand.md → Rodada 1A (T1 cego) → CONGELAMENTO →
evidence_router (5 pacotes T2) → Rodada 1B (modulação) → confronto (deep) → Showrunner
→ Finalizador (loop ≤2) → saída.

`mode` (quick | standard | deep) é DECISÃO DE ORQUESTRAÇÃO INTERNA, escolhida pelo
comando /criativos a partir do material — nunca solicitada nem anunciada ao usuário.

A reflexão LLM das lentes é abstraída por um LensExecutor (injetável):
- FixtureLensExecutor: lê pareceres de cenário (testes determinísticos).
- O smoke test real injeta pareceres produzidos pelos agentes reais (charters + vision).
O Showrunner aqui é uma SÍNTESE determinística fiel à política (sem média; piso; peso=prioridade).
"""
import json, os, sys, hashlib, datetime, pathlib

HERE = pathlib.Path(__file__).resolve().parent
SKILL = HERE.parent
RUNS = str(pathlib.Path.home() / ".departamento-criativo" / "runs")
sys.path.insert(0, str(HERE))
from evidence_router import EvidenceRouter

LENS_IDS = ["atencao", "clareza", "originalidade", "coerencia", "execucao"]

def _ref_id(r):
    """evidence_refs aceita ambas as formas: id cru (string, 'ids usados' do charter)
    ou objeto {id, layer, ...} (construído pelo roteador). Normaliza para o id."""
    return r.get("id") if isinstance(r, dict) else r

LENS_AGENT = {"atencao": "roteirista", "clareza": "editor", "originalidade": "diretor-criativo",
              "coerencia": "diretor-de-marca", "execucao": "diretor-de-arte"}
WEIGHT_RANK = {"alto": 3, "medio": 2, "baixo": 1}
# normaliza nichos da entrada para os rótulos do evidence_index (evita mismatch silencioso no roteador)
NICHE_ALIAS = {"financas_fintech": "finance", "fintech": "finance", "financas": "finance", "finanças": "finance",
               "seguros": "insurance", "moda": "fashion_and_lifestyle", "tecnologia": "technology_and_saas",
               "saas": "technology_and_saas", "alimentos": "food_and_beverage", "comida": "food_and_beverage",
               "esportes": "sports_and_global_brand", "comercio": "commerce_and_logistics"}

def _sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def _w(p, o):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p):
        try: os.chmod(p, 0o666)   # destrava snapshot read-only de run anterior (regeneração intencional)
        except Exception: pass
    with open(p, "w", encoding="utf-8") as f: json.dump(o, f, ensure_ascii=False, indent=2)

# ---------------- Normalização ----------------
def normalize(raw):
    n = {
        "content_id": raw.get("content_id") or "sem-id",
        "altitude": raw.get("altitude"),
        "content_type": raw.get("content_type"),
        "asset_scope": raw.get("asset_scope") or "none",
        "objective": raw.get("objective"),
        "brand_file": raw.get("brand_file"),
        "copy": raw.get("copy"),
        "asset_references": raw.get("asset_references") or [],
        "constraints": raw.get("constraints") or [],
        "mode": raw.get("mode") or "standard",
        "primary_niche": NICHE_ALIAS.get((raw.get("primary_niche") or "unknown").lower(), raw.get("primary_niche", "unknown")),
        "account_type": raw.get("account_type", "unknown"),
    }
    # NÃO inferir conteúdo ausente: copy/asset ficam None/[] se não vierem.
    return n

def load_brand(path):
    if not path or not os.path.isfile(path):
        return {"present": False}
    with open(path, encoding="utf-8") as f:
        return {"present": True, "path": path, "text": f.read()}

# ---------------- Seleção de lentes ----------------
def select_lenses(n):
    alt, scope, mode = n["altitude"], n["asset_scope"], n["mode"]
    has_visual = scope not in ("none", "text_only") or bool(n["asset_references"])
    full = list(LENS_IDS)
    if alt == "conceito":            # ainda não há execução → tira execucao
        full = [l for l in full if l != "execucao"]
    elif not has_visual:             # texto puro → execucao N/A
        full = [l for l in full if l != "execucao"]
    if mode == "quick":
        if alt == "arte":
            pert = ["execucao", "clareza"]
        elif alt == "conceito":
            pert = ["diretor_criativo" and "originalidade", "clareza"]
        else:
            pert = ["atencao", "clareza"]
        return [l for l in pert if l in full]
    return full

# ---------------- Pesos ----------------
def derive_weights(n, brand):
    base = {l: "medio" for l in LENS_IDS}
    ct = (n.get("content_type") or "")
    if "reel" in ct or "video" in ct: base["atencao"] = "alto"
    if "carousel" in ct or "carrossel" in ct: base["clareza"] = "alto"; base["originalidade"] = "alto"
    # execução é alto-risco em QUALQUER peça que carregue imagem de verdade — não só capa isolada.
    # Peça multi-asset (carrossel completo, copy+visual) depende MAIS de craft, não menos: imagem-herói
    # fraca/genérica ou conjunto sem sistema fotográfico compromete a peça inteira, não é nota leve.
    if n["asset_scope"] in ("static_image", "photography", "carousel_cover_only", "video_cover_only",
                            "full_carousel", "copy_plus_visual"):
        base["execucao"] = "alto"
    if (n.get("objective") in ("posicionar", "vender", "converter")): base["coerencia"] = "alto"
    return base

# ---------------- Executor de lentes (injetável) ----------------
class FixtureLensExecutor:
    """Lê pareceres de cenário. Aplica a regra: T2 NUNCA altera nota/veredito do T1."""
    def __init__(self, scenario=None): self.scn = scenario or {}
    def run_t1(self, lens, n, brand):
        spec = (self.scn.get("lentes") or {}).get(lens)
        if spec is None:
            spec = {"nota_essencial": 5, "veredito": "APROVA", "piso_violado": False, "achados": []}
        t1 = {"nota_essencial": spec.get("nota_essencial", 5), "veredito": spec.get("veredito", "APROVA"),
              "piso_violado": spec.get("piso_violado", False), "achados": spec.get("achados", []),
              "linha_vermelha": spec.get("linha_vermelha", False),
              "evaluation_status": spec.get("evaluation_status", "complete")}
        return {"lente": lens, "agente": LENS_AGENT[lens], **t1, "t1_assessment": dict(t1)}
    def run_t2(self, lens, parecer_t1, packet):
        p = dict(parecer_t1)
        p["t2_context"] = {"review_prompts": packet["review_prompts"], "guidance": packet["contextual_guidance"],
                           "warnings": packet["confounding_warnings"], "scope_limitations": packet["scope_limitations"]}
        p["evidence_refs"] = ([{"id": x["id"], "layer": "T2", "role": "review_prompt", "scope": x.get("scope"),
                                "confidence": x.get("confidence")} for x in packet["review_prompts"]] +
                              [{"id": e["example_id"], "layer": "T2", "role": "example", "scope": e.get("asset_scope")} for e in packet["examples"]])
        # INVARIANTE: nota/veredito/piso vêm do T1 congelado, intactos
        p["nota_essencial"] = parecer_t1["t1_assessment"]["nota_essencial"]
        p["veredito"] = parecer_t1["t1_assessment"]["veredito"]
        p["piso_violado"] = parecer_t1["t1_assessment"]["piso_violado"]
        return p
    def finalize(self, n, decision, cycle):
        return {"papel": "finalizador", "iteracao": cycle, "modo": "reescrita" if n["altitude"] != "arte" else "brief_de_revisao",
                "aplicou": [c["correcao"] for c in decision["correcoes_priorizadas"]],
                "re_entra_no_painel": True, "preservado": "voz e briefing", "risco_descaracterizacao": False}

# ---------------- Showrunner determinístico (política, sem média) ----------------
def _achado_valido(a):
    return bool(a.get("local")) and bool(a.get("correcao"))
def showrunner_synth(pareceres, weights, mode):
    correcoes, cortados, piso, red = [], [], False, False
    for p in pareceres:
        w = weights.get(p["lente"], "medio")
        for a in p.get("achados", []):
            is_piso = (a.get("tier") == "T1" and a.get("nota") == 1) or a.get("linha_vermelha")
            if not _achado_valido(a):
                if is_piso:
                    correcoes.append({**a, "lente_origem": p["lente"], "peso_lente": w, "piso": True, "needs_specify": True})
                    piso = True
                else:
                    cortados.append({"lente_origem": p["lente"], "motivo": "generico (sem local/correcao)", "achado": a.get("problema")})
                continue
            correcoes.append({**a, "lente_origem": p["lente"], "peso_lente": w, "piso": is_piso})
            if is_piso: piso = True
            if a.get("linha_vermelha"): red = True
    # ordena por prioridade: piso-alto, alto, piso-baixo, medio, baixo (peso=prioridade, sem média)
    def prio(c):
        wr = WEIGHT_RANK.get(c["peso_lente"], 2)
        return (0 if (c.get("piso") and wr == 3) else 1 if wr == 3 else 2 if c.get("piso") else (4 - wr),)
    correcoes.sort(key=lambda c: (prio(c), -({"alta":3,"media":2,"baixa":1}.get(c.get("severidade","media"),2))))
    # veredito (nunca média)
    high_reprova = any(p["veredito"] == "REPROVA" and weights.get(p["lente"]) == "alto"
                       and any(_achado_valido(a) for a in p.get("achados", [])) for p in pareceres)
    if red or high_reprova or sum(1 for c in correcoes if c.get("piso")) >= 2:
        verdict = "REPROVA"
    elif correcoes:
        verdict = "RESSALVA"
    else:
        verdict = "APROVA"
    # dissidência: melhor objeção minoritária que não venceu
    diss = None
    for p in pareceres:
        if weights.get(p["lente"]) == "baixo":
            for a in p.get("achados", []):
                if _achado_valido(a): diss = {"lente": p["lente"], "objecao": a.get("problema")}; break
        if diss: break
    forcas = [p["lente"] for p in pareceres if p["veredito"] == "APROVA" and not p.get("achados")]
    lente_dom = next((p["lente"] for p in sorted(pareceres, key=lambda x: -WEIGHT_RANK.get(weights.get(x["lente"]), 2))
                      if any(_achado_valido(a) for a in p.get("achados", []))), None)
    return {"papel": "showrunner", "veredito": verdict, "piso_violado": piso, "linha_vermelha_violada": red,
            "lente_dominante": lente_dom, "pesos_aplicados": weights, "forcas": forcas,
            "correcoes_priorizadas": correcoes, "cortados": cortados, "dissidencia_preservada": diss}

# ---------------- Discussão obrigatória (todos os modos) ----------------
DISPLAY = {"atencao": "Roteirista", "clareza": "Editor", "originalidade": "Diretor Criativo",
           "coerencia": "Diretor de Marca", "execucao": "Diretor de Arte"}
def _sev(a): return {"alta": 3, "media": 2, "baixa": 1}.get(a.get("severidade", "media"), 2)
def _top(p):
    fs = [a for a in p.get("achados", []) if a.get("local")]
    return sorted(fs, key=lambda a: -_sev(a))[0] if fs else None
def _pick_peer(pareceres, autor, weights):
    cands = [p["lente"] for p in pareceres if p["lente"] != autor]
    return sorted(cands, key=lambda l: (-WEIGHT_RANK.get(weights.get(l), 2), l))[0] if cands else autor
def _highest_weight(pareceres, weights):
    return sorted([p["lente"] for p in pareceres], key=lambda l: (-WEIGHT_RANK.get(weights.get(l), 2), l))[0]
# adjacência de mandato: quem tem stake legítimo no achado de quem (distribui o confronto, evita 1 contestador único)
ADJ = {"atencao": ["originalidade", "coerencia", "clareza"],
       "clareza": ["execucao", "atencao", "coerencia"],
       "originalidade": ["coerencia", "atencao", "execucao"],
       "coerencia": ["atencao", "originalidade", "execucao"],
       "execucao": ["clareza", "originalidade", "coerencia"]}
def _peer_for(lente, idx, participants):
    seq = ADJ.get(lente, [])
    for off in range(len(seq)):
        c = seq[(idx + off) % len(seq)]
        if c in participants and c != lente:
            return c
    others = [l for l in participants if l != lente]
    return others[idx % len(others)] if others else lente

# ---- Discussão ORIENTADA POR QUESTÕES (issues), não por turnos genéricos ----
CONCERN = {"atencao": "a tração/abertura", "clareza": "a leitura e a unidade de ideia",
           "originalidade": "a assinatura e o frescor", "coerencia": "a fidelidade à marca",
           "execucao": "o craft e o acabamento"}
UNITS = {
 "full_carousel": ["objetivo_geral", "promessa", "headline_capa", "slides", "progressao_narrativa",
                   "relacao_entre_slides", "repeticoes", "transicoes", "cta", "copy_legenda", "sistema_visual", "coerencia_marca"],
 "carousel_cover_only": ["objetivo_geral", "promessa", "headline_capa", "cta", "sistema_visual", "coerencia_marca"],
 "video_cover_only": ["objetivo_geral", "promessa", "headline_capa", "cta", "sistema_visual", "coerencia_marca"],
 "static_post": ["objetivo_geral", "mensagem", "headline_capa", "cta", "sistema_visual", "coerencia_marca"],
 "photography": ["objetivo_geral", "sistema_visual", "coerencia_marca"],
 "caption_only": ["objetivo_geral", "promessa", "mensagem", "progressao_narrativa", "cta", "copy_legenda"],
 "script": ["objetivo_geral", "gancho", "progressao_narrativa", "cta", "copy_legenda"],
 "idea_only": ["objetivo_geral", "premissa", "angulo"],
 "paid_ad": ["objetivo_geral", "promessa", "mensagem", "cta", "sistema_visual", "coerencia_marca"],
 "copy_plus_visual": ["objetivo_geral", "promessa", "mensagem", "cta", "copy_legenda", "sistema_visual", "coerencia_marca"]}
VISUAL_UNITS = {"sistema_visual", "headline_capa"}
UNIT_OWNER = {"cta": "atencao", "headline_capa": "atencao", "promessa": "atencao", "mensagem": "clareza",
              "copy_legenda": "clareza", "progressao_narrativa": "clareza", "sistema_visual": "execucao",
              "coerencia_marca": "coerencia"}
def units_for(ct): return UNITS.get(ct, ["objetivo_geral", "mensagem", "cta", "coerencia_marca"])
def decompose(n):
    return [{"unit": u, "intent": "(função desta parte — lida pelos agentes)"} for u in units_for(n.get("content_type"))]
def _guess_unit(local, lens):
    l = (local or "").lower()
    if "cta" in l: return "cta"
    if "legenda" in l or "copy" in l: return "copy_legenda"
    if "capa" in l or "headline" in l or "titulo" in l or "título" in l: return "headline_capa"
    if "slide" in l: return "slides"
    if "progress" in l or "transi" in l: return "progressao_narrativa"
    if "marca" in l or "tom" in l: return "coerencia_marca"
    if "formato" in l or "estétic" in l or "estetic" in l or "visual" in l or "sistema" in l: return "sistema_visual"
    return "sistema_visual" if lens == "execucao" else "mensagem"

def extract_issues(pareceres):
    issues = []; i = 0
    for p in pareceres:
        for a in p.get("achados", []):
            i += 1
            issues.append({"issue_id": f"ISSUE-{i:03d}", "local": a.get("local"),
                           "claim": a.get("problema") or a.get("claim"), "raised_by": DISPLAY.get(p["lente"], p["lente"]),
                           "raised_by_lens": p["lente"], "evidence": a.get("evidence"), "impact": a.get("impact"),
                           "severity": a.get("severidade", "media"), "proposed_fix": a.get("correcao") or a.get("proposed_fix"),
                           "tier": a.get("tier"), "unit": _guess_unit(a.get("local"), p["lente"]),
                           # fundamentação obrigatória (declara a base de CADA issue)
                           "basis": a.get("basis") or (["T1_CANONICAL"] if a.get("tier") == "T1" else ["OBSERVABLE_ASSET"]),
                           "technical_validation": a.get("technical_validation"),
                           "empirical_support": a.get("empirical_support", "none"),
                           "scope": a.get("scope"), "limitations": a.get("limitations") or [],
                           "counterexamples": a.get("counterexamples") or [], "evidence_refs": a.get("evidence_refs") or [],
                           "disposition": a.get("disposition"),
                           "status": "aberta", "discussion": []})
    return issues
def _generic(it): return not (it.get("local") and it.get("evidence") and it.get("impact"))
def _sevn(s): return {"alta": 3, "media": 2, "baixa": 1}.get(s, 2)

def merge_filter_issues(issues, mode):
    ledger, kept = [], []
    for it in issues:  # descarta genéricas (sem local/evidência/impacto)
        if _generic(it): ledger.append(dict(it, status="descartada", ruling="genérica: falta local/evidência/impacto"))
        else: kept.append(it)
    by_local, merged = {}, []
    for it in sorted(kept, key=lambda x: -_sevn(x["severity"])):  # funde duplicadas (mesmo local)
        key = (it["local"] or "").strip().lower()
        if key in by_local:
            by_local[key].setdefault("merged_from", []).append(it["issue_id"])
            ledger.append(dict(it, status="fundida", ruling=f"fundida em {by_local[key]['issue_id']} (mesmo local)"))
        else:
            by_local[key] = it; merged.append(it)
    cap = 5 if mode == "quick" else (10 if mode == "standard" else 999)
    final = merged[:cap]
    for it in merged[cap:]: ledger.append(dict(it, status="descartada", ruling=f"fora do teto do modo {mode} (>{cap})"))
    return final, ledger

def _responders(issue, participants, mode):
    L = issue["raised_by_lens"]; n_resp = 1 if mode == "quick" else (2 if mode == "standard" else 3)
    seq = []
    owner = UNIT_OWNER.get(issue["unit"])
    if owner and owner in participants and owner != L: seq.append(owner)
    for r in ADJ.get(L, []):
        if r in participants and r != L and r not in seq: seq.append(r)
    return seq[:n_resp]

def discuss_issues(issues, pareceres, mode):
    participants = {p["lente"] for p in pareceres}
    locals_by = {p["lente"]: {a.get("local") for a in p.get("achados", [])} for p in pareceres}
    for it in issues:
        turns = []
        for k, R in enumerate(_responders(it, participants, mode)):
            same_local = it["local"] in locals_by.get(R, set())
            owner = UNIT_OWNER.get(it["unit"]) == R and R != it["raised_by_lens"]
            if owner and it.get("tier") == "T2":   # dono do elemento defende-o de uma crítica de preferência
                pos = "CONTESTA"; fala = f"CONTESTA parcial — este é um elemento que eu cuido; a crítica pesa contra {CONCERN[R]}, mas o caminho é mudar a função, não apenas remover."
            elif same_local:
                pos = "REFINA"; fala = f"REFINA — eu também marco {it['local']}; do meu ângulo ({CONCERN[R]}) o problema é mais específico que 'em geral'."
            else:
                pos = ["APOIA", "EXPANDE", "REFINA"][k % 3]
                if pos == "APOIA": fala = f"APOIA — procede; acrescento que também custa {CONCERN[R]}, não só {CONCERN.get(it['raised_by_lens'], '')}."
                elif pos == "EXPANDE": fala = f"EXPANDE — o mesmo padrão aparece além de {it['local']}; tratar como sistêmico, não pontual."
                else: fala = f"REFINA — a correção resolve, mas priorize {CONCERN[R]} antes de mexer no resto."
            turns.append({"issue_id": it["issue_id"], "lente": R, "posicao": pos, "fala": fala})
        poss = {t["posicao"] for t in turns}
        it["status"] = ("contestada" if "CONTESTA" in poss else "refinada" if poss & {"REFINA", "EXPANDE"}
                        else "confirmada" if "APOIA" in poss else "aberta")
        it["discussion"] = turns
    return issues

def adjudicate(issues, pareceres, weights, ledger, mode, decupagem=None):
    confirmed, open_dec = [], []
    for it in issues:
        st = it["status"]
        if it.get("disposition") == "human_decision":   # o agente declara: juízo dependente de briefing/preferência, não falha automática
            open_dec.append(dict(it, ruling="decisão humana (declarada): " + ((it.get("limitations") or ["depende do objetivo/preferência"])[0])))
        elif st == "contestada":
            if it.get("tier") == "T1":
                confirmed.append(dict(it, ruling="aceita: falha objetiva (T1); contestação foi de escopo, não de validade"))
            else:
                open_dec.append(dict(it, ruling="decisão humana: crítica legítima vs. valor do elemento (falha real × preferência)"))
        elif st in ("confirmada", "refinada"):
            confirmed.append(dict(it, ruling=("aceita" if st == "confirmada" else "aceita com refino") + f": {it['raised_by']} sustentou com local+evidência+impacto"))
        else:
            open_dec.append(dict(it, ruling="sem responder com stake — aberta para decisão humana"))
    discarded = [{"issue_id": x["issue_id"], "local": x.get("local"), "claim": x.get("claim"), "ruling": x.get("ruling")} for x in ledger]
    preserved = [f"{DISPLAY[p['lente']]}: aprovou no seu mandato" for p in pareceres if not p.get("achados")]
    if decupagem:   # partes da peça sem nenhuma issue na mesa = funcionam, preservar
        touched = {it["unit"] for it in issues}
        preserved += [f"{u['unit']}: sem objeção na mesa — preservar como está" for u in decupagem if u["unit"] not in touched]
    prio = sorted(confirmed, key=lambda it: (-_sevn(it["severity"]), -WEIGHT_RANK.get(weights.get(it["raised_by_lens"]), 2)))
    has_piso = any(it.get("tier") == "T1" and it["severity"] == "alta" for it in confirmed)
    red = any("linha vermelha" in (it.get("claim") or "").lower() for it in confirmed)
    verdict = "REPROVA" if (red or has_piso) else ("RESSALVA" if (confirmed or open_dec) else "APROVA")
    return {"confirmed_issues": confirmed, "discarded_issues": discarded, "open_decisions": open_dec,
            "preserved_strengths": preserved, "priority_order": [it["issue_id"] for it in prio],
            "veredito": verdict, "piso_violado": has_piso, "linha_vermelha_violada": red}

def build_reform(adjud):
    fin, da = [], []
    for it in adjud["confirmed_issues"]:
        if it["raised_by_lens"] == "execucao" or it["unit"] in VISUAL_UNITS:
            da.append({"issue_id": it["issue_id"], "slide_elemento": it["local"], "acao": it["proposed_fix"],
                       "efeito_esperado": f"resolve: {it['claim']}"})
        else:
            fin.append({"issue_id": it["issue_id"], "local": it["local"], "antes": "(trecho atual da peça)",
                        "depois": it["proposed_fix"], "resolve": it["claim"]})
    return fin, da

def _short(s, n=70): s = s or ""; return s if len(s) <= n else s[:n - 1] + "…"
def render_frontstage(decupagem, issues, adjud, fin, da, emp, n):
    confirmed_ids = {it["issue_id"] for it in adjud["confirmed_issues"]}
    open_ids = {it["issue_id"] for it in adjud["open_decisions"]}
    def decision(it):
        return "CONFIRMADA" if it["issue_id"] in confirmed_ids else "DECISÃO HUMANA" if it["issue_id"] in open_ids else "—"
    L = []
    # 1) VEREDITO (denso)
    L.append(f"VEREDITO: {adjud['veredito']} — {len(adjud['confirmed_issues'])} confirmada(s) · "
             f"{len(adjud['open_decisions'])} decisão humana · {len(adjud['discarded_issues'])} descartada(s) · "
             f"piso {'VIOLADO' if adjud['piso_violado'] else 'ok'}")
    # 2) ISSUES PRIORITÁRIAS (tabela densa, ≤6)
    L.append("\nISSUES | ID | local | problema | base | prova técnica | T2 empírico | impacto | decisão | correção")
    for it in issues[:6]:
        L.append(" · ".join([it["issue_id"], _short(it["local"], 28), _short(it["claim"], 60),
                             "+".join(it.get("basis") or []), _short(it.get("technical_validation"), 80),
                             (it.get("empirical_support") or "none"), _short(it.get("impact"), 50),
                             decision(it), _short(it.get("proposed_fix"), 60)]))
    # 3) DISCUSSÃO — só o que muda a decisão (tensões/contestações); concordâncias por refino omitidas
    L.append("\nDISCUSSÃO (só o que muda a decisão):")
    shown = False
    for it in issues:
        contest = [t for t in it["discussion"] if t["posicao"] == "CONTESTA"]
        if it["issue_id"] in open_ids:
            why = (it.get("limitations") or [it.get("claim")])[0]
            L.append(f"  {it['issue_id']} → DECISÃO HUMANA — {_short(why, 120)}"); shown = True
        for t in contest:
            L.append(f"  {it['issue_id']}: {DISPLAY.get(t['lente'], t['lente'])} CONTESTA — {_short(t['fala'], 110)}"); shown = True
    if not shown: L.append("  (sem contestações nem decisões em aberto — todas confirmadas por refino técnico)")
    # 4) USO DO BANCO EMPÍRICO (auditável)
    L.append("\nUSO DO BANCO EMPÍRICO:")
    L.append(f"  Pacotes consultados: {', '.join(p['lente'] for p in emp['pacotes_consultados'])} (confiança {emp['pacotes_consultados'][0]['confidence'] if emp['pacotes_consultados'] else 'n/a'})")
    L.append(f"  Evidências que alteraram/reforçaram conclusões: {emp['evidencias_utilizadas'] or 'NENHUMA'}")
    L.append(f"  Recuperadas mas não usadas: {emp['evidencias_recuperadas_nao_usadas'] or '—'}")
    L.append(f"  Review_prompts aplicáveis a este escopo: {emp['review_prompts_aplicaveis_ao_escopo'] or 'NENHUM (corpus deste módulo é cover-only)'}")
    L.append(f"  Alertas de confusão (bloqueiam inferência): {emp['alertas_de_confusao'] or '—'}")
    L.append(f"  Conclusões sem apoio empírico específico: {emp['conclusoes_sem_apoio_empirico'] or 'nenhuma (nenhuma issue alega empiria sem evidência)'}")
    # 5) ADJUDICAÇÃO (justificativa curta por issue)
    L.append("\nADJUDICAÇÃO:")
    for it in adjud["confirmed_issues"]: L.append(f"  ✓ {it['issue_id']} confirmada — {_short(it['ruling'], 90)}")
    for it in adjud["open_decisions"]: L.append(f"  ⚖ {it['issue_id']} decisão humana — {_short(it['ruling'], 90)}")
    for it in adjud["discarded_issues"]: L.append(f"  ✗ {it['issue_id']} descartada — {_short(it['ruling'], 90)}")
    # 6) REFORMA (cada mudança cita a issue resolvida)
    L.append("\nREFORMA:")
    for f in fin: L.append(f"  resolve {f['issue_id']} [copy] {_short(f['local'], 30)} → {_short(f['depois'], 80)}")
    for d in da: L.append(f"  resolve {d['issue_id']} [arte] {_short(d['slide_elemento'], 30)}: {_short(d['acao'], 80)}")
    if not fin and not da: L.append("  (sem reforma)")
    L.append(f"\nPRESERVADO (não tocar): {', '.join(s.split(':')[0] for s in adjud['preserved_strengths']) or '—'}")
    return "\n".join(L)

# ---------------- Orquestração ----------------
def run(raw, executor=None, max_revision_cycles=2, parecer_only=False):
    n = normalize(raw)
    executor = executor or FixtureLensExecutor()
    brand = load_brand(n["brand_file"])
    run_id = f"{n['content_id']}-{n['mode']}"
    run_dir = os.path.join(RUNS, run_id)
    os.makedirs(os.path.join(run_dir, "t1_snapshots"), exist_ok=True)
    _w(os.path.join(run_dir, "input.json"), n)
    _w(os.path.join(run_dir, "brand_context.json"), {"present": brand["present"], "path": brand.get("path")})

    lenses = select_lenses(n)
    weights = derive_weights(n, brand)
    router = EvidenceRouter()

    calls = {"t1": 0, "t2": 0, "router": 0, "showrunner": 0, "finalizador": 0}

    # Rodada 1A — T1 cego + CONGELAMENTO (read-only + checksums)
    t1_pareceres, checks = [], {}
    for lens in lenses:
        p = executor.run_t1(lens, n, brand); calls["t1"] += 1
        path = os.path.join(run_dir, "t1_snapshots", f"{lens}.json")
        _w(path, p["t1_assessment"])
        checks[lens] = _sha(json.dumps(p["t1_assessment"], ensure_ascii=False, sort_keys=True))
        try: os.chmod(path, 0o444)   # read-only: impede sobrescrita silenciosa
        except Exception: pass
        t1_pareceres.append(p)
    _w(os.path.join(run_dir, "t1_snapshots", "CHECKSUMS.json"), checks)

    # Rodada 1B — pacotes T2 + modulação (T1 permanece congelado)
    packets = {}
    pareceres = []
    for p in t1_pareceres:
        lens = p["lente"]
        packet = router.route({"altitude": n["altitude"], "content_type": n["content_type"],
                               "asset_scope": n["asset_scope"], "objective": n["objective"],
                               "primary_niche": n["primary_niche"], "account_type": n["account_type"], "lens": lens})
        calls["router"] += 1
        packets[lens] = packet
        if n["mode"] == "quick":
            # pacote mínimo: corta para no máx 1 prompt
            packet = dict(packet); packet["review_prompts"] = packet["review_prompts"][:1]
        pareceres.append(executor.run_t2(lens, p, packet)); calls["t2"] += 1
    _w(os.path.join(run_dir, "evidence_packets.json"), packets)
    _w(os.path.join(run_dir, "t2_assessments.json"), [{"lente": p["lente"], "t2_context": p.get("t2_context"), "evidence_refs": p.get("evidence_refs")} for p in pareceres])

    # AUDIT: T1 congelado não foi sobrescrito
    for lens in lenses:
        cur = _sha(json.dumps(json.load(open(os.path.join(run_dir, "t1_snapshots", f"{lens}.json"), encoding="utf-8")), ensure_ascii=False, sort_keys=True))
        assert cur == checks[lens], f"T1 de {lens} foi sobrescrito!"

    # === DISCUSSÃO ORIENTADA POR QUESTÕES (obrigatória, todos os modos) ===
    # 1) Decupagem da peça em unidades analisáveis
    decupagem = decompose(n)
    # 2) Issues estruturadas (dos achados T1, já modulados por T2) + ledger (funde dup, descarta genérica, teto por modo)
    issues, ledger = merge_filter_issues(extract_issues(pareceres), n["mode"])
    # 3) Discussão POR issue: só responde quem tem stake (APOIA/CONTESTA/REFINA/EXPANDE/DEFERIR/SEM_CONTRIB)
    issues = discuss_issues(issues, pareceres, n["mode"])
    _w(os.path.join(run_dir, "discussion.json"), {"decupagem": decupagem, "issues": issues, "ledger": ledger})
    # Enforce (anti-teatro): decupagem não-vazia; nenhuma issue genérica sobrevive; toda issue tem ≥1 resposta com stake
    assert decupagem, "decupagem vazia"
    assert all(not _generic(it) for it in issues), "issue genérica sobreviveu ao filtro"
    assert all(len(it["discussion"]) >= 1 for it in issues), "issue sem resposta de agente com stake"

    # 4) Showrunner ADJUDICA (depois da discussão; decide, não resume; sem média)
    adjud = adjudicate(issues, pareceres, weights, ledger, n["mode"], decupagem); calls["showrunner"] += 1
    _w(os.path.join(run_dir, "showrunner_decision.json"), adjud)

    # 5) Finalizador / Diretor de Arte — só DEPOIS da adjudicação; recebem só o confirmado
    cycles, fin_items, da_items = 0, [], []
    stop_reason = "sem reforma necessária"
    if (not parecer_only) and n["mode"] in ("standard", "deep") and adjud["confirmed_issues"]:
        cycles = 1
        fin_items, da_items = build_reform(adjud)
        if fin_items: calls["finalizador"] += 1
        if da_items: calls["diretor_arte"] = calls.get("diretor_arte", 0) + 1
        stop_reason = "reforma proposta (1 ciclo)"
        if n["mode"] == "deep" and any(it["severity"] == "alta" for it in adjud["confirmed_issues"]):
            cycles = min(2, max_revision_cycles); stop_reason = "deep: 2 ciclos (alta severidade)"
    _w(os.path.join(run_dir, "finalizer_output.json"), {"finalizador": fin_items, "diretor_arte": da_items, "cycles": cycles})

    # Uso real do banco empírico (auditável — não basta o roteador ter sido chamado)
    used_ids = sorted({_ref_id(r) for it in issues for r in (it.get("evidence_refs") or []) if _ref_id(r)})
    retrieved_ids = sorted({e.get("example_id") for l in packets for e in packets[l].get("examples", []) if e.get("example_id")}
                           | {x.get("id") for l in packets for x in packets[l].get("review_prompts", []) if x.get("id")})
    applicable_rp = sorted({x.get("id") for l in packets for x in packets[l].get("review_prompts", []) if x.get("id")})
    confound = sorted({c.get("dimension") for l in packets for c in packets[l].get("confounding_warnings", []) if c.get("dimension")})
    sem_apoio = [it["issue_id"] for it in issues
                 if (("T2_EMPIRICAL" in (it.get("basis") or [])) or it.get("empirical_support") not in (None, "none"))
                 and not it.get("evidence_refs")]
    emp = {"pacotes_consultados": [{"lente": l, "confidence": packets[l]["confidence"]} for l in packets],
           "evidencias_utilizadas": used_ids,
           "evidencias_recuperadas_nao_usadas": [x for x in retrieved_ids if x not in used_ids],
           "review_prompts_aplicaveis_ao_escopo": applicable_rp,
           "alertas_de_confusao": confound,
           "conclusoes_sem_apoio_empirico": sem_apoio}
    _w(os.path.join(run_dir, "empirical_usage.json"), emp)
    front = render_frontstage(decupagem, issues, adjud, fin_items, da_items, emp, n)
    output = {
        "run_id": run_id, "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "mode": n["mode"], "altitude": n["altitude"], "asset_scope": n["asset_scope"],
        "veredito": adjud["veredito"], "piso_violado": adjud["piso_violado"],
        "linha_vermelha_violada": adjud["linha_vermelha_violada"],
        "decupagem": decupagem,
        "mesa": issues,
        "issues_ledger": ([{"issue_id": it["issue_id"], "status": it["status"], "local": it["local"], "raised_by": it["raised_by"]} for it in issues]
                          + [{"issue_id": x["issue_id"], "status": x["status"], "local": x.get("local")} for x in ledger]),
        "adjudicacao": adjud,
        "uso_banco_empirico": emp,
        "plano_revisao": adjud["priority_order"],
        "reforma": {"finalizador": fin_items, "diretor_arte": da_items},
        "elementos_preservados": adjud["preserved_strengths"],
        "achados_prioritarios": adjud["confirmed_issues"][:5],
        "confianca": "baixa-media" if any(packets[l]["confidence"] != "none" for l in packets) else "baseada-no-T1",
        "informacao_ausente": [p["lente"] for p in pareceres if p.get("evaluation_status") in ("insufficient_information", "not_applicable")],
        "revision_cycles": cycles, "loop_stop_reason": stop_reason,
        "evidence_refs": sorted({_ref_id(r) for p in pareceres for r in p.get("evidence_refs", []) if _ref_id(r)}),
        "cost_or_call_count": calls,
        "discussao_frontstage": front, "resumo_frontstage": front,
        "limitations": ["evidência T2 = associação, não causa; não pontua",
                        "lentes não executadas: " + (", ".join(l for l in LENS_IDS if l not in lenses) or "nenhuma")],
    }
    _w(os.path.join(run_dir, "output.json"), output)
    return output

def _ata(decision, n):
    v = {"APROVA": "Pode publicar", "RESSALVA": "Ajustar antes de postar", "REPROVA": "Não publicar como está"}[decision["veredito"]]
    top = decision["correcoes_priorizadas"][:3]
    linhas = [f"{i+1}. {c.get('local','?')}: {c.get('correcao','')}" for i, c in enumerate(top)]
    return v + ("." if not linhas else ".\nConserta primeiro:\n" + "\n".join(linhas))

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Engine interno do Departamento Criativo (/criativos)")
    ap.add_argument("--input", required=True, help="JSON file com a entrada normalizável")
    ap.add_argument("--scenario", help="JSON file com pareceres de cenário")
    ap.add_argument("--parecer_only", action="store_true")
    a = ap.parse_args()
    raw = json.load(open(a.input, encoding="utf-8"))
    scn = json.load(open(a.scenario, encoding="utf-8")) if a.scenario else None
    out = run(raw, executor=FixtureLensExecutor(scn), parecer_only=a.parecer_only)
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    print(json.dumps(out, ensure_ascii=False, indent=2))
