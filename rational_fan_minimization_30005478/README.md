# Rational-fan minimization: accepted partial results

Problem 30005478; source key OWR-12697711-014; row 1843. Status: **UNSOLVED**, five research avenues. Prepared 2026-10-21 UTC.

For arbitrary finite rational fans, computing the rational-subspace minimum is equivalent under effective finite oracle reductions to deciding rational-point existence on projective algebraic sets over Q (not necessarily irreducible). An explicit nonpure rational simplicial fan has real minimum 6 and rational minimum 7.

These are partial results, not a terminating algorithm, undecidability theorem, or polynomial-time claim. No pure, balanced, tropical-realizable, or irreducible-tropical extension is established.

## Reading order and proof dependencies

- SOURCE_GATE.md identifies the exact problem and distinguishes adjacent special cases.
- projective_equivalence.md gives both reductions and the genuine hyperplane-arrangement fan realization.
- independent_reduction_audit.md supplies the complete rational Veronese inverse and checks anchors, loopless graphs, boundaries, projective conditions, and the arithmetic gap. Its PASS concerns the mathematics of the original proof reports, not a later package-wide review.
- arithmetic_gap.md contains the universal proof and explicit six-cone construction.
- FIVE_AVENUES.md is a final editorial synthesis, with provisional contradictions removed and provenance stated.
- VERIFICATION.md explains exact checks, controls, and limits.

Reineke's complex-source construction is used only with the explicit rational descent calculation in the audit. No rational-point conclusion is deduced merely from a complex isomorphism. The reductions use only finite rational constructions, not a presently supplied decision algorithm for rational points.

## Reproduction

From this directory, with Python 3 and SymPy installed:

    python verify_arithmetic_gap.py --manifest
    python -O verify_arithmetic_gap.py --manifest
    python test_controls.py

The checker uses explicit exceptions, not Python assert statements. Controls change actual matrices/generators and separately corrupt manifest content and inventory. Finite checks complement but do not replace the universal written proofs.

## Publication scope

Only authored mathematical reports, executable verification, audits, and public metadata are included. No third-party source documents, extracted source text, dataset contents, or private coordination material are included. Public source hashes record prior retrieval/inspection history, not a claim of new downloads during packaging. MANIFEST.json hashes every package file other than itself; it excludes Python bytecode cache files. The external package receipt supplies the manifest hash.
