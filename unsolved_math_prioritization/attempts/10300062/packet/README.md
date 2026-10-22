# Rank 670 / 10300062: scoped partial results

Source target: Calegari, *Problems in foliations and laminations of 3-manifolds*, Question 14.2, arXiv:math/0209081v1, p.31.

**Outcome: no unqualified resolution.** A nonzero-Euler circle-bundle suspension gives a complete counterexample to coherent compact-domain approximation by closed incompressible surfaces. The source only says that images of growing balls converge. A separate covering-map control proves image convergence need not imply coherence. This semantic bridge, and any hyperbolic-only version, remain unresolved here.

Contents:

- `PROOF_AND_PARTIALS.md`: full construction, elementary group obstruction, convergence countercontrol, positive irrational-plane example, and other precise partials.
- `APPROACH_LOG.md`: five distinct methods, failed hypotheses and exact remaining gaps.
- `SOURCE_VERIFICATION.json`: source locations, PDF hashes/sizes, public dataset binding, retrieval limits, and manuscript-status metadata.
- `verify.py` and `verification_results.json`: exact small controls with explicit assertion scope.
- `verify_manifest.py` and `MANIFEST.json`: frozen file-integrity inventory.

Replay from this directory with Python 3.10+ and only its standard library:

    python3 verify.py
    python3 verify_manifest.py

The replay checks algebraic guardrails and byte integrity. It is not a formal proof verifier and does not certify the topological arguments or resolve the convergence interpretation.

This safe packet contains authored mathematical text, code and public verification metadata only. It excludes source PDFs, extracted source text, source datasets and coordination material. No remote writes were made. A fresh independent audit is required before publication; no novelty or first-resolution claim is made.
