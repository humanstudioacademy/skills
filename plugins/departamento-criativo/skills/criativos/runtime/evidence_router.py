#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Roteador determinístico de evidência T2 (Etapa 3).
NÃO é um subagente: é uma função pura que, dado o contexto da peça + a lente,
devolve um PACOTE PEQUENO de evidência empírica compatível (review prompts,
orientações, 1 exemplo, 1 contraexemplo, alertas de confusão, limitações de escopo).

Garantias:
- Filtra por lente (lens_routing), asset_scope (scope estrito), nicho e tipo de conta.
- Limites duros por lente: <=3 prompts, <=2 guidance, <=1 exemplo, <=1 contraexemplo, <=2 alertas.
- Devolve vazio quando não há evidência pertinente (nunca inventa correspondência).
- NUNCA transforma hipótese/observação em regra (essas nem entram no índice de runtime).
- NUNCA carrega pesquisa extensa: lê só os arquivos de runtime do módulo.
- Confiança baixa por construção (corpus = associação, não causa).
"""
import json, os, sys, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODULE = os.path.normpath(os.path.join(HERE, "..", "evidencias", "social-instagram-v1", "runtime"))
DEFAULT_BALIZAS = os.path.normpath(os.path.join(HERE, "..", "evidencias", "social-instagram-v1", "balizas"))

LIMITS = {"review_prompts": 3, "contextual_guidance": 2, "examples": 1, "counterexamples": 1, "confounding_warnings": 2}

LENSES = {"atencao", "clareza", "originalidade", "coerencia", "execucao"}


def _rd(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def _rdl(p):
    out = []
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if l:
            out.append(json.loads(l))
    return out

def _as_list(x, *keys):
    if isinstance(x, list):
        return x
    for k in keys:
        if isinstance(x, dict) and k in x and isinstance(x[k], list):
            return x[k]
    return x.get("items", []) if isinstance(x, dict) else []


class EvidenceRouter:
    def __init__(self, module_dir=DEFAULT_MODULE, balizas_dir=DEFAULT_BALIZAS):
        self.lens_routing = _rd(os.path.join(module_dir, "lens_routing.json"))["lenses"]
        self.scope_rules = _rd(os.path.join(module_dir, "scope_rules.json"))["scopes"]
        self.review_prompts = _as_list(_rd(os.path.join(module_dir, "review_prompts.json")), "review_prompts")
        self.contextual_guidance = _as_list(_rd(os.path.join(module_dir, "contextual_guidance.json")), "contextual_guidance")
        self.confounded = _as_list(_rd(os.path.join(module_dir, "confounded_patterns.json")), "confounded_patterns")
        self.examples = _rdl(os.path.join(balizas_dir, "examples_index.jsonl"))
        # Submodulos por asset_scope — carregados se o diretório existir
        self._submodules = {}
        self._load_fc_submodule(module_dir)

    def _load_fc_submodule(self, module_dir):
        fc_dir = os.path.join(module_dir, "full_carousel")
        if not os.path.isdir(fc_dir):
            return
        # Review prompts FC: normaliza campo "prompt" → "question" para compatibilidade
        rp_path = os.path.join(fc_dir, "full_carousel_review_prompts.json")
        if os.path.isfile(rp_path):
            fc_rps = _as_list(_rd(rp_path), "review_prompts")
            for rp in fc_rps:
                if "prompt" in rp and "question" not in rp:
                    rp["question"] = rp["prompt"]
            self.review_prompts.extend(fc_rps)
        # Exemplos FC (positivos e negativos): adicionados ao pool compartilhado
        ex_path = os.path.join(fc_dir, "full_carousel_examples.jsonl")
        if os.path.isfile(ex_path):
            self.examples.extend(_rdl(ex_path))
        cx_path = os.path.join(fc_dir, "full_carousel_counterexamples.jsonl")
        if os.path.isfile(cx_path):
            self.examples.extend(_rdl(cx_path))

    # --- helpers de compatibilidade ---
    def _scope_compatible(self, item_scope, input_scope):
        # estrito: mesmo escopo, ou item agnóstico (None/'all'). Evita extrapolar cover-only<->completo.
        if item_scope in (None, "", "all"):
            return True
        return item_scope == input_scope

    def _dim_lens_ok(self, dimension, lens):
        if not dimension:
            return True  # itens sem dimensão são genéricos
        # igualdade ESTRITA: a dimensão precisa estar explicitamente listada na lente.
        # (sem casamento por prefixo — copy.X de uma lente não vaza para outra)
        allowed = self.lens_routing.get(lens, {}).get("allowed_dimensions", [])
        return dimension in allowed

    def _fc_example_lens_ok(self, example, lens):
        # Para exemplos FC com relevant_features: aceita só se ao menos 1 feature
        # do exemplo estiver nas allowed_dimensions da lente. Evita o mesmo exemplo
        # aparecendo em todas as lentes.
        rf = example.get("relevant_features")
        if not rf:
            return True  # sem filtro de lente: aceita em todas
        allowed = self.lens_routing.get(lens, {}).get("allowed_dimensions", [])
        return any(feat in allowed for feat in rf.keys())

    def route(self, inp):
        lens = inp.get("lens")
        if lens not in LENSES:
            raise ValueError(f"lens inválida: {lens}")
        asset_scope = inp.get("asset_scope") or "none"
        niche = inp.get("primary_niche")
        niche_ok = bool(niche) and niche != "unknown"
        acct = inp.get("account_type")
        acct_ok = bool(acct) and acct != "unknown"

        # review prompts: dimensão pertence à lente + escopo compatível
        prompts = []
        for rp in self.review_prompts:
            dim = rp.get("related_feature")
            if not self._dim_lens_ok(dim, lens):
                continue
            if not self._scope_compatible(rp.get("asset_scope"), asset_scope):
                continue
            prompts.append({
                "id": rp.get("prompt_id"), "question": rp.get("question"),
                "scope": rp.get("asset_scope"), "confidence": rp.get("confidence", "baixa"),
                "scores": False, "penalizes": False,
            })

        # contextual guidance
        guidance = []
        for g in self.contextual_guidance:
            dim = g.get("analysis_dimension")
            if not self._dim_lens_ok(dim, lens):
                continue
            if not self._scope_compatible(g.get("asset_scope"), asset_scope):
                continue
            guidance.append({
                "dimension": dim, "scope": g.get("asset_scope"),
                "class": g.get("final_class"), "scores": False, "penalizes": False,
            })

        # confounding warnings (guarda de não-inferência): mesma dimensão da lente + escopo
        warnings = []
        for c in self.confounded:
            dim = c.get("dimension")
            if not self._dim_lens_ok(dim, lens):
                continue
            if not self._scope_compatible(c.get("scope"), asset_scope):
                continue
            warnings.append({
                "dimension": dim, "value": c.get("value"), "scope": c.get("scope"),
                "do_not_use_as_proof": True,
                "warning": f"'{dim}={c.get('value')}' é associação confundida no escopo {c.get('scope')}; não inferir causa.",
            })

        # exemplos / contraexemplos: escopo compatível, preferir nicho e tipo de conta.
        # Bonus +3 para match exato de asset_scope.
        # Bonus +2 para exemplos com relevant_features (registros de submodulo FC):
        # garante que exemplos diferenciados por lente prevalecem sobre balizas genéricas.
        def _rank(e):
            s = 0
            if e.get("asset_scope") == asset_scope: s += 3
            if e.get("relevant_features"): s += 2
            if niche_ok and e.get("niche") == niche: s += 2
            if acct_ok and e.get("account_type") == acct: s += 1
            return -s
        pos = [e for e in self.examples if e.get("role") == "positive"
               and e.get("sensitivity") != "highly_sensitive"
               and self._scope_compatible(e.get("asset_scope"), asset_scope)
               and self._fc_example_lens_ok(e, lens)]
        neg = [e for e in self.examples if e.get("role") in ("negative", "counterexample")
               and e.get("sensitivity") != "highly_sensitive"
               and self._scope_compatible(e.get("asset_scope"), asset_scope)
               and self._fc_example_lens_ok(e, lens)]
        pos.sort(key=_rank); neg.sort(key=_rank)
        examples = [{"example_id": e["example_id"], "role": e["role"], "asset_scope": e.get("asset_scope"),
                     "niche": e.get("niche"), "demonstrates": e.get("dimension_demonstrated"),
                     "file": e.get("file"), "limitation": "ilustrativo; associação não-causal"} for e in pos[:LIMITS["examples"]]]
        counter = [{"example_id": e["example_id"], "role": e["role"], "asset_scope": e.get("asset_scope"),
                    "niche": e.get("niche"), "demonstrates": e.get("dimension_demonstrated"),
                    "file": e.get("file"), "limitation": "ilustrativo; múltiplas features mudaram, nada isolável"} for e in neg[:LIMITS["counterexamples"]]]

        # limitações de escopo
        scope_lim = []
        sr = self.scope_rules.get(asset_scope)
        if sr and sr.get("proibido"):
            scope_lim.append(f"asset_scope={asset_scope}: NÃO analisar {', '.join(sr['proibido'])}.")

        # aplica limites duros
        prompts = prompts[:LIMITS["review_prompts"]]
        guidance = guidance[:LIMITS["contextual_guidance"]]
        warnings = warnings[:LIMITS["confounding_warnings"]]

        # confiança (baixa por construção)
        matched = len(prompts) + len(guidance) + len(examples) + len(counter)
        if matched == 0:
            confidence = "none"
        elif niche_ok or acct_ok:
            confidence = "baixa-media"
        else:
            confidence = "baixa"

        return {
            "evidence_packet_id": f"ep-{lens}-{asset_scope}",
            "lens": lens, "asset_scope": asset_scope,
            "review_prompts": prompts, "contextual_guidance": guidance,
            "examples": examples, "counterexamples": counter,
            "confounding_warnings": warnings, "scope_limitations": scope_lim,
            "confidence": confidence,
        }


def main():
    ap = argparse.ArgumentParser(description="Roteador de evidência T2 (determinístico).")
    ap.add_argument("--lens", required=True)
    ap.add_argument("--asset_scope", default="none")
    ap.add_argument("--content_type", default=None)
    ap.add_argument("--altitude", default=None)
    ap.add_argument("--objective", default=None)
    ap.add_argument("--primary_niche", default="unknown")
    ap.add_argument("--account_type", default="unknown")
    a = ap.parse_args()
    r = EvidenceRouter()
    pkt = r.route(vars(a))
    print(json.dumps(pkt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
