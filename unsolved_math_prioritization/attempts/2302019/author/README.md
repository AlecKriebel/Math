# 2302019 / AMR-022-2019: asymmetric exponential-type bounds

This is newly authored reconstruction packet
`2302019-reconstruction-20261005-v1`, dated 2026-10-05 UTC.

**Mathematical status: unsolved.** The sharp modulus at a general nonreal
point remains unresolved here. The prior research history reports five
substantive turns ending unsolved. This reconstruction has a new freeze
and requires its own independent review; it does not inherit a previous
audit or claim byte identity with an unavailable earlier packet.

`PROOFS.md` contains all mathematical claims in this reconstruction:

- Compactness and extremal attainment
- A step-Poisson upper bound, impossible equality, and a strict supremum gap
- A Bernstein ramp improvement with an explicit positive penalty
- An admissible integrated-sinc example with genuinely unequal half-axis suprema
- A rigorous local-uniform approximation obstruction for globally admissible
  finite real-frequency sums

`SOURCE_SCOPE.md` records public references and precise inspection limits.
`SOURCE_METADATA.json` contains public provenance metadata only. No source
PDF, copied source text, source image, catalogue row, or private coordination
file is part of this author packet.

Verification requires Python 3's standard library only. From this folder run:

    python3 verify_math.py
    python3 verify_integrity.py

The mathematical checker uses both exact rational identities and expressly
labeled floating-point smoke checks. Its output must match
`EXPECTED_CHECKS.json`. Finite checks do not prove the infinite-dimensional
theorems or determine the unknown sharp bound. The integrity checker
verifies the frozen file list, byte counts, and SHA-256 hashes; an independent
record of the manifest hash is needed to authenticate the freeze itself.

AI tools were used for reconstruction and verification. This work is
unrefereed. Independent AI-assisted audit, when supplied separately, is
not human peer review. Nothing here authorizes merging, releasing, or
claiming a new solution.
