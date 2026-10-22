# Balanced permutations: prior resolution audit

This edition documents the existing solution of problem 3100034, the exact balanced-subsequence-pattern question. The original theorem is by Gal Beniamini, Nir Lavee and Nati Linial: *How Balanced Can Permutations Be?*, Combinatorica 45, article 9 (2025), https://doi.org/10.1007/s00493-024-00127-x.

- PROOF.md gives the complete elementary obstruction for n>=k>=4, all endpoints, elementary orders 1 and 2, order-3 arithmetic and analytical constructions, and the explicit finite premise F1.
- AUDIT.md explains the independent checks and their exact scope.
- ACCEPTANCE.md and ACCEPTANCE.json record acceptance of the prior exact-target resolution.
- SOURCES.json identifies public sources, source PDF hashes and historical inspection.
- VERIFICATION.json summarizes historical checks without numerical proof payloads.
- MANIFEST.json lists all eight files and hashes the seven other members. Its own hash must be pinned externally.

The source Table 1 supplies 19 separately checked exceptional witnesses for order 3. Obtain the identified table and independently enumerate its triple patterns to reproduce F1. This edition includes no copied source documents or passages, numerical permutation witness lists, per-witness outcome tables, raw computational certificates, or executable code. Its analytical formulas and finite-summation derivations are mathematical exposition.

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit of the exact target, not external human peer review, journal acceptance of this exposition, formal proof-assistant certification, or CI verification. No novelty or exhaustive literature-status claim is made.

The complete low-order classification cannot be independently reproduced from this edition alone. This is not a complete self-contained proof of the finite-witness part. Hashes alone do not prove the omitted premise F1. The nonexistence theorem for n>=k>=4 and the order-1 and order-2 classifications have complete elementary proofs in PROOF.md.
