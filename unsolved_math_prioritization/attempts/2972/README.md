# KP-4.96: a scoped unresolved investigation

The intended closed-manifold problem is **unsolved after five substantive attempts**. This package records no new complete solution and claims no novelty.

- `PROOF.md`: exact unresolved target, full proofs of partial reductions and restricted results, and counterexamples to invalid shortcuts.
- `SOURCE_GATE.md`: primary-source identification, current 2025–2026 literature, scope distinctions, and prior-attempt checks.
- `RESEARCH_LOG.md`: five approach families with outcomes and precise gaps.
- `verify.py` and `verification.json`: 11,393 exact, deterministic algebra controls.
- `STATUS.json`: machine-readable limits.
- `SHA256SUMS`: frozen public payload integrity.

Run from this directory:

    python3 verify.py > /tmp/kp496-verification.json
    cmp verification.json /tmp/kp496-verification.json
    sha256sum -c SHA256SUMS

The script requires only standard-library Python 3.8 or later. Source PDFs and private working material are deliberately absent. The computation is not a proof of a global symplectic classification.

Independent review is pending for this frozen snapshot. AI-assisted research; no human peer review or historical priority is claimed. The separate relative Stein-filling result reported in the current literature does not resolve the closed question.
