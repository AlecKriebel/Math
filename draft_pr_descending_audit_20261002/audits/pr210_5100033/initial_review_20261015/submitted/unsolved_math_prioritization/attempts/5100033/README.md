# 5100033: outer focal-pedal area product

**Complete first-turn candidate, independent review pending.** No novelty claim.

For every odd primitive N-periodic billiard family in a nondegenerate confocal ellipse pair, including primitive stars, the product of the two signed focal-pedal areas of the outer tangent polygon is constant.

The exact target is arXiv Table 7 **k605,a**, renamed **k606** in the published edition. Published k605 is a different, unprimed invariant. See SOURCES.md before interpreting the code.

- PROOF.md: complete meromorphic argument and exact geometry
- verify.py and verification.json: finite exact controls and separately labeled numerical diagnostics
- SOURCES.md, source_manifest.json and readiness.json: primary inputs, scope and source gate
- RESEARCH_LOG.md and turn_ledger.json: author-turn history
- MANIFEST.json: frozen candidate file hashes

Run `python3 verify.py` in this directory and compare its JSON with verification.json. It uses installed SymPy and mpmath, not downloaded source software. Numerical comparisons support debugging; the all-period proof is in PROOF.md.

The proof cancels the double-pole coefficient of a simultaneous two-endpoint singularity, then uses reflection, imaginary anti-periodicity and the divisor of a two-pole elliptic function. It makes no division by a potentially zero pedal area. Hyperbolic caustics and repeated-period relabeling are outside the restored source scope.

The earlier SOURCE_CHECKPOINT.md is preserved as a historical zero-turn source checkpoint. The current ledger controls the attempt count. Shared queue state is not regenerated from incomplete local history.
