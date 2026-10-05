# KP-4.122: necessary conditions for a universal branching surface

Status: partial results and obstruction audit. The existence question is not solved here.

This packet concerns UnsolvedMath ID 2998, rank 695, modern K3 Problem 4.122. It does not concern the problem carrying the same number in the 1997 Kirby list. The primary locator is the 436-page April 2026 author version of Baykur, Kirby and Ruberman, printed/PDF pages 291–292.

The authored results show that a universal, closed, locally flat embedded branch surface in the usual finite branched-cover category must:

1. Have components with both positive and negative normal Euler number.
2. Have positive Euler-characteristic mass at least three, and therefore at least three components.
3. Have a complement group with a finite-index subgroup surjecting onto the free group of rank two.
4. Use unbounded covering degrees; simple coverings alone cannot suffice.

Doubling the known orientable universal ribbon surface in the four-ball cannot produce such a surface: every cover of the doubled branch surface has zero signature.

These are necessary conditions, not a construction, classification, or general nonexistence theorem. No novelty claim is made. The imported signature theorem is explicitly identified, and the remaining steps have proofs in `RESULTS.md`.

Files:

- `RESULTS.md`: complete authored arguments and the exact unresolved extension problem.
- `APPROACH_LOG.md`: five distinct approaches, with outcomes and stopping points.
- `SOURCE_VERIFICATION.md`: source/category/numbering checks and proof limits.
- `SOURCE_METADATA.json`: public source URLs, hashes, sizes and inspection metadata.
- `controls.py`, `CONTROL_RESULTS.json`: exact finite arithmetic sanity checks.
- `verify_manifest.py`, `AUTHOR_MANIFEST.json`: frozen authored-file integrity checks.

Replay: run `python controls.py`, then `python verify_manifest.py`, from this directory. Python's standard library suffices. The checks do not construct a surface, enumerate genuine covering representations, or formally verify the topology proofs.

Only authored mathematics/code and public verification metadata are in this directory. It contains no source PDFs, extracted source text, dataset records, or private coordination material. Independent review is still required before any remote publication.
