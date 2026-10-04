# 2305070 — Function Theory 5.70

**Unsolved after five substantive approaches.** No full solution or novelty claim.

The strongest explicit control is a bounded zero-free analytic function with nowhere-zero derivative whose modulus-one level has infinite total length but only finite-length components. It exposes the principal quantifier trap in this problem. Other results bound rational-exponent levels, quantify Herglotz truncation tails, and demonstrate loss of regular level length under compact convergence.

- PROOF.md: exact target, full auxiliary proofs, and precise remaining gaps.
- ATTEMPT_LOG.md: the five distinct approaches and their outcomes.
- SOURCE_GATE.md and SOURCE_MANIFEST.json: source provenance and limits of the literature check.
- verify.py and CHECKS.json: deterministic finite controls using Python's standard library.
- SHA256SUMS.json and verify_manifest.py: full public-file allowlist and integrity check.

Reproduce from this directory:

    python3 verify.py
    python3 verify_manifest.py

The numerical entries are diagnostics, not validated interval computations or proofs of the infinite assertions. The exact finite checks also do not settle the original question. No source PDFs or source corpus are included.
