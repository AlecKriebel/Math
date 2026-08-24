# Exact generic-rank upper certificates

## 2026-08-21 — Start

Goal: replace every sampled-Jacobian rank (a lower bound only) by a
deterministic, exactly replayable upper certificate for all 4,379 unique
four-port `MapDescriptor`s.  The preferred certificate is a structurally
explained family of rational Jacobian-kernel vector fields.  Exact symbolic
kernel certificates are the fallback; numerical or probabilistic rank claims
are inadmissible.

Initial completion estimate: **10%**.  The finite universe and exact lower
minors already exist; the load-bearing missing item is a scalable upper-bound
certificate.

## 2026-08-21 — Universal field census

The multilinear-in-inheritance polynomial vector-field ansatz gives exact
generic-rank upper bounds for 3,515 of 4,379 descriptors.  The remaining 864
form seven sharply concentrated rank families; no probabilistic upper claim
was made.

Completion estimate for the rank-upper subgoal: **65%**.

## 2026-08-21 — Exceptional orbit closure

Implemented and cross-checked the exact port/reticulation action on
descriptors.  The 864 exceptional descriptors form 75 relevant port orbits.
For every representative, generated one or two primitive polynomial
log-kernel fields and verified `J V = 0` coefficientwise in all 36 outputs.
Exact evaluation proves the combined fields have the full required nullity.

Completion estimate for the rank-upper subgoal: **95%**.

## 2026-08-21 — Full replay and mutations

The full replay recomputed all 3,515 universal coefficient systems and all 75
representative certificates, then checked 864 exact transports.  Result:
4,379/4,379 exact upper/lower matches, zero unresolved, 117.43 seconds for the
descriptor coverage phase on the local M1 Pro.  All six adversarial mutations
were rejected, with zero survivors.

Completion estimate for the exact generic-rank upper-certificate subgoal:
**100%**.  Integration into the independently regenerated raw ledger remains a
separate global-closure task owned by the raw-ledger audit.
