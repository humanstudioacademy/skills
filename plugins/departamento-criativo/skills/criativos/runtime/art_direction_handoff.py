#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adaptador de handoff para o Diretor de Arte EXISTENTE (Etapa 4).
NÃO é um agente. Monta o pacote técnico que o Diretor de Arte (agents/diretor-de-arte.md)
consome: asset_reference, asset_scope, brand.md, altitude, evidence_packet_execucao (T2).
Deriva do contrato do pacote (visual_review_bridge), mas o bridge NÃO vira agente.

Regra dura: se altitude == 'arte', asset_reference é obrigatória; senão handoff_status='blocked'.
"""
import json, os, sys, argparse
from evidence_router import EvidenceRouter


def build_handoff(asset_reference, asset_scope, fmt, altitude, brand_summary, objective,
                  primary_niche="unknown", account_type="unknown", router=None):
    router = router or EvidenceRouter()
    status = "complete"
    blocking = []
    if altitude == "arte" and not asset_reference:
        status = "blocked"; blocking.append("altitude=arte exige asset_reference")
    if not brand_summary:
        status = "needs_brand_context" if status == "complete" else status

    ep = router.route({
        "altitude": altitude, "content_type": fmt, "asset_scope": asset_scope,
        "objective": objective, "primary_niche": primary_niche,
        "account_type": account_type, "lens": "execucao",
    })

    return {
        "target_agent": "diretor-de-arte",
        "asset_reference": asset_reference,
        "asset_scope": asset_scope,
        "format": fmt,
        "altitude": altitude,
        "brief_summary": brand_summary,
        "objective": objective,
        "evidence_packet_execucao": ep,   # T2 — só recomendação/escopo; NÃO altera nota T1
        "handoff_status": status,
        "blocking_reasons": blocking,
        "contract_notes": [
            "Diretor de Arte mantém T1 (luz/forma/cor/anti-slop) como veredito.",
            "evidence_packet_execucao é T2: capa/dispersão/legibilidade/relação texto-imagem no mesmo asset_scope.",
            "T2 nunca apaga piso T1; nunca vira nota.",
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--asset_reference", default="")
    ap.add_argument("--asset_scope", default="static_image")
    ap.add_argument("--format", dest="fmt", default="static_post")
    ap.add_argument("--altitude", default="arte")
    ap.add_argument("--brand_summary", default="")
    ap.add_argument("--objective", default=None)
    ap.add_argument("--primary_niche", default="unknown")
    ap.add_argument("--account_type", default="unknown")
    a = ap.parse_args()
    print(json.dumps(build_handoff(a.asset_reference, a.asset_scope, a.fmt, a.altitude,
                                   a.brand_summary, a.objective, a.primary_niche, a.account_type),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
