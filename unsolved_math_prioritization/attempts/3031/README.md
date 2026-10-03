# Exact graph colorings 3031: reviewed partial results

**Original target: UNSOLVED. Author budget: exhausted, 5/5. Novelty: unverified.**

The [independent review](review/REVIEW.md) gives a scoped mathematical PASS with a mandatory additive strict-validation supplement. This does not solve Erickson's conjecture or establish novelty.

## What is proved

- Complete finite rooted models, explicit size bounds and crossing-core constraints, with the general reduction credited to Stacey–Weidl: [finite models](packet/FINITE_MODELS.md).
- Explicit constructions for the normalized deficit-difference-six subfamily, including the exact hypotheses and cited boundary cases: [strongest construction](packet/TURN_2.md).
- Larger fixed-gap semigroup families: [turn 3](packet/TURN_3.md).
- An exact (217,43) construction and a compact-padding obstruction: [turn 4](packet/TURN_4.md).
- An obstruction to palette-disjoint arbitrary-color extensions: [turn 5](packet/TURN_5.md).

Both failed constructions remain explicitly rejected: compact padding at (262,64) and the simple extension to (113,43). Source alias 3114 is reserved against another attempt; there is no separate queue row for it.

## Current validation and replay instructions

Use the additive strict checker for integer-label validation:

    python review/rooted_verify_strict.py packet/rooted_c112_m43.json --full-spectrum

The original checker remains unchanged for historical reproducibility. Its upper-triangle type-validation defect and the exact repair are documented in the review. Do not use its historical validation promise without the strict supplement. The valid frozen certificates are unaffected.

Run all public-integrity checks, author replays, independent controls and strict-validation regression tests:

    python replay_public.py

The deliberately failed extension must return exit 1. The malformed-label control must return exit 2. The valid certificate must return exit 0.

## Distribution and provenance

Every distributed frozen proof, code file and certificate is byte-identical to its reviewed original. Historical statements about pending review or an unchanged remote queue refer to the author-freeze time. This README and the public replay supersede historical execution instructions where strict validation is promised.

One local administrative provenance file, packet/SOURCE_GATE.md, is omitted. Its hash is identified in PUBLICATION_SCOPE.json; the public replay explicitly checks that omission and verifies only the 38 distributed author-manifest entries plus the complete review distribution. It does not claim that the absent administrative file was reverified from this public package. Public mathematical source facts are recorded in [SOURCE_SUMMARY.md](SOURCE_SUMMARY.md). No raw source corpus, PDFs, personal correspondence or credentials are distributed.

The original and review manifests are preserved as historical manifests. PUBLIC_DISTRIBUTION_MANIFEST.json identifies this actual public distribution.
